import streamlit as st
import requests

# Set up the OpenWeatherMap API
url = "https://api.openweathermap.org/data/2.5/weather?"
api_key = "66869939e0b182ac2d6e17228f1a15c6"

# Get the location input from the user
location = st.text_input("Enter the location", "Chennai")

# Set up the query parameters
querystring = {"q":location, "appid":api_key, "units":"metric"}

# Get the forecast data from the API
response = requests.request("GET", url, headers=headers, params=querystring)
result = response.text

# Parse the JSON data
try:
    data = json.loads(result)
except json.JSONDecodeError as e:
    st.write("Error: could not parse JSON data")
    st.write(e)
    return

# Display the forecast data
if "name" in 
    st.title("Weather Forecast")
    st.subheader(data["name"])
    st.write(f"Temperature: {data['main']['temp']}°C")
    st.write(f"Feels like: {data['main']['feels_like']}°C")
    st.write(f"Humidity: {data['main']['humidity']}%")
    st.write(f"Wind speed: {data['wind']['speed']} m/s")
    st.write(f"Description: {data['weather'][0]['description']}")
else:
    st.write("Error: could not get weather data")
