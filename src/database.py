import pymongo
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Get URI from .env file
MONGO_URI = os.getenv('MONGO_URI')

@st.cache_resource
def get_db():
    try:
        # Check if URI exists
        if not MONGO_URI:
            st.error("MONGO_URI not found in .env file!")
            return None
            
        # Initialize Client
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        
        # Force a connection test to see if server is actually running
        client.server_info() 
        
        db = client["GM_Detections_DB"]
        return db
    except Exception as e:
        st.error(f"📡 Database Offline: Please ensure MongoDB is running. Error: {e}")
        return None

def verify_user(email, password):
    db = get_db()
    # SAFETY CHECK: If db is None, don't try to access .users
    if db is not None:
        user = db.users.find_one({"email": email, "password": password})
        return user
    return None

def add_user(name, email, password):
    db = get_db()
    # SAFETY CHECK: If db is None, return a failure status
    if db is None:
        return "error"
        
    # Check if email is already registered
    if db.users.find_one({"email": email}):
        return "exists"
    
    # Insert new user data
    db.users.insert_one({
        "name": name,
        "email": email,
        "password": password
    })
    return "success"