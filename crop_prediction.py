import streamlit as st
from streamlit_option_menu import option_menu
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Flask API URL
FLASK_API_URL = os.getenv('FLASK_API_URL')

# Create the Streamlit app
with st.sidebar:
    selected = option_menu('Crop Predictor',
                            ['Crops Predictor'],
                            icons=['activity'],
                            default_index=0)

if selected == 'Crops Predictor':
    st.title('Crop Recommendation By Using Machine Learning')
    st.write("**Note: N, P & K are in grams per Hector, Temperature is in Degree Celsius & Soil Moisture in Percentage (%)**")
    
    # Create input fields for user to enter features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        N = st.text_input('Nitrogen')
    with col2:
        P = st.text_input('Phosphorus')
    with col3:
        K = st.text_input('Potassium')
    with col1:
        ph = st.text_input('Ph')
    with col2:
        temperature = st.text_input('Temperature')
    with col3:
        moisture = st.text_input('Moisture')
            
    if st.button('Predict'):
        try:
            input_features = {
                "Nitrogen": float(N),
                "Phosphorus": float(P),
                "Potassium": float(K),
                "Ph": float(ph),
                "Temperature": float(temperature),
                "Moisture": float(moisture),
            }
            
            print("Input features:", input_features)
            
            if float(moisture) < 20:
                st.warning("⚠️⚠️LOW WATER LEVEL IN YOUR SOIL⚠️⚠️")
                
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                farmer_phone_number = '+918567098852'
                message = f"Attention: ⚠️⚠️LOW WATER LEVEL IN YOUR SOIL⚠️⚠️"
                client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=farmer_phone_number)
            
            try:
                response = requests.post(FLASK_API_URL, json=input_features)
                if response.status_code == 200:
                    result = response.json()
                    crop = result.get("prediction")
                    Region = result.get("Region")
                    
                    st.write(
                        f'<div style="background-color: black; padding: 15px; margin-bottom: 20px; border-radius: 5px; color: white; font-size: 20px;">'
                        f'Soil is fit to grow {crop}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.write(
                        f'<div style="background-color: grey; padding: 15px; margin-bottom: 20px; border-radius: 5px; color: white; font-size: 20px;">'
                        f'Details: {Region}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Send SMS using Twilio
                    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                    farmer_phone_number = '+918567098852'
                    message = f"Soil is suitable for growing {crop}.\n\nDetails: {Region}.\n\nThank you for using our crop predictor."
                    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=farmer_phone_number)

                    # st.write('<div style="background-color: black; padding: 15px; border-radius: 5px; color: white; font-size: 20px;">'
                    #         '<strong>SMS sent to Farmer\'s phone number</strong>'
                    #         '</div>', unsafe_allow_html=True)
                else:
                    st.error("Failed to get prediction from the server.")
            except requests.exceptions.ConnectionError:
                st.error("Error: Unable to connect to the server. Please make sure the server is running.")
        except ValueError:
            st.error("Invalid input. Please provide valid numeric values for all features.")
