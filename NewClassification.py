import streamlit as st
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import StrOutputParser
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
from langchain_openai import AzureChatOpenAI
import re
import requests
import json

# Set environment variables or use default values
AZURE_OPENAI_KEY = ""
AZURE_OPENAI_ENDPOINT = "https://zeus-model-eastus2.openai.azure.com/"
AZURE_OPENAI_MODEL = "gpt-4o-mini"
AZURE_OPENAI_MODEL_NAME = "gpt-4o-mini"
AZURE_OPENAI_VERSION = "2024-08-01-preview"
AZURE_OPENAI_EMBEDDING_NAME = "textembedding"
AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"
WEAVIATE_CLIENT_URL = os.environ.get("WEAVIATE_CLIENT_URL") or "http://weaviate.compas-weaviate.svc.cluster.local:80"


def send_chat_compas(message,conversation_id, cookie_value):
    payload = {
        "message": [
            {
                "role": "user",
                "content": message
            }
        ],
        "conversationID": conversation_id,
        "stream": False# Set to False if you want a non-streaming response
    }
    
    # Set up headers with the cookie
    headers = {
        "Content-Type": "application/json",
        "Cookie": cookie_value
    }

    response = requests.post(
                'https://compas.adobe.com/api/chat',
                headers=headers,
                data=json.dumps(payload)
            )
    
    print("Complete response:", response.json())
    return response.json()

cookie_value="OptanonAlertBoxClosed=2024-12-17T03:38:57.307Z; kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_consent=general%3Din; previousUserConsent=in; isIMSSession=true; fltk=segID%3D13330890; userGUID=D6CC4E7062858D7B0A495C75@adobe.com; kndctr_8F99160E571FC0427F000101_AdobeOrg_consent=general%3Din; _gcl_au=1.1.941039015.1740108119; _mkto_trk=id:360-KCI-804&token:_mch-adobe.com-6a2b465bf56db0e1b16201de83a64ad; kndctr_0B6930256441790E0A495FFE_AdobeOrg_identity=CiY3NzI2NzE3NzQ1MDM3NjU5Nzg4MTk1NDA4ODEwNzQwNzEyMTIyNFISCJiDtonSMhABGAEqA1ZBNjAA8AG9mcqs0zI=; acaplup=learner; kndctr_B504732B5D3B2A790A495ECF_AdobeOrg_identity=CiYwNjc3ODMxNTE0NDg1MTI5NzM2MjQ1NTA3NTA2MTY3NDY2ODE4NlIQCLys5_zTMhgBKgNWQTYwAfABvKzn_NMy; AMCV_B504732B5D3B2A790A495ECF%40AdobeOrg=MCMID|06778315144851297362455075061674668186; _tt_enable_cookie=1; _ttp=01JN6SF1P0KXG14YBTQ8AYRSYA_.tt.1; dcy.at=type3; platformMetaData=%7B%22isAndroidAppInstalled%22%3Afalse%2C%22isAcrobatDesktopInstalled%22%3Atrue%2C%22isExtensionInstalled%22%3Atrue%2C%22isPWAInstalled%22%3Afalse%7D; mmac_machine=2025-03-06T20:27:05.988Z; mmac_760319056=2025-03-06T20:27:06.051Z; mmac_machine_dc_web_visitor=09788282032222563874327935044695880524; mmac_machine_dc_web=2025-03-06T20:27:06.089Z; mmac_760319056_dc_web=2025-03-06T20:27:06.108Z; mmac_machine_dc_web_recipient_view=2025-03-06T20:27:11.203Z; mmac_760319056_dc_web_recipient_view=2025-03-06T20:27:11.245Z; sc_locale=en_US; sc_locale_numbers=en_US; mmac_machine_chrome-extension=2025-03-12T14:04:54.941Z; s_fid=3716D7A2A3B37C74-1DE89F391D277D8B; RDC=AQ2Y0Fe6mGVkX3FFZxE0-KkJrQOKyhvtOJhKeYAPeZbJKv4E-z1Yf9aSvclMieZ8GPMttMs9GafPyvIF4mHmK6BB3ner-02OqymPUIDv10DatG2HS4AlY88u3OdDscwq8lP1QcbAyioFUU9PDWUe7g89F5QP; _fbp=fb.1.1741795178693.834646736; kndctr_B3FC0A6762EA412C0A495ED8_AdobeOrg_identity=CiYwOTc4ODI4MjAzMjIyMjU2Mzg3NDMyNzkzNTA0NDY5NTg4MDUyNFIQCLP89uS9MhgBKgNWQTYwA_ABv-u_29gy; AMCV_B3FC0A6762EA412C0A495ED8%40AdobeOrg=MCMID|09788282032222563874327935044695880524; s_cid=7015Y0000048qnyQAA; TID=-ZXL8DRN2-; _gcl_aw=GCL.1741803857.EAIaIQobChMI47bj_JSFjAMVwnhHAR1WXDlCEAAYASAAEgL2efD_BwE; _gcl_gs=2.1.k1$i1741803852$u49029685; userGuid=d972351264232aa60a495ea1@02491e85636c53f8495e07.e; AMCV_8F99160E571FC0427F000101%40AdobeOrg=MCMID|46146078712486483334426344718263253867; kndctr_DF021EE0647F46FB0A495F95_AdobeOrg_identity=CiYxMDM1MDI5OTUxNTYwNTMwODQ4MjY3NzE0NzcxMTMyNjUwNTI2NlIQCNKa6uLWMhgBKgNWQTYwAfABsd2cgNky; OptanonChoice=1; _scid=Ez2_BZ4zmdNQUcuPA6uaEBXCe4B3Pr-JzpOneQ; _ScCbts=%5B%22442%3Bchrome.2%3A2%3A5%22%5D; _cs_c=0; _sctr=1%7C1742184000000; AMCV_92D346EB57C994D87F000101%40AdobeOrg=MCMID%7C68361463375121612791917018995502874623; adcloud={%22_les_v%22:%22c%2Cy%2Cadobe.com%2C1742411306%22}; event-origin=https%3A%2F%2Fbusiness.adobe.com%2Fsummit%2F2025%2Fsessions%2Fhow-workfront-is-bringing-enterpriseready-ai-os808.html; _cs_id=7d0baf38-fc47-a8a5-dacf-27cc7d3b30a6.1734576296.26.1742409607.1742405042.1717775740.1768740296795.1; _scid_r=FT2_BZ4zmdNQUcuPA6uaEBXCe4B3Pr-JzpOnig; _uetsid=9a6c5e30036b11f09d4e195c042d33dc; _uetvid=3b950470bdb311efb223c50782cf097f; _rdt_uuid=1737486785226.2e00c973-6b27-4734-bdde-f69b0761701e; kndctr_6AD033CF62197E1C0A495FDD_AdobeOrg_identity=CiYwOTgyNTczODg1MTM5OTg1NTAzMjc5OTIwMzA0NjQ3MTY1MzA2OVIQCKXfy5W9MhgBKgNWQTYwAfABr4udidsy; kndctr_8F99160E571FC0427F000101_AdobeOrg_identity=CiY0NjE0NjA3ODcxMjQ4NjQ4MzMzNDQyNjM0NDcxODI2MzI1Mzg2N1ISCKDbrK3TMhABGAEqA1ZBNjAA8AGOlJ2J2zI=; kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_identity=CiYwOTc4ODI4MjAzMjIyMjU2Mzg3NDMyNzkzNTA0NDY5NTg4MDUyNFISCI%5Fe2Iy9MhABGAEqA1ZBNjAA8AH6kvye2zI%3D; shellImsEnv=prod; s_ims=https://ims-na1.adobelogin.com/ims/session/v1/ZWM1NzZmM2YtZGMzZC00MGNlLWE4NzAtNmMwZWQwMTgyY2I3LS1EQ0E2NEUwRTYyOThEQjQyMEE0OTVDQkFAMTQzNzI0NTk2MWU4ZjA2YzQ5NWU3OS5l; s_cc=true; sc_ident=Adobe%20AGS447%7C%7Ceahn%40adobe.com~~Premier%20Support%20Consulting%7C%7Ceahn%40adobe.com~~Delta%7C%7Ceahn%40adobe.com~~Cisco%7C%7Ceahn%40adobe.com~~Microsoft%20Store%7C%7Ceahn%40adobe.com; mc_company=Adobe%20AGS447; s_vnum=1744430202031%26vn%3D7; lang=en%3AUS; AMCVS_CB20F0CC53FCF3AC0A4C98A1%40AdobeOrg=1; AMCV_CB20F0CC53FCF3AC0A4C98A1%40AdobeOrg=179643557%7CMCIDTS%7C20168%7CMCMID%7C01175932912991398923088290189720732582%7CMCAAMLH-1743084328%7C7%7CMCAAMB-1743084328%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1742486728s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-2121179033%7CMCMID%7C09788282032222563874327935044695880524%7CMCAID%7CNONE%7CMCOPTOUT-1742487067s%7CNONE%7CMCAAMLH-1743084667%7C7%7CMCAAMB-1743084667%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C5.3.0%7CMCIDTS%7C20166%7CMCCIDH%7C-179492357; s_dslv=1742479871010; s_ppv=[%22documentcloud.adobe.com/spodintegration/index.html%22%2C100%2C0%2C1058%2C2010%2C1058%2C3200%2C1333%2C2%2C%22P%22]; AMCVS_E8F928AE56CDB5647F000101%40AdobeOrg=1; AMCV_E8F928AE56CDB5647F000101%40AdobeOrg=870038026%7CMCIDTS%7C20168%7CMCMID%7C00826784236049960083053355333325608250%7CMCAAMLH-1743090225%7C7%7CMCAAMB-1743090225%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1742492625s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.0; s_nr=1742486374972-Repeat; apt.uid=AP-PCBATQJJQHRG-2-1742486516046-31839925.0.2.430ec173-b93b-4929-92e4-0137bf9f2d8a; s_sq=gcoeaguprod%3D%2526pid%253Dindex%2526pidt%253D1%2526oid%253Dblob%25253Ahttp%25253A%25252F%25252Fgcoe.corp.adobe.com%25252F3310323a-d428-4b83-867d-c6ec460de7bc%2526ot%253DA%26adbadobenonacdcprod%252Cadbadobeprototype%3D%2526c.%2526a.%2526activitymap.%2526page%253Ddocumentcloud.adobe.com%25253Aspodintegration%25253Aindex%2526link%253Dd1d1d1d1d2d1d1d1d1d1d2d1d1d1d1d1d2d1d4d1d1d1d1d2-%2526region%253Dother%2526xy%253D1050%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c; fg=ZJRBNQ4WXPP74HUKPMQV27AACA======; aux_sid=AVQ9qQC6uRx8wrqYyT0spItTvNkb9_4H1wp5y_CWWfKEb5e7Sc70fNAcZkM6B-U-KE_ROiJjefWRHEANBTxpjK2c5viN4xGat3hE-G9Adg7k9gJm3nJ-VFgl1jgg2w0MQiqy5Dq3RYXEq7ZfP3ApwnmVikETTEqBIkVoYCtBInhBBqMCnlhVfgF2pKFMNtjUS-BOal0ydFDOD2i6wSUE2TDjZZy9ngb1Uybm2TT3jcenWevbyeR8XUlO_l179W-pJeRpkqlWWbGwfctvMp6p5Zyj_KiJed5Zj0oD2Zt7RY_wP00kmhUlILjINSXwRhfr9CnxRJ2l2z_Ws2n6ifdS9zAhKGv5An12sL6IYEMLpLS5vQGl2vVcg27dh7nSn20gyDgSNRlayN0Os4Q62YWnXFwS7oJgAbcFHJNnQaMZVmGdv3BhVJkhQW08wHjtpcL6eKh1nOvVQKL6mbfO7Nlv2d8sJfPG5liIwaud3NW_VtbohXDsI-oVZPkPs8vJ0meDftJVy2vUTPj15fatpEvj2PvqaBuWlvwSAV0cadBCo823g024FHbSxFFAxn23hkz1zk0YK8N-RUaGU8loRmeI2Itz1oJRLQrKbxQE6pWlFQutJ0SS3J9zOAQADRJfrD9Yne5Dn9Nbvb1pQcLS8wf_jVQd0LcOdBqqYDZ9kJNM-bbq17gkcaYbmXuEQqHyS8kIRi3VtzwVUVUQ-xQ5fqVnSbh970A_eOcxpZUP-qYuekeScRkoKC7RFGa4vV7sol2nlitAWhoGAWaEkSg862hbQzCL_QFK4DjVXSlWBqoq4ou59U0; OptanonConsent=groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&isGpcEnabled=0&datestamp=Thu+Mar+20+2025+12%3A22%3A30+GMT-0400+(Eastern+Daylight+Time)&version=202311.1.0&browserGpcFlag=0&geolocation=US%3BNJ&isIABGlobal=false&hosts=&consentId=ef1010f1-aa7e-4b61-9bfc-ffa9cec4baa7&interactionCount=0&landingPath=https%3A%2F%2Freg.adobe.com%2Fflow%2Fadobe%2Fas25%2Fsessions%2Fpage%2Fcatalog%3Fsearch&tab.allsessions=1643149273691001NFtR&search.product=option_1636755970075; mbox=session%2309788282032222563874327935044695880524%2DvohyxA%231742489611%7CPC%2309788282032222563874327935044695880524%2DfYQyWf%2E34%5F0%231805158304; session=.eJwljjEKAzEMBP_iOgeyZZ2k-0ywLIkEUt2RKuTvMWSqLQZ2PuWeZ1yPcuR4XXEr96eXowQZo6N6Nuw002r0ho2xaSVSrhU51wSJ1OaiMbOKtx2mJthkGzGhNdbaF3syMHgn04E5FbtZDndGFiHoGetkkOEwdMeeZYW8rzj_NUtmr4jbTlW2niKbkttmU4Y5wS4TyvcH00A43w.Z9xCLQ.9kXtuJpROPvw9FfZ4cSdMEZ1z7s"
conversation_id="3ebc11e0-077e-11f0-a754-72e782200e78"

# Initialize Weaviate client

# client = weaviate.Client("https://lorrdtftleztqq0pon3jw.c0.us-east1.gcp.weaviate.cloud",auth_client_secret= weaviate.AuthApiKey('n44LQVgeyigroQ57sijG0scN8y6MzdvZ1LaU'))       

# Initialize embedding model
llm = AzureOpenAI(
    model=AZURE_OPENAI_MODEL,
    deployment_name=AZURE_OPENAI_MODEL_NAME,
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_VERSION,
)

llm_chat = AzureChatOpenAI(
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

    extract_prompt = PromptTemplate(
    input_variables=["customer_request"],
    template=("""
    # Task
    Analyze the customer request to determine if it contains both WHAT they need help with and WHY they need that help.

    # Input
    Customer Request: {customer_request}

    # Evaluation Criteria
    - WHAT: Any clear indication of what the customer wants assistance with (a feature, concept, tool, process)
    - WHY: Any mention of purpose, goal, or outcome (even if brief or functional)
    - SOLUTION: Explicit mention of a specific Adobe Experience Cloud solution (e.g., Adobe Tags/Data Collection, Adobe Analytics/AA, Adobe Target/AT, Adobe Campaign, Adobe Experience Manager/AEM, Customer Journey Analytics/CJA, Adobe Commerce, etc.)
    
    # Examples
    Example 1: "Need help with segmentation in Adobe Analytics"
    Analysis: Missing WHY component <missing>No indication why they need segmentation help</missing>
    
    Example 2: "Customer would like to learn about the CJA Connector so they can use the connector to send data from AA to CJA"
    Analysis: Complete request - Contains WHAT (learn about CJA Connector), WHY (to send data from AA to CJA), and SOLUTION (CJA and AA/Adobe Analytics)
    
    Example 3: "We need assistance setting up data views in CJA to visualize our cross-channel performance"
    Analysis: Complete request - Contains WHAT (setting up data views), WHY (to visualize cross-channel performance), and SOLUTION (CJA)
    
    Example 4: "Can you help us understand how to create segments for our marketing campaigns?"
    Analysis: Missing SOLUTION component <missing>No specific Adobe Experience Cloud solution mentioned</missing>

    # Instructions
    1. First identify the explicit WHAT, WHY, and SOLUTION components
    3. Err on the side of identifying purpose when reasonably implied
    4. Look for both full names and common abbreviations of Adobe solutions (AA, CJA, AEM, etc.)
    
    # Output Format
    - If WHAT, WHY, and SOLUTION are all present: respond with only "True"
    - If any component is missing: explain which one and the reason why inside <missing></missing> tags
    """
    )
)

    extract_chain = extract_prompt | llm_chat | StrOutputParser()
    extract_result=extract_chain.invoke({"customer_request": customer_ask})
    print(extract_result)
    missing_match = re.search(r'<missing>(.*?)</missing>', extract_result, re.DOTALL)
   
    
    if missing_match:
        # If there are missing details, return the content inside <missing> tags
        missing_content = missing_match.group(1).strip()
        return f"Please provide the following details and resubmit your customer request: {missing_content}"
    else:
        input=f"""
            You are an Adobe Experience League Documentation Expert. Think step by step on how you can reword and summarize the customer request below using only official termminology from Adobe Experience League Documentation.  For each described functionality or feature, identify and replace it with the most specific corresponding official term from Adobe Experience League.  Make sure to preserve the essential meaning of what the customer needs help with and why.
            Here is the customer request: {customer_ask}
            Respond only with the reworded and summarized customer request in the <summary></summary> tag.
            """

        response=send_chat_compas(input,conversation_id, cookie_value)# If there's a summary, return the content inside <summary> tags
        match = re.search(r'<summary>(.*?)</summary>',response['message']['content'], re.DOTALL | re.IGNORECASE)
        summary=match.group(1).strip()
        return summary
    # relevant_prompt=f"""
    #     Think step by step on if the customer request is relevent based on the criteria below , but only keep a minimum draft for each thinking step, with 5 words at most. Place your thought process in <thinking></thinking> tags. One you have finished your thought process, respond with <answer></answer> tags.
    #     Here is the customer request: {customer_ask}
    #     Here are the criteria:
    #     - The customer request is a customer need or request for action.
    #     - The customer request involves a Adobe Experience Cloud or Adobe Experience Platform suite product.
    #     """

    # relevant_response = llm.complete(relevant_prompt)
    # relevant_text = relevant_response.text.strip()

    # print(relevant_text)

    # if relevant_text == "Irrelevant":
    #     return relevant_text
    # else:
    # extract_prompt= PromptTemplate(
    #     input_variables=["customer_request"],
    #     template=( """
    #         Think step by step on if the customer request contains all the details below , but only keep a minimum draft for each thinking step, with 5 words at most. One you have finished your thought process, place your thought process in <thinking></thinking> tags and your response inside <answer></answer> tags.
    #         Inside the <answer></answer> tags, respond with only "Yes" if it contains all the details, otherwise respond with what details are missing in a short explanation.
    #         Here is the customer request: {customer_request}
    #         Here are the details:
    #             - The customer request should clearly state what they need help with.
    #             - The customer request should clearly state why they need help with that. It should be a valid reason for help.
                
    #         """
    #     )
    # )
        
        # multi_ask_template = PromptTemplate(
        #     input_variables=["engagement_ask"],
        #     template="""
        #         You are an AI assistant analyzing the structure of a customer request. Your goal is to determine whether the given Engagement Ask consists of **multiple distinct requests** or just one cohesive request.  

        #         ### **Instructions:**
        #         1. **Identify Separate Requests:**  
        #         - If the ask contains multiple distinct requests that are not inherently related (e.g., different topics, different functionalities), classify it as a **multi-part request**.  
        #         - If the ask contains related components that belong to the same general request (e.g., different steps of the same process), classify it as a **single request**.  

        #         2. **Response Output:**  
        #         - If it's a **multi-part request**, return:  
        #             _"This request contains multiple distinct asks. Please resubmit one request at a time: [Provide a breakdown of the separate requests]."_  
        #         - If it's a **single request**, return:  
        #             _"This is a single, cohesive request because [Explain why the components are part of one overarching request]."_  

        #         ### **Engagement Ask to Analyze:**  
        #         "{engagement_ask}"
        #         """
        # )
        


        # scope_prompt = PromptTemplate(
        #     input_variables=["customer_request"],
        
        #     template=("""
        #         You are a classification assistant. Determine if the following customer query is within the scope of services provided. If it is out of scope, respond with "Out of Scope" and the reason. Otherwise, respond with "In Scope".

        #         Out-of-Scope Criteria:
        #         - Custom code solutions
        #         - Requests for unsupported features that are not part of the Adobe Experience Cloud or Adobe Experience Platform suite
        #         - Requests for services not provided by Adobe Experience Cloud or Adobe Experience Platform suite
        #         - Requests that involve the Adobe Experience Cloud or Adobe Experience Platform suite products implemented using third party tools or services 

        #         Customer Query: {customer_request}
        #         """
        #     )
        # )

        


        # if extract_result.startswith("Please add the following details"):
        #     return extract_result
        # st.session_state.user_input=extract_result
        # print(st.session_state.user_input)

        # multi_ask_chain=multi_ask_template | llm_chat | StrOutputParser()
        # multi_ask_response=multi_ask_chain.invoke({"engagement_ask": extract_result})
        # print(multi_ask_response.startswith("This request contains multiple distinct asks"))
        # if multi_ask_response.startswith("This request contains multiple distinct asks"):
        #     return multi_ask_response

        # scope_chain= scope_prompt | llm_chat | StrOutputParser()
        
        # scope_response=scope_chain.invoke({"customer_request": extract_result})
        # scope_text = scope_response.strip()
        # print(scope_text)
        # if scope_text.startswith("Out of Scope"):
        #     return "The customer ask is out of scope for a Success Accelerator."
        # else:
        #     return "In Scope"




def assistant(customer_ask):
    enablement_prompt = f"""
    You are a classification assistant. Determine if the following customer request involves a 101 Enablement Bootcamp or a multi-session training program for new users, focusing on learning the basics of the Adobe Solution. If it does, respond with "True". Otherwise, respond with "False".

    Customer Query: "{customer_ask}"
    """
    enablement_response = llm.complete(enablement_prompt)
    enablement_text = enablement_response.text.strip()

    if enablement_text=="True":
        return "Enablement Bootcamp"

def check_guardrails(activity_type,customer_ask,solutions_involved):
    # if solutions_involved and isinstance(solutions_involved, str):
    #     solutions_list = [s.strip() for s in solutions_involved.split(',')]
    # elif solutions_involved:
    #     solutions_list = solutions_involved
    # else:
    #     solutions_list = []

    # if len(solutions_list)==1:
    #     unsupported={
    #         ("Audience Manager","Environment Review"): "That customer request aligns most with Environment Review. Unfortunately, Environment Review is not offered for Audience Manager.",
    #         ("Experience Platform Core","Adoption Review"):"That customer request aligns most with Adoption Review. Unfortunately, Adoption Review is not offered for Experience Platform Core.",
    #         ("Experience Platform Core","Solution Review"):"That customer request aligns most with Solution Review. Unfortunately, Solution Review is not offered for Experience Platform Core."
    #         }
        
        
    #     if (solution[0],activity_type) in unsupported:
    #         return unsupported[(solution[0], activity_type)]
    
    activity_guardrails = {
        "Deskside Coaching": [
            "Enablement on a third party non-Adobe library, third party non-Adobe extension, or third party integrations with the Adobe Experience Cloud Product",
            "Enablement on a non-Adobe product",
            "Enablement on custom code"
        ],
        "Upgrade or Migration Readiness": [
            "Acting as a Project Manager (owning meetings, driving upgrade/migration processes)",
            "Executing upgrades or migrations directly (instead of providing guidance)"
        ],
        "Solution Troubleshooting": [
            "Troubleshooting an issue related to a third party non-Adobe library, third party non-Adobe extension, or third party integrations with the Adobe Experience Cloud Product",
            "Troubleshooting an issue related to a non-Adobe product",
            "Troubleshooting an issue related to custom code"
        ],
        "Solution Review": [
            "Reviewing any third party non-Adobe product, third party non-Adobe extension, or third party integrations with the Adobe Experience Cloud Product",
            "Performance or Latency Testing"
        ],
        "Environment Review": [
            "Reviewing any third party non-Adobe product, third party non-Adobe extension, or third party integrations with the Adobe Experience Cloud Product",
            "Performance or Latency Testing"
        ]
    }

    # solution_guardrails = {
    #     "Adobe Analytics": {
    #         "Deskside Coaching": [
    #             "Creating or implementing data layer specifications",
    #             "Writing custom JavaScript for tracking"
    #         ],
    #         "Performance Optimization": [
    #             "Optimizing server infrastructure",
    #             "Debugging custom implementation code"
    #         ]
    #     },
     
    #     "Adobe Target": {
    #         "Deskside Coaching": [
    #             "Designing creative assets for tests",
    #             "Building custom implementation code"
    #         ]
    #     }
    #    
    # }
    all_guardrails = []
    if activity_type in activity_guardrails:
        all_guardrails.extend(activity_guardrails[activity_type])
    
    # # Add solution-specific guardrails if available
    # for solution in solutions_list:
    #     if solution in solution_guardrails and activity_type in solution_guardrails[solution]:
    #         all_guardrails.extend(solution_guardrails[solution][activity_type])

    
    guardrail_list = "\n".join([f"{i+1}. {guardrail}" for i, guardrail in enumerate(all_guardrails)])
    
    guardrail_prompt = f"""
        Evaluate whether the customer request falls within Adobe's support scope by checking against the provided guardrails.

        # Input
        Customer Request: {customer_ask}

        # Guardrails (Out of Scope Activities)
        {guardrail_list}

        # Instructions
        1. Think step by step, analyzing if the customer request violates any guardrails.
        2. For each thinking step, keep your analysis brief (5 words maximum per step).
        3. If the request crosses multiple guardrails, identify all that apply.

        # Output Format
        <thinking>
        Brief step 1 (≤5 words)
        Brief step 2 (≤5 words)
        ...
        </thinking>

        <scope_decision>IN_SCOPE</scope_decision> or <scope_decision>OUT_OF_SCOPE</scope_decision>

        <reason>Brief explanation of your decision</reason>
    """
    
    # Get response from LLM
    guardrail_response = llm.complete(guardrail_prompt)
    guardrail_response_text = guardrail_response.text.strip()
    
    # Extract scope decision
    match = re.search(r'<scope_decision>(.*?)</scope_decision>', guardrail_response_text, re.DOTALL | re.IGNORECASE)
    scope_decision = match.group(1).strip() if match else "IN_SCOPE"  # Default to in-scope if pattern not found
    
    # Extract reason
    match = re.search(r'<reason>(.*?)</reason>', guardrail_response_text, re.DOTALL | re.IGNORECASE)
    scope_reason = match.group(1).strip() if match else "No specific reason provided"
    
    # Create scope response for out-of-scope requests
    scope_response = ""
    if scope_decision == "OUT_OF_SCOPE":
        scope_response = f"""
            Unfortunately, the customer request is **out of scope** for a Success Accelerator and is better suited for a Adobe Professional Services engagement.  
            
            **Reason:** {scope_reason}
        """
    
    return (scope_decision == "IN_SCOPE"), scope_reason, scope_response


def classify_customer_ask_with_rag(customer_ask, solution):
    # solution_property = solution_mapping.get(solution)

    # query_embedding = embedding_model.get_text_embedding(customer_ask)

    # # Query Weaviate for relevant matches using near-vector search
    # response = client.query.get(
    #     class_name="WorkfrontClassification",
    #     properties=["description", "activity_type", solution_property]
    # ).with_near_vector({
    #     "vector": query_embedding,
    #     "certainty": 0.5
    # }).with_additional(["certainty"]).with_limit(5).do()

    # top_matches = response.get("data", {}).get("Get", {}).get("WorkfrontClassification", [])
    # print(top_matches)

    # # Extract relevant matches
    # retrieved_data = []
    # if response["data"]["Get"]["WorkfrontClassification"]:
    #     for match in response["data"]["Get"]["WorkfrontClassification"]:
    #         # print(match.get(solution_property))
    #         # if match.get(solution_property) == 'Not Applicable':
    #         #     continue  
    #         item = {
    #             "activity_type": match["activity_type"],
    #             "description": match["description"]
    #         }
    #         if solution_property in match and match[solution_property]:
    #             item[solution_property] = match[solution_property]
    #         retrieved_data.append(item)
    # else:
    #     return {"activity_type": "No match found", "description": None}
    

 
    # formatted_context = "\n\n".join(
    #     f"- Activity Type: {item['activity_type']}\n  Description: {item['description']}\n {item.get(solution_property)}"
    #     for item in retrieved_data
    # )


    

    # guardrail_solutions={
    #     "Adobe Analytics": 
    #     """
    #     1. Do not classify requests involving integrations as Solution Review or Environment Review.
    #     2. Focus on the specific intent of the customer's query, prioritizing what is explicitly asked rather than implied.
    #     3. Avoid assigning broad categories like Solution Review or Environment Review unless the customer explicitly requests a review or evaluation of their implementation.
    #     """,

    #     "Target":
    #     """
    #     1. Do not classify requests involving integrations other than Analytics with Target (A4T) as Solution Review or Environment Review.
    #     """,
    #     "Audience Manager":
    #     """
    #     """
    # }

    # guardrails=guardrail_solutions.get(solution)

    
   




    final_prompt = f"""
        Think step by step on which activity is most relevant to the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. 
        Here is the customer request: {customer_ask}
        Here are the activities to choose from:
            1. Deskside Coaching:Enablement of a specific feature, concept or best practices, and product integrations for a specific Adobe solution. 
            2. Environment Review:Conduct a detailed assessment of the customer's product environment to ensure compliance with contract terms and system limits. Focus on analyzing usage patterns, identifying overages, and providing guidance to remain within contractual boundaries.
            3. Solution Review: Audit or review of a specific implementation component of the customer's Adobe Solution to ensure it is implemented according to best practices. Not to be used to resolve an issue.
            4. Event Planning and Monitoring:Planning critical go-lives, campaigns, product launches, and rollouts. Assist customers in preparing for major events, ensure systems can handle increased traffic and server demand. 24/7 monitoring during live events to ensure that nothing goes down.
            5. Solution Troubleshooting:Troubleshoot Adobe Experience Cloud Solution issues for certain features, configurations, or performance-related problems. Provide findings and guidance to resolve these issues.
            6. Upgrade or Migration Readiness:Customer needs to understand how to upgrade their Adobe Solution or migrate from one Adobe Solution to another.
            7. Use Case Mapping to Solution Capability:Customer needs help coming with use cases and Key Performance Indicators (KPI's)
            9. Tool Workflow and Governance Optimization:Customer needs to ensure proper permissions, access, and controls are setup within the Adobe solution.
            10. Adoption Review:Focus on identifying underutilized features, integration opportunities, and areas for expanded solution use that the customer is not aware of.
            11. Change Management and Communication Strategies:Discuss communication strategies to ensure change is adopted within the organization, for example if they are trying to get users to start using a new Adobe Solution.
            12. Digital Review and Benchmarking:Adobe Digital Experience Maturity Assessment to help you assess your current Digital Experience complexity level against industry standards.
            13. Operating Model and Organization Governance:Establishing Centers of Excellence (CoE) and operating models within the customer's organization to promote collaboration and strong leadership support.
            14. Strategic Roadmap and Cycle Planning:Identify areas for improvement in strategic roadmap and developing an effective marketing strategy using the Adobe Experience Cloud Solutions. Focued on the strategy and not the technical setup.
        
        Place your thought process in <thinking></thinking> tags. One you have finished your thought process, respond with only the activity name and a explanation why it is the most relevant in <answer></answer> tags.
        """

    llm_response = llm.complete(final_prompt)
    print(llm_response)
    response_text=llm_response.text.strip()
    import re
    answer_match = re.search(r'<answer>(.*?)</answer>', response_text, re.DOTALL)
    if answer_match:
        extracted_answer = answer_match.group(1).strip()
        st.session_state.recommended_accelerator=extracted_answer
        check_prompt=f"""
        Identify which activity is in the answer below. Respond with only the name of the activity.
        List of activities:
        - Deskside Coaching
        - Environment Review
        - Solution Review
        - Event Planning and Monitoring
        - Solution Troubleshooting
        - Upgrade or Migration Readiness
        - Use Case Mapping to Solution Capability
        - Tool Workflow and Governance Optimization
        - Adoption Review
        - Change Management and Communication Strategies
        - Digital Review and Benchmarking
        - Operating Model and Organization Governance
        - Strategic Roadmap and Cycle Planning

        Answer: {extracted_answer}
        """
        check_response=llm.complete(check_prompt)
        check_response_text=check_response.text.strip()

        
        if "Solution Troubleshooting" in check_response_text:

            input=f"""
                Based on the latest Experience League documentation, think step by step on which Adobe Experience Cloud Product expertise is required to resolve the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. 
                
                Customer request: {customer_ask}

                Place your thought process in <thinking></thinking> tags. Respond only with the names of the Adobe Experience Cloud products in order of importance, separated by commas, within <product></product> tags.
            """
            solution_response=send_chat_compas(input,conversation_id, cookie_value)
            match = re.search(r'<product>(.*?)</product>',solution_response['message']['content'], re.DOTALL | re.IGNORECASE)
            solutions_involved=match.group(1).strip()
            st.session_state.solution=solutions_involved
            is_in_scope, scope_reason, scope_response = check_guardrails("Solution Troubleshooting", customer_ask, solutions_involved)
            if not is_in_scope:
                scope_response=f"""
                        Unfortunately, the customer request is **out of scope** for a Success Accelerator and is better suited for a Adobe Professional Services engagement.  
                        
                        **Reason:** {scope_reason}
                        """
                return scope_response
            else:
                input=f"""
                    You are an Adobe AI Customer Support Assistant for Adobe Field Engineering, tasked with suggesting a solution to the customer issue before they are routed to the Adobe Field Engineering team. Think step by step to determine if you can address and resolve the customer request without submitting a Solution Troubleshooting success accelerator activity. Analyze the request thoroughly, leveraging Adobe Experience League documentation and your knowledge of Adobe solutions. Keep a minimum draft for each thinking step, with 5 words at most.
                    
                    Customer issue: {customer_ask}

                    Place your thought process in <thinking></thinking> tags and your response in the <answer></answer> tags.
                    """

                troubleshooting_response=send_chat_compas(input,conversation_id, cookie_value)
                match = re.search(r'<answer>(.*?)</answer>',troubleshooting_response['message']['content'], re.DOTALL | re.IGNORECASE)
                troubleshooting_response=match.group(1).strip()
                handle_response(troubleshooting_response)
        elif "Deskside Coaching" in check_response_text:
            input=f"""
                Based on the latest Experience League documentation, think step by step on which Adobe Experience Cloud Product expertise is required to give an enablement to the customer based on the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. 
                
                Customer request: {customer_ask}

                Place your thought process in <thinking></thinking> tags. Respond only with the names of the Adobe Experience Cloud products in order of importance, separated by commas, within <product></product> tags.
                """
            solution_response=send_chat_compas(input,conversation_id, cookie_value)
            match = re.search(r'<product>(.*?)</product>',solution_response['message']['content'], re.DOTALL | re.IGNORECASE)
            solutions_involved=match.group(1).strip()
            st.session_state.solution=solutions_involved
            is_in_scope, scope_reason, scope_response = check_guardrails("Deskside Coaching", customer_ask, solutions_involved)
            if not is_in_scope:
                scope_response=f"""
                        Unfortunately, the customer request is **out of scope** for a Success Accelerator and is better suited for a Adobe Professional Services engagement.  
                        
                        **Reason:** {scope_reason}
                        """
                return scope_response
            else:
                st.session_state.step="Deskside"
                st.rerun()
        
        elif "Upgrade or Migration Readiness" in check_response_text:

            input=f"""
                    Based on the latest Experience League documentation, think step by step on which Adobe Experience Cloud Products are directly involved in the upgrade or migration process based on the customer request, but only keep a minimum draft for each thinking step, with 5 words at most.

                    Customer request: {st.session_state.user_input}

                    Place your thought process in <thinking></thinking> tags. Respond only with the names of the Adobe Experience Cloud products in order of importance, separated by commas, within <product></product> tags.
            """
            solution_response=send_chat_compas(input,conversation_id, cookie_value)
            match = re.search(r'<product>(.*?)</product>',solution_response['message']['content'], re.DOTALL | re.IGNORECASE)
            solutions_involved=match.group(1).strip()
            st.session_state.solution=solutions_involved

            is_in_scope, scope_reason, scope_response = check_guardrails("Upgrade or Migration Readiness", customer_ask, solutions_involved)

           
            if not is_in_scope:
                scope_response=f"""
                        Unfortunately, the customer request is **out of scope** for a Success Accelerator and is better suited for a Adobe Professional Services engagement.  
                        
                        **Reason:** {scope_reason}
                        """
                return scope_response
            else:
                st.session_state.step="Migration"
                st.rerun()
        
        elif "Event Planning" in check_response_text:
            input=f"""
                Based on the latest Experience League documentation, think step by step on which Adobe Experience Cloud Products are ACTIVELY NEEDED to address the customer's primary goal, but only keep a minimum draft for each thinking step, with 5 words at most. 

                Customer request: {customer_ask}

                Important instructions:
                - Focus on products needed to solve the specific problem goal, not just products mentioned
                - Distinguish between products that are part of the context versus products needed for the solution
                - Consider which product expertise would be directly required to fulfill the request


                Place your thought process in <thinking></thinking> tags. Respond only with the names of the Adobe Experience Cloud products in order of importance, separated by commas, within <product></product> tags.
            """
            solution_response=send_chat_compas(input,conversation_id, cookie_value)
            match = re.search(r'<product>(.*?)</product>',solution_response['message']['content'], re.DOTALL | re.IGNORECASE)
            solutions_involved=match.group(1).strip()
            st.session_state.solution=solutions_involved
            st.session_state.step="Event Planning"
            st.rerun()
        
        elif "Solution Review" in check_response_text:
            input=f"""
                Based on the latest Experience League documentation, think step by step on which Adobe Experience Cloud Products are ACTIVELY NEEDED to address the customer's primary goal, but only keep a minimum draft for each thinking step, with 5 words at most. 

                Customer request: {customer_ask}

                Important instructions:
                - Focus on products needed to solve the specific problem goal, not just products mentioned
                - Distinguish between products that are part of the context versus products needed for the solution
                - Consider which product expertise would be directly required to fulfill the request


                Place your thought process in <thinking></thinking> tags. Respond only with the names of the Adobe Experience Cloud products in order of importance, separated by commas, within <product></product> tags.
            """
            solution_response=send_chat_compas(input,conversation_id, cookie_value)
            match = re.search(r'<product>(.*?)</product>',solution_response['message']['content'], re.DOTALL | re.IGNORECASE)
            solutions_involved=match.group(1).strip()
            st.session_state.solution=solutions_involved
            is_in_scope, scope_reason, scope_response = check_guardrails("Solution Troubleshooting", customer_ask, solutions_involved)
            if not is_in_scope:
                scope_response=f"""
                        Unfortunately, the customer request is **out of scope** for a Success Accelerator and is better suited for a Adobe Professional Services engagement.  
                        
                        **Reason:** {scope_reason}
                        """
                return scope_response
            else:
                response=f"""
                    **Summarized Customer Request:** {st.session_state.user_input}

                    **Recommended Success Accelerator:** {st.session_state.recommended_accelerator}

                    **Solutions Involved:** {st.session_state.solution}


            
        #     input=f"""
        #     Think step by step on which Adobe Experience Cloud Product expertise is needed to resolve the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. 
        #     Here is the customer request: {customer_ask}
        #     Place your thought process in <thinking></thinking> tags. Respond only with the names of the Adobe Experience Cloud products separated by commas, and in order of priority inside the same <product></product> tag.
        #     """
        #     solution_response=send_chat_compas(input,conversation_id, cookie_value)
        #     match = re.search(r'<product>(.*?)</product>',solution_response['message']['content'], re.DOTALL | re.IGNORECASE)
        #     solution_involved=match.group(1).strip()
        #     combined_message = f"""
        #         **Solutions Involved:** {solution_involved}

        #         **Recommended Success Accelerator:** {extracted_answer}
        #     """
        #     return combined_message
    # for line in response_text.split('\n'):
    #     if line.startswith("Activity Type:"):
    #         activity_type = line.split(":")[1].strip()
    #         break
    
    # if len(st.session_state.solution)==1:
    #     unsupported={
    #         ("Audience Manager","Environment Review"): "That customer request aligns most with Environment Review. Unfortunately, Environment Review is not offered for Audience Manager.",
    #         ("Experience Platform Core","Adoption Review"):"That customer request aligns most with Adoption Review. Unfortunately, Adoption Review is not offered for Experience Platform Core.",
    #         ("Experience Platform Core","Solution Review"):"That customer request aligns most with Solution Review. Unfortunately, Solution Review is not offered for Experience Platform Core."
    #         }
        
        
    #     if (solution[0],activity_type) in unsupported:
    #         return unsupported[(solution[0], activity_type)]

    # return llm_response.text.strip()





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

if 'request_result' not in st.session_state:
    st.session_state.request_result = ""

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

if "migration_submitted" not in st.session_state:
    st.session_state.migration_submitted = False

if "deskside_submitted" not in st.session_state:
    st.session_state.deskside_submitted = False

if "deskside_topic" not in st.session_state:
    st.session_state.deskside_topic = ""

if "event_planning_submitted" not in st.session_state:
    st.session_state.event_planning_submitted = False

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
        st.session_state.solution = ""
        st.session_state.migration_submitted = False
        st.session_state.step = 1
        st.session_state.precheck_result = None
        st.session_state.assistant_check=False
        st.session_state.launch_advisory_submitted=False
        st.session_state.solution_submitted=False
        st.session_state.deskside_submitted=False
        st.session_state.deskside_topic=""
        st.session_state.event_planning_submitted=False
        st.rerun()

# Solution selection

def handle_response(response):
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    with st.chat_message("assistant", avatar='Zeus.png'):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response word by word
        for word in response.split(" "):
            full_response += word + " "
            message_placeholder.markdown(full_response)
            time.sleep(0.02)

    # def stream_data():
    #     for word in response.split(" "):
    #         yield word + " "
    #         time.sleep(0.02)

    # with st.chat_message("assistant", avatar='Zeus.png'):
    #     st.write_stream(stream_data)
    st.session_state.feedback=True
    # Reset input and solution selector
    st.session_state.result=response
    st.session_state.last_input = st.session_state.user_input
    st.session_state.last_solution = st.session_state.solution
    st.session_state.user_input = ""
    st.session_state.solution = ""
    st.session_state.step = 1
    st.session_state.migration_submitted = False
    st.session_state.precheck_result = None
    st.session_state.assistant_check=False
    st.session_state.launch_advisory_submitted=False
    st.session_state.solution_submitted=False
    st.session_state.deskside_submitted=False
    st.session_state.deskside_topic=""
    st.session_state.event_planning_submitted=False
    st.rerun()

if 'recommended_accelerator' not in st.session_state:
    st.session_state.recommended_accelerator=""

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

def out_of_scope(response):
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
    st.session_state.migration_submitted = False
    st.session_state.deskside_submitted=False
    st.session_state.deskside_topic=""
    st.session_state.event_planning_submitted=False
    st.rerun()


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
        if precheck_result.startswith("Please provide the following details"):
            response=precheck_result
            handle_response(response)
        # # elif precheck_result.startswith("This request contains multiple distinct asks"):
        # #     response=precheck_result
        # #     handle_response(response)
        # elif precheck_result.startswith("Out of Scope"):
        #     response=precheck_result
        #     handle_response(response)
        # elif precheck_result == "Irrelevant":
        #     response="The input provided is not a customer request. Please provide a relevant customer request for classification."
        #     handle_response(response)
        
        else:
            st.session_state.precheck_result = precheck_result
            st.session_state.user_input=precheck_result
            print(st.session_state.user_input)
            st.session_state.step = 2

# #If the input is relevant, we will check to see which solution the request is related to
# if st.session_state.step==2 and not st.session_state.solution_submitted:
#         # ph=st.empty()
#         # with ph.container():
#         #     solution=st.multiselect("Select Solution(s)", list(solution_mapping.keys()), key="solution_select",disabled=st.session_state.solution_submitted)
#         #     if st.button("Submit", key="submit_solution"):
#                 st.session_state.solution_submitted = True
#         #         st.session_state.chat_history.append({"role": "user", "content": f"Solution(s): {', '.join(solution)}"})
#         #         st.session_state.solution = solution
#         #         print(st.session_state.solution)
#         #         with st.chat_message("user"):
#         #             st.markdown(f"Solution(s): {', '.join(solution)}")
#                 st.session_state.step = 3
#                 # ph.empty()
#                 # st.rerun()

#Once the solution is selected, we will check if the request is related to the Enablement Bootcamp to determine if it is a Launch Advisory
if st.session_state.step==2:
    if not st.session_state.assistant_check:
        #Check if the request is related to the Enablement Bootcamp
        assistant_check = assistant(st.session_state.user_input)
        st.session_state.assistant_check = assistant_check
        print(st.session_state.assistant_check)
        if assistant_check == "Enablement Bootcamp":
            response = """
            Unfortunately Solution Introductions / Enablement Bootcamps are not supported as part of a Success Accelerator.
            Here are some paid offerings that the customer could consider:
            - ADLS
            """
            out_of_scope(response)
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
                    out_of_scope(response)
                    # st.session_state.chat_history.append({"role": "assistant", "content": response})
                    # # with st.chat_message("user"):
                    # #     st.markdown(f"Unfortunately that customer request can only be submitted alongside Launch Advisory.")
                    # st.session_state.last_input = st.session_state.user_input
                    # st.session_state.last_solution = st.session_state.solution
                    # st.session_state.result=response
                    # st.session_state.user_input = ""
                    # st.session_state.solution = ""
                    # st.session_state.step = 1
                    # st.session_state.precheck_result = None
                    # st.session_state.assistant_check=False
                    # st.session_state.launch_advisory_submitted=False
                    # st.session_state.solution_submitted=False
                    # st.session_state.feedback=True
                    # st.rerun()
                    
                else:
                    st.session_state.step="Classify"
                    ph.empty()
                    st.rerun()

#If the request is not related to the Enablement Bootcamp, we will classify the request
if st.session_state.step=="Classify":
    with st.spinner("Classifying..."):
        response = classify_customer_ask_with_rag(st.session_state.user_input, st.session_state.solution)
    handle_response(response)

if st.session_state.step=="Migration" and not st.session_state.migration_submitted:
        ph=st.empty()
        with ph.container():
            migration_phase = st.selectbox("If the client is looking for Migration Readiness, what phase of the migration are they in?", ["Not Migrating. Upgrade Readiness", "Early Phase","Kicking off Soon","In Progress/Post-Migration"], key="migration_phase")
            if st.button("Submit", key="submit_migration"):
                st.session_state.migration_submitted = True
                st.session_state.chat_history.append({"role": "user", "content": f"Migration Phase: {migration_phase}"})
                with st.chat_message("user"):
                    st.markdown(f"Migration Phase: {migration_phase}")
    
                if migration_phase == "Kicking off Soon":
                    response = f"""
                    **Summarized Customer Request:** {st.session_state.user_input}

                    **Recommended Success Accelerator:** Launch Advisory

                    This may mean they are past the initial planning phase and this Success Accelerator would provide less value.  Instead, **please consider opening a Launch Advisory Success Accelerator** to have a team support them throughout their migration project.  They can even review the migration plan already created by the client to find potential efficiencies and best practices. It might be the case the client has already started the migration project but is struggling in general.  In those cases, a LA might still be valuable, we would just focus on activities that align to the current state of the project and do a retrospective review where applicable.
                    
                    """
                    handle_response(response)
                elif migration_phase == "In Progress/Post-Migration":
                    response = f"""If they are far along their migration project and just need some specific support or guidance, then please consider **submitting a different Success Accelerator**, based on what they need help with. """
                    handle_response(response)
                else:
                    if migration_phase == "Early Phase":
                        early_phase_response=f"""
                        **Summarized Customer Request:** {st.session_state.user_input}

                        **Recommended Success Accelerator:** {st.session_state.recommended_accelerator}

                        **Solution(s) Involved:** {st.session_state.solution}

                        **Note:** This is a great Success Accelerator to help them with that initial planning phase; however, do consider the [Solution Specific Use Cases and Guardrails](https://adobe.sharepoint.com/sites/FieldEngineeringTeam/SitePages/Upgrade-or-Migration-Readiness.aspx) section in the Field Engineering Sharepoint before moving forward.  Additionally, after a Migration Readiness Success Accelerator, please consider making a request for the Launch Advisory (LA) Success Accelerator to align with the start of the client's migration project.  The LA engagement can provide them ongoing support through the migration project and make sure the client is following best practices during their migration.
                        """
                        handle_response(early_phase_response)
                    else:
                        combined_message = f"""
                        **Summarized Customer Request:** {st.session_state.user_input}

                        **Recommended Success Accelerator:** {st.session_state.recommended_accelerator}

                        **Solution(s) Involved:** {st.session_state.solution}
                        """
                        handle_response(combined_message)
if st.session_state.step=="Deskside" and not st.session_state.deskside_submitted:
    ph=st.empty()
    with ph.container():
        deskside_type = st.selectbox("What type of enablement support is needed?", ["One Hour High-Level Enablement Session","Robust or Tailored Enablement Sessions"], key="deskside_type")
        if st.button("Submit", key="submit_deskside"):
            st.session_state.deskside_submitted = True

            input=f"""
                    Think step by step to identify the specific feature or capability within {st.session_state.solution} that the customer would like enablement on, based on the customer request. Analyze the request thoroughly, considering the context, functionality, and terminology from the latest Adobe Experience League documentation. Keep a minimum draft for each thinking step, with 5 words at most.

                    Customer request: {st.session_state.user_input}

                    Place your thought process in <thinking></thinking> tags. In the <topic></topic> tags, respond ONLY with the exact feature or capability name (e.g., "Adobe Analytics Source Connector") WITHOUT including words like "Enablement," "Training," or similar terms. Ensure the response is precise, relevant, and consistent with Adobe Experience League documentation.
                    """
            deskside_response=send_chat_compas(input,conversation_id, cookie_value)
            match = re.search(r'<topic>(.*?)</topic>',deskside_response['message']['content'], re.DOTALL | re.IGNORECASE)
            topic_involved=match.group(1).strip()
            st.session_state.deskside_topic=topic_involved
            
            st.session_state.chat_history.append({"role": "user", "content": f"{deskside_type}"})
            with st.chat_message("user"):
                st.markdown(f"{deskside_type}")
            if deskside_type == "One Hour High-Level Enablement Session":
                response = f"""
                **Summarized Customer Request:** {st.session_state.user_input}

                **Recommended Success Accelerator:** Mentor Session

                **Enablement Topic:** {st.session_state.deskside_topic}

                **Solution(s) Involved:** {st.session_state.solution}

                **Note:** Mentor sessions are limited to the topics available in the [Mentor Session Asset Library](https://adobe.sharepoint.com/sites/DXCEKnowledgeTransferAssetLibrary/Lists/Knowledge%20Transfer%20topics/Published%20Content.aspx?useFiltersInViewXml=1&FilterField1=Publish%5Fx0020%5FStatus&FilterValue1=Final%20Doc%20Published&FilterType1=Choice&FilterOp1=In).  Please check the asset library to see if the topic is available.


                """
                handle_response(response)
            else:
                #Checking with Neo4j to see who has expertise on that topic
                from langchain_neo4j import Neo4jGraph
                AURA_CONNECTION_URI="neo4j+ssc://79831a17.databases.neo4j.io"
                AURA_USERNAME="neo4j"
                AURA_PASSWORD="vo_GyAdkN5fs82KBYfvnuNiWROSG9DYX9cMHXOqaa2o"
                graph = Neo4jGraph(
                    url=AURA_CONNECTION_URI,
                    username=AURA_USERNAME,
                    password=AURA_PASSWORD
                )

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
                

                

                def fetch_topics(graph):
                    query = """
                    MATCH (a:Accelerator {name: 'Deskside Coaching'})-[:HAS_TOPIC]->(c:Topic)
                    RETURN c.name AS name
                    """
                    result = graph.query(query)
                    formatted_topics = ""
                    for i, topic in enumerate(result, start=1):
                        formatted_topics += f"{i}. {topic['name']}\n"
                    print(formatted_topics)
                    return formatted_topics
                    topics = [record["name"] for record in result]
                    return topics
                
                existing_topics=fetch_topics(graph)
                input=f"""
                    Think step by step to determine whether the new topic matches one of the existing topics. Compare the new topic with each existing topic individually, considering key attributes, context, and scope. Keep a minimum draft for each thinking step, with 5 words at most.
                    Here are the existing topics:
                    {existing_topics}

                    Here is the new topic: {st.session_state.deskside_topic}
                    
                    
                    Place your thought process in <thinking></thinking> tags. Respond with either the name of the matching existing topic or the new topic itself if it does not fit under any of the existing topics, in the <answer></answer> tags. Ensure the comparison is thorough and no relevant match is overlooked.
                """

                topic_response=send_chat_compas(input,conversation_id, cookie_value)
                match = re.search(r'<answer>(.*?)</answer>',topic_response['message']['content'], re.DOTALL | re.IGNORECASE)
                topic_involved=match.group(1).strip()

                if topic_exists(graph, topic_involved):
                    experts=get_experts_for_topic(graph, topic_involved)
                else:
                    experts="Unfortunately, we do not have any experts for this topic yet."
            

                # def add_category(graph, name):
                #     query = """
                #     MATCH (a:Accelerator {name: 'Deskside Coaching'})
                #     CREATE (c:Topic {name: $name})
                #     CREATE (a)-[:HAS_TOPIC]->(c)
                #     """
                #     params = {"name": name}
                #     graph.query(query, params=params)
                

                # existing_topics=fetch_topics(graph)
                # if topic_involved not in existing_topics:
                #     add_category(graph, topic_involved)

                combined_message = f"""
                **Summarized Customer Request:** {st.session_state.user_input}

                **Recommended Success Accelerator:** {st.session_state.recommended_accelerator}
                
                **Solution(s) Involved:** {st.session_state.solution}

                **Recommended Resources:** {experts}
                """
                handle_response(combined_message)

if st.session_state.step=="Event Planning" and not st.session_state.event_planning_submitted:
    ph=st.empty()
    with ph.container():
        event_planning_type = st.selectbox("Please confirm when the event is happening.", ["Less than 4 weeks away","4 or more weeks later"], key="event_planning_type")
        if st.button("Submit", key="submit_event_planning"):
            st.session_state.event_planning_submitted = True
            st.session_state.chat_history.append({"role": "user", "content": f"Event Date: {event_planning_type}"})
            with st.chat_message("user"):
                st.markdown(f"Event Date: {event_planning_type}")
            if event_planning_type == "Less than 4 weeks":
                response = f"""
                Unfortunately, Event Planning/Monitoring must be submitted **4 weeks prior to the live event**.
                """
                handle_response(response)
            else:
                response = f"""
                **Summarized Customer Request:** {st.session_state.user_input}

                **Recommended Success Accelerator:** Event Planning/Monitoring

                **Solution(s) Involved:** {st.session_state.solution}

                **Note:** Event Planning is a pre-requisite to Event Monitoring. If your customer requires monitoring as well, please submit both accelerators at the **SAME TIME**. Please note that Event Planning and Event Monitoring need to be submitted **4 weeks prior to the live event**.
                """
                handle_response(response)
