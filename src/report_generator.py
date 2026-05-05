"""
Report Generation Module
Creates CSV reports, charts, and saves weather data
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from typing import Dict, List
import json

# Set matplotlib to use Agg backend to avoid GUI issues
plt.switch_backend('Agg')

class ReportGenerator:
    """Generates reports and visualizations from weather data"""
    
    def __init__(self, data_dir: str = "data", outputs_dir: str = "outputs", reports_dir: str = "reports"):
        """
        Initialize report generator
        
        Args:
            data_dir: Directory for CSV data files
            outputs_dir: Directory for charts/images
            reports_dir: Directory for text reports
        """
        self.data_dir = data_dir
        self.outputs_dir = outputs_dir
        self.reports_dir = reports_dir
        
        # Create all directories
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(outputs_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)
    
    def save_current_weather_csv(self, weather_data: Dict) -> str:
        """
        Save current weather data to CSV in data folder
        
        Args:
            weather_data: Current weather dictionary
            
        Returns:
            Path to saved file
        """
        if not weather_data:
            return ""
        
        filename = f"current_weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        # Convert to DataFrame
        df = pd.DataFrame([weather_data])
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"[OK] Current weather saved to: {filepath}")
        return filepath
    
    def save_forecast_csv(self, forecast_data: List[Dict]) -> str:
        """
        Save forecast data to CSV in data folder
        
        Args:
            forecast_data: List of forecast dictionaries
            
        Returns:
            Path to saved file
        """
        if not forecast_data:
            return ""
        
        filename = f"forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        # Convert to DataFrame
        df = pd.DataFrame(forecast_data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"[OK] Forecast saved to: {filepath}")
        return filepath
    
    def save_alerts_report(self, alerts: List[Dict], filename: str = None) -> str:
        """
        Save alerts to a report file in reports folder
        
        Args:
            alerts: List of alerts
            filename: Custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            filename = f"alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("WEATHER ALERTS REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            if not alerts:
                f.write("No active alerts at this time.\n")
            else:
                for i, alert in enumerate(alerts, 1):
                    f.write(f"Alert #{i}\n")
                    f.write(f"  Type: {alert.get('type', 'Unknown')}\n")
                    f.write(f"  Severity: {alert.get('severity', 'Unknown')}\n")
                    f.write(f"  Message: {alert.get('message', 'No message')}\n")
                    if 'value' in alert:
                        f.write(f"  Value: {alert['value']}\n")
                    if 'date' in alert:
                        f.write(f"  Date: {alert['date']}\n")
                    f.write("\n")
        
        print(f"[OK] Alerts report saved to: {filepath}")
        return filepath
    
    def create_temperature_chart(self, forecast_data: List[Dict]) -> str:
        """
        Create a temperature trend chart in outputs folder
        
        Args:
            forecast_data: List of forecast data
            
        Returns:
            Path to saved chart image
        """
        if not forecast_data:
            return ""
        
        # Create DataFrame
        df = pd.DataFrame(forecast_data)
        
        # Create chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        dates = df['date']
        temps_max = df['temp_max']
        temps_min = df['temp_min']
        temps_avg = df['temp_avg']
        
        ax.plot(dates, temps_max, 'r-', marker='o', label='Max Temperature', linewidth=2)
        ax.plot(dates, temps_min, 'b-', marker='s', label='Min Temperature', linewidth=2)
        ax.plot(dates, temps_avg, 'g--', marker='^', label='Average Temperature', linewidth=2)
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Temperature (C)', fontsize=12)
        ax.set_title('Weather Forecast - Temperature Trends', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save chart
        filename = f"temperature_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.outputs_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"[OK] Temperature chart saved to: {filepath}")
        return filepath
    
    def create_rain_chart(self, forecast_data: List[Dict]) -> str:
        """
        Create a rainfall chart in outputs folder
        
        Args:
            forecast_data: List of forecast data
            
        Returns:
            Path to saved chart image
        """
        if not forecast_data:
            return ""
        
        # Create DataFrame
        df = pd.DataFrame(forecast_data)
        
        # Create chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        dates = df['date']
        rain = df['rain_mm']
        
        bars = ax.bar(dates, rain, color='skyblue', edgecolor='navy', alpha=0.7)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Rainfall (mm)', fontsize=12)
        ax.set_title('Weather Forecast - Rainfall Prediction', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars, rain):
            if value > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{value:.1f}', ha='center', va='bottom', fontsize=9)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save chart
        filename = f"rain_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.outputs_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"[OK] Rain chart saved to: {filepath}")
        return filepath
    
    def create_humidity_chart(self, forecast_data: List[Dict]) -> str:
        """
        Create a humidity chart in outputs folder
        
        Args:
            forecast_data: List of forecast data
            
        Returns:
            Path to saved chart image
        """
        if not forecast_data:
            return ""
        
        # Create DataFrame
        df = pd.DataFrame(forecast_data)
        
        # Create chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        dates = df['date']
        humidity = df['humidity_avg']
        
        ax.fill_between(dates, humidity, color='lightblue', alpha=0.5)
        ax.plot(dates, humidity, 'b-o', linewidth=2, markersize=8)
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Humidity (%)', fontsize=12)
        ax.set_title('Weather Forecast - Humidity Trends', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add horizontal line for high humidity threshold
        ax.axhline(y=70, color='orange', linestyle='--', label='High Humidity Warning (70%)')
        ax.legend()
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save chart
        filename = f"humidity_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.outputs_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        print(f"[OK] Humidity chart saved to: {filepath}")
        return filepath
    
    def generate_complete_report(self, weather_data: Dict, forecast_data: List[Dict],
                                  alerts: List[Dict], recommendations: List[str]) -> str:
        """
        Generate a complete weather report in reports folder
        
        Args:
            weather_data: Current weather data
            forecast_data: Forecast data
            alerts: Active alerts
            recommendations: Recommendations
            
        Returns:
            Path to saved report
        """
        filename = f"weather_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("COMPLETE WEATHER FORECAST & ALERT REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            # Current Weather Section
            f.write("[CURRENT WEATHER CONDITIONS]\n")
            f.write("-"*50 + "\n")
            if weather_data:
                f.write(f"City: {weather_data.get('city', 'Unknown')}\n")
                f.write(f"Temperature: {weather_data.get('temperature', 'N/A')}C\n")
                f.write(f"Feels Like: {weather_data.get('feels_like', 'N/A')}C\n")
                f.write(f"Humidity: {weather_data.get('humidity', 'N/A')}%\n")
                f.write(f"Wind Speed: {weather_data.get('wind_speed', 'N/A')} m/s\n")
                f.write(f"Pressure: {weather_data.get('pressure', 'N/A')} hPa\n")
                f.write(f"Conditions: {weather_data.get('description', 'N/A')}\n")
                if weather_data.get('rain', 0) > 0:
                    f.write(f"Rainfall: {weather_data.get('rain', 0)} mm\n")
            else:
                f.write("No current weather data available.\n")
            f.write("\n")
            
            # Forecast Section
            f.write("[5-DAY WEATHER FORECAST]\n")
            f.write("-"*50 + "\n")
            if forecast_data:
                for day in forecast_data:
                    f.write(f"\n[Date: {day.get('date', 'Unknown Date')}]\n")
                    f.write(f"   Max Temp: {day.get('temp_max', 'N/A')}C | Min Temp: {day.get('temp_min', 'N/A')}C\n")
                    f.write(f"   Avg Temp: {day.get('temp_avg', 'N/A')}C\n")
                    f.write(f"   Humidity: {day.get('humidity_avg', 'N/A')}%\n")
                    f.write(f"   Rainfall: {day.get('rain_mm', 'N/A')} mm\n")
                    f.write(f"   Conditions: {day.get('description', 'N/A')}\n")
            else:
                f.write("No forecast data available.\n")
            f.write("\n")
            
            # Alerts Section
            f.write("[ALERTS & WARNINGS]\n")
            f.write("-"*50 + "\n")
            if alerts:
                for alert in alerts:
                    severity_symbol = "[CRITICAL]" if alert.get('severity') == 'critical' else "[WARNING]" if alert.get('severity') == 'warning' else "[INFO]"
                    f.write(f"{severity_symbol} {alert.get('message', 'No message')}\n")
            else:
                f.write("[OK] No active alerts.\n")
            f.write("\n")
            
            # Recommendations Section
            f.write("[RECOMMENDATIONS]\n")
            f.write("-"*50 + "\n")
            if recommendations:
                for rec in recommendations:
                    f.write(f"  -> {rec}\n")
            else:
                f.write("No specific recommendations at this time.\n")
            f.write("\n")
            
            # Footer
            f.write("="*70 + "\n")
            f.write("Report generated by Weather Forecast & Alert Application\n")
            f.write("="*70 + "\n")
        
        print(f"[OK] Complete report saved to: {filepath}")
        return filepath