import streamlit as st
import requests
import json
from PIL import Image
import io
import pandas as pd
from datetime import datetime
import time
import numpy as np

# Page configuration - MUST be first
st.set_page_config(
    page_title="🧬 AI Dermatology Studio",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import plotly, fall back gracefully if not available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Advanced CSS with modern design, animations, and glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.8), 0 0 60px rgba(118, 75, 162, 0.6); }
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Override Streamlit defaults */
    .stApp > div:first-child {
        background: transparent !important;
    }
    
    /* Main container with glassmorphism */
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Hero header with 3D text effect */
    .hero-header {
        font-family: 'Inter', sans-serif;
        font-size: 4.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
        margin: 2rem 0;
        text-shadow: 0 10px 20px rgba(0,0,0,0.3);
        animation: float 6s ease-in-out infinite;
        position: relative;
    }
    
    .hero-header::before {
        content: '🧬 AI DERMATOLOGY STUDIO';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Premium prediction card */
    .prediction-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        animation: pulse 4s ease-in-out infinite;
    }
    
    .prediction-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, rgba(255,255,255,0.1), transparent);
        animation: rotate 4s linear infinite;
    }
    
    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }
    
    .prediction-content {
        position: relative;
        z-index: 2;
    }
    
    /* Confidence indicators with neon effect */
    .confidence-high {
        background: linear-gradient(135deg, #00f260, #0575e6);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 242, 96, 0.5);
        border: 2px solid rgba(5, 117, 230, 0.6);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, #ff9a56, #ffad56);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 154, 86, 0.5);
        animation: pulse 3s ease-in-out infinite;
    }
    
    .confidence-low {
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Interactive buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 50px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #764ba2, #667eea) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    /* Metric cards with 3D effect */
    .metric-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: rotateX(10deg) rotateY(10deg) translateZ(20px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
    }
    
    /* Loading animations */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 6px solid rgba(255, 255, 255, 0.3);
        border-top: 6px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
        border-radius: 10px !important;
        height: 15px !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed rgba(255, 255, 255, 0.5) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(102, 126, 234, 0.8) !important;
        background: rgba(255, 255, 255, 0.2) !important;
        transform: scale(1.02) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    /* Status indicators */
    .status-connected {
        background: linear-gradient(135deg, #00f260, #0575e6);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(0, 242, 96, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .status-disconnected {
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.4);
        animation: pulse 1s ease-in-out infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-header {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1rem;
        }
        
        .glass-card {
            padding: 1rem;
        }
    }
    
    /* Chart container */
    .chart-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Success animations */
    .success-animation {
        animation: successPulse 0.6s ease-out;
    }
    
    @keyframes successPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_URL = "http://localhost:8000"

# Enhanced disease information with emojis
DISEASE_INFO = {
    "Eczeme": {
        "description": "A condition that makes your skin red and itchy. It's common in children but can occur at any age.",
        "symptoms": ["Dry skin", "Itching", "Red to brownish-gray patches", "Small raised bumps"],
        "treatment": "Moisturizers, topical corticosteroids, antihistamines",
        "emoji": "🔴",
        "severity": "Moderate"
    },
    "Melanoma": {
        "description": "The most serious type of skin cancer. Develops in melanocytes (cells that produce melanin).",
        "symptoms": ["Asymmetrical moles", "Border irregularities", "Color changes", "Diameter > 6mm"],
        "treatment": "Surgical removal, immunotherapy, targeted therapy, chemotherapy",
        "emoji": "⚫",
        "severity": "High"
    },
    "Atopic Dermatits": {
        "description": "A type of eczema that makes skin red and itchy. Most common in children.",
        "symptoms": ["Dry, cracked skin", "Intense itching", "Red or brownish patches", "Small bumps"],
        "treatment": "Moisturizers, topical medications, oral medications, light therapy",
        "emoji": "🔴",
        "severity": "Moderate"
    },
    "Basal Cell Cercinoma": {
        "description": "A type of skin cancer that begins in the basal cells. Most common form of skin cancer.",
        "symptoms": ["Pearly white bump", "Brown/black lesion", "Flat, scaly patch", "Waxy scar-like lesion"],
        "treatment": "Surgical excision, Mohs surgery, radiation therapy, topical medications",
        "emoji": "🟤",
        "severity": "High"
    },
    "Melanocytic Nevi": {
        "description": "Commonly known as moles. Usually benign growths of melanocytes.",
        "symptoms": ["Brown or black spots", "Uniform color", "Regular borders", "Stable over time"],
        "treatment": "Usually no treatment needed, monitor for changes, surgical removal if suspicious",
        "emoji": "🤎",
        "severity": "Low"
    },
    "Benign keratosis like lesions": {
        "description": "Non-cancerous skin growths that appear as the skin ages.",
        "symptoms": ["Waxy, scaly patches", "Brown, black or light colored", "Raised appearance"],
        "treatment": "Usually no treatment needed, removal for cosmetic reasons",
        "emoji": "🟫",
        "severity": "Low"
    },
    "Psorisis / Lichen planus / related": {
        "description": "Autoimmune conditions causing skin cell buildup and inflammation.",
        "symptoms": ["Red patches with silvery scales", "Dry, cracked skin", "Itching or burning"],
        "treatment": "Topical treatments, light therapy, systemic medications",
        "emoji": "🔴",
        "severity": "Moderate"
    },
    "Seborrheic Keratoses / other Benign Tumors": {
        "description": "Common, benign skin growths that appear as people age.",
        "symptoms": ["Waxy, scaly appearance", "Brown, black or tan color", "Stuck-on appearance"],
        "treatment": "Usually no treatment needed, removal for cosmetic or comfort reasons",
        "emoji": "🟫",
        "severity": "Low"
    },
    "Tinea Ringworm Candidias and other Fungal Infections": {
        "description": "Fungal infections of the skin, hair, or nails.",
        "symptoms": ["Ring-shaped rash", "Itchy, scaly skin", "Red, inflamed areas"],
        "treatment": "Antifungal medications (topical or oral), keeping area clean and dry",
        "emoji": "🟡",
        "severity": "Moderate"
    },
    "Warts Molluscum and other Viral Infections": {
        "description": "Viral infections causing skin growths or lesions.",
        "symptoms": ["Small, raised bumps", "Rough texture", "May spread to other areas"],
        "treatment": "May resolve on their own, cryotherapy, topical treatments, surgical removal",
        "emoji": "🔵",
        "severity": "Low"
    }
}

def check_api_health():
    """Check if API is running with enhanced error handling"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)

def get_disease_classes():
    """Get available disease classes from API"""
    try:
        response = requests.get(f"{API_URL}/classes", timeout=5)
        if response.status_code == 200:
            return response.json().get("classes", [])
        return []
    except:
        return []

def predict_image(image_file):
    """Send image to API for prediction with enhanced error handling"""
    try:
        files = {"file": image_file}
        response = requests.post(f"{API_URL}/predict", files=files, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Connection Error: {str(e)}"}

def create_confidence_visualization(predictions_dict):
    """Create stunning confidence visualization"""
    df = pd.DataFrame([
        {"Disease": disease, "Confidence": confidence * 100, "Color": f"hsl({i*36}, 70%, 60%)"} 
        for i, (disease, confidence) in enumerate(predictions_dict.items())
    ])
    
    # Take top 6 predictions and sort
    df = df.head(6).sort_values('Confidence', ascending=True)
    
    if PLOTLY_AVAILABLE:
        # Create a beautiful polar chart
        fig = go.Figure()
        
        # Add bar chart
        fig.add_trace(go.Bar(
            x=df["Confidence"],
            y=df["Disease"],
            orientation='h',
            marker=dict(
                color=df["Confidence"],
                colorscale='Viridis',
                showscale=True,
                line=dict(color='rgba(255,255,255,0.8)', width=2)
            ),
            text=[f'{conf:.1f}%' for conf in df["Confidence"]],
            textposition='auto',
            textfont=dict(size=12, color='white', family='Inter')
        ))
        
        fig.update_layout(
            title=dict(
                text="🎯 Confidence Analysis",
                font=dict(size=24, color='white', family='Inter'),
                x=0.5
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            height=400,
            showlegend=False,
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.2)',
                title=dict(text='Confidence (%)', font=dict(color='white')),
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(color='white')
            ),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    else:
        return df

def get_confidence_class(confidence):
    """Get confidence class for styling"""
    if confidence >= 0.8:
        return "confidence-high"
    elif confidence >= 0.5:
        return "confidence-medium"
    else:
        return "confidence-low"

def create_animated_progress_bar():
    """Create an animated progress bar for loading"""
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(0)
    
    for i in range(101):
        time.sleep(0.02)
        progress_bar.progress(i)
    
    time.sleep(0.5)
    progress_placeholder.empty()

def main():
    # Initialize session state
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    # Hero Section
    st.markdown("""
    <div class="main-container">
        <div class="hero-header">🧬 AI DERMATOLOGY STUDIO</div>
        <div class="hero-subtitle">Revolutionary AI-Powered Skin Analysis • EfficientNet-B3 Deep Learning</div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status Check with enhanced UI
    api_status, api_info = check_api_health()
    
    # Sidebar with glass effect
    with st.sidebar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 System Status")
        
        if api_status:
            st.markdown('<div class="status-connected">🟢 API CONNECTED</div>', unsafe_allow_html=True)
            if api_info:
                st.success(f"🔥 Model: {api_info.get('Model loaded', 'Unknown')}")
                st.info(f"💻 Device: {api_info.get('device', 'Unknown')}")
        else:
            st.markdown('<div class="status-disconnected">🔴 API OFFLINE</div>', unsafe_allow_html=True)
            st.error("Please start the FastAPI server")
            st.code("python main.py", language="bash")
            st.code("uvicorn main:app --reload", language="bash")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced sidebar info
        st.markdown("""
        <div class="glass-card">
            <h3>🧠 About This AI</h3>
            <p>State-of-the-art EfficientNet-B3 architecture trained on thousands of dermatological images. 
            Our AI provides instant analysis with professional-grade accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h3>⚠️ Medical Disclaimer</h3>
            <p style="color: #ffaa44;">This AI is for educational purposes only. 
            Always consult qualified dermatologists for medical diagnosis and treatment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show supported conditions
        classes = get_disease_classes()
        if classes:
            st.markdown("""
            <div class="glass-card">
                <h3>🏷️ Supported Conditions</h3>
            """, unsafe_allow_html=True)
            for i, class_name in enumerate(classes, 1):
                emoji = DISEASE_INFO.get(class_name, {}).get("emoji", "📋")
                st.markdown(f"{emoji} {class_name}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    if not api_status:
        st.stop()
    
    # Main Analysis Section
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">📤 Upload & Analyze</h2>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a high-quality skin image...",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear, well-lit image of the skin condition for AI analysis"
        )
        
        if uploaded_file is not None:
            # Display uploaded image with enhanced styling
            image = Image.open(uploaded_file)
            st.image(image, caption="📸 Uploaded Image", use_container_width=True)
            
            # Enhanced image info
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: white;">📊 Image Details</h4>
                <p style="color: rgba(255,255,255,0.8);">
                    <strong>File:</strong> {uploaded_file.name}<br>
                    <strong>Resolution:</strong> {image.size[0]} × {image.size[1]} pixels<br>
                    <strong>Format:</strong> {image.format}<br>
                    <strong>Size:</strong> {len(uploaded_file.getvalue()) / 1024:.1f} KB
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tips section with enhanced styling
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; text-align: center;">💡 Pro Tips for Best Results</h3>
            <div style="color: rgba(255,255,255,0.9); line-height: 1.8;">
                🔆 Use natural lighting or bright indoor light<br>
                📏 Focus on the affected area with some surrounding skin<br>
                📱 Hold camera steady to avoid blur<br>
                🎯 Fill the frame with the skin condition<br>
                ⚡ Higher resolution images provide better accuracy
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">🤖 AI Analysis Engine</h2>
        """, unsafe_allow_html=True)
        
        if uploaded_file is not None:
            if st.button("🔬 ANALYZE WITH AI", type="primary", use_container_width=True):
                # Animated loading sequence
                st.markdown("""
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                </div>
                <p style="text-align: center; color: white; margin-top: 1rem;">
                    🧠 AI is analyzing your image...
                </p>
                """, unsafe_allow_html=True)
                
                # Progress animation
                create_animated_progress_bar()
                
                # Reset file pointer and predict
                uploaded_file.seek(0)
                result = predict_image(uploaded_file)
                
                if result and result.get("Success"):
                    prediction = result["prediction"]
                    predicted_class = prediction["predicted_class"]
                    confidence = prediction["confidence"]
                    all_predictions = prediction["all_predictions"]
                    
                    # Store in history
                    st.session_state.prediction_history.append({
                        "predicted_class": predicted_class,
                        "confidence": confidence,
                        "all_predictions": all_predictions,
                        "timestamp": datetime.now(),
                        "filename": uploaded_file.name
                    })
                    
                    # Main prediction display with stunning animation
                    confidence_class = get_confidence_class(confidence)
                    st.markdown(f'''
                    <div class="{confidence_class} success-animation">
                        <div class="prediction-content">
                            <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">🎯 DIAGNOSIS</h2>
                            <h1 style="font-size: 3rem; margin: 1rem 0;">{predicted_class}</h1>
                            <h2 style="font-size: 2rem;">📊 {confidence:.1%} CONFIDENCE</h2>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Confidence interpretation with enhanced styling
                    if confidence >= 0.8:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #00f260, #0575e6); padding: 1rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0; box-shadow: 0 0 30px rgba(0,242,96,0.5);">
                            ✅ <strong>HIGH CONFIDENCE PREDICTION</strong><br>
                            The AI is very confident in this diagnosis
                        </div>
                        """, unsafe_allow_html=True)
                    elif confidence >= 0.5:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #ff9a56, #ffad56); padding: 1rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0; box-shadow: 0 0 30px rgba(255,154,86,0.5);">
                            ⚠️ <strong>MEDIUM CONFIDENCE</strong><br>
                            Consider consulting a dermatologist for confirmation
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a6f); padding: 1rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0; box-shadow: 0 0 30px rgba(255,107,107,0.5);">
                            ❌ <strong>LOW CONFIDENCE</strong><br>
                            Professional medical evaluation strongly recommended
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Celebration effect
                    st.balloons()
                    
                else:
                    st.error("❌ Analysis failed. Please try again with a different image.")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.7);">
                <h3>👆 Upload an image to begin AI analysis</h3>
                <p>Our advanced AI will analyze your skin condition in seconds</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Results Section
    if hasattr(st.session_state, 'prediction_history') and st.session_state.prediction_history:
        latest_prediction = st.session_state.prediction_history[-1]
        
        st.markdown("---")
        st.markdown("""
        <div class="glass-card">
            <h1 style="text-align: center; color: white; font-size: 2.5rem; margin-bottom: 2rem;">
                📊 DETAILED ANALYSIS REPORT
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Three-column detailed analysis
        col1, col2, col3 = st.columns([1, 1, 1], gap="large")
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            # Confidence visualization
            chart_data = create_confidence_visualization(latest_prediction["all_predictions"])
            
            if PLOTLY_AVAILABLE and hasattr(chart_data, 'update_layout'):
                st.plotly_chart(chart_data, use_container_width=True)
            else:
                st.markdown("### 📊 Top Predictions")
                if isinstance(chart_data, pd.DataFrame):
                    for _, row in chart_data.iterrows():
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(102,126,234,0.3), rgba(118,75,162,0.3)); 
                                   padding: 1rem; margin: 0.5rem 0; border-radius: 10px; color: white;">
                            <strong>{row['Disease']}</strong><br>
                            <span style="font-size: 1.5rem; color: #4facfe;">{row['Confidence']:.1f}%</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🏆 Top 3 Predictions")
            
            rank_emojis = ["🥇", "🥈", "🥉"]
            colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
            
            for i, (disease, conf) in enumerate(list(latest_prediction["all_predictions"].items())[:3]):
                emoji = DISEASE_INFO.get(disease, {}).get("emoji", "📋")
                st.markdown(f"""
                <div class="metric-card" style="border: 2px solid {colors[i]}; background: linear-gradient(135deg, {colors[i]}20, {colors[i]}10);">
                    <h3 style="color: white; margin-bottom: 1rem;">{rank_emojis[i]} {emoji} {disease}</h3>
                    <h1 style="color: {colors[i]}; font-size: 2.5rem; margin: 0;">{conf:.1%}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📚 Medical Information")
            
            predicted_class = latest_prediction["predicted_class"]
            if predicted_class in DISEASE_INFO:
                info = DISEASE_INFO[predicted_class]
                severity_colors = {"High": "#ff6b6b", "Moderate": "#ffa726", "Low": "#66bb6a"}
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
                    <h4 style="color: white; margin-bottom: 1rem;">{info['emoji']} {predicted_class}</h4>
                    <div style="background: {severity_colors.get(info['severity'], '#666')}; padding: 0.5rem; border-radius: 8px; margin-bottom: 1rem; text-align: center;">
                        <strong>Severity: {info['severity']}</strong>
                    </div>
                    <p style="color: rgba(255,255,255,0.9); line-height: 1.6;">{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Symptoms
                st.markdown("**🔍 Common Symptoms:**")
                for symptom in info["symptoms"]:
                    st.markdown(f"• {symptom}", unsafe_allow_html=False)
                
                # Treatment
                st.markdown("**💊 Typical Treatment:**")
                st.markdown(f"_{info['treatment']}_")
                
            else:
                st.info("📝 Medical information not available for this condition.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis Summary Dashboard
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Analysis Dashboard")
        
        # Create 4 columns for metrics
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: rgba(255,255,255,0.7);">Primary Diagnosis</h4>
                <h2 style="color: white; margin: 0.5rem 0;">{latest_prediction['predicted_class']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[1]:
            confidence_color = "#00f260" if latest_prediction['confidence'] >= 0.8 else "#ffa726" if latest_prediction['confidence'] >= 0.5 else "#ff6b6b"
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: rgba(255,255,255,0.7);">Confidence Score</h4>
                <h2 style="color: {confidence_color}; margin: 0.5rem 0;">{latest_prediction['confidence']:.1%}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[2]:
            second_best = list(latest_prediction["all_predictions"].items())[1]
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: rgba(255,255,255,0.7);">Alternative</h4>
                <h3 style="color: white; margin: 0.5rem 0; font-size: 1rem;">{second_best[0]}</h3>
                <h4 style="color: #4facfe;">{second_best[1]:.1%}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[3]:
            severity = DISEASE_INFO.get(latest_prediction['predicted_class'], {}).get('severity', 'Unknown')
            severity_colors = {"High": "#ff6b6b", "Moderate": "#ffa726", "Low": "#66bb6a", "Unknown": "#666"}
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: rgba(255,255,255,0.7);">Severity Level</h4>
                <h3 style="color: {severity_colors[severity]}; margin: 0.5rem 0;">{severity}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis timestamp with enhanced styling
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 15px; margin: 2rem 0;">
            <p style="color: rgba(255,255,255,0.7); margin: 0;">
                ⏰ Analysis completed at: <strong>{latest_prediction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</strong><br>
                📄 File: <strong>{latest_prediction['filename']}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: rgba(0,0,0,0.2); border-radius: 20px; margin: 2rem 0;'>
        <h3 style='color: white; margin-bottom: 1rem;'>🧬 AI Dermatology Studio</h3>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-bottom: 1rem;'>
            Powered by EfficientNet-B3 Deep Learning • Built with Streamlit & FastAPI
        </p>
        <div style='background: linear-gradient(135deg, #ff6b6b, #ffa726); padding: 1rem; border-radius: 15px; margin-top: 1rem;'>
            <strong style='color: white; font-size: 1.2rem;'>⚠️ MEDICAL DISCLAIMER</strong><br>
            <span style='color: white;'>This AI tool is for educational and research purposes only. Always consult qualified healthcare professionals for medical diagnosis, treatment, and advice.</span>
        </div>
        <div style='margin-top: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;'>
            <p style='color: rgba(255,255,255,0.6); margin: 0; font-size: 0.9rem;'>
                🔬 Advanced AI • 🎯 Professional Accuracy • 🚀 Instant Results • 💡 Educational Tool
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()