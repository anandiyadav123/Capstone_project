import streamlit as st

st.set_page_config(
    page_title="Real Estate Analytics Hub",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .feature-description {
        font-size: 1rem;
        color: #333;
        line-height: 1.6;
    }
    .highlight-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #2196f3;
        margin: 1rem 0;
    }
    .step-box {
        background-color: #f1f8e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🏠 Real Estate Analytics Hub</h1>', unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="highlight-box">
    <h3>🎯 Welcome to Your Complete Real Estate Analytics Solution!</h3>
    <p>This platform provides three powerful tools to help you make informed real estate decisions in Gurgaon. 
    Whether you're buying, selling, or just exploring the market, we've got you covered with data-driven insights.</p>
</div>
""", unsafe_allow_html=True)

# Feature 1: Price Predictor
st.markdown("""
<div class="feature-card">
    <div class="feature-title">💰 Price Predictor</div>
    <div class="feature-description">
        <strong>What it does:</strong> Predicts property prices based on your specific requirements using advanced machine learning models.
        <br><br>
        <strong>Perfect for:</strong> Buyers who want to know if a property is fairly priced, sellers who want to set competitive prices, and investors analyzing market value.
        <br><br>
        <strong>How to use:</strong>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="step-box">
    <strong>Step 1:</strong> Select your property type (House/Flat)
</div>
<div class="step-box">
    <strong>Step 2:</strong> Choose the sector/location in Gurgaon
</div>
<div class="step-box">
    <strong>Step 3:</strong> Enter property details (bedrooms, bathrooms, area, etc.)
</div>
<div class="step-box">
    <strong>Step 4:</strong> Click "Predict Price" to get a price range estimate
</div>
""", unsafe_allow_html=True)

# Feature 2: Analysis Dashboard
st.markdown("""
<div class="feature-card">
    <div class="feature-title">📊 Analysis Dashboard</div>
    <div class="feature-description">
        <strong>What it does:</strong> Interactive visualizations and analytics to explore market trends, property distributions, and price patterns across different sectors.
        <br><br>
        <strong>Perfect for:</strong> Market research, understanding price trends, comparing different areas, and getting insights into property characteristics.
        <br><br>
        <strong>Key Features:</strong>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="step-box">
        🗺️ <strong>Interactive Map:</strong> Visualize average prices by sector
    </div>
    <div class="step-box">
        📈 <strong>Scatter Plots:</strong> Area vs Price analysis
    </div>
    <div class="step-box">
        🥧 <strong>Distribution Charts:</strong> Bedroom and property type analysis
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-box">
        🔤 <strong>Word Clouds:</strong> Feature frequency visualization
    </div>
    <div class="step-box">
        📊 <strong>Box Plots:</strong> Price distribution by bedroom count
    </div>
    <div class="step-box">
        🔗 <strong>Correlation Matrix:</strong> Feature relationships
    </div>
    """, unsafe_allow_html=True)

# Feature 3: Recommendation System
st.markdown("""
<div class="feature-card">
    <div class="feature-title">🎯 Property Recommendations</div>
    <div class="feature-description">
        <strong>What it does:</strong> Finds similar properties and recommends apartments based on location preferences and property characteristics.
        <br><br>
        <strong>Perfect for:</strong> Buyers looking for alternatives, investors exploring similar properties, and anyone wanting to discover new options.
        <br><br>
        <strong>Two Powerful Tools:</strong>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="step-box">
        <strong>📍 Location-Based Search:</strong>
        <br>• Select any location in Gurgaon
        <br>• Set your preferred radius (in km)
        <br>• Find all properties within that area
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-box">
        <strong>🤖 AI Recommendations:</strong>
        <br>• Choose any property as reference
        <br>• Get similar properties based on features
        <br>• Adjust similarity threshold
    </div>
    """, unsafe_allow_html=True)

# Getting Started Section
st.markdown("## 🚀 Getting Started")
st.markdown("""
<div class="highlight-box">
    <h4>Quick Start Guide:</h4>
    <ol>
        <li><strong>For Price Prediction:</strong> Use the "Price Predictor" page to estimate property values</li>
        <li><strong>For Market Analysis:</strong> Explore the "Analysis Dashboard" to understand trends and patterns</li>
        <li><strong>For Property Discovery:</strong> Try the "Recommendations" page to find similar properties</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Data Information
st.markdown("## 📋 About Our Data")
st.markdown("""
<div class="feature-card">
    <div class="feature-description">
        <strong>Data Source:</strong> Comprehensive real estate data from Gurgaon, including:
        <br>• Property details (type, size, bedrooms, bathrooms)
        <br>• Location information (sector, coordinates)
        <br>• Pricing data and market trends
        <br>• Property features (furnishing, age, amenities)
        <br><br>
        <strong>Model Accuracy:</strong> Our machine learning models are trained on extensive historical data to provide reliable price predictions and recommendations.
    </div>
</div>
""", unsafe_allow_html=True)

# Tips Section
st.markdown("## 💡 Pro Tips")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="step-box">
        <strong>🔍 For Best Results:</strong>
        <br>• Use multiple tools together
        <br>• Compare predictions with market analysis
        <br>• Check recommendations for validation
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-box">
        <strong>📱 Mobile Friendly:</strong>
        <br>• Works great on all devices
        <br>• Interactive charts and maps
        <br>• Easy navigation
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-box">
        <strong>🔄 Real-time Updates:</strong>
        <br>• Filters update instantly
        <br>• Dynamic visualizations
        <br>• Responsive interface
    </div>
    """, unsafe_allow_html=True)

# Navigation Guide
st.markdown("## 🧭 Navigation Guide")
st.markdown("""
<div class="highlight-box">
    <p><strong>Use the sidebar on the left to navigate between different features:</strong></p>
    <ul>
        <li><strong>💰 Price Predictor:</strong> Get property price estimates</li>
        <li><strong>📊 Analysis Dashboard:</strong> Explore market data and trends</li>
        <li><strong>🎯 Recommendations:</strong> Find similar properties and location-based searches</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🏠 Real Estate Analytics Hub | Powered by Machine Learning & Data Science</p>
    <p>Get started by selecting a feature from the sidebar above! 👆</p>
</div>
""", unsafe_allow_html=True)