import requests
import streamlit as st
from gtts import gTTS
from io import BytesIO
import os 


# Determine the backend URL based on environment
def get_backend_url():
    # For deployment, use the environment variable
    backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
    return backend_url

BACKEND_URL = get_backend_url()
    
    
# Page configuration
st.set_page_config(
    page_title="RoboTranslate - Friendly AI Translator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Friendly Robot CSS Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');
    
    /* Friendly Robot Base Theme */
    .stApp {
        background: linear-gradient(135deg, #e0f7ff 0%, #edf2ff 100%);
        font-family: 'Fredoka', sans-serif;
        color: #2d3436;
    }
    
    /* Main Container */
    .main-container {
        background: rgba(255, 255, 255, 0.92);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 100, 200, 0.1);
        border: 2px solid #a7c9ff;
        position: relative;
        overflow: hidden;
    }
    
    /* Robot Headers */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #4361ee;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Fredoka', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .subheader {
        font-size: 1.3rem;
        color: #7209b7;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
        font-family: 'Fredoka', sans-serif;
    }
    
    /* Robot Chat Bubbles */
    .chat-bubble {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 2px solid #4361ee;
        position: relative;
        box-shadow: 0 6px 20px rgba(67, 97, 238, 0.15);
    }
    
    .chat-bubble::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 30px;
        border-width: 10px 10px 0;
        border-style: solid;
        border-color: #4361ee transparent;
    }
    
    .chat-bubble.user {
        border-color: #7209b7;
        background: rgba(255, 255, 255, 0.95);
    }
    
    .chat-bubble.user::after {
        border-color: #7209b7 transparent;
        left: auto;
        right: 30px;
    }
    
    /* Card headers */
    .chat-bubble h3 {
        color: #4361ee !important;
        margin-top: 0;
        font-family: 'Fredoka', sans-serif;
    }
    
    .chat-bubble.user h3 {
        color: #7209b7 !important;
    }
    
    /* Robot Buttons */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        color: white !important;
        border: none;
        padding: 1rem 2rem;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.2rem;
        font-family: 'Fredoka', sans-serif;
        box-shadow: 0 0 20px rgba(67, 97, 238, 0.4);
        transition: all 0.3s ease;
        border: 2px solid #4cc9f0;
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(67, 97, 238, 0.6);
        background: linear-gradient(135deg, #4cc9f0 0%, #4361ee 100%);
        color: white !important;
    }
    
    .stButton button:disabled {
        background: #b8c2ff;
        transform: none;
        box-shadow: none;
        border: 2px solid #c4c8e6;
        color: #f8f9ff !important;
    }
    
    /* Robot Inputs */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #4361ee !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        font-size: 1.1rem !important;
        color: #2d3436 !important;
        font-family: 'Fredoka', sans-serif !important;
        box-shadow: inset 0 2px 8px rgba(67, 97, 238, 0.1);
    }
    
    .stTextArea textarea:focus {
        border-color: #7209b7 !important;
        box-shadow: inset 0 2px 12px rgba(114, 9, 183, 0.2);
        color: #2d3436 !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #88a0cc !important;
    }
    
    .stSelectbox select {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #4361ee !important;
        border-radius: 14px !important;
        padding: 0.8rem !important;
        color: #2d3436 !important;
        font-family: 'Fredoka', sans-serif !important;
        font-size: 1rem !important;
    }
    
    .stSelectbox select:focus {
        border-color: #7209b7 !important;
        box-shadow: 0 0 12px rgba(114, 9, 183, 0.2);
    }
    
    /* Checkbox styling */
    .stCheckbox label {
        color: #2d3436 !important;
        font-weight: 600;
        font-family: 'Fredoka', sans-serif;
    }
    
    /* LED Status Indicators */
    .led-status {
        display: flex;
        align-items: center;
        padding: 0.8rem 1.2rem;
        border-radius: 16px;
        margin: 0.3rem 0;
        font-weight: 600;
        gap: 0.8rem;
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        font-family: 'Fredoka', sans-serif;
    }
    
    .led-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }
    
    .led-on {
        background: #4ade80;
        box-shadow: 0 0 8px #4ade80;
    }
    
    .led-off {
        background: #f87171;
        box-shadow: 0 0 8px #f87171;
    }
    
    .status-text {
        font-weight: 600;
    }
    
    /* Robot Output Bubble */
    .robot-bubble {
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        color: white;
        font-size: 1.2rem;
        line-height: 1.6;
        font-family: 'Fredoka', sans-serif;
        box-shadow: 0 8px 25px rgba(67, 97, 238, 0.3);
        position: relative;
    }
    
    .robot-bubble::before {
        content: '🤖';
        position: absolute;
        top: -15px;
        left: 20px;
        font-size: 2rem;
        background: white;
        border-radius: 50%;
        padding: 5px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    .robot-bubble::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 30px;
        border-width: 10px 10px 0;
        border-style: solid;
        border-color: #3a0ca3 transparent;
    }
    
    /* Alert boxes */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #4361ee !important;
        border-radius: 16px !important;
        color: #2d3436 !important;
        font-family: 'Fredoka', sans-serif;
    }
    
    /* Spinner color */
    .stSpinner > div {
        background-color: #4361ee !important;
    }
    
    /* Sidebar - Robot Dashboard */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #3a0ca3 0%, #4361ee 100%);
        color: white;
    }
    
    .sidebar-header {
        color: #4361ee!important;
        font-family: 'Fredoka', sans-serif;
            
    }
    
    .sidebar-text {
        color: #7209b7 !important;
        font-family: 'Fredoka', sans-serif;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.2rem;
        }
        .chat-bubble {
            padding: 1.2rem;
        }
    }
    
    /* Simple footer */
    .robot-footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: #4361ee;
        font-weight: 600;
        font-family: 'Fredoka', sans-serif;
    }
    
    /* Divider style */
    .robot-divider {
        border: 0;
        height: 2px;
        background: linear-gradient(to right, transparent, #4361ee, transparent);
        margin: 1.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Functions
# Update all your API call functions to use BACKEND_URL
def check_server_connection():
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=3)
        return response.status_code == 200
    except:
        return False

def check_groq_connection():
    try:
        response = requests.get(f"{BACKEND_URL}/check_groq", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": "Cannot connect to server"}
    except:
        return {"status": "error", "message": "Connection failed"}

def get_available_models():
    try:
        response = requests.get(f"{BACKEND_URL}/models", timeout=3)
        if response.status_code == 200:
            return response.json().get("models", [])
        else:
            return ["llama3-8b-8192", "llama3-70b-8192"]
    except:
        return ["llama3-8b-8192", "llama3-70b-8192"]

def get_available_languages():
    try:
        response = requests.get(f"{BACKEND_URL}/languages", timeout=3)
        if response.status_code == 200:
            languages = response.json().get("languages", [])
            return languages if languages else get_default_languages()
        else:
            return get_default_languages()
    except:
        return get_default_languages()

def get_default_languages():
    return ["English", "French", "Spanish", "German", "Italian", "Portuguese", 
            "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Russian"]

def get_translation(input_text, language, model_name):
    if not input_text or not input_text.strip():
        return {"status": "error", "message": "Text is required"}
    
    json_body = {
        "text": input_text.strip(),
        "language": language,
        "model": model_name
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/translate", 
            json=json_body, 
            timeout=20
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

def text_to_speech(text, language):
    try:
        lang_code = {
            "English": "en", "French": "fr", "Spanish": "es", "German": "de",
            "Italian": "it", "Portuguese": "pt", "Chinese": "zh", "Japanese": "ja",
            "Korean": "ko", "Hindi": "hi", "Arabic": "ar", "Russian": "ru"
        }.get(language, 'en')
        
        tts = gTTS(text, lang=lang_code)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return audio_file
    except Exception as e:
        return None

# UI Components
def render_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<h1 class="main-header">RoboTranslate</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subheader">🤖 Your Friendly Robot Translation Assistant! 💬</p>', unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        # Sidebar styling
        st.markdown("""
            <style>
            .sidebar .sidebar-content {
                background: linear-gradient(135deg, #3a0ca3 0%, #4361ee 100%);
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<h3 class="sidebar-header">🤖 Robot Dashboard</h3>', unsafe_allow_html=True)
        
        # System status
        server_status = check_server_connection()
        groq_status = check_groq_connection()
        
        st.markdown('<p class="sidebar-text">System Status:</p>', unsafe_allow_html=True)
        if server_status:
            st.markdown('<div class="led-status"><span class="led-dot led-on"></span> <span class="status-text">Robot Online!</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="led-status"><span class="led-dot led-off"></span> <span class="status-text">Robot Offline</span></div>', unsafe_allow_html=True)
        
        if groq_status.get("status") == "success":
            st.markdown('<div class="led-status"><span class="led-dot led-on"></span> <span class="status-text">AI Active!</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="led-status"><span class="led-dot led-off"></span> <span class="status-text">AI Inactive</span></div>', unsafe_allow_html=True)
        
        st.markdown('<hr class="robot-divider">', unsafe_allow_html=True)
        
        st.markdown('<p class="sidebar-text">🤖 Robot Brain:</p>', unsafe_allow_html=True)
        
        # Model selection
        available_models = get_available_models()
        selected_model = st.selectbox(
            "Choose your AI model",
            available_models,
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown('<hr class="robot-divider">', unsafe_allow_html=True)
        
        st.markdown('<p class="sidebar-text">🔊 Robot Voice:</p>', unsafe_allow_html=True)
        
        enable_audio = st.checkbox("Enable Voice Synthesis", value=True)
        
        st.markdown('<hr class="robot-divider">', unsafe_allow_html=True)
        
        # Tech stats
        st.markdown('<p class="sidebar-text">📊 Robot Stats:</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Languages**")
            st.markdown("##### 12+")
        with col2:
            st.markdown("**AI Models**")
            st.markdown("##### 2")
        
        return selected_model, enable_audio

def render_main_content(selected_model, enable_audio):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chat-bubble user">', unsafe_allow_html=True)
        st.markdown('### 📝 Your Message')
        
        input_text = st.text_area(
            "What would you like to say?",
            height=120,
            placeholder="Type your message here... 🎯",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chat-bubble">', unsafe_allow_html=True)
        st.markdown('### 🌐 Languages')
        
        available_languages = get_available_languages()
        selected_language = st.selectbox(
            "Choose language",
            available_languages,
            index=0,
            label_visibility="collapsed"
        )
        
        # # Language modules
        # st.markdown('**Available Languages:**')
        # st.markdown('🇫🇷 French · 🇪🇸 Spanish · 🇩🇪 German · 🇯🇵 Japanese · 🇨🇳 Chinese')
        # st.markdown('</div>', unsafe_allow_html=True)
    
    # Translate button
    if st.button(
        "🚀 Activate Translation!", 
        type="primary",
        disabled=not input_text or not input_text.strip(),
        use_container_width=True
    ):
        if input_text and input_text.strip():
            with st.spinner('🤖 Robot is processing...'):
                result = get_translation(input_text, selected_language, selected_model)
            
            if result.get("status") in ["success", "partial_success"]:
                if result.get("status") == "partial_success":
                    st.warning("Using backup translation systems! 🔄")
                
                st.markdown('### ✅ Translation Complete!')
                
                # Display output in robot bubble
                translation = result.get("output", "")
                st.markdown(f'<div class="robot-bubble">{translation}</div>', unsafe_allow_html=True)
                
                # Audio playback
                if enable_audio:
                    audio_file = text_to_speech(translation, selected_language)
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                        st.info("🔊 Robot voice generated!")
            
            elif result.get("status") == "error":
                st.error("Robot malfunction! Please try again 🔧")
                st.info("Check your connection and try again soon!")
    
    # Simple footer
    st.markdown('<div class="robot-footer">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #3a56e6; 
                font-weight: 600; font-family: 'Fredoka', sans-serif; position: relative; 
                bottom: 0; width: 100%;">
        <p style="margin-bottom: 0.5rem;">Powered by RoboTranslate Technology</p>
        <p style="font-size: 1.2rem; margin: 0;">🤖 💬 🌍 🔊</p>
    </div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    render_header()
    selected_model, enable_audio = render_sidebar()
    render_main_content(selected_model, enable_audio)

if __name__ == "__main__":
    main()
