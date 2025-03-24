from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence, RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_neo4j import Neo4jGraph, Neo4jVector
import json

AURA_CONNECTION_URI="neo4j+ssc://79831a17.databases.neo4j.io"
AURA_USERNAME="neo4j"
AURA_PASSWORD="vo_GyAdkN5fs82KBYfvnuNiWROSG9DYX9cMHXOqaa2o"

AZURE_OPENAI_KEY = ""
AZURE_OPENAI_ENDPOINT = "https://zeus-model-eastus2.openai.azure.com/"
AZURE_OPENAI_MODEL =  "gpt-4o-mini"
AZURE_OPENAI_MODEL_NAME = "gpt-4o-mini"
AZURE_OPENAI_VERSION = "2024-08-01-preview"

AZURE_OPENAI_EMBEDDING_NAME =  "textembedding"
AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"

embeddings=AzureOpenAIEmbeddings(model=AZURE_OPENAI_EMBEDDING_MODEL,azure_deployment=AZURE_OPENAI_EMBEDDING_NAME, api_version="2024-08-01-preview",api_key=AZURE_OPENAI_KEY,azure_endpoint=AZURE_OPENAI_ENDPOINT)


# graph = Neo4jGraph(
#     url=AURA_CONNECTION_URI,
#     username=AURA_USERNAME,
#     password=AURA_PASSWORD
# )

llm = AzureChatOpenAI(
    model=AZURE_OPENAI_MODEL,
    deployment_name=AZURE_OPENAI_MODEL_NAME,
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_VERSION,
)

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






# extract_prompt = PromptTemplate(
#     input_variables=["customer_request","activity_types"],
#     template=( """
#               You are an Adobe AI assistant that is tasked with classifying customer requests as needing technical or strategic support.
#               Customer Request: {customer_request}
#               Respond with technical or strategic if you are confident in your answer, otherwise respond with what additional details you need to gather to be able to become more confident in your answer.
    
        
#         """
#     )

# )


# category_prompt = PromptTemplate(
#     input_variables=["customer_request"],
#     template=( """
#         Based on the customer request below, go through each activity below and determine which activity is most relevant to the customer request and why? For the other activities, explain when they would be the most relevant to the customer request.
#         Here is the customer request: {customer_request}
#         Here are the activities to choose from:
#             1. Deskside Coaching:Enablement of a specific feature, concept or best practices, and product integrations for a specific Adobe solution. 
#             2. Environment Review:Conduct a detailed assessment of the customer's product environment to ensure compliance with contract terms and system limits. Focus on analyzing usage patterns, identifying overages, and providing guidance to remain within contractual boundaries.
#             3. Solution Review:For reviewing web implementation,  it can involve one or more of the following: Health of Current Implementation Variables (Health Dashboard), Scan of Website for General Tagging Failures (Observepoint Scan), Component Management and Best Practices (Component Review), Marketing Channel Audit. For mobile implementation, it involves the following: Checking lifecycle metrics, page level tracking, consistent MID across all calls, validate variables are being set in the flow properly
#             4. Event Planning and Monitoring:Planning critical go-lives, campaigns, product launches, and rollouts. Assist customers in preparing for major events, ensure systems can handle increased traffic and server demand. 24/7 monitoring during live events to ensure that nothing goes down.
#             5. Solution Troubleshooting:Troubleshoot Adobe Experience Cloud Solution issues for certain features, configurations, or performance-related problems. Provide findings and guidance to resolve these issues.
#             6. Upgrade or Migration Readiness:Customer needs to understand how to upgrade their Adobe Solution or migrate from one Adobe Solution to another.
            
#        Respond in the following format:
#         Activity: Activity Name
#         Reason: Reason for the answer
       
#         """
#     )
# )

accelerators={
        "Adoption and Enablement": {"Use Case Mapping to Solution Capability":"Customer needs help coming with use cases and Key Performance Indicators (KPI's)",
                                    "Deskside Coaching":"Enablement of a specific feature, concept or best practices, and product integrations for a specific  Adobe solution." , 
                                    "Tool Workflow and Governance Optimization":"Tool governance related to the Adobe solution. Access, permissions, and controls to ensure proper management of the solution", 
                                    "Adoption Review":"Focus on identifying underutilized features, integration opportunities, and areas for expanded solution use that the customer is not aware of."},
        "Technical Readiness": {"Environment Review":"Conduct a detailed assessment of the customer's product environment to ensure compliance with contract terms and system limits. Focus on analyzing usage patterns, identifying overages, and providing guidance to remain within contractual boundaries.",
                                "Solution Review":"For reviewing web implementation,  it can involve one or more of the following: Health of Current Implementation Variables (Health Dashboard), Scan of Website for General Tagging Failures (Observepoint Scan), Component Management and Best Practices (Component Review), Marketing Channel Audit. For mobile implementation, it involves the following: Checking lifecycle metrics, page level tracking, consistent MID across all calls, validate variables are being set in the flow properly",
                                "Event Planning and Monitoring":"Planning critical go-lives, campaigns, product launches, and rollouts. Assist customers in preparing for major events, ensure systems can handle increased traffic and server demand. 24/7 monitoring during live events to ensure that nothing goes down.",
                                "Solution Troubleshooting":"Troubleshoot Adobe Experience Cloud Solution issues for certain features, configurations, or performance-related problems. Provide findings and guidance to resolve these issues.",
                                "Upgrade or Migration Readiness":"Customer needs to understand how to upgrade their Adobe Solution or migrate from one Adobe Solution to another."},
        "Organizational Readiness": {"Change Management and Communication Strategies": "Discuss communication strategies to ensure change is adopted within the organization, for example if they are trying to get users to start using a new Adobe Solution.",
                                     "Digital Review and Benchmarking":"Benchmarking and digital maturity assessments to help customers understand where they stand in comparison to their competitors and industry standards.",
                                     "Operating Model and Organization Governance": "Establishing Centers of Excellence (CoE) and operating models within the customer's organization to promote collaboration and strong leadership support.",
                                     "Strategic Roadmap and Cycle Planning":"Identify areas for improvement in strategic roadmap and developing an effective marketing strategy using the Adobe Experience Cloud Solutions."}
                                     

    }
category_prompt = PromptTemplate(
    input_variables=["customer_request"],
    template=( """
        Think step by step on which activity is most relevant to the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. Place your thought process in <thinking></thinking> tags. One you have finished your thought process, respond with only the activity name in <answer></answer> tags.
        Here is the customer request: {customer_request}
        Here are the activities to choose from:
            1. Deskside Coaching:Enablement of a specific feature, concept or best practices, and product integrations for a specific Adobe solution. 
            2. Environment Review:Conduct a detailed assessment of the customer's product environment to ensure compliance with contract terms and system limits. Focus on analyzing usage patterns, identifying overages, and providing guidance to remain within contractual boundaries.
            3. Solution Review: Audit or review of a specific implementation component of the customer's Adobe Solution. Not to be used to resolve an issue.
            4. Event Planning and Monitoring:Planning critical go-lives, campaigns, product launches, and rollouts. Assist customers in preparing for major events, ensure systems can handle increased traffic and server demand. 24/7 monitoring during live events to ensure that nothing goes down.
            5. Solution Troubleshooting:Troubleshoot Adobe Experience Cloud Solution issues for certain features, configurations, or performance-related problems. Provide findings and guidance to resolve these issues.
            6. Upgrade or Migration Readiness:Customer needs to understand how to upgrade their Adobe Solution or migrate from one Adobe Solution to another.
            7. Use Case Mapping to Solution Capability:Customer needs help coming with use cases and Key Performance Indicators (KPI's)
            9. Tool Workflow and Governance Optimization:Tool governance related to the Adobe solution. Access, permissions, and controls to ensure proper management of the solution
            10. Adoption Review:Focus on identifying underutilized features, integration opportunities, and areas for expanded solution use that the customer is not aware of.
            11. Change Management and Communication Strategies:Discuss communication strategies to ensure change is adopted within the organization, for example if they are trying to get users to start using a new Adobe Solution.
            12. Digital Review and Benchmarking:Benchmarking and digital maturity assessments to help customers understand where they stand in comparison to their competitors and industry standards.
            13. Operating Model and Organization Governance:Establishing Centers of Excellence (CoE) and operating models within the customer's organization to promote collaboration and strong leadership support.
            14. Strategic Roadmap and Cycle Planning:Identify areas for improvement in strategic roadmap and developing an effective marketing strategy using the Adobe Experience Cloud Solutions.
        """
    )
)

solution_prompt = PromptTemplate(
    input_variables=["customer_request"],
    template=( """
        Think step by step on which Adobe solutions the customer request could apply to, but only keep a minimum draft for each thinking step, with 5 words at most. Place your thought process in <thinking></thinking> tags. One you have finished your thought process, respond in <answer></answer> tags.
        Customer Request: {customer_request}
        Adobe solutions: 
              1. Adobe Analytics: Web and mobile analytics solution that helps businesses collect, analyze, and visualize data to understand customer behavior
              2. Adobe Target: Personalization platform that helps businesses optimize and deliver personalized experiences to customers across various channels
              3. Adobe Customer Journey Analytics: Analyze customer journeys across channels using data from the Adobe Experience Platform
              4. Adobe Experience Platform: Centralized data storage and management system for all customer data which is used to power the Adobe Experience Cloud solutions.
              5. Adobe Audience Manager: Helps you bring your audience data assets together, making it easy to collect commercially relevant information about site visitors, create marketable segments, and serve targeted advertising and content to the right audience
              6. Adobe Campaign
              7. Adobe Real-Time CDP
              8. Adobe Marketo Engage
              9. Adobe Commerce
              10. Adobe Journey Optimizer
              11. Adobe Journey Orchestration
              12. Adobe Experience Manager
        """
    )
)

issue_prompt = PromptTemplate(
    input_variables=["customer_request"],
    template=( """
        Analyze the following customer input and classify the issue into a category of Adobe Analytics. Only state the category name and write a short one sentence description of the category. When writing the description, be sure to ignore any specific details from the customer input and focus on the general category description.
        Customer Input: {customer_request}
        """
    )
)

relevant_prompt = PromptTemplate(
    input_variables=["customer_request"],
    template=( """
        Think step by step on if the customer request is relevent based on the criteria below , but only keep a minimum draft for each thinking step, with 5 words at most. Place your thought process in <thinking></thinking> tags. One you have finished your thought process, respond with <answer></answer> tags.
        Here is the customer request: {customer_request}
        Here are the criteria:
        - The customer request is a customer need or request for action.
        - The customer request involves a Adobe Experience Cloud or Adobe Experience Platform suite product.
        """
    )
)

extract_prompt= PromptTemplate(
    input_variables=["customer_request"],
    template=( """
        You are an Adobe AI Customer Support Agent to help the customer with technical and strategic support.
        Before, you can help the customer, you need to understand their request, to ensure you have all the information to route the request under the correct activity.
        Determine if the customer request contains all the details below,
        Here is the customer request: {customer_request}
        Here are the details:
            - Customer need 
            - Reason for customer need
        
        If all the details above are present, respond with a summary of both the customer need and reason for the need in a single paragraph, with no extra details inside a <summary></summary> tag.
        If any of the details are missing, respond with what details are missing inside a <missing></missing> tag.
            
        """
    )
)

# solution_prompt= PromptTemplate(
#     input_variables=["customer_request"],
#     template=( """
#         Based on the customer request below, 
#         Customer Request: {customer_request}
#         """
#     )
# )
              
def fetch_categories(graph):
    query = """
    MATCH (a:Accelerator {name: 'Solution Troubleshooting'})-[:HAS_ISSUE]->(c:Issue)
    RETURN c.name AS name, c.description AS description
    """
    result = graph.query(query)
    categories = [{"name": record["name"], "description": record["description"]} for record in result]
    formatted_categories = ""
    for i, category in enumerate(categories, start=1):
        formatted_categories += f"{i}. {category['name']}: {category['description']}\n"
    print(formatted_categories)
    return formatted_categories
 
def add_category(graph, name, description):
    query = """
    MATCH (a:Accelerator {name: 'Solution Troubleshooting'})
    CREATE (c:Issue {name: $name, description: $description})
    CREATE (a)-[:HAS_ISSUE]->(c)
    """
    params = {"name": name, "description": description}
    graph.query(query, params=params)

def parse_response(response):
    category_name = response.get("category_name")
    description = response.get("description")
    status = response.get("status")
    return category_name, description, status


topic_prompt=  PromptTemplate(
    input_variables=["customer_request","categories"],
    template=( """
            Task:
            I have a list of categories related to customer issues in Adobe Analytics. Your task is to review the customer's issue below and suggest the most appropriate category from the list provided.
            
            Existing Categories:
            {categories}
              
            Customer Issue: {customer_request}
            
            Instructions:
              1. Review the customer issue above.
              2. Select the category that best fits the customer issue from the list of existing categories.
              3. If no existing category fits the customer issue, suggest a new category and provide a short one sentence general description of the category. If the category already exists, the status will be "Exists", otherwise it will be "New".  state the category name and write a short one sentence description of the category. When writing the description, be sure to ignore any specific details from the customer input and focus on the general category description.
              4. Respond with ONLY a valid JSON object in the following format (no other text before or after): : 
                {{
                    "category_name": "Category Name",
                    "description": "Description",
                    "status": "status"
                }}
        """
    )
)

similar_prompt = PromptTemplate(
    input_variables=["documents","customer_issue"],
    template=( """
        Based on the documents below retrieved from Neo4jVector, can you identify the top 3 most similar documents to the customer issue provided?
        Documents: {documents}
        Customer Issue: {customer_issue}
              """
    ))

deskside_prompt = PromptTemplate(
    input_variables=["customer_request"],
    template=( """
        Reword the following customer request to use more accurate terminology based on the latest dobe Experience League documentation
        Customer Request: {customer_request}
        """
    ))

deskside_chain= deskside_prompt | llm | StrOutputParser()

solution_chain= solution_prompt | llm | StrOutputParser()

extract_chain = extract_prompt | llm | StrOutputParser()

category_chain=category_prompt | llm | StrOutputParser()

issue_chain = issue_prompt | llm | StrOutputParser()

topic_chain= topic_prompt | llm | JsonOutputParser()

similar_chain= similar_prompt | llm | StrOutputParser()

relevant_chain= relevant_prompt | llm | StrOutputParser()


def process_customer_request(customer_request):
    # Step 1: Extract key details
    # categories=fetch_categories(graph)
    # extraction_result = topic_chain.invoke({"customer_request": customer_request,"categories":categories})
    # desk_result=deskside_chain.invoke({"customer_request":customer_request})
    # return desk_result
    # extract_result=extract_chain.invoke({"customer_request":customer_request})
    # print(extract_result)

    # category_result=category_chain.invoke({"customer_request":customer_request})
    # print(category_result)
  
    extract_result=extract_chain.invoke({"customer_request":customer_request})
    print(extract_result)

    # solution_result=solution_chain.invoke({"customer_request":customer_request})
    # print(solution_result)
    # category_name,description,status=parse_response(extraction_result)
    # if status=="New":
    #     add_category(graph, category_name,description)
    
    # activity_store= Neo4jVector.from_existing_index(
    #     embedding=embeddings,
    #     url=AURA_CONNECTION_URI,
    #     username=AURA_USERNAME,
    #     password=AURA_PASSWORD,
    #     index_name="activity_index",
    #     text_node_property="description",
    # )

    # results = activity_store.similarity_search_with_score("they would like to understand how to get the CJA data connector launched")
    # THRESHOLD=0.80
    # filtered_results = [(doc, score) for doc, score in results if score > THRESHOLD]
    # print(filtered_results)
    # similar_result=similar_chain.invoke({"documents":filtered_results,"customer_issue":customer_request})
    # print(similar_result)
    # # Parse extracted details
    # return similar_result


    # # Step 2: Classify the request
    # classification_result = classification_chain.invoke({
    #     "customer_challenge": customer_challenge,
    #     "engagement_ask": engagement_ask
    # })

    

# Example customer request
customer_request =  """
When come to Adobe Launch Implementation, what the best approach will be? Our current implementation has heavy JS code on the Adobe Launch with less rules set up, and we don’t use Adobe Analytics datalayer extension plug-in to define the object.  However, during my recent discussion for Adobe Analytics update, it was brought to my attention that the best practice should be building all data in Magento datalayer, then build data object in Adobe Analytics datalayer extension and finally build analytics rules is Adobe Launch to capture the data, which could potentially help with the future CJA migration.

FYI, for our implementation, we have customized implementation for production finding method, add to cart location by leverage Merch evar.
 
Could we have discussion on the pros and cons on each implementation? What is the better way for future maintenance and migration to CJA?
"""

# Run the pipeline
result = process_customer_request(customer_request)

# Output the final result
print(result)