import streamlit as st 
import africastalking
import os

from dotenv import load_dotenv

load_dotenv()

# genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime

col1, col2 = st.columns(2)




with col1:
	with st.form("user_registration"):
	    st.subheader("User Self Registration")
	    names = st.text_input("Official Names")
	    username = st.text_input('Username:')
	    email = st.text_input("Email: ")
	    phone_number = st.number_input("Phone Number:", value=None, min_value=0, max_value=int(10e10))
	    password = st.text_input('Passowrd', type="password")
	    confirm_password = st.text_input('Confirm password', type='password')

	    checkbox_val = st.checkbox("Subscribe to our Newsletter")

	    submitted = st.form_submit_button("Submit")

	    # Every form must have a submit button.
	    if password != confirm_password:
	    	st.error('Password mismatch', icon='⚠️')

	    else:
		    
		    if not (email and password):
		    	st.warning('Please enter your credentials!', icon='⚠️')
		    else:
		    	st.success('Proceed to engaging with the system!', icon='👉')

		    	

		    	if submitted:

			        amount = "10"
			        currency_code = "KES"

			        recipients = [f"+254{str(phone_number)}"]

			        airtime_rec = "+254" + str(phone_number)

			        print(recipients)
			        print(phone_number)

			        # Set your message
			        message = f"Welcome to ResQBot!";

			        # Set your shortCode or senderId
			        sender = 20880

			        try:
			        	responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)
			        	response = sms.send(message, recipients, sender)

			        	print(response)

			        	print(responses)

			        except Exception as e:
			        	print(f'Houston, we have a problem: {e}')

	

	# st.write("Outside the form")

with col2:
	st.image('./src/reg.png', width=700)