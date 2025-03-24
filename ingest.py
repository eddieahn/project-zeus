from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore
import weaviate
import os
import pandas as pd
import weaviate.connect


AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_API_KEY") or ""
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT") or "https://zeus-model-eastus2.openai.azure.com/"
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL") or "gpt-4o-mini"
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_OPENAI_MODEL_NAME") or "gpt-4o-mini"
AZURE_OPENAI_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION") or "2024-08-01-preview"
AZURE_OPENAI_EMBEDDING_NAME = os.environ.get("AZURE_OPENAI_EMBEDDING_NAME") or "textembedding"
AZURE_OPENAI_EMBEDDING_MODEL = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL") or "text-embedding-3-large"
WEAVIATE_CLIENT_URL = os.environ.get("WEAVIATE_CLIENT_URL") or "http://weaviate.compas-weaviate.svc.cluster.local:80"


embedding_model = AzureOpenAIEmbedding(
    model=AZURE_OPENAI_EMBEDDING_MODEL,
    deployment_name=AZURE_OPENAI_EMBEDDING_NAME,
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_VERSION,
)

print(AZURE_OPENAI_KEY)
print(AZURE_OPENAI_ENDPOINT)

#client = weaviate.Client("http://weaviate.compas-weaviate.svc.cluster.local:80")

client = weaviate.Client("https://lorrdtftleztqq0pon3jw.c0.us-east1.gcp.weaviate.cloud",auth_client_secret= weaviate.AuthApiKey('n44LQVgeyigroQ57sijG0scN8y6MzdvZ1LaU'))                                  

print(client.is_ready())

# # Retrieve all objects of the WorkfrontClassification class
# response = client.query.get(
#     class_name="WorkfrontClassification",
#     properties=["_additional { id }"]
# ).do()

# # Delete the retrieved objects
# if response["data"]["Get"]["WorkfrontClassification"]:
#     for obj in response["data"]["Get"]["WorkfrontClassification"]:
#         object_id = obj["_additional"]["id"]
#         client.data_object.delete(object_id)
#         print(f"Deleted object with ID {object_id}.")
# else:
#     print("No objects found in the WorkfrontClassification class.")





# response = client.query.get(
#     class_name="WorkfrontClassification",
#     properties=["description", "activity_type","adobe_analytics","customer_journey_analytics","target","experience_platform_core","audience_manager"]
# ).do()


# # Print the retrieved objects
# if response["data"]["Get"]["WorkfrontClassification"]:
#     for obj in response["data"]["Get"]["WorkfrontClassification"]:
#         print(obj)
# else:
#     print("No objects found in the WorkfrontClassification class.")



columns_to_read = [
    "Activity Name", "Description", "General Guardrails", "Adobe Analytics",
    "Customer Journey Analytics", "Target", "Experience Platform Core", "Audience Manager"
]

csv_file_path="Workfront Classification.csv"
df=pd.read_csv(csv_file_path, usecols=columns_to_read)
df.fillna(" ", inplace=True)
df = df[df["Activity Name"].str.strip() != ""]
activity_descriptions = df.to_dict(orient="records")
print(activity_descriptions)


schema = {
    "classes": [
        {
            "class": "WorkfrontClassification",
            "properties": [
                {"name": "description", "dataType": ["text"]},
                {"name": "activity_type", "dataType": ["text"]},
                {"name": "adobe_analytics", "dataType": ["text"]},
                {"name": "customer_journey_analytics", "dataType": ["text"]},
                {"name": "target", "dataType": ["text"]},
                {"name": "experience_platform_core", "dataType": ["text"]},
                {"name": "audience_manager", "dataType": ["text"]},  
            ]
        }
    ]
}


# # Check if the schema already exists
# existing_classes = client.schema.get()["classes"]
# if not any(cls["class"] == "WorkfrontClassification" for cls in existing_classes):
#     client.schema.create(schema)



# Add data to Weaviate
for activity in activity_descriptions:
    # Generate embedding for the description using AzureOpenAIEmbedding
    embedding = embedding_model.get_text_embedding(activity["Description"])
    
    # Check if the object already exists by activity type
    response = client.query.get(
        class_name="WorkfrontClassification",
        properties=["_additional { id }"]
    ).with_where({
        "path": ["activity_type"],
        "operator": "Equal",
        "valueText": activity["Activity Name"]
    }).do()

    if response["data"]["Get"]["WorkfrontClassification"]:
        # Update existing object
        object_id = response["data"]["Get"]["WorkfrontClassification"][0]["_additional"]["id"]
        client.data_object.update(
            data_object={
                "description": activity["Description"],
                "activity_type": activity["Activity Name"],
                "adobe_analytics": activity["Adobe Analytics"],
                "customer_journey_analytics": activity["Customer Journey Analytics"],
                "target": activity["Target"],
                "experience_platform_core": activity["Experience Platform Core"],
                "audience_manager": activity["Audience Manager"]
            },
            class_name="WorkfrontClassification",
            uuid=object_id,
            vector=embedding
        )
        print(f"Updated object with ID {object_id}.")
    else:
        # Create new object
        client.data_object.create(
            data_object={
                "description": activity["Description"],
                "activity_type": activity["Activity Name"],
                "adobe_analytics": activity["Adobe Analytics"],
                "customer_journey_analytics": activity["Customer Journey Analytics"],
                "target": activity["Target"],
                "experience_platform_core": activity["Experience Platform Core"],
                "audience_manager": activity["Audience Manager"]
            },
            class_name="WorkfrontClassification",
            vector=embedding
        )
        print(f"Created new object for activity type {activity['Activity Name']}.")













# # Initialize WeaviateVectorStore and VectorStoreIndex
# vector_store = WeaviateVectorStore(client, index_name="WorkfrontClassification")
# index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embedding_model)

# def classify_customer_ask(customer_ask):
#     # Generate embedding for the customer ask using embed_query
#     query_embedding = embedding_model.get_text_embedding(customer_ask)
    
#     # Query Weaviate directly with the embedding
#     response = client.query.get(
#         class_name="WorkfrontClassification",
#         properties=["description", "activity_type"]
#     ).with_near_vector({
#         "vector": query_embedding,
#         "certainty": 0.7
#     }).with_limit(5).do()


#     retrieved_data = []
#     if response["data"]["Get"]["WorkfrontClassification"]:
#         for match in response["data"]["Get"]["WorkfrontClassification"]:
#             retrieved_data.append({
#                 "activity_type": match["activity_type"],
#                 "description": match["description"]
#             })
#     else:
#         # No matches found
#         return {"activity_type": "No match found", "description": None}
    
#     return retrieved_data
#     # # If matches found, return the activity type and description
#     # if response["data"]["Get"]["WorkfrontClassification"]:
#     #     match = response["data"]["Get"]["WorkfrontClassification"][0]
#     #     description = match["description"]
#     #     activity_type = match["activity_type"]
#     #     return {"activity_type": activity_type, "description": description}
    
#     # return {"activity_type": "No match found", "description": None}

# customer_ask = "Customer migrating from Segment to Tag Manager"
# activity_type = classify_customer_ask(customer_ask)
# print(activity_type)
# print(f"Classified Activity Type: {activity_type['activity_type']}")

