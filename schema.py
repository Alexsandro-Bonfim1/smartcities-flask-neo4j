import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from neo4j import GraphDatabase
from flask import current_app

class Location(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    type = graphene.String()
    coordinates = graphene.List(graphene.Float)
    properties = graphene.JSONString()

class NetworkConnection(graphene.ObjectType):
    id = graphene.ID()
    source = graphene.Field(Location)
    target = graphene.Field(Location)
    type = graphene.String()
    properties = graphene.JSONString()

class Query(graphene.ObjectType):
    locations = graphene.List(Location)
    network_connections = graphene.List(NetworkConnection)
    location = graphene.Field(Location, id=graphene.ID())
    location_by_name = graphene.Field(Location, name=graphene.String())
    locations_by_type = graphene.List(Location, type=graphene.String())
    shortest_path = graphene.List(Location, source_id=graphene.ID(), target_id=graphene.ID())
    network_metrics = graphene.JSONString()

    def resolve_locations(self, info):
        with current_app.driver.session() as session:
            result = session.run("MATCH (l:Location) RETURN l")
            return [Location(
                id=node['l'].id,
                name=node['l']['name'],
                type=node['l']['type'],
                coordinates=node['l']['coordinates'],
                properties=node['l']['properties']
            ) for node in result]

    def resolve_network_connections(self, info):
        with current_app.driver.session() as session:
            result = session.run("MATCH (s:Location)-[r]->(t:Location) RETURN s, r, t")
            return [NetworkConnection(
                id=rel['r'].id,
                source=Location(
                    id=node['s'].id,
                    name=node['s']['name'],
                    type=node['s']['type'],
                    coordinates=node['s']['coordinates'],
                    properties=node['s']['properties']
                ),
                target=Location(
                    id=node['t'].id,
                    name=node['t']['name'],
                    type=node['t']['type'],
                    coordinates=node['t']['coordinates'],
                    properties=node['t']['properties']
                ),
                type=rel['r']['type'],
                properties=rel['r']['properties']
            ) for rel in result]

    def resolve_location(self, info, id):
        with current_app.driver.session() as session:
            result = session.run("MATCH (l:Location {id: $id}) RETURN l", id=id)
            node = result.single()
            if node:
                return Location(
                    id=node['l'].id,
                    name=node['l']['name'],
                    type=node['l']['type'],
                    coordinates=node['l']['coordinates'],
                    properties=node['l']['properties']
                )
            return None

    def resolve_location_by_name(self, info, name):
        with current_app.driver.session() as session:
            result = session.run("MATCH (l:Location {name: $name}) RETURN l", name=name)
            node = result.single()
            if node:
                return Location(
                    id=node['l'].id,
                    name=node['l']['name'],
                    type=node['l']['type'],
                    coordinates=node['l']['coordinates'],
                    properties=node['l']['properties']
                )
            return None

    def resolve_locations_by_type(self, info, type):
        with current_app.driver.session() as session:
            result = session.run("MATCH (l:Location {type: $type}) RETURN l", type=type)
            return [Location(
                id=node['l'].id,
                name=node['l']['name'],
                type=node['l']['type'],
                coordinates=node['l']['coordinates'],
                properties=node['l']['properties']
            ) for node in result]

    def resolve_shortest_path(self, info, source_id, target_id):
        with current_app.driver.session() as session:
            result = session.run(
                "MATCH (s:Location {id: $source_id})-[:CONNECTS*]->(t:Location {id: $target_id}) "
                "RETURN s, t",
                source_id=source_id,
                target_id=target_id
            )
            nodes = result.single()
            if nodes:
                return [Location(
                    id=node.id,
                    name=node['name'],
                    type=node['type'],
                    coordinates=node['coordinates'],
                    properties=node['properties']
                ) for node in nodes]
            return []

    def resolve_network_metrics(self, info):
        with current_app.driver.session() as session:
            # Get basic network metrics
            result = session.run(
                "MATCH (l:Location) "
                "RETURN count(DISTINCT l) as nodes, count(DISTINCT ()-[]->()) as edges"
            )
            metrics = result.single()
            return {
                "nodes": metrics['nodes'],
                "edges": metrics['edges']
            }

class CreateLocation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        type = graphene.String(required=True)
        coordinates = graphene.List(graphene.Float, required=True)
        properties = graphene.JSONString()

    location = graphene.Field(lambda: Location)

    def mutate(self, info, name, type, coordinates, properties=None):
        with current_app.driver.session() as session:
            result = session.run(
                "CREATE (l:Location {name: $name, type: $type, coordinates: $coordinates, properties: $properties}) RETURN l",
                name=name,
                type=type,
                coordinates=coordinates,
                properties=properties
            )
            node = result.single()
            return CreateLocation(location=Location(
                id=node['l'].id,
                name=node['l']['name'],
                type=node['l']['type'],
                coordinates=node['l']['coordinates'],
                properties=node['l']['properties']
            ))

class CreateConnection(graphene.Mutation):
    class Arguments:
        source_id = graphene.ID(required=True)
        target_id = graphene.ID(required=True)
        type = graphene.String(required=True)
        properties = graphene.JSONString()

    connection = graphene.Field(lambda: NetworkConnection)

    def mutate(self, info, source_id, target_id, type, properties=None):
        with current_app.driver.session() as session:
            result = session.run(
                "MATCH (s:Location {id: $source_id}) "
                "MATCH (t:Location {id: $target_id}) "
                "CREATE (s)-[r:CONNECTS {type: $type, properties: $properties}]->(t) "
                "RETURN s, r, t",
                source_id=source_id,
                target_id=target_id,
                type=type,
                properties=properties
            )
            rel = result.single()
            return CreateConnection(connection=NetworkConnection(
                id=rel['r'].id,
                source=Location(
                    id=rel['s'].id,
                    name=rel['s']['name'],
                    type=rel['s']['type'],
                    coordinates=rel['s']['coordinates'],
                    properties=rel['s']['properties']
                ),
                target=Location(
                    id=rel['t'].id,
                    name=rel['t']['name'],
                    type=rel['t']['type'],
                    coordinates=rel['t']['coordinates'],
                    properties=rel['t']['properties']
                ),
                type=rel['r']['type'],
                properties=rel['r']['properties']
            ))

class Mutation(graphene.ObjectType):
    create_location = CreateLocation.Field()
    create_connection = CreateConnection.Field()
    update_location = graphene.Field(
        Location,
        id=graphene.ID(required=True),
        name=graphene.String(),
        type=graphene.String(),
        coordinates=graphene.List(graphene.Float),
        properties=graphene.JSONString()
    )

    def mutate(self, info, id, name=None, type=None, coordinates=None, properties=None):
        with current_app.driver.session() as session:
            query = "MATCH (l:Location {id: $id})"
            params = {"id": id}
            
            if name or type or coordinates or properties:
                updates = []
                if name: updates.append("l.name = $name")
                if type: updates.append("l.type = $type")
                if coordinates: updates.append("l.coordinates = $coordinates")
                if properties: updates.append("l.properties = $properties")
                
                query += " SET " + ", ".join(updates)
                
                if name: params["name"] = name
                if type: params["type"] = type
                if coordinates: params["coordinates"] = coordinates
                if properties: params["properties"] = properties
            
            query += " RETURN l"
            
            result = session.run(query, params)
            node = result.single()
            
            if node:
                return Location(
                    id=node['l'].id,
                    name=node['l']['name'],
                    type=node['l']['type'],
                    coordinates=node['l']['coordinates'],
                    properties=node['l']['properties']
                )
            return None

schema = graphene.Schema(query=Query, mutation=Mutation)
