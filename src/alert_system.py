"""
Alert System Module
Checks weather conditions against thresholds and generates alerts
"""

from typing import Dict, List, Tuple
from datetime import datetime
import json

class AlertSystem:
    """Weather alert system that evaluates conditions and generates alerts"""
    
    def __init__(self, thresholds: Dict = None):
        """
        Initialize alert system with custom thresholds
        
        Args:
            thresholds: Custom threshold values (optional)
        """
        # Default thresholds
        self.default_thresholds = {
            'high_temperature': 35,      # Celsius
            'low_temperature': 0,         # Celsius
            'high_humidity': 80,          # Percentage
            'low_humidity': 20,           # Percentage
            'high_wind': 15,              # m/s (approx 54 km/h)
            'rain': 5,                    # mm in 3 hours
            'heavy_rain': 20,             # mm in 3 hours
            'high_pressure': 1020,        # hPa
            'low_pressure': 990           # hPa
        }
        
        # Override with custom thresholds
        self.thresholds = thresholds or self.default_thresholds
        
        # Alert severity levels
        self.severity = {
            'info': '[INFO]',
            'warning': '[WARNING]',
            'critical': '[CRITICAL]'
        }
    
    def check_current_weather(self, weather_data: Dict) -> List[Dict]:
        """
        Check current weather conditions for alerts
        
        Args:
            weather_data: Current weather data dictionary
            
        Returns:
            List of active alerts
        """
        alerts = []
        
        if not weather_data:
            return alerts
        
        # Check temperature high
        temp = weather_data.get('temperature', 0)
        if temp >= self.thresholds['high_temperature']:
            alerts.append({
                'type': 'high_temperature',
                'severity': 'warning',
                'message': f"HIGH TEMPERATURE: {temp}C detected! Stay hydrated and avoid direct sunlight.",
                'value': temp,
                'threshold': self.thresholds['high_temperature']
            })
        
        # Check temperature low
        if temp <= self.thresholds['low_temperature']:
            alerts.append({
                'type': 'low_temperature',
                'severity': 'warning',
                'message': f"LOW TEMPERATURE: {temp}C detected! Wear warm clothing.",
                'value': temp,
                'threshold': self.thresholds['low_temperature']
            })
        
        # Check humidity
        humidity = weather_data.get('humidity', 0)
        if humidity >= self.thresholds['high_humidity']:
            alerts.append({
                'type': 'high_humidity',
                'severity': 'info',
                'message': f"HIGH HUMIDITY: {humidity}% - Feels muggy, stay cool.",
                'value': humidity,
                'threshold': self.thresholds['high_humidity']
            })
        
        if humidity <= self.thresholds['low_humidity']:
            alerts.append({
                'type': 'low_humidity',
                'severity': 'info',
                'message': f"LOW HUMIDITY: {humidity}% - Skin may feel dry.",
                'value': humidity,
                'threshold': self.thresholds['low_humidity']
            })
        
        # Check wind speed
        wind = weather_data.get('wind_speed', 0)
        if wind >= self.thresholds['high_wind']:
            alerts.append({
                'type': 'high_wind',
                'severity': 'warning',
                'message': f"STRONG WIND: {wind} m/s - Secure outdoor objects!",
                'value': wind,
                'threshold': self.thresholds['high_wind']
            })
        
        # Check rain
        rain = weather_data.get('rain', 0)
        if rain >= self.thresholds['heavy_rain']:
            alerts.append({
                'type': 'heavy_rain',
                'severity': 'critical',
                'message': f"HEAVY RAIN: {rain}mm - Flooding possible! Take precautions.",
                'value': rain,
                'threshold': self.thresholds['heavy_rain']
            })
        elif rain >= self.thresholds['rain']:
            alerts.append({
                'type': 'rain',
                'severity': 'warning',
                'message': f"RAIN ALERT: {rain}mm expected. Carry umbrella!",
                'value': rain,
                'threshold': self.thresholds['rain']
            })
        
        # Check weather condition
        condition = weather_data.get('main_condition', '')
        if condition == 'Thunderstorm':
            alerts.append({
                'type': 'thunderstorm',
                'severity': 'critical',
                'message': "THUNDERSTORM ALERT! Seek shelter immediately!",
                'value': condition,
                'threshold': 'Thunderstorm'
            })
        
        return alerts
    
    def check_forecast(self, forecast_data: List[Dict]) -> List[Dict]:
        """
        Check forecast data for future alerts
        
        Args:
            forecast_data: List of daily forecast data
            
        Returns:
            List of forecast-based alerts
        """
        alerts = []
        
        if not forecast_data:
            return alerts
        
        for day in forecast_data:
            date = day.get('date', 'Unknown')
            
            # Check high temperature in forecast
            temp_max = day.get('temp_max', 0)
            if temp_max >= self.thresholds['high_temperature']:
                alerts.append({
                    'type': 'forecast_high_temp',
                    'severity': 'info',
                    'message': f"FORECAST for {date}: High temperature of {temp_max}C expected.",
                    'value': temp_max,
                    'date': date
                })
            
            # Check rain in forecast
            rain = day.get('rain_mm', 0)
            if rain >= self.thresholds['rain']:
                alerts.append({
                    'type': 'forecast_rain',
                    'severity': 'info',
                    'message': f"FORECAST for {date}: {rain}mm of rain expected.",
                    'value': rain,
                    'date': date
                })
        
        return alerts
    
    def generate_alert_summary(self, current_alerts: List[Dict], forecast_alerts: List[Dict]) -> str:
        """
        Generate a human-readable summary of all alerts
        
        Args:
            current_alerts: List of current weather alerts
            forecast_alerts: List of forecast alerts
            
        Returns:
            Formatted alert summary string
        """
        all_alerts = current_alerts + forecast_alerts
        
        if not all_alerts:
            return "[OK] No active weather alerts. All conditions are normal."
        
        summary = "\n" + "="*60 + "\n"
        summary += "WEATHER ALERT SUMMARY\n"
        summary += "="*60 + "\n\n"
        
        # Group by severity
        critical = [a for a in all_alerts if a['severity'] == 'critical']
        warnings = [a for a in all_alerts if a['severity'] == 'warning']
        info = [a for a in all_alerts if a['severity'] == 'info']
        
        if critical:
            summary += f"{self.severity['critical']} ALERTS:\n"
            for alert in critical:
                summary += f"  -> {alert['message']}\n"
            summary += "\n"
        
        if warnings:
            summary += f"{self.severity['warning']} ALERTS:\n"
            for alert in warnings:
                summary += f"  -> {alert['message']}\n"
            summary += "\n"
        
        if info:
            summary += f"{self.severity['info']} NOTIFICATIONS:\n"
            for alert in info:
                summary += f"  -> {alert['message']}\n"
            summary += "\n"
        
        summary += "="*60 + "\n"
        summary += f"Total Alerts: {len(all_alerts)} | "
        summary += f"Critical: {len(critical)} | "
        summary += f"Warnings: {len(warnings)} | "
        summary += f"Info: {len(info)}\n"
        summary += "="*60 + "\n"
        
        return summary
    
    def get_alert_recommendations(self, alerts: List[Dict]) -> List[str]:
        """
        Get actionable recommendations based on alerts
        
        Args:
            alerts: List of alerts
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for alert in alerts:
            alert_type = alert['type']
            
            if alert_type == 'high_temperature':
                recommendations.append("[HEAT] Drink plenty of water and avoid outdoor activities during peak hours (12 PM - 4 PM)")
            elif alert_type == 'low_temperature':
                recommendations.append("[COLD] Wear layered clothing and limit time outdoors")
            elif alert_type == 'high_wind':
                recommendations.append("[WIND] Secure outdoor furniture and avoid parking under trees")
            elif alert_type == 'rain':
                recommendations.append("[RAIN] Carry an umbrella and be cautious while driving")
            elif alert_type == 'heavy_rain':
                recommendations.append("[FLOOD] Avoid low-lying areas and stay indoors. Monitor local flood warnings")
            elif alert_type == 'thunderstorm':
                recommendations.append("[STORM] Stay indoors, avoid using electrical appliances, and unplug devices")
            elif alert_type == 'high_humidity':
                recommendations.append("[HUMIDITY] Use air conditioning or dehumidifier. Stay in ventilated areas")
        
        # Remove duplicates
        return list(set(recommendations))