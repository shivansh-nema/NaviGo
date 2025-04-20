import streamlit as st
import requests

st.set_page_config(
    page_title="Navigo",
    page_icon="Navigo_Icon.png",
)

page_bg_img = """
<style>
.block-container {
        padding-top: 3rem !important;
}
# header { visibility: hidden; }

[data-testid="stAppViewContainer"]{
    background-image: url(https://images.unsplash.com/photo-1551309292-e185c0b6e22a?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D);
    background-size: cover;
}

[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}

[data-testid="stSidebarContent"]{
    background-image: url(https://images.unsplash.com/photo-1669295384050-a1d4357bd1d7?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D);
    background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Weather Forecast")

def get_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        countries = sorted([country["name"]["common"] for country in data])
        return ["Select a country..."] + countries  # Add placeholder at the top
    else:
        return ["Error fetching countries"]
    
def get_states(country):
    url = "https://countriesnow.space/api/v0.1/countries/states"
    response = requests.post(url, json={"country": country})
    if country == "Select a country...":
        return []
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "states" in data["data"]:
            states = sorted([state["name"] for state in data["data"]["states"]])
            return ["Select a state..."] + states
    return ["No states found"]

def get_cities(country , state):
    if country == "Select a country..." or state == "No states found":
        return []
    url = "https://countriesnow.space/api/v0.1/countries/state/cities"
    response = requests.post(url, json={"country": country, "state": state})
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            cities = sorted(data["data"])
            return ["Select a city..."] + cities
    return ["No cities found"]

countries = get_countries()
selected_country = st.selectbox("Choose a country:", countries, index=0)

states = get_states(selected_country)
selected_state = st.selectbox("Choose a state:", states, index=0)

cities = get_cities(selected_country, selected_state)
selected_city = st.selectbox("Choose a city:", cities, index=0)

headers = {
    "authorization": st.secrets["WEATHER_API_KEY"],
    "content-type": "application/json"
}

def get_weather(city):
    url = f"https://api.weatherbit.io/v2.0/current?city={city}&key={WEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "data" in data:
        weather_info = data["data"][0]
        return {
            "city": weather_info["city_name"],
            "temperature": weather_info["temp"],
            "weather": weather_info["weather"]["description"],
            "humidity": weather_info["rh"],
            "wind_speed": weather_info["wind_spd"],
            "icon": weather_info["weather"]["icon"]
        }
    else:
        return None

if st.button("Get Weather"):
    weather_data = get_weather(selected_city)

    if weather_data:
        st.subheader(f"Weather in {weather_data['city']}")
        st.image(f"https://www.weatherbit.io/static/img/icons/{weather_data['icon']}.png", width=100)
        st.write(f"→ Temperature: **{weather_data['temperature']}°C**")
        st.write(f"→ Weather: **{weather_data['weather']}**")
        st.write(f"→ Humidity: **{weather_data['humidity']}%**")
        st.write(f"→ Wind Speed: **{weather_data['wind_speed']} m/s**")
    else:
        st.error("City not found. Please try again.")