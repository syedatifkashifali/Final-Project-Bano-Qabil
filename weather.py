import streamlit as st
import requests
import json

# Set up the Weather API
url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
headers = {
    'X-RapidAPI-Key': 'YOUR-API-KEY',
    'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
}

# Get the location input from the user
location = st.text_input("Enter the location", "Chennai")

# Set up the query parameters
querystring = {"q":location}

# Get the forecast data from the API
response = requests.request("GET", url, headers=headers, params=querystring)
result = response.text

# Parse the JSON data
data = json.loads(result)

# Display the forecast data
st.title("Weather Forecast")
st.subheader(data["location"]["name"])
st.write(f"Forecast for the next 5 days:")

for forecast in data["forecast"]:
    st.write(f"{forecast['date']}: {forecast['day']['condition']['text']} - {forecast['day']['maxtemp_c']}°C / {forecast['day']['mintemp_c']}°C")
