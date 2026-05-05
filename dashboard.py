"""
Weather Forecast Dashboard - Streamlit Web Application
Interactive dashboard for weather monitoring and alerts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.weather_api import WeatherAPI
from src.alert_system import AlertSystem
from src.report_generator import ReportGenerator
from src.simulation import WeatherSimulator

# Page configuration
st.set_page_config(
    page_title="Weather Forecast Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .alert-critical {
        background-color: #ff6b6b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background-color: #ffd93d;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-info {
        background-color: #6c5ce7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'weather_api' not in st.session_state:
        st.session_state.weather_api = WeatherAPI()
    if 'alert_system' not in st.session_state:
        st.session_state.alert_system = AlertSystem()
    if 'report_gen' not in st.session_state:
        st.session_state.report_gen = ReportGenerator()
    if 'simulator' not in st.session_state:
        st.session_state.simulator = WeatherSimulator()
    if 'current_weather' not in st.session_state:
        st.session_state.current_weather = None
    if 'forecast' not in st.session_state:
        st.session_state.forecast = None
    if 'selected_city' not in st.session_state:
        st.session_state.selected_city = "London"

def get_city_list():
    """Get list of popular cities"""
    return [
        "London", "New York", "Tokyo", "Paris", "Sydney", 
        "Mumbai", "Dubai", "Singapore", "Berlin", "Toronto",
        "Los Angeles", "Chicago", "Shanghai", "Hong Kong", "Moscow"
    ]

def display_current_weather_card(weather_data):
    """Display current weather in a beautiful card format"""
    if not weather_data:
        st.warning("No weather data available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌡️ Temperature",
            value=f"{weather_data.get('temperature', 'N/A')}°C",
            delta=f"Feels like {weather_data.get('feels_like', 'N/A')}°C"
        )
    
    with col2:
        st.metric(
            label="💧 Humidity",
            value=f"{weather_data.get('humidity', 'N/A')}%",
            delta=None
        )
    
    with col3:
        st.metric(
            label="💨 Wind Speed",
            value=f"{weather_data.get('wind_speed', 'N/A')} m/s",
            delta=None
        )
    
    with col4:
        st.metric(
            label="🎯 Pressure",
            value=f"{weather_data.get('pressure', 'N/A')} hPa",
            delta=None
        )
    
    # Weather description
    st.info(f"🌤️ Conditions: {weather_data.get('description', 'N/A').title()}")
    
    if weather_data.get('rain', 0) > 0:
        st.warning(f"☔ Rainfall: {weather_data.get('rain', 0)} mm in last 3 hours")

def display_forecast_charts(forecast_data):
    """Display forecast charts using Plotly"""
    if not forecast_data:
        st.warning("No forecast data available")
        return
    
    df = pd.DataFrame(forecast_data)
    
    # Temperature Chart
    st.subheader("📈 Temperature Forecast")
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=df['date'], y=df['temp_max'],
        mode='lines+markers', name='Max Temp',
        line=dict(color='red', width=2)
    ))
    fig_temp.add_trace(go.Scatter(
        x=df['date'], y=df['temp_min'],
        mode='lines+markers', name='Min Temp',
        line=dict(color='blue', width=2)
    ))
    fig_temp.add_trace(go.Scatter(
        x=df['date'], y=df['temp_avg'],
        mode='lines+markers', name='Avg Temp',
        line=dict(color='green', width=2, dash='dash')
    ))
    fig_temp.update_layout(
        title="Temperature Trends (5 Days)",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Rainfall Chart
    st.subheader("☔ Rainfall Forecast")
    fig_rain = go.Figure()
    fig_rain.add_trace(go.Bar(
        x=df['date'], y=df['rain_mm'],
        name='Rainfall',
        marker_color='lightblue',
        text=df['rain_mm'].round(1),
        textposition='auto'
    ))
    fig_rain.update_layout(
        title="Rainfall Prediction",
        xaxis_title="Date",
        yaxis_title="Rainfall (mm)",
        height=400
    )
    st.plotly_chart(fig_rain, use_container_width=True)
    
    # Humidity Chart
    st.subheader("💧 Humidity Forecast")
    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(
        x=df['date'], y=df['humidity_avg'],
        mode='lines+markers', name='Humidity',
        fill='tozeroy',
        line=dict(color='purple', width=2)
    ))
    fig_hum.add_hline(y=70, line_dash="dash", line_color="red", 
                      annotation_text="High Humidity Warning")
    fig_hum.update_layout(
        title="Humidity Trends",
        xaxis_title="Date",
        yaxis_title="Humidity (%)",
        height=400
    )
    st.plotly_chart(fig_hum, use_container_width=True)

def display_alerts_section(alerts, recommendations):
    """Display alerts and recommendations"""
    if not alerts:
        st.success("✅ No active alerts! Weather conditions are normal.")
        return
    
    st.subheader("🚨 Active Weather Alerts")
    
    for alert in alerts:
        severity = alert.get('severity', 'info')
        message = alert.get('message', 'Alert')
        
        if severity == 'critical':
            st.error(f"🔴 CRITICAL: {message}")
        elif severity == 'warning':
            st.warning(f"⚠️ WARNING: {message}")
        else:
            st.info(f"ℹ️ INFO: {message}")
    
    if recommendations:
        st.subheader("💡 Recommendations")
        for rec in recommendations:
            st.write(f"• {rec}")

def display_side_panel():
    """Display sidebar with additional info"""
    with st.sidebar:
        st.markdown("## 📊 Dashboard Controls")
        
        # City selection
        city_list = get_city_list()
        selected_city = st.selectbox(
            "🌍 Select City",
            city_list,
            index=city_list.index(st.session_state.selected_city) if st.session_state.selected_city in city_list else 0
        )
        
        if selected_city != st.session_state.selected_city:
            st.session_state.selected_city = selected_city
            st.session_state.current_weather = None
            st.session_state.forecast = None
        
        # Fetch button
        if st.button("🔄 Refresh Weather Data", use_container_width=True):
            with st.spinner(f"Fetching weather data for {selected_city}..."):
                st.session_state.current_weather = st.session_state.weather_api.get_current_weather(selected_city)
                st.session_state.forecast = st.session_state.weather_api.get_forecast(selected_city, 5)
            st.success("Data refreshed!")
        
        st.markdown("---")
        
        # Report generation
        st.markdown("## 📁 Generate Reports")
        if st.button("📊 Save Current Data to CSV", use_container_width=True):
            if st.session_state.current_weather:
                st.session_state.report_gen.save_current_weather_csv(st.session_state.current_weather)
                st.success("Current weather saved to data/ folder!")
            else:
                st.warning("No weather data available")
        
        if st.button("📈 Save Forecast to CSV", use_container_width=True):
            if st.session_state.forecast:
                st.session_state.report_gen.save_forecast_csv(st.session_state.forecast)
                st.success("Forecast saved to data/ folder!")
            else:
                st.warning("No forecast data available")
        
        if st.button("📸 Generate Charts", use_container_width=True):
            if st.session_state.forecast:
                st.session_state.report_gen.create_temperature_chart(st.session_state.forecast)
                st.session_state.report_gen.create_rain_chart(st.session_state.forecast)
                st.session_state.report_gen.create_humidity_chart(st.session_state.forecast)
                st.success("Charts saved to outputs/ folder!")
            else:
                st.warning("No forecast data available")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Weather Forecast & Alert Application**
        
        Features:
        - Real-time weather data
        - 5-day forecast
        - Automated alerts
        - Data export to CSV
        - Visual charts
        """)

def main():
    """Main dashboard function"""
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">🌤️ Weather Forecast & Alert Dashboard</div>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    display_side_panel()
    
    # Main content area
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## 📍 Weather for {st.session_state.selected_city}")
    
    with col2:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"**Last Updated:** {current_time}")
    
    with col3:
        # Check simulation mode
        if st.session_state.weather_api.simulation_mode:
            st.info("🎮 Simulation Mode")
    
    # Fetch data if not available
    if st.session_state.current_weather is None:
        with st.spinner(f"Loading weather data for {st.session_state.selected_city}..."):
            st.session_state.current_weather = st.session_state.weather_api.get_current_weather(st.session_state.selected_city)
            st.session_state.forecast = st.session_state.weather_api.get_forecast(st.session_state.selected_city, 5)
    
    # Display current weather
    if st.session_state.current_weather:
        display_current_weather_card(st.session_state.current_weather)
    
    st.markdown("---")
    
    # Generate alerts
    if st.session_state.current_weather and st.session_state.forecast:
        alerts = st.session_state.alert_system.check_current_weather(st.session_state.current_weather)
        forecast_alerts = st.session_state.alert_system.check_forecast(st.session_state.forecast)
        all_alerts = alerts + forecast_alerts
        recommendations = st.session_state.alert_system.get_alert_recommendations(all_alerts)
        
        # Display alerts
        display_alerts_section(all_alerts, recommendations)
        
        st.markdown("---")
        
        # Display forecast charts
        display_forecast_charts(st.session_state.forecast)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Weather Forecast & Alert Application | Powered by OpenWeatherMap API"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()