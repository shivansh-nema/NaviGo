import streamlit as st

st.set_page_config(
    page_title="Navigo",
    page_icon="Navigo_Icon.png",
    layout="wide"
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

st.title("Navigo - Your Intelligent Travel Companion")
st.write("In an era where seamless travel experiences are a priority, our AI-powered Travel Companion App redefines the way you explore the world. Designed to enhance every stage of your journey, our app integrates cutting-edge technology to provide personalized AI assistance, real-time weather forecasts, city exploration tools, and a built-in currency converter—ensuring a smooth, informed, and enriching travel experience.")

st.header("Key Features & Capabilities")

st.subheader("→ AI Travel Assistance")
st.write("Leverage the power of artificial intelligence to receive tailored travel recommendations, curated itineraries, and expert insights. Whether you're seeking top-rated attractions, hidden gems, or efficient transportation routes, our AI assistant provides instant, data-driven suggestions customized to your preferences.")

st.subheader("→ City Exploration & Local Insights")
st.write("  Navigate new destinations effortlessly with our comprehensive city exploration feature, which enables you to:")
st.write(" • Discover highly-rated hotels for a comfortable and convenient stay")
st.write(" • Find top restaurants, cafés, and culinary hotspots suited to your taste")
st.write(" • Access details on must-visit tourist attractions and cultural landmarks")
st.write(" • Locate essential services such as ATMs, pharmacies, and transit stations")


st.subheader("→ Real-Time Weather Forecasting")
st.write("Stay prepared with live weather updates that provide detailed forecasts, temperature trends, and climate conditions for your chosen destinations. Whether planning an outdoor excursion or scheduling business meetings, our weather insights help you make informed decisions and optimize your itinerary.")

st.subheader("→ Currency Converter – Global Exchange Made Simple")
st.write("With our built-in currency converter, travelers can instantly access up-to-date exchange rates for hassle-free transactions. Whether booking accommodations, dining out, or shopping, this feature ensures accurate conversions and financial transparency in any country.")