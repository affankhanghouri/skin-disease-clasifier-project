import streamlit as st
import requests
import json
from PIL import Image
import io
import pandas as pd
from datetime import datetime
import time
import numpy as np


# note : THis code is CLAUDE GENERATED 


# Frontend optimized for smooth aesthetics
st.set_page_config(
    page_title="🧬 AI Dermatology Studio",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Refined CSS with smooth aesthetics and better color harmony
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 300% 300%;
        animation: gentleFlow 20s ease-in-out infinite;
    }
    
    @keyframes gentleFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes smoothPulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.02); opacity: 1; }
    }
    
    @keyframes smoothFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes slideIn {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes softGlow {
        0%, 100% { box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 12px 48px rgba(102, 126, 234, 0.5); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp > div:first-child {background: transparent !important;}
    
    /* Glass morphism containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideIn 0.6s ease-out;
    }
    
    .glass-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border-color: rgba(255, 255, 255, 0.25);
    }
    
    /* Hero section with elegant typography */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #ffffff, #f0f9ff, #e0f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1.5rem 0;
        animation: smoothFloat 8s ease-in-out infinite;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.85);
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Refined prediction card */
    .prediction-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(76, 175, 254, 0.9));
        backdrop-filter: blur(20px);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: smoothPulse 3s ease-in-out infinite;
    }
    
    /* Smooth confidence indicators */
    .confidence-high {
        background: linear-gradient(135deg, #10b981, #059669);
        padding: 1.2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        animation: softGlow 3s ease-in-out infinite;
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        padding: 1.2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        animation: smoothPulse 3s ease-in-out infinite;
    }
    
    .confidence-low {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        padding: 1.2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
        animation: smoothPulse 2.5s ease-in-out infinite;
    }
    
    /* Elegant buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #4facfe) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 25px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #4facfe, #667eea) !important;
    }
    
    /* Status indicators */
    .status-online {
        background: linear-gradient(135deg, #10b981, #059669);
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        animation: smoothPulse 2s ease-in-out infinite;
    }
    
    .status-offline {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
        animation: smoothPulse 1.5s ease-in-out infinite;
    }
    
    /* Metric cards with subtle 3D effect */
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.8rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Smooth loading animation */
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid #4facfe;
        border-radius: 50%;
        animation: spin 1.2s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #4facfe, #f093fb) !important;
        border-radius: 8px !important;
        height: 12px !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed rgba(255, 255, 255, 0.4) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(79, 172, 254, 0.8) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #4facfe);
        border-radius: 10px;
    }
    
    /* Success animation */
    .success-pulse {
        animation: successPulse 0.6s ease-out;
    }
    
    @keyframes successPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1rem; }
        .glass-container { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Configuration
API_URL = "http://localhost:8000"

# Disease information with refined styling
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
    """Check if API is running"""
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
    """Send image to API for prediction"""
    try:
        files = {"file": image_file}
        response = requests.post(f"{API_URL}/predict", files=files, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Connection Error: {str(e)}"}

def create_confidence_chart(predictions_dict):
    """Create smooth confidence visualization"""
    df = pd.DataFrame([
        {"Disease": disease, "Confidence": confidence * 100} 
        for disease, confidence in predictions_dict.items()
    ])
    
    df = df.head(5).sort_values('Confidence', ascending=True)
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df["Confidence"],
            y=df["Disease"],
            orientation='h',
            marker=dict(
                color=df["Confidence"],
                colorscale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']],
                showscale=False,
                line=dict(color='rgba(255,255,255,0.6)', width=1)
            ),
            text=[f'{conf:.1f}%' for conf in df["Confidence"]],
            textposition='auto',
            textfont=dict(size=11, color='white', family='Inter')
        ))
        
        fig.update_layout(
            title=dict(
                text="🎯 Confidence Analysis",
                font=dict(size=20, color='white', family='Inter'),
                x=0.5
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Inter'),
            height=350,
            showlegend=False,
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                title=dict(text='Confidence (%)', font=dict(color='white')),
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(color='white')
            ),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        return fig
    else:
        return df

def smooth_progress():
    """Create smooth progress animation"""
    progress = st.empty()
    bar = progress.progress(0)
    
    for i in range(101):
        time.sleep(0.015)
        bar.progress(i)
    
    time.sleep(0.3)
    progress.empty()

def main():
    # Initialize session state
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    # Hero Section
    st.markdown("""
    <div class="glass-container">
        <div class="hero-title">🧬 AI Dermatology Studio</div>
        <div class="hero-subtitle">Advanced AI-Powered Skin Analysis • EfficientNet-B3 Deep Learning</div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status Check
    api_status, api_info = check_api_health()
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("### 🚀 System Status")
        
        if api_status:
            st.markdown('<div class="status-online">🟢 API Connected</div>', unsafe_allow_html=True)
            if api_info:
                st.success(f"🔥 Model: {api_info.get('Model loaded', 'Unknown')}")
        else:
            st.markdown('<div class="status-offline">🔴 API Offline</div>', unsafe_allow_html=True)
            st.error("Please start the FastAPI server")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sidebar info
        st.markdown("""
        <div class="glass-container">
            <h3>🧠 About This AI</h3>
            <p style="color: rgba(255,255,255,0.85); line-height: 1.5;">
            Advanced EfficientNet-B3 architecture providing professional-grade skin analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-container">
            <h3>⚠️ Medical Disclaimer</h3>
            <p style="color: #f59e0b; line-height: 1.4;">
            For educational purposes only. Always consult healthcare professionals.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if not api_status:
        st.stop()
    
    # Main Analysis Section
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload & Analyze")
        
        uploaded_file = st.file_uploader(
            "Choose a skin image...",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear, well-lit image for AI analysis"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="📸 Uploaded Image", use_container_width=True)
            
            # Image details
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <strong>File:</strong> {uploaded_file.name}<br>
                <strong>Size:</strong> {image.size[0]} × {image.size[1]} pixels
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tips section
        st.markdown("""
        <div class="glass-container">
            <h3>💡 Tips for Best Results</h3>
            <div style="color: rgba(255,255,255,0.85); line-height: 1.6;">
                🔆 Use natural or bright lighting<br>
                📏 Focus on the affected area<br>
                📱 Keep camera steady<br>
                🎯 Fill frame with condition<br>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Analysis")
        
        if uploaded_file is not None:
            if st.button("🔬 Analyze Image", type="primary", use_container_width=True):
                st.markdown("""
                <div style="text-align: center; padding: 2rem;">
                    <div class="loading-spinner"></div>
                    <p style="color: white; margin-top: 1rem;">Analyzing image...</p>
                </div>
                """, unsafe_allow_html=True)
                
                smooth_progress()
                
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
                    
                    # Main prediction display
                    confidence_class = "confidence-high" if confidence >= 0.8 else "confidence-medium" if confidence >= 0.5 else "confidence-low"
                    st.markdown(f'''
                    <div class="{confidence_class} success-pulse">
                        <h2 style="font-size: 2rem; margin-bottom: 1rem;">🎯 Diagnosis</h2>
                        <h1 style="font-size: 2.5rem; margin: 1rem 0;">{predicted_class}</h1>
                        <h2 style="font-size: 1.8rem;">📊 {confidence:.1%} Confidence</h2>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Confidence interpretation
                    if confidence >= 0.8:
                        st.success("✅ High confidence prediction")
                    elif confidence >= 0.5:
                        st.warning("⚠️ Medium confidence - consider professional consultation")
                    else:
                        st.error("❌ Low confidence - professional evaluation recommended")
                    
                    st.balloons()
                    
                else:
                    st.error("❌ Analysis failed. Please try again.")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.7);">
                <h3>👆 Upload an image to begin</h3>
                <p>Our AI will analyze your skin condition instantly</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Results Section
    if hasattr(st.session_state, 'prediction_history') and st.session_state.prediction_history:
        latest_prediction = st.session_state.prediction_history[-1]
        
        st.markdown("---")
        st.markdown("""
        <div class="glass-container">
            <h1 style="text-align: center; color: white; font-size: 2rem; margin-bottom: 1.5rem;">
                📊 Analysis Results
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Three-column layout
        col1, col2, col3 = st.columns([1, 1, 1], gap="large")
        
        with col1:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            
            # Confidence chart
            chart_data = create_confidence_chart(latest_prediction["all_predictions"])
            
            if PLOTLY_AVAILABLE and hasattr(chart_data, 'update_layout'):
                st.plotly_chart(chart_data, use_container_width=True)
            else:
                st.markdown("### 📊 Predictions")
                if isinstance(chart_data, pd.DataFrame):
                    for _, row in chart_data.iterrows():
                        st.markdown(f"""
                        <div class="metric-card">
                            <strong>{row['Disease']}</strong><br>
                            <span style="font-size: 1.3rem; color: #4facfe;">{row['Confidence']:.1f}%</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("### 🏆 Top 3 Predictions")
            
            colors = ["#10b981", "#f59e0b", "#ef4444"]
            
            for i, (disease, conf) in enumerate(list(latest_prediction["all_predictions"].items())[:3]):
                st.markdown(f"""
                <div class="metric-card" style="border: 2px solid {colors[i]};">
                    <h4 style="color: white;">{disease}</h4>
                    <h2 style="color: {colors[i]}; font-size: 2rem;">{conf:.1%}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.markdown("### 📚 Medical Info")
            
            predicted_class = latest_prediction["predicted_class"]
            if predicted_class in DISEASE_INFO:
                info = DISEASE_INFO[predicted_class]
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px;">
                    <h4 style="color: white;">{info['emoji']} {predicted_class}</h4>
                    <p style="color: rgba(255,255,255,0.85);">{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Symptoms:**")
                for symptom in info["symptoms"]:
                    st.markdown(f"• {symptom}")
                
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis timestamp
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 15px; margin: 1rem 0;">
            <p style="color: rgba(255,255,255,0.7);">
                ⏰ Analysis: {latest_prediction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}<br>
                📄 File: {latest_prediction['filename']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: rgba(0,0,0,0.2); border-radius: 20px; margin: 2rem 0;'>
        <h3 style='color: white; margin-bottom: 1rem;'>🧬 AI Dermatology Studio</h3>
        <p style='color: rgba(255,255,255,0.8); margin-bottom: 1rem;'>
            Powered by EfficientNet-B3 • Built with Streamlit & FastAPI
        </p>
        <div style='background: linear-gradient(135deg, #ef4444, #f59e0b); padding: 1rem; border-radius: 15px;'>
            <strong style='color: white;'>⚠️ MEDICAL DISCLAIMER</strong><br>
            <span style='color: white;'>Educational purposes only. Consult healthcare professionals for medical advice.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()