import streamlit as st
from dotenv import load_dotenv
import os
import mysql.connector

# 1. Inject custom CSS to style the Delete button
st.markdown("""
    <style>
    .stButton > button {
        background-color: #dc3545 !important; /* "Danger" red */
        color: white !important;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        border-radius: 0.25rem;
        cursor: pointer;
        white-space: nowrap; /* Prevents text from wrapping */
    }
    .stButton > button:hover {
        background-color: #c82333 !important; /* Darker red on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(
        host="162.55.20.122",
        user="ycyawtrr_huzaifa",
        password="intellectualtalkfypdatabase",
        database="ycyawtrr_cartkro"
    )

# Function to retrieve the ads with only the required fields
def get_ads():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT ad_id, user_id, title, brand_id, rating, img_id, price
        FROM ads
    """
    cursor.execute(query)
    ads = cursor.fetchall()
    cursor.close()
    conn.close()
    return ads

# Function to delete an ad by its id
def delete_ad(ad_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ads WHERE ad_id = %s", (ad_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Streamlit app title
st.title("Ads Administration Dashboard")

# Get the current ads from the database
ads = get_ads()

if ads:
    # Create a table header with the field names and an empty header for the delete button
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 1, 2, 1, 1])
    col1.write("User ID")
    col2.write("Title")
    col3.write("Brand ID")
    col4.write("Rating")
    col5.write("Image ID")
    col6.write("Price")
    col7.write("")  # For the delete button header

    # Loop over each ad and display the fields with a delete button
    for ad in ads:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 1, 2, 1, 1])
        col1.write(ad['user_id'])
        col2.write(ad['title'])
        col3.write(ad['brand_id'])
        col4.write(ad['rating'])
        col5.write(ad['img_id'])
        col6.write(ad['price'])
        
        # Use a unique key for each button
        if col7.button("Delete", key=ad['ad_id']):
            delete_ad(ad['ad_id'])
            st.success(f"Deleted ad with id {ad['ad_id']}. Please refresh the page.")
else:
    st.write("No ads found!")
