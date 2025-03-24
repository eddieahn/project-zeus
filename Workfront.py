from langchain.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain, Neo4jVector
from neo4jgraph import GraphDatabase
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.generation import GraphRAG



AURA_CONNECTION_URI="neo4j+ssc://79831a17.databases.neo4j.io"
AURA_USERNAME="neo4j"
AURA_PASSWORD="vo_GyAdkN5fs82KBYfvnuNiWROSG9DYX9cMHXOqaa2o"

AZURE_OPENAI_KEY = ""
AZURE_OPENAI_ENDPOINT = "https://zeus-model-eastus2.openai.azure.com/"
AZURE_OPENAI_MODEL =  "gpt-4o-mini"
AZURE_OPENAI_MODEL_NAME = "gpt-4o-mini"
AZURE_OPENAI_EMBEDDING_NAME =  "textembedding"
AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"

embeddings=AzureOpenAIEmbeddings(model=AZURE_OPENAI_EMBEDDING_MODEL,azure_deployment=AZURE_OPENAI_EMBEDDING_NAME, api_version="2024-08-01-preview",api_key=AZURE_OPENAI_KEY,azure_endpoint=AZURE_OPENAI_ENDPOINT)

driver=GraphDatabase.driver(AURA_CONNECTION_URI, auth=(AURA_USERNAME, AURA_PASSWORD))
driver.close()

graph = Neo4jGraph(
    url=AURA_CONNECTION_URI,
    username=AURA_USERNAME,
    password=AURA_PASSWORD
)

# retrieval_query="""
# MATCH
# (a:Accelerator)-[:HAS_ACTIVITY]->(node)
# RETURN
# node.name AS success_accelerator,
# """


# vc_retriever=VectorCypherRetriever(
#     driver,
#     index_name="activity_index",
#     embedder=embeddings,
#     retrieval_query=retrieval_query,
# )

# activity_graph= Neo4jVector.from_existing_graph(
#     embedding=embeddings,
#     url=AURA_CONNECTION_URI,
#     username=AURA_USERNAME,
#     password=AURA_PASSWORD,
#     index_name="activity_index",
#     node_label="Activity",
#     text_node_properties=["description"],
#     embedding_node_property="activity_embedding"
# )

activity_store= Neo4jVector.from_existing_index(
    embedding=embeddings,
    url=AURA_CONNECTION_URI,
    username=AURA_USERNAME,
    password=AURA_PASSWORD,
    index_name="activity_index",
    text_node_property="description",
)

results = activity_store.similarity_search_with_score("learn about the CJA Data Connector")
THRESHOLD=0.5
filtered_results = [(doc, score) for doc, score in results if score > THRESHOLD]
print(filtered_results)



# chain = GraphCypherQAChain.from_llm(
#     AzureChatOpenAI(azure_deployment=AZURE_OPENAI_MODEL_NAME, api_version="2024-08-01-preview",api_key=AZURE_OPENAI_KEY,azure_endpoint=AZURE_OPENAI_ENDPOINT),
#     graph=graph,
#     return_intermediate_steps=True,
#     allow_dangerous_requests=True
# )
# response=chain.invoke("What are the top Solution Troubleshooting issues that have been submitted?")
# print(response)
