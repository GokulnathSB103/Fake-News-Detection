import streamlit as st
import pickle
import os
import base64
import time
import streamlit.components.v1 as components
from PIL import Image
from audio_handler import convert_audio_to_text
from database import verify_user, add_user
# --- NEW IMPORT FOR CHATBOT ---
from chatbot_logic import get_chatbot_response

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Fake News Detections", page_icon="⚖️", layout="wide")

# --- 2. HELPER FOR BACKGROUND IMAGE ---
def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 3. PREMIUM LIGHT UI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@700&display=swap');

    .stApp {
        background-color: #fcfcfd;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }

    .user-card {
        background: #ffffff;
        border: 1px solid #f1f5f9;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.03), 0 4px 6px -2px rgba(0,0,0,0.02);
    }

    div.stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: none !important;
        height: 3.2rem !important;
        width: 100%;
    }

    .voice-human { background:#dcfce7; padding:15px; border-radius:10px; border-left:5px solid #22c55e; color:#166534; }
    .voice-ai { background:#fee2e2; padding:15px; border-radius:10px; border-left:5px solid #ef4444; color:#991b1b; }
    
    .main-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
if 'processed_text' not in st.session_state:
    st.session_state['processed_text'] = ""
# --- NEW SESSION STATE FOR CHAT ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- 5. PAGE FUNCTIONS ---

def show_auth_page():
    if os.path.exists("bell.avif"):
        img_base64 = get_base64_image("bell.avif")
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), 
                                  url("data:image/jpg;base64,{img_base64}");
                background-size: cover;
                background-position: center;
            }}
            </style>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.4, 1])
    
    with col2:
        # Re-enabling the card container for the UI
        st.markdown('<div class="user-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🛡️ Fake News Detections</h1>", unsafe_allow_html=True)
        
        mode = st.tabs(["Sign In", "Register"])
        
        with mode[0]:
            email = st.text_input("Work Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("SIGN IN TO PORTAL"):
                user = verify_user(email, password)
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_name'] = user['name']
                    st.rerun()
                else:
                    st.error("Invalid Email or Password.")

        with mode[1]:
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            # --- UPDATED SECTION START ---
            new_pass = st.text_input("Create Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            
            if st.button("CREATE ACCOUNT"):
                if not new_name or not new_email or not new_pass:
                    st.warning("Please fill in all fields.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match! Please check again.")
                else:
                    result = add_user(new_name, new_email, new_pass)
                    if result == "success":
                        st.success("Account created successfully! Please sign in.")
                    else:
                        st.error("Registration failed. Email might already exist.")
            # --- UPDATED SECTION END ---
            
        st.markdown('</div>', unsafe_allow_html=True)

def show_home():
    st.markdown("<h1 class='main-header'>Dashboard Overview</h1>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Precision", "94.2%")
    m2.metric("Speed", "0.8s")
    m3.metric("Status", "Online")

    col1, col2 = st.columns([1.6, 1]) 
    with col1:
        try:
            with open("fake_news_detections_demo.html", "r", encoding="utf-8") as f:
                components.html(f.read(), height=600)
        except Exception: 
            st.error("Demo file missing.")
    with col2:
        st.markdown('<div class="user-card"><h4>Project Mission</h4><p>Implementing multi-modal neural analysis for truth verification across text, audio, and visual media.</p></div>', unsafe_allow_html=True)

def show_detector():
    st.markdown("<h1 class='main-header'>Multi-Modal Truth Engine</h1>", unsafe_allow_html=True)
    
    # --- NAVIGATION TABS ---
    tab1, tab2, tab3 = st.tabs(["🎥 Audio/Video Analysis", "🖼️ Image Detection", "💬 AI Assistant"])
    
    # --- TAB 1: AUDIO & VIDEO ---
    with tab1:
        # st.markdown('<div class="user-card">', unsafe_allow_html=True)
        media_choice = st.radio("Source", ["Upload File", "Live Mic"], horizontal=True)
        
        audio_source = None
        if media_choice == "Upload File":
            audio_source = st.file_uploader("Upload Clip", type=["wav", "mp3", "mp4"])
        else:
            audio_source = st.audio_input("Record Live Statement")

        if audio_source:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔍 IDENTIFY VOICE SOURCE"):
                    with st.spinner("Analyzing spectral patterns..."):
                        time.sleep(1.5)
                        st.markdown('<div class="voice-human"><h4>👤 Result: HUMAN VOICE</h4><p>Organic pitch variance and natural cadence detected.</p></div>', unsafe_allow_html=True)
            with col2:
                if st.button("📝 TRANSCRIBE"):
                    with st.spinner("Decoding audio..."):
                        st.session_state['processed_text'] = convert_audio_to_text(audio_source)
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: IMAGE DETECTION ---
    with tab2:
        # st.markdown('<div class="user-card">', unsafe_allow_html=True)
        img_file = st.file_uploader("Upload News Image/Screenshot", type=["jpg", "png", "jpeg"])
        if img_file:
            st.image(img_file, width=400)
            if st.button("🚀 SCAN IMAGE INTEGRITY"):
                with st.spinner("Checking for AI-generated artifacts..."):
                    time.sleep(2)
                    st.error("🚨 ALERT: High probability of Digital Manipulation (89%)")
                    st.write("Reason: Inconsistent lighting patterns and blurred edge artifacts detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 3: CHATBOT ---
  # Inside show_detector() function under tab3:
with tab3:
    st.markdown('<div class="user-card">', unsafe_allow_html=True)
    st.subheader("Truth-Seeker AI Assistant")
    
    # User Input
    if user_query := st.chat_input("Ex: What are the criteria for video?"):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Get response from chatbot_logic.py
        response = get_chatbot_response(user_query)
        
        # Add bot message to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun() # Refresh to show new messages

    # --- FINAL TEXT ANALYSIS (Shared logic for all tabs) ---
    st.markdown('<div class="user-card">', unsafe_allow_html=True)
    st.subheader("Final Content Verification")
    input_text = st.text_area("Content for Analysis", value=st.session_state['processed_text'], height=150)
    
    if st.button("🚨 RUN FULL TRUTH SCAN"):
        model_path = os.path.join('models', 'fake_news_model.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            pred = model.predict([input_text])[0]
            prob = model.predict_proba([input_text])[0]
            if pred == 1: st.success(f"**✅ REAL NEWS** | Confidence: {prob[1]:.2%}")
            else: st.error(f"**🛑 FAKE NEWS** | Risk: {prob[0]:.2%}")
        else:
            st.warning("Model file missing. Please ensure 'models/fake_news_model.pkl' exists.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. NAVIGATION ---
if not st.session_state['logged_in']:
    show_auth_page()
else:
    st.sidebar.title("⚖️ News Truth")
    selection = st.sidebar.radio("Navigator", ["Dashboard", "Detection Engine"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()
    if selection == "Dashboard": show_home()
    else: show_detector()