#!/usr/bin/env python3
"""
Weather Forecast & Alert Application
Main entry point for the application

This application fetches weather data, generates alerts,
and creates reports for any city worldwide.
"""

import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.weather_api import WeatherAPI
from src.alert_system import AlertSystem
from src.report_generator import ReportGenerator
from src.simulation import WeatherSimulator

# Load environment variables
load_dotenv()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print application banner"""
    banner = """
    ============================================================
          WEATHER FORECAST & ALERT APPLICATION
          Real-time Weather | Forecast | Alerts | Reports
    ============================================================
    """
    print(banner)

def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("MAIN MENU")
    print("="*60)
    print("1. [CURRENT] Get Current Weather")
    print("2. [FORECAST] Get Weather Forecast (5 days)")
    print("3. [ALERTS] Check Weather Alerts")
    print("4. [REPORT] Generate Complete Report")
    print("5. [DEMO] Demo Mode (Pre-defined cities)")
    print("6. [INFO] About")
    print("0. [EXIT] Exit")
    print("="*60)

def display_current_weather(weather_data):
    """Display current weather information"""
    if not weather_data:
        print("\n[ERROR] No weather data available.")
        return
    
    print("\n" + "="*60)
    print(f"CURRENT WEATHER - {weather_data.get('city', 'Unknown')}")
    print("="*60)
    print(f"Temperature:      {weather_data.get('temperature', 'N/A')} C")
    print(f"Feels Like:       {weather_data.get('feels_like', 'N/A')} C")
    print(f"Humidity:         {weather_data.get('humidity', 'N/A')}%")
    print(f"Wind Speed:       {weather_data.get('wind_speed', 'N/A')} m/s")
    print(f"Pressure:         {weather_data.get('pressure', 'N/A')} hPa")
    print(f"Conditions:       {weather_data.get('description', 'N/A')}")
    
    if weather_data.get('rain', 0) > 0:
        print(f"Rainfall:         {weather_data.get('rain', 0)} mm")
    
    print(f"Last Updated:     {weather_data.get('timestamp', 'N/A')}")
    
    if weather_data.get('simulation', False):
        print("\n[NOTE] Using SIMULATED data (no API key detected)")
        print("       Get a free API key from: https://openweathermap.org/api")
    
    print("="*60)

def display_forecast(forecast_data):
    """Display forecast information"""
    if not forecast_data:
        print("\n[ERROR] No forecast data available.")
        return
    
    print("\n" + "="*60)
    print("5-DAY WEATHER FORECAST")
    print("="*60)
    
    for day in forecast_data:
        print(f"\n[Date: {day.get('date', 'Unknown Date')}]")
        print(f"   Max: {day.get('temp_max', 'N/A')}C | Min: {day.get('temp_min', 'N/A')}C | Avg: {day.get('temp_avg', 'N/A')}C")
        print(f"   Humidity: {day.get('humidity_avg', 'N/A')}%")
        print(f"   Rainfall: {day.get('rain_mm', 'N/A')} mm")
        print(f"   Conditions: {day.get('description', 'N/A')}")
    
    print("\n" + "="*60)

def display_alerts(alerts, recommendations):
    """Display alerts and recommendations"""
    if not alerts:
        print("\n[OK] No active alerts! Weather conditions are normal.")
        return
    
    print("\n" + "="*60)
    print("ACTIVE WEATHER ALERTS")
    print("="*60)
    
    for alert in alerts:
        severity = alert.get('severity', 'info')
        if severity == 'critical':
            print(f"[CRITICAL] {alert.get('message', 'Alert')}")
        elif severity == 'warning':
            print(f"[WARNING] {alert.get('message', 'Alert')}")
        else:
            print(f"[INFO] {alert.get('message', 'Alert')}")
    
    if recommendations:
        print("\n" + "="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        for rec in recommendations:
            print(f"  -> {rec}")
    
    print("="*60)

def demo_mode():
    """Run demo mode with pre-defined cities"""
    clear_screen()
    print_banner()
    
    print("\n[DEMO MODE] Showing weather for multiple cities\n")
    
    simulator = WeatherSimulator()
    alert_system = AlertSystem()
    report_gen = ReportGenerator()
    
    cities = simulator.get_all_cities()[:5]
    
    for city in cities:
        print(f"\n{'='*50}")
        print(f"LOCATION: {city}")
        print('='*50)
        
        # Get simulated weather
        weather = simulator.get_simulated_weather(city)
        forecast = simulator.get_simulated_forecast(city, 3)
        
        # Check alerts
        alerts = alert_system.check_current_weather(weather)
        forecast_alerts = alert_system.check_forecast(forecast)
        all_alerts = alerts + forecast_alerts
        
        # Display
        print(f"Temperature: {weather['temperature']}C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Conditions: {weather['description']}")
        
        if all_alerts:
            print("\n[ALERTS]")
            for alert in all_alerts[:2]:
                print(f"   -> {alert['message']}")
    
    print("\n" + "="*60)
    input("\nPress Enter to continue...")

def about():
    """Display about information"""
    clear_screen()
    print_banner()
    
    print("\n" + "="*60)
    print("ABOUT THIS APPLICATION")
    print("="*60)
    print("\nPROJECT: Weather Forecast & Alert Application")
    print("VERSION: 1.0.0")
    print("\nPURPOSE:")
    print("   Real-time weather monitoring and alert system for")
    print("   travelers, businesses, farmers, and general users.")
    print("\nFEATURES:")
    print("   -> Current weather conditions")
    print("   -> 5-day weather forecast")
    print("   -> Automated weather alerts (rain, heat, wind, etc.)")
    print("   -> CSV reports and charts")
    print("   -> Email notifications (optional)")
    print("\nTECH STACK:")
    print("   -> Python 3.8+")
    print("   -> Requests (API calls)")
    print("   -> Pandas (data processing)")
    print("   -> Matplotlib (charts)")
    print("   -> OpenWeatherMap API (or simulation)")
    print("\nOUTPUTS:")
    print("   -> CSV weather data files")
    print("   -> Temperature/Rain/Humidity charts")
    print("   -> Alert reports")
    print("   -> Complete weather reports")
    print("\n" + "="*60)
    input("\nPress Enter to continue...")

def main():
    """Main application loop"""
    
    # Initialize components
    weather_api = WeatherAPI()
    alert_system = AlertSystem()
    report_gen = ReportGenerator()
    
    current_weather = None
    current_forecast = None
    
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == '0':
            print("\n[EXIT] Thank you for using Weather Alert System!")
            print("Stay safe and weather-aware!")
            break
        
        elif choice == '1':  # Current Weather
            clear_screen()
            print_banner()
            city = input("\nEnter city name (e.g., London, New York): ").strip()
            
            if city:
                print(f"\n[FETCHING] Getting weather for {city}...")
                current_weather = weather_api.get_current_weather(city)
                display_current_weather(current_weather)
                
                # Option to save
                save = input("\nSave to CSV? (y/n): ").strip().lower()
                if save == 'y':
                    report_gen.save_current_weather_csv(current_weather)
            
            input("\nPress Enter to continue...")
        
        elif choice == '2':  # Forecast
            clear_screen()
            print_banner()
            city = input("\nEnter city name for forecast: ").strip()
            
            if city:
                print(f"\n[FETCHING] Getting 5-day forecast for {city}...")
                current_forecast = weather_api.get_forecast(city)
                display_forecast(current_forecast)
                
                # Option to save
                save = input("\nSave forecast to CSV? (y/n): ").strip().lower()
                if save == 'y':
                    report_gen.save_forecast_csv(current_forecast)
                    
                # Option to create charts
                chart = input("\nCreate weather charts? (y/n): ").strip().lower()
                if chart == 'y' and current_forecast:
                    report_gen.create_temperature_chart(current_forecast)
                    report_gen.create_rain_chart(current_forecast)
                    report_gen.create_humidity_chart(current_forecast)
                    print("\n[OK] Charts saved to 'outputs' folder!")
            
            input("\nPress Enter to continue...")
        
        elif choice == '3':  # Check Alerts
            clear_screen()
            print_banner()
            city = input("\nEnter city name to check alerts: ").strip()
            
            if city:
                print(f"\n[ANALYZING] Weather for {city}...")
                
                # Get weather data if not available
                if not current_weather or current_weather.get('city', '').lower() != city.lower():
                    current_weather = weather_api.get_current_weather(city)
                    current_forecast = weather_api.get_forecast(city)
                else:
                    # Check if we need new forecast
                    if not current_forecast:
                        current_forecast = weather_api.get_forecast(city)
                
                # Generate alerts
                alerts = alert_system.check_current_weather(current_weather)
                forecast_alerts = alert_system.check_forecast(current_forecast)
                all_alerts = alerts + forecast_alerts
                recommendations = alert_system.get_alert_recommendations(all_alerts)
                
                # Display alerts
                display_alerts(all_alerts, recommendations)
                
                # Option to save alerts report
                if all_alerts:
                    save = input("\nSave alerts report? (y/n): ").strip().lower()
                    if save == 'y':
                        report_gen.save_alerts_report(all_alerts)
                        
                    # Show alert summary
                    summary = alert_system.generate_alert_summary(alerts, forecast_alerts)
                    print(summary)
            
            input("\nPress Enter to continue...")
        
        elif choice == '4':  # Complete Report
            clear_screen()
            print_banner()
            city = input("\nEnter city name for complete report: ").strip()
            
            if city:
                print(f"\n[GENERATING] Complete report for {city}...")
                
                # Get fresh data
                weather = weather_api.get_current_weather(city)
                forecast = weather_api.get_forecast(city, 5)
                
                # Generate alerts
                alerts = alert_system.check_current_weather(weather)
                forecast_alerts = alert_system.check_forecast(forecast)
                all_alerts = alerts + forecast_alerts
                recommendations = alert_system.get_alert_recommendations(all_alerts)
                
                # Display summary
                print("\n[OUTPUTS] Generating files...")
                
                # Save CSV files
                report_gen.save_current_weather_csv(weather)
                report_gen.save_forecast_csv(forecast)
                
                # Create charts
                if forecast:
                    report_gen.create_temperature_chart(forecast)
                    report_gen.create_rain_chart(forecast)
                    report_gen.create_humidity_chart(forecast)
                
                # Save alerts report
                if all_alerts:
                    report_gen.save_alerts_report(all_alerts)
                
                # Generate complete report
                report_gen.generate_complete_report(weather, forecast, all_alerts, recommendations)
                
                print("\n" + "="*60)
                print("[SUCCESS] COMPLETE REPORT GENERATED!")
                print("="*60)
                print("Check these folders for outputs:")
                print("   -> outputs/ - CSV files and charts")
                print("   -> reports/ - Alert and complete reports")
                print("="*60)
            
            input("\nPress Enter to continue...")
        
        elif choice == '5':  # Demo Mode
            demo_mode()
        
        elif choice == '6':  # About
            about()
        
        else:
            print("\n[ERROR] Invalid choice! Please enter 0-6.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        # Set UTF-8 encoding for Windows console
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        
        main()
    except KeyboardInterrupt:
        print("\n\n[EXIT] Application terminated by user. Goodbye!")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        print("Please check your internet connection and try again.")
        input("\nPress Enter to exit...")