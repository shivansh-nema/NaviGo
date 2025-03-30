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

API_KEY = "eee0d050b3328859b4b81b7e"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

def get_exchange_rates(base_currency):
    url = BASE_URL + base_currency
    response = requests.get(url)
    data = response.json()
    
    if data.get("result") == "success":
        return data["conversion_rates"]
    else:
        return None

st.title("Currency Converter")
st.write("Convert between different currencies in real time!")

currencies = ["USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "CNY"]
base_currency = st.selectbox("Select Base Currency", currencies, index=0)
target_currency = st.selectbox("Select Target Currency", currencies, index=1)

amount = st.number_input("Enter Amount", min_value=0.01, value=1.0, step=0.01)

if st.button("Convert"):
    rates = get_exchange_rates(base_currency)
    
    if rates and target_currency in rates:
        converted_amount = amount * rates[target_currency]
        st.success(f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
    else:
        st.error("Failed to fetch exchange rates. Try again later.")
