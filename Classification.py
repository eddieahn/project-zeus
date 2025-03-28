import streamlit as st
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
import weaviate
import os
import time
import sqlite3
from sqlalchemy import text
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import ssl
import datetime
from streamlit_feedback import streamlit_feedback

# Set environment variables or use default values
AZURE_OPENAI_KEY = ""
AZURE_OPENAI_ENDPOINT = "https://zeus-model-eastus2.openai.azure.com/"
AZURE_OPENAI_MODEL = "gpt-4o-mini"
AZURE_OPENAI_MODEL_NAME = "gpt-4o-mini"
AZURE_OPENAI_VERSION = "2024-08-01-preview"
AZURE_OPENAI_EMBEDDING_NAME = "textembedding"
AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"
WEAVIATE_CLIENT_URL = os.environ.get("WEAVIATE_CLIENT_URL") or "http://weaviate.compas-weaviate.svc.cluster.local:80"


# Initialize Weaviate client

client = weaviate.Client("https://lorrdtftleztqq0pon3jw.c0.us-east1.gcp.weaviate.cloud",auth_client_secret= weaviate.AuthApiKey('n44LQVgeyigroQ57sijG0scN8y6MzdvZ1LaU'))       

# Initialize embedding model
llm = AzureOpenAI(
    model=AZURE_OPENAI_MODEL,
    deployment_name=AZURE_OPENAI_MODEL_NAME,
    api_key=AZURE_OPENAI_KEY,
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

solution_mapping = {
    "Adobe Analytics": "adobe_analytics",
    "Customer Journey Analytics": "customer_journey_analytics",
    "Target": "target",
}



def precheck(customer_ask):

    relevant_prompt=f"""
    You are a classification assistant. Determine if the input is a customer request.
    Respond "Relevant" if it expresses a customer need or request for action.
    Respond "Irrelevant" if it provides general information or lacks a specific request.
    Assume implied intent when the language suggests a need, even if not explicitly stated.

    Input: "{customer_ask}"
    """
    relevant_response = llm.complete(relevant_prompt)
    relevant_text = relevant_response.text.strip()

    print(relevant_text)

    if relevant_text == "Irrelevant":
        return relevant_text
    else:
        return "In Scope"

    # else:
    #     scope_prompt = f"""
    #     You are a classification assistant. Determine if the following customer query is within the scope of services provided. If it is out of scope, respond with "Out of Scope". Otherwise, respond with "In Scope".

    #     Out-of-Scope Criteria:
    #     - Custom code solutions
    #     - Requests for unsupported features that are not part of the Adobe Experience Cloud or Adobe Experience Platform suite
    #     - Requests for services not provided by Adobe Experience Cloud or Adobe Experience Platform suite
    #     - Requests that involve the Adobe Experience Cloud or Adobe Experience Platform suite products implemented using third party tools or services 

    #     Customer Query: "{customer_ask}"
    #     """
    #     scope_response = llm.complete(scope_prompt)
    #     scope_text = scope_response.text.strip()
    #     if scope_text == "Out of Scope":
    #         return "The customer ask is out of scope for a Success Accelerator."
    #     else:
    #         return "In Scope"




def assistant(customer_ask):
    enablement_prompt = f"""
    You are a classification assistant. Determine if the following customer request involves a 101 Enablement Bootcamp or a multi-session training program for new users, focusing on learning the basics of the Adobe Solution. If it does, respond with "True". Otherwise, respond with "False".

    Customer Query: "{customer_ask}"
    """
    enablement_response = llm.complete(enablement_prompt)
    enablement_text = enablement_response.text.strip()

    if enablement_text=="True":
        return "Enablement Bootcamp"


def classify_customer_ask_with_rag(customer_ask, solution):
    solution_property = solution_mapping.get(solution)

    query_embedding = embedding_model.get_text_embedding(customer_ask)

    # Query Weaviate for relevant matches using near-vector search
    response = client.query.get(
        class_name="WorkfrontClassification",
        properties=["description", "activity_type", solution_property]
    ).with_near_vector({
        "vector": query_embedding,
        "certainty": 0.5
    }).with_additional(["certainty"]).with_limit(5).do()

    top_matches = response.get("data", {}).get("Get", {}).get("WorkfrontClassification", [])
    print(top_matches)

    # Extract relevant matches
    retrieved_data = []
    if response["data"]["Get"]["WorkfrontClassification"]:
        for match in response["data"]["Get"]["WorkfrontClassification"]:
            # print(match.get(solution_property))
            # if match.get(solution_property) == 'Not Applicable':
            #     continue  
            item = {
                "activity_type": match["activity_type"],
                "description": match["description"]
            }
            if solution_property in match and match[solution_property]:
                item[solution_property] = match[solution_property]
            retrieved_data.append(item)
    else:
        return {"activity_type": "No match found", "description": None}
    

 
    formatted_context = "\n\n".join(
        f"- Activity Type: {item['activity_type']}\n  Description: {item['description']}\n {item.get(solution_property)}"
        for item in retrieved_data
    )


    additional_prompt=f"""
    If the customer request is talking about reviewing their implementation, see if there are any issues and ask if the customer would benefit from a holistic review of their overall implementation or if they would like take a deeper dive into the specific issue/implementation?

    """
    
    follow_up_response=llm.complete(additional_prompt)
    follow_up_text = follow_up_response.text.strip()


    guardrail_solutions={
        "Adobe Analytics": 
        """
        1. Do not classify requests involving integrations as Solution Review or Environment Review.
        2. Focus on the specific intent of the customer's query, prioritizing what is explicitly asked rather than implied.
        3. Avoid assigning broad categories like Solution Review or Environment Review unless the customer explicitly requests a review or evaluation of their implementation.
        """,

        "Target":
        """
        1. Do not classify requests involving integrations other than Analytics with Target (A4T) as Solution Review or Environment Review.
        """,
        "Audience Manager":
        """
        """
    }

    guardrails=guardrail_solutions.get(solution)
    llm_prompt = f"""
    You are a classification assistant. When classifying customer requests, go through the following steps
    1. Ensure the following guardrails are adhered to:
    {guardrails}

    2. Review the customer request below and classify it based on the following options, while remembering the guardrails above:
    Customer Query: "{customer_ask}

    Options:
    {formatted_context}

    Respond only with the top three most relevant activity types and the reasoning in the following format without specifying any rules or restating the customer request:
    Activity Type: [activity type]

    [reasoning]
    """

    llm_response = llm.complete(llm_prompt)
    print(llm_response)
    response_text=llm_response.text.strip()
    for line in response_text.split('\n'):
        if line.startswith("Activity Type:"):
            activity_type = line.split(":")[1].strip()
            break
    

    unsupported={
        ("Audience Manager","Environment Review"): "That customer request aligns most with Environment Review. Unfortunately, Environment Review is not offered for Audience Manager.",
        ("Experience Platform Core","Adoption Review"):"That customer request aligns most with Adoption Review. Unfortunately, Adoption Review is not offered for Experience Platform Core.",
        ("Experience Platform Core","Solution Review"):"That customer request aligns most with Solution Review. Unfortunately, Solution Review is not offered for Experience Platform Core."
        }
    
    
    if (solution,activity_type) in unsupported:
        return unsupported[(solution, activity_type)]

    return llm_response.text.strip()





st.title("Classification Assistant")
st.logo('FE-logo.png',size='large')
st.caption("Please note that this is a beta release and only classifies activities for Adobe Analytics, Customer Journey Analytics, and Target. This early access release allows you to test out the features and functionality before the official launch, and your feedback is essential in shaping the final product.")

if 'step' not in st.session_state:
    st.session_state.step = 1

if 'result' not in st.session_state:
    st.session_state.result=""

if 'customer_ask' not in st.session_state:
    st.session_state.customer_ask=""

if 'solution' not in st.session_state:
    st.session_state.solution=""

# Display chat messages
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'precheck_result' not in st.session_state:
    st.session_state.precheck_result = None

if 'assistant_check' not in st.session_state:
    st.session_state.assistant_check = None

if 'user_input' not in st.session_state:
    st.session_state.user_input=""

if 'solution_submitted' not in st.session_state:
    st.session_state.solution_submitted = False

if 'launch_advisory_submitted' not in st.session_state:
    st.session_state.launch_advisory_submitted = False

if 'feedback' not in st.session_state:
    st.session_state.feedback = False

if 'last_input' not in st.session_state:
    st.session_state.last_input = None

if 'last_solution' not in st.session_state:
    st.session_state.last_solution = ""


# Display initial message if chat history is empty
if not st.session_state.chat_history:
    st.session_state.chat_history.append({"role": "assistant", "content": "Hi! I am Zeus, the Classification Assistant! Please submit a customer request and I will help you determine which Success Accelerator is the best fit!"})

# Display chat messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"],avatar='Zeus.png' if message["role"]=="assistant" else None):
        st.markdown(message["content"])

# User input
if user_input := st.chat_input("Enter your customer ask:"):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.user_input = user_input
    with st.chat_message("user"):
        st.markdown(user_input)
        st.session_state.feedback=False
        st.rerun()

# Solution selection

def handle_response(response):
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    def stream_data():
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.02)

    with st.chat_message("assistant", avatar='Zeus.png'):
        st.write_stream(stream_data)
    st.session_state.feedback=True
    # Reset input and solution selector
    st.session_state.result=response
    st.session_state.last_input = st.session_state.user_input
    st.session_state.last_solution = st.session_state.solution
    st.session_state.user_input = ""
    st.session_state.solution = ""
    st.session_state.step = 1
    st.session_state.precheck_result = None
    st.session_state.assistant_check=False
    st.session_state.launch_advisory_submitted=False
    st.session_state.solution_submitted=False
    st.rerun()

if 'step' not in st.session_state:
    st.session_state.step = 1
 
if'feedback_chosen' not in st.session_state:
    st.session_state.feedback_chosen=None


ssl._create_default_https_context = ssl._create_unverified_context
def append_row(df, row):
    return pd.concat([
        df,
        pd.DataFrame([row], columns=row.index)]
    ).reset_index(drop=True)

def create_GSheetsConnection():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn

def store_feedback(feedback):

    conn=create_GSheetsConnection()
    df = conn.read(ttl=1)
    record={'solution':st.session_state.last_solution,'user_input':st.session_state.last_input, 'response':st.session_state.result, 'feedback':feedback['score'],'comments':feedback['text'], 'timestamp':datetime.datetime.now()}
    new_row=pd.Series(record)
    df=append_row(df,new_row)
    conn.update(data=df)
    # conn = st.connection('feedback_db',type='sql')
    # with conn.session as s:
    #     s.execute(text('''
    #         INSERT INTO feedback (user_input, response, feedback)
    #         VALUES (:user_input, :response, :feedback)
    #     '''), {
    #         'user_input': st.session_state.last_input,
    #         'response': st.session_state.result,
    #         'feedback': st.session_state.feedback_chosen
    #     })
    #     s.commit()
    st.session_state.feedback=False


if st.session_state.feedback:
    feedback=streamlit_feedback(feedback_type="thumbs", optional_text_label="Please provide feedback!", review_on_positive=False, key=f"feedback_{st.session_state.feedback_key}", on_submit=store_feedback)
    st.session_state.feedback_chosen=feedback
    #st.feedback("thumbs", key="feedback_chosen", on_change=store_feedback)
    # st.session_state.feedback_chosen=st.feedback("thumbs")
    # store_feedback()

if 'feedback_key' not in st.session_state:
    st.session_state.feedback_key=0

#Checking to see if the user has inputted a customer request. If so, then we will check if the input is relevant
if st.session_state.user_input and st.session_state.step==1:
    st.session_state.feedback_key+=1
    if not st.session_state.precheck_result:
        precheck_result=precheck(st.session_state.user_input)
        st.session_state.precheck_result = precheck_result
        if precheck_result == "Irrelevant":
            response="The input provided is not a customer request. Please provide a relevant customer request for classification."
            handle_response(response)
        else:
            st.session_state.step = 2

#If the input is relevant, we will check to see which solution the request is related to
if st.session_state.step==2 and not st.session_state.solution_submitted:
        ph=st.empty()
        with ph.container():
            solution=st.selectbox("Select Solution", list(solution_mapping.keys()), key="solution_select",disabled=st.session_state.solution_submitted)
            if st.button("Submit", key="submit_solution"):
                st.session_state.solution_submitted = True
                st.session_state.chat_history.append({"role": "user", "content": f"Solution: {solution}"})
                st.session_state.solution = solution
                with st.chat_message("user"):
                    st.markdown(f"Solution: {solution}")
                st.session_state.step = 3
                ph.empty()
                st.rerun()

#Once the solution is selected, we will check if the request is related to the Enablement Bootcamp to determine if it is a Launch Advisory
if st.session_state.step==3:
    if not st.session_state.assistant_check:
        #Check if the request is related to the Enablement Bootcamp
        assistant_check = assistant(st.session_state.user_input)
        st.session_state.assistant_check = assistant_check
        if assistant_check == "Enablement Bootcamp":
            st.session_state.step="Launch"
        else:
            #If the request is not related to the Enablement Bootcamp, we will classify the request. Go to classify step.
            st.session_state.step="Classify"

#If the request is related to the Enablement Bootcamp, we will check if it is being submitted as part of a Launch Advisory
if st.session_state.step=="Launch" and not st.session_state.launch_advisory_submitted:
        ph=st.empty()
        with ph.container():
            launch_advisory = st.selectbox("Is this being submitted as part of a Launch Advisory activity?", ["Yes", "No"], key="launch_advisory")
            if st.button("Submit", key="submit_launch_advisory"):
                st.session_state.launch_advisory_submitted = True
                st.session_state.chat_history.append({"role": "user", "content": f"Launch Advisory: {launch_advisory}"})
                with st.chat_message("user"):
                    st.markdown(f"Launch Advisory: {launch_advisory}")
                if launch_advisory == "No":
                    response = "Unfortunately that customer request can only be submitted alongside Launch Advisory."
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    # with st.chat_message("user"):
                    #     st.markdown(f"Unfortunately that customer request can only be submitted alongside Launch Advisory.")
                    st.session_state.last_input = st.session_state.user_input
                    st.session_state.last_solution = st.session_state.solution
                    st.session_state.result=response
                    st.session_state.user_input = ""
                    st.session_state.solution = ""
                    st.session_state.step = 1
                    st.session_state.precheck_result = None
                    st.session_state.assistant_check=False
                    st.session_state.launch_advisory_submitted=False
                    st.session_state.solution_submitted=False
                    st.session_state.feedback=True
                    st.rerun()
                    
                else:
                    st.session_state.step="Classify"
                    ph.empty()
                    st.rerun()

#If the request is not related to the Enablement Bootcamp, we will classify the request
if st.session_state.step=="Classify":
    with st.spinner("Classifying..."):
        response = classify_customer_ask_with_rag(st.session_state.user_input, st.session_state.solution)
    handle_response(response)




#multi series enablement to help onboard new users