import requests
import json

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
    return response

cookie_value="OptanonAlertBoxClosed=2024-12-17T03:38:57.307Z; kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_consent=general%3Din; previousUserConsent=in; isIMSSession=true; fltk=segID%3D13330890; userGUID=D6CC4E7062858D7B0A495C75@adobe.com; kndctr_8F99160E571FC0427F000101_AdobeOrg_consent=general%3Din; _gcl_au=1.1.941039015.1740108119; _mkto_trk=id:360-KCI-804&token:_mch-adobe.com-6a2b465bf56db0e1b16201de83a64ad; kndctr_0B6930256441790E0A495FFE_AdobeOrg_identity=CiY3NzI2NzE3NzQ1MDM3NjU5Nzg4MTk1NDA4ODEwNzQwNzEyMTIyNFISCJiDtonSMhABGAEqA1ZBNjAA8AG9mcqs0zI=; acaplup=learner; kndctr_B504732B5D3B2A790A495ECF_AdobeOrg_identity=CiYwNjc3ODMxNTE0NDg1MTI5NzM2MjQ1NTA3NTA2MTY3NDY2ODE4NlIQCLys5_zTMhgBKgNWQTYwAfABvKzn_NMy; AMCV_B504732B5D3B2A790A495ECF%40AdobeOrg=MCMID|06778315144851297362455075061674668186; _tt_enable_cookie=1; _ttp=01JN6SF1P0KXG14YBTQ8AYRSYA_.tt.1; dcy.at=type3; platformMetaData=%7B%22isAndroidAppInstalled%22%3Afalse%2C%22isAcrobatDesktopInstalled%22%3Atrue%2C%22isExtensionInstalled%22%3Atrue%2C%22isPWAInstalled%22%3Afalse%7D; mmac_machine=2025-03-06T20:27:05.988Z; mmac_760319056=2025-03-06T20:27:06.051Z; mmac_machine_dc_web_visitor=09788282032222563874327935044695880524; mmac_machine_dc_web=2025-03-06T20:27:06.089Z; mmac_760319056_dc_web=2025-03-06T20:27:06.108Z; mmac_machine_dc_web_recipient_view=2025-03-06T20:27:11.203Z; mmac_760319056_dc_web_recipient_view=2025-03-06T20:27:11.245Z; sc_locale=en_US; sc_locale_numbers=en_US; mmac_machine_chrome-extension=2025-03-12T14:04:54.941Z; s_fid=3716D7A2A3B37C74-1DE89F391D277D8B; RDC=AQ2Y0Fe6mGVkX3FFZxE0-KkJrQOKyhvtOJhKeYAPeZbJKv4E-z1Yf9aSvclMieZ8GPMttMs9GafPyvIF4mHmK6BB3ner-02OqymPUIDv10DatG2HS4AlY88u3OdDscwq8lP1QcbAyioFUU9PDWUe7g89F5QP; _fbp=fb.1.1741795178693.834646736; kndctr_B3FC0A6762EA412C0A495ED8_AdobeOrg_identity=CiYwOTc4ODI4MjAzMjIyMjU2Mzg3NDMyNzkzNTA0NDY5NTg4MDUyNFIQCLP89uS9MhgBKgNWQTYwA_ABv-u_29gy; AMCV_B3FC0A6762EA412C0A495ED8%40AdobeOrg=MCMID|09788282032222563874327935044695880524; s_cid=7015Y0000048qnyQAA; TID=-ZXL8DRN2-; _gcl_aw=GCL.1741803857.EAIaIQobChMI47bj_JSFjAMVwnhHAR1WXDlCEAAYASAAEgL2efD_BwE; _gcl_gs=2.1.k1$i1741803852$u49029685; userGuid=d972351264232aa60a495ea1@02491e85636c53f8495e07.e; AMCV_8F99160E571FC0427F000101%40AdobeOrg=MCMID|46146078712486483334426344718263253867; kndctr_DF021EE0647F46FB0A495F95_AdobeOrg_identity=CiYxMDM1MDI5OTUxNTYwNTMwODQ4MjY3NzE0NzcxMTMyNjUwNTI2NlIQCNKa6uLWMhgBKgNWQTYwAfABsd2cgNky; OptanonChoice=1; _scid=Ez2_BZ4zmdNQUcuPA6uaEBXCe4B3Pr-JzpOneQ; _ScCbts=%5B%22442%3Bchrome.2%3A2%3A5%22%5D; _cs_c=0; _sctr=1%7C1742184000000; AMCV_92D346EB57C994D87F000101%40AdobeOrg=MCMID%7C68361463375121612791917018995502874623; adcloud={%22_les_v%22:%22c%2Cy%2Cadobe.com%2C1742411306%22}; event-origin=https%3A%2F%2Fbusiness.adobe.com%2Fsummit%2F2025%2Fsessions%2Fhow-workfront-is-bringing-enterpriseready-ai-os808.html; _cs_id=7d0baf38-fc47-a8a5-dacf-27cc7d3b30a6.1734576296.26.1742409607.1742405042.1717775740.1768740296795.1; _scid_r=FT2_BZ4zmdNQUcuPA6uaEBXCe4B3Pr-JzpOnig; _uetsid=9a6c5e30036b11f09d4e195c042d33dc; _uetvid=3b950470bdb311efb223c50782cf097f; _rdt_uuid=1737486785226.2e00c973-6b27-4734-bdde-f69b0761701e; kndctr_6AD033CF62197E1C0A495FDD_AdobeOrg_identity=CiYwOTgyNTczODg1MTM5OTg1NTAzMjc5OTIwMzA0NjQ3MTY1MzA2OVIQCKXfy5W9MhgBKgNWQTYwAfABr4udidsy; kndctr_8F99160E571FC0427F000101_AdobeOrg_identity=CiY0NjE0NjA3ODcxMjQ4NjQ4MzMzNDQyNjM0NDcxODI2MzI1Mzg2N1ISCKDbrK3TMhABGAEqA1ZBNjAA8AGOlJ2J2zI=; kndctr_9E1005A551ED61CA0A490D45_AdobeOrg_identity=CiYwOTc4ODI4MjAzMjIyMjU2Mzg3NDMyNzkzNTA0NDY5NTg4MDUyNFISCI%5Fe2Iy9MhABGAEqA1ZBNjAA8AH6kvye2zI%3D; shellImsEnv=prod; s_ims=https://ims-na1.adobelogin.com/ims/session/v1/ZWM1NzZmM2YtZGMzZC00MGNlLWE4NzAtNmMwZWQwMTgyY2I3LS1EQ0E2NEUwRTYyOThEQjQyMEE0OTVDQkFAMTQzNzI0NTk2MWU4ZjA2YzQ5NWU3OS5l; s_cc=true; sc_ident=Adobe%20AGS447%7C%7Ceahn%40adobe.com~~Premier%20Support%20Consulting%7C%7Ceahn%40adobe.com~~Delta%7C%7Ceahn%40adobe.com~~Cisco%7C%7Ceahn%40adobe.com~~Microsoft%20Store%7C%7Ceahn%40adobe.com; mc_company=Adobe%20AGS447; s_vnum=1744430202031%26vn%3D7; lang=en%3AUS; AMCVS_CB20F0CC53FCF3AC0A4C98A1%40AdobeOrg=1; AMCV_CB20F0CC53FCF3AC0A4C98A1%40AdobeOrg=179643557%7CMCIDTS%7C20168%7CMCMID%7C01175932912991398923088290189720732582%7CMCAAMLH-1743084328%7C7%7CMCAAMB-1743084328%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1742486728s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.5.0; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-2121179033%7CMCMID%7C09788282032222563874327935044695880524%7CMCAID%7CNONE%7CMCOPTOUT-1742487067s%7CNONE%7CMCAAMLH-1743084667%7C7%7CMCAAMB-1743084667%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C5.3.0%7CMCIDTS%7C20166%7CMCCIDH%7C-179492357; s_dslv=1742479871010; s_ppv=[%22documentcloud.adobe.com/spodintegration/index.html%22%2C100%2C0%2C1058%2C2010%2C1058%2C3200%2C1333%2C2%2C%22P%22]; AMCVS_E8F928AE56CDB5647F000101%40AdobeOrg=1; AMCV_E8F928AE56CDB5647F000101%40AdobeOrg=870038026%7CMCIDTS%7C20168%7CMCMID%7C00826784236049960083053355333325608250%7CMCAAMLH-1743090225%7C7%7CMCAAMB-1743090225%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1742492625s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.0; s_nr=1742486374972-Repeat; apt.uid=AP-PCBATQJJQHRG-2-1742486516046-31839925.0.2.430ec173-b93b-4929-92e4-0137bf9f2d8a; s_sq=gcoeaguprod%3D%2526pid%253Dindex%2526pidt%253D1%2526oid%253Dblob%25253Ahttp%25253A%25252F%25252Fgcoe.corp.adobe.com%25252F3310323a-d428-4b83-867d-c6ec460de7bc%2526ot%253DA%26adbadobenonacdcprod%252Cadbadobeprototype%3D%2526c.%2526a.%2526activitymap.%2526page%253Ddocumentcloud.adobe.com%25253Aspodintegration%25253Aindex%2526link%253Dd1d1d1d1d2d1d1d1d1d1d2d1d1d1d1d1d2d1d4d1d1d1d1d2-%2526region%253Dother%2526xy%253D1050%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c; fg=ZJRBNQ4WXPP74HUKPMQV27AACA======; aux_sid=AVQ9qQC6uRx8wrqYyT0spItTvNkb9_4H1wp5y_CWWfKEb5e7Sc70fNAcZkM6B-U-KE_ROiJjefWRHEANBTxpjK2c5viN4xGat3hE-G9Adg7k9gJm3nJ-VFgl1jgg2w0MQiqy5Dq3RYXEq7ZfP3ApwnmVikETTEqBIkVoYCtBInhBBqMCnlhVfgF2pKFMNtjUS-BOal0ydFDOD2i6wSUE2TDjZZy9ngb1Uybm2TT3jcenWevbyeR8XUlO_l179W-pJeRpkqlWWbGwfctvMp6p5Zyj_KiJed5Zj0oD2Zt7RY_wP00kmhUlILjINSXwRhfr9CnxRJ2l2z_Ws2n6ifdS9zAhKGv5An12sL6IYEMLpLS5vQGl2vVcg27dh7nSn20gyDgSNRlayN0Os4Q62YWnXFwS7oJgAbcFHJNnQaMZVmGdv3BhVJkhQW08wHjtpcL6eKh1nOvVQKL6mbfO7Nlv2d8sJfPG5liIwaud3NW_VtbohXDsI-oVZPkPs8vJ0meDftJVy2vUTPj15fatpEvj2PvqaBuWlvwSAV0cadBCo823g024FHbSxFFAxn23hkz1zk0YK8N-RUaGU8loRmeI2Itz1oJRLQrKbxQE6pWlFQutJ0SS3J9zOAQADRJfrD9Yne5Dn9Nbvb1pQcLS8wf_jVQd0LcOdBqqYDZ9kJNM-bbq17gkcaYbmXuEQqHyS8kIRi3VtzwVUVUQ-xQ5fqVnSbh970A_eOcxpZUP-qYuekeScRkoKC7RFGa4vV7sol2nlitAWhoGAWaEkSg862hbQzCL_QFK4DjVXSlWBqoq4ou59U0; OptanonConsent=groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&isGpcEnabled=0&datestamp=Thu+Mar+20+2025+12%3A22%3A30+GMT-0400+(Eastern+Daylight+Time)&version=202311.1.0&browserGpcFlag=0&geolocation=US%3BNJ&isIABGlobal=false&hosts=&consentId=ef1010f1-aa7e-4b61-9bfc-ffa9cec4baa7&interactionCount=0&landingPath=https%3A%2F%2Freg.adobe.com%2Fflow%2Fadobe%2Fas25%2Fsessions%2Fpage%2Fcatalog%3Fsearch&tab.allsessions=1643149273691001NFtR&search.product=option_1636755970075; mbox=session%2309788282032222563874327935044695880524%2DvohyxA%231742489611%7CPC%2309788282032222563874327935044695880524%2DfYQyWf%2E34%5F0%231805158304; session=.eJwljjEKAzEMBP_iOgeyZZ2k-0ywLIkEUt2RKuTvMWSqLQZ2PuWeZ1yPcuR4XXEr96eXowQZo6N6Nuw002r0ho2xaSVSrhU51wSJ1OaiMbOKtx2mJthkGzGhNdbaF3syMHgn04E5FbtZDndGFiHoGetkkOEwdMeeZYW8rzj_NUtmr4jbTlW2niKbkttmU4Y5wS4TyvcH00A43w.Z9xCLQ.9kXtuJpROPvw9FfZ4cSdMEZ1z7s"
conversation_id="f6e5ab38-0688-11f0-aedc-96fa18d741f1"


# input=f"""
# Think step by step on if you think you can address and resolve the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. Respond in detail your response after all your thinking steps in the <answer></answer> tag
# Here is the customer request: {customer_input}.
# """

customer_input="""
The customer is looking for guidance on how to get the CJA data connector launched so they can utilize the connector be able to migrate from AA to CJA.
"""

# input=f"""
# Can you reword the customer request below to use more accurate termminology stricly based on the latest Adobe Experience League Documentation as well as summarizing what the customer needs help with and why?
# Here is the customer request: {customer_input}.
# Respond only with the rewored and summarized customer request in the <summary></summary> tag.
# """

# input=f"""
# You are an Adobe Experience League Documentation Expert. Think step by step on how you can reword and summarize the customer request below using only official termminology from Adobe Experience League Documentation.  For each described functionality or feature, identify and replace it with the most specific corresponding official term from Adobe Experience League.  Make sure to preserve the essential meaning of what the customer needs help with and why.
# Here is the customer request: "Customer seeks guidance on stitching based on identity to enable them to have a more accurate view of their customers with CJA."
# Respond only with the reworded and summarized customer request in the <summary></summary> tag.
# """


# input="""
# Based on the latest Experience League documentation, think step by step on which Adobe Experience Cloud Product expertise is needed to resolve the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. 
# Here is the customer request: "Customer requests guidance on implementing Identity Stitching within Adobe Customer Journey Analytics (CJA) to achieve a unified and accurate customer view by leveraging identity resolution capabilities."
# Place your thought process in <thinking></thinking> tags. Respond only with the names of the Adobe Experience Cloud products separated by commas, and in order of priority inside the same <product></product> tag.
# """

input="""
Think step by step on identifying which area of Customer Journey Analytics, Adobe Experience Platform, the customer would like enablement on based on the customer request, but only keep a minimum draft for each thinking step, with 5 words at most. Ensure the topic chosen is based on the latest Adobe Experience League Documentation, to ensure topics are accurate and consistent.
Here is the customer request: "Customer requests guidance on implementing Identity Stitching within Adobe Customer Journey Analytics (CJA) to achieve a unified and accurate customer view by leveraging identity resolution capabilities."
Place your thought process in <thinking></thinking> tags. In the <topic></topic> tags, respond ONLY with the exact feature or capability name (e.g., "Adobe Analytics Source Connector") WITHOUT including words like "Enablement," "Training," or similar terms.
"""

# input="""
#     Think step by step on whether the new topic is the same as one of the existing topics, but only keep a minimum draft for each thinking step, with 5 words at most.
#     Here are the existing topics:
#     1. Analytics Source Connector

#     Here is the new topic: Adobe Analytics Source Connector for CJA
    
    
#     Place your thought process in <thinking></thinking> tags. Respond with either only thename of existing topic or only the new topic if it doesn't fit under any of the existing topics in the <answer></answer> tags.
# """

response=send_chat_compas(input,conversation_id, cookie_value)
print(response)