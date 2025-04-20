import streamlit as st
import requests
from streamlit_option_menu import option_menu
from requests.structures import CaseInsensitiveDict

st.set_page_config(
    page_title="NaviGo",
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

st.title("City Navigator")

def get_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        countries = sorted([country["name"]["common"] for country in data])
        return ["Select a country..."] + countries
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

navigation_api_key = st.secrets["NAVIGATION_API_KEY"]
headers = {
    "authorization": navigation_api_key,
    "content-type": "application/json"
}

def get_coordinates(city):
    url = f"https://api.geoapify.com/v1/geocode/search?text={city}&apiKey={navigation_api_key}"
    response = requests.get(url)
    data = response.json()
    
    if "features" in data and len(data["features"]) > 0:
        lat = data["features"][0]["geometry"]["coordinates"][1]
        lon = data["features"][0]["geometry"]["coordinates"][0]
        return lat, lon
    else:
        return None, None

def get_places(lat, lon, category):
    if lat is None or lon is None:
        return []

    url = f"https://api.geoapify.com/v2/places?categories={category}&lat={lat}&lon={lon}&radius=5000&limit=10&apiKey={navigation_api_key}"
    response = requests.get(url)
    data = response.json()
        
    places = []
    if "features" in data:
        for place in data["features"]:
            places_lat = place["properties"].get("lat", lat)
            places_lon = place["properties"].get("lon", lon)
            places_info = {
                "name": place["properties"].get("name", "Unnamed Place"),
                "address": place["properties"].get("formatted", "Address not available"),
                "google_maps_link": f"https://www.google.com/maps/search/?api=1&query={places_lat},{places_lon}",
            }
            places.append(places_info)

    return places[:5]

place_type = option_menu(
    "What are you looking for?", 
    options=["Hotels","Travel", "Restaurants", "Cafes"], 
    icons=["building-fill","geo-alt-fill", "cup-straw", "cup-hot-fill"], 
    menu_icon="arrow-right-circle-fill",  
    default_index=0, 
    orientation="horizontal",
)

category_mapping = {
    "Hotels": "accommodation.hotel",
    "Restaurants": "catering.restaurant",
    "Cafes": "catering.cafe",
    "Travel": "tourism"
}

if st.button(f"Find {place_type}") and selected_city:
    lat, lon = get_coordinates(selected_city)
    if lat and lon:
        places = get_places(lat, lon, category_mapping[place_type])
        
        if places:
            st.header(f"{place_type} in {selected_city}:")
            for place in places:
                st.subheader(f"{"●"} **{place['name']}**")
                st.write(f"→ {place['address']}")
                st.markdown(f"→ [View on Google Maps]({place['google_maps_link']})", unsafe_allow_html=True)
                st.write("---")
        else:
            st.warning(f"No {place_type.lower()} found. Try another city.")
    else:
        st.error("Could not find the location. Check the city name.")   