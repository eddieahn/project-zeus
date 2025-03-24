from langchain_neo4j import Neo4jGraph
AURA_CONNECTION_URI="neo4j+ssc://79831a17.databases.neo4j.io"
AURA_USERNAME="neo4j"
AURA_PASSWORD="vo_GyAdkN5fs82KBYfvnuNiWROSG9DYX9cMHXOqaa2o"


topic_involved="Analytics Source Connector"
graph = Neo4jGraph(
    url=AURA_CONNECTION_URI,
    username=AURA_USERNAME,
    password=AURA_PASSWORD
)

# def fetch_topics(graph):
#     query = """
#     MATCH (a:Accelerator {name: 'Deskside Coaching'})-[:HAS_TOPIC]->(c:Topic)
#     RETURN c.name AS name
#     """
#     result = graph.query(query)
#     topics = [record["name"] for record in result]
#     return topics

def get_experts_for_topic(graph, topic):
    query = "MATCH (t:Topic {name: $topic_name})<-[:EXPERT_IN]-(r:Resource) RETURN r.name AS name"
    result = graph.query(query, {"topic_name": topic})
    experts=[record["name"] for record in result]
    experts_text = ", ".join(experts)
    return experts_text

def topic_exists(graph, topic):
    query = "MATCH (t:Topic) WHERE t.name = $topic_name RETURN COUNT(t) > 0 as exists"
    result = graph.query(query, {"topic_name": topic})
    return result[0]["exists"] if result else False

print(topic_exists(graph, topic_involved))
print(get_experts_for_topic(graph, topic_involved))