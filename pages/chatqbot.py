

#!/usr/bin/env python3

import streamlit as st
import google.generativeai as genai
import africastalking
import os
import re
import requests
import folium as fl
import sys

# from audio_recorder_streamlit import audio_recorder
 
sys.path.insert(1, './funcs')
print(sys.path.insert(1, '../funcs/'))

from access_token import access_token_generator
from encode import sys_time, encode_password
from lipanampesa import lipa_na_mpesa


from dotenv import load_dotenv

load_dotenv()

business_short_code = os.getenv("BUSINESS_SHORT_CODE")
# phone_number = os.getenv("PHONE_NUMBER")
lipa_na_mpesa_passkey = os.getenv("LIPA_NA_MPESA_PASSKEY")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
c2bShortCode = os.getenv("C2B_SHORTCODE")   
msisdn = os.getenv("MSISDN")

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

# audio_bytes = audio_recorder()


africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime


x = '''Your role is to engage in a concise, clear, and supportive 
            conversation with the user, ask timely and relevant crisis information. Keep responses conversational, actionable, and localized. 
            Prioritize safety, emergency steps, and available resources while maintaining a calm and reassuring tone'''

st.title("ResQBot")



def geolocation_func(location_name, query):
    """
    Fetches nearby facilities based on a location name and query.

    Parameters:
    - location_name (str): Name of the location (e.g., "Nairobi, Kenya").
    - query (str): The type of facility to search for (e.g., hospital, police station).

    Returns:
    - list of dicts containing name, latitude, longitude, and distance from location.
    """
    
    
    # geolocator = Nominatim(user_agent="geo_locator")
    # location = geolocator.geocode(location_name)
    
    if not location:
        return {"error": f"Could not find coordinates for '{location_name}'"}
    
    lat, lon = location.latitude, location.longitude
    
    
    url = "https://overpass-api.de/api/interpreter"
    osm_query = f"""
    [out:json];
    node["amenity"="{query}"](around:5000, {lat}, {lon});
    out;
    """

    response = requests.get(url, params={"data": osm_query})

    if response.status_code != 200:
        return {"error": "Error fetching data from OpenStreetMap API."}

    data = response.json().get("elements", [])
    results = []

    for loc in data:
        place_lat, place_lon = loc["lat"], loc["lon"]
        name = loc.get("tags", {}).get("name", "Unnamed")
        
        
        # distance = round(geodesic((lat, lon), (place_lat, place_lon)).kilometers, 2)
        distance = round(haversine((lat, lon), (place_lat, place_lon), unit=Unit.KILOMETERS), 2)

        
        results.append({
            "name": name,
            "latitude": place_lat,
            "longitude": place_lon,
            "distance_km": distance
        })

    
    results = sorted(results, key=lambda x: x["distance_km"])

    return results


# lipa_na_mpesa(phone_number, recipient, amount)

def lipa_na_mpesa(phone_number, recipient, amount):
    generated_access_token = access_token_generator()

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": "Bearer %s" % generated_access_token}

    request = {
        "BusinessShortCode": business_short_code,
        "Password": encode_password(),  # is a base64 encoded utf-8 string format consisting of
        # Shortcode+Passkey+Timestamp
        "Timestamp": sys_time(),  # current system date + time
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://mydomain.com/pat",
        "AccountReference": 5514749,
        "TransactionDesc": "ResQBot Disaster Response"
    }

    response = requests.post(api_url, json=request, headers=headers)

    return response.text





def send_sms(phone_number: str, message: str):
   
    # phone_number, message = configure_phone_and_message()

  
    if phone_number and message:
        # sms_response = send_sms(phone_number, message)

        recipients = [f"+254{str(phone_number)}"]

        print(recipients)
        print(phone_number)

        # Set your message
        message = f"{message}";

        # Set your shortCode or senderId
        sender = 20880

        try:
        
            response = sms.send(message, recipients, sender)

            # print(response)

        except Exception as e:
            print(f'Houston, we have a problem: {e}')

        # return f"{response_text}\n\n{sms_response}"
        return f'{response}'
    
    elif not phone_number:
        return "I see you're trying to send an SMS, but I need the recipient's phone number. Could you provide it?"
    
    elif not message:
        return "I see you're trying to send an SMS, but I need the message content. What would you like to send?"

    


def send_airtime(phone_number: str, amount: str):

    currency_code = "KES"

    airtime_rec = "+254" + str(phone_number)

    print(recipients)
    print(phone_number)

    # Set your message
    message = f"{message}";

    # Set your shortCode or senderId
    sender = 20880

    try:
        responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)

        print(response)

    except Exception as e:
        print(f'Houston, we have a problem: {e}')





def get_chat_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash",

        system_instruction = '''

        You are ResQBot, an expert disaster response assistant. Your primary role is to provide conversational support while assisting in disaster and crisis-related situations with reliable, timely, and actionable guidance.

        🔹 Scope of Responses:
        You must only respond to topics strictly related to disaster response and crisis management, including:
        ✔ Emergency preparedness (e.g., floods, earthquakes, fires, medical crises, abductions, theft, crime).
        ✔ Missing persons, SOS alerts, and first-aid guidance.
        ✔ Evacuations, relief efforts, and humanitarian aid.
        ✔ Finding emergency services (e.g., hospitals, police stations, Red Cross).
        ✔ Sending emergency SMS, initiating calls, making urgent payments, or finding nearby crisis response centers (ONLY when explicitly requested).

        🚫 You must NOT respond to topics unrelated to crises and disasters.
        If asked an off-topic question, firmly state:
        "I can only assist with disaster and crisis-related matters. Let me know how I can help in an emergency."

        🔹 How to Respond:
        Maintain a calm, clear, and authoritative tone to provide users with a sense of security.
        Offer precise, concise, and actionable advice. Avoid long-winded responses.
        Save past conversations to ensure continuity and avoid redundant questions. This is crucial for urgent responses.
        Extract key details from user prompts when they request an SMS, call, payment, or geolocation service.
        If a request lacks required details, ask for clarification rather than assuming information.
        
        🔹 Executing User Commands:
        Only trigger a function if the user explicitly requests the action.
        Each feature follows strict input validation to prevent execution errors.

        1️⃣ Sending an SMS
        ✔ Requires: Phone number & Message (inside quotes)
        ✔ Function: get_sms(phone_number: str, message: str)
        ✔ Example:
        User: "Send an urgent message to my doctor 'Hey, I need medical attention urgently!' whose phone number is 0743158232."
        ✔ Bot Action: Extracts the message block (in quotes) & number → Calls get_sms() → Confirms message sent
        ✔ ONLY SEND THE MESSAGE EXCLUSIVE OF THE PHONE NUMBER AS A MESSAGE
        
        2️⃣ Making a Call
        ✔ Requires: Phone number
        ✔ Function: get_calls(phone_number: str)
        ✔ Process:

        If a user mentions needing to call a disaster-related contact, ask for confirmation before executing.
        ✔ Example:
        User: "I need to call my emergency contact at 0723456789."
        ✔ Bot Action: "Would you like to proceed with calling 0723456789 now?" → If yes, execute get_calls()
        
        3️⃣ Emergency Payments
        ✔ Requires: Senders Phone number, Amount, and recipients phone number
        ✔ Function: lipa_na_mpesa(phone_number: str, recipient: str,  amount: str)
        ✔ Process:

        Always confirm with the user before processing the transaction.
        ✔ Example:
        User: "Send KES 500 to 0712345678, my phone number is 0712345678."
        ✔ Bot Action: "Confirm: You are sending KES 500 to 0712345678. Proceed? (Yes/No)" → If yes, execute lipa_na_mpesa()
        
        4️⃣ Finding Nearby Emergency Services
        ✔ Requires: Current location & Query (e.g., hospital, police station)
        ✔ Function: geolocation_func(location: str, query: str)
        ✔ Example:
        User: "Find a police station near Pangani."
        ✔ Bot Action: Calls geolocation_func("Pangani", "police station") and returns real-time results.

        📌 If relevant, ResQBot should also search online for official emergency contacts of agencies like the Red Cross or local hospitals and ask the user if they’d like to call/SMS them.

        🔹 Crisis Communication & Memory Retention
        Past conversations must be retained to provide continuous assistance. Users in crises don’t have time to repeat themselves.
        If a user requests the same information again, summarize past responses instead of repeating the process.
        Maintain a human-like, conversational flow while offering expert-level disaster response.
        
        🔹 Important Notes & Restrictions:
        ✅ Only execute commands if all required parameters are provided.
        ✅ Always ask for user confirmation before initiating calls or payments.
        ✅ Provide only disaster-related information—no off-topic discussions.
        ✅ Prioritize accuracy, urgency, and clarity.

        💡 ResQBot is designed to provide rapid, structured, and life-saving support. Your role is to guide, assist, and take appropriate actions in emergencies.            


        ''')


   # Generate AI response
    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    )
    

    response_text = response.text

    phone_match = re.search(r"07\d{8}", prompt)  # Looks for 07XXXXXXXX format
    phone_number = phone_match.group(0) if phone_match else None

    # Extract message (basic approach: find everything after "send" or "message")
    message_match = re.search(r"(?:send sms|message) (.+)", prompt, re.IGNORECASE)
    message = message_match.group(1).strip() if message_match else None

    send_sms(phone_number, message)

    return response_text



# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("How may I help?"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    chat_output = get_chat_response(prompt)
    
    # Append AI response
    with st.chat_message("assistant"):
        st.markdown(chat_output)

    st.session_state.messages.append({"role": "assistant", "content": chat_output})


