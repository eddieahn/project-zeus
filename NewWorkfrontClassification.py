from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.weaviate import WeaviateVectorStore
import weaviate
import os
import pandas as pd


AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_API_KEY") or "de94456faa5b415b943034ed720811ed"
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT") or "https://compasaoaiuks.openai.azure.com/"
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL") or "gpt-4"
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_OPENAI_MODEL_NAME") or "gpt4"
AZURE_OPENAI_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION") or "2024-03-01-preview"
AZURE_OPENAI_EMBEDDING_NAME = os.environ.get("AZURE_OPENAI_EMBEDDING_NAME") or "textembedding"
AZURE_OPENAI_EMBEDDING_MODEL = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL") or "text-embedding-ada-002"
WEAVIATE_CLIENT_URL = os.environ.get("WEAVIATE_CLIENT_URL") or "http://weaviate.compas-weaviate.svc.cluster.local:80"




client = weaviate.Client("http://localhost:8080")



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





# Initialize embedding model
llm = AzureOpenAI(
    model=AZURE_OPENAI_MODEL,
    deployment_name=AZURE_OPENAI_MODEL_NAME,
    api_key='de94456faa5b415b943034ed720811ed',
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_VERSION,
)

embedding_model = AzureOpenAIEmbedding(
    model=AZURE_OPENAI_EMBEDDING_MODEL,
    deployment_name=AZURE_OPENAI_EMBEDDING_NAME,
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_VERSION,
)

csv_file_path="Workfront Classification.csv"
df=pd.read_csv(csv_file_path)
df.fillna("", inplace=True)
activity_descriptions = df.to_dict(orient="records")



# schema = {
#     "classes": [
#         {
#             "class": "WorkfrontClassification",
#             "properties": [
#                 {"name": "description", "dataType": ["text"]},
#                 {"name": "activity_type", "dataType": ["text"]},
#                 {"name": "adobe_analytics", "dataType": ["text"]},
#                 {"name": "customer_journey_analytics", "dataType": ["text"]},
#                 {"name": "target", "dataType": ["text"]},
#                 {"name": "experience_platform_core", "dataType": ["text"]},
#                 {"name": "audience_manager", "dataType": ["text"]},  
#             ]
#         }
#     ]
# }


# # Check if the schema already exists
# existing_classes = client.schema.get()["classes"]
# if not any(cls["class"] == "WorkfrontClassification" for cls in existing_classes):
#     client.schema.create(schema)



# # Add data to Weaviate
# for activity in activity_descriptions:
#     # Generate embedding for the description using AzureOpenAIEmbedding
#     embedding = embedding_model.get_text_embedding(activity["Description"])
    
#     # Check if the object already exists by activity type
#     response = client.query.get(
#         class_name="WorkfrontClassification",
#         properties=["_additional { id }"]
#     ).with_where({
#         "path": ["activity_type"],
#         "operator": "Equal",
#         "valueText": activity["Activity Name"]
#     }).do()

#     if response["data"]["Get"]["WorkfrontClassification"]:
#         # Update existing object
#         object_id = response["data"]["Get"]["WorkfrontClassification"][0]["_additional"]["id"]
#         client.data_object.update(
#             data_object={
#                 "description": activity["Description"],
#                 "activity_type": activity["Activity Name"],
#                 "adobe_analytics": activity["Adobe Analytics"],
#                 "customer_journey_analytics": activity["Customer Journey Analytics"],
#                 "target": activity["Target"],
#                 "experience_platform_core": activity["Experience Platform Core"],
#                 "audience_manager": activity["Audience Manager"]
#             },
#             class_name="WorkfrontClassification",
#             uuid=object_id,
#             vector=embedding
#         )
#         print(f"Updated object with ID {object_id}.")
#     else:
#         # Create new object
#         client.data_object.create(
#             data_object={
#                 "description": activity["Description"],
#                 "activity_type": activity["Activity Name"],
#                 "adobe_analytics": activity["Adobe Analytics"],
#                 "customer_journey_analytics": activity["Customer Journey Analytics"],
#                 "target": activity["Target"],
#                 "experience_platform_core": activity["Experience Platform Core"],
#                 "audience_manager": activity["Audience Manager"]
#             },
#             class_name="WorkfrontClassification",
#             vector=embedding
#         )
#         print(f"Created new object for activity type {activity['Activity Name']}.")



activity_mapping={
    "Adobe Analytics": "adobe_analytics",
    "Customer Journey Analytics": "customer_journey_analytics",
    "Target": "target",
    "Experience Platform Core": "experience_platform_core",
    "Audience Manager": "audience_manager"
}



def classify_customer_ask_with_rag(customer_ask,activity_type):
    solution_property = activity_mapping.get(activity_type)

    scope_prompt = f"""
You are a classification assistant. Determine if the following customer query is within the scope of services provided. If it is out of scope, respond with "Out of Scope". Otherwise, respond with "In Scope".

Out-of-Scope Criteria:
- Custom code solutions
- Requests for unsupported features that are not part of the Adobe Experience Cloud or Adobe Experience Platform suite
- Requests for services not provided by Adobe Experience Cloud or Adobe Experience Platform suite
- Requests that involve the Adobe Experience Cloud or Adobe Experience Platform suite products implemented using third party tools or services 

Customer Query: "{customer_ask}"
"""
    scope_response = llm.complete(scope_prompt)
    scope_text = scope_response.text.strip()
    if scope_text == "Out of Scope":
        print("The customer ask is out of scope for a Success Accelerator.")
        return
    
    query_embedding = embedding_model.get_text_embedding(customer_ask)
    
    # Query Weaviate for relevant matches using near-vector search
    response = client.query.get(
        class_name="WorkfrontClassification",
        properties=["description", "activity_type",solution_property]
    ).with_near_vector({
        "vector": query_embedding,
        "certainty": 0.7 
    }).with_additional(["certainty"]).with_limit(10).do()

    top_matches = response.get("data", {}).get("Get", {}).get("WorkfrontClassification", [])

    # Print and debug matches
    for idx, match in enumerate(top_matches):
        print(f"Rank {idx+1}:")
        print(f"Activity Type: {match['activity_type']}")
        print(f"Description: {match['description']}")
        if solution_property in match and match[solution_property]:
            print(f"{activity_type}: {match[solution_property]}")
        print(f"Score: {match['_additional']['certainty']}")
    
    # Extract relevant matches
    retrieved_data = []
    if response["data"]["Get"]["WorkfrontClassification"]:
        for match in response["data"]["Get"]["WorkfrontClassification"]:
            if match.get(solution_property) == "N/A":
                continue  # Skip matches with "N/A" value for the solution property
            item = {
                "activity_type": match["activity_type"],
                "description": match["description"]
            }
            if solution_property in match and match[solution_property]:
                item[solution_property] = match[solution_property]
            retrieved_data.append(item)
    else:
        # No matches found
        return {"activity_type": "No match found", "description": None}
    
    # Check if the relevant property has "N/A"
    if any(item.get(solution_property) == "N/A" for item in retrieved_data):
        return f"The specific solution for the activity type '{activity_type}' is not covered."
    
    # Format retrieved data as a prompt for LLM
    formatted_context = "\n\n".join(
        f"- Activity Type: {item['activity_type']}\n  Description: {item['description']}\n {activity_type}: {item.get(solution_property, '')}"
        for item in retrieved_data
    )
    # llm_prompt = f"""
    # # You are a classification assistant. Based on the customer's query, identify the most relevant activity type without the description, but include an explanation why that is the best choice.

    # # Customer Query: "{customer_ask}"

    # # Options:
    # # {formatted_context}

    # # Respond with the activity type and a brief explanation.
    # #   """

    llm_prompt = f"""
You are a classification assistant. When classifying customer requests, ensure the following rules are adhered to:
1. Focus only on the activity types that meet the given conditions.

Customer Query: "{customer_ask}"

Options:
{formatted_context}

Respond only with the most relevant activity type and its description in the following format:
Activity Type: [activity type]
Resoning: [description]
"""

    #Use Azure OpenAI LLM to classify based on retrieved context
    llm_response = llm.complete(llm_prompt)

            
    #Log the full LLM response to understand its structure
    print("LLM Response:", llm_response)
    response_text = llm_response.text.strip()
    activity_type = None
    for line in response_text.split('\n'):
        if line.startswith("Activity Type:"):
            activity_type = line.split(":")[1].strip()
            break

    print(f"Extracted Activity Type: {activity_type}")


customer_ask = """Conduct a detailed assessment of the customer's product environment to ensure compliance with contract terms and system limits."""
activity_type="Adobe Analytics"
activity_classification = classify_customer_ask_with_rag(customer_ask,activity_type)













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

