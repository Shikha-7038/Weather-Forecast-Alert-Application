"""
Weather API Integration Module
Handles fetching weather data from OpenWeatherMap API
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherAPI:
    """Weather API client for fetching current and forecast weather"""
    
    def __init__(self):
        """Initialize the weather API client"""
        self.api_key = os.getenv('WEATHER_API_KEY', '')
        self.base_url = os.getenv('API_BASE_URL', 'http://api.openweathermap.org/data/2.5')
        self.simulation_mode = os.getenv('SIMULATION_MODE', 'True').lower() == 'true'
        
    def get_current_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch current weather for a given city
        
        Args:
            city: City name (e.g., "London", "New York")
            
        Returns:
            Dictionary containing weather data or None if error
        """
        if self.simulation_mode or not self.api_key:
            return self._get_simulation_weather(city)
        
        try:
            # Build API URL
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Celsius
            }
            
            # Make API request
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract relevant information
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'main_condition': data['weather'][0]['main'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add rain if present
            if 'rain' in data:
                weather_data['rain'] = data['rain'].get('1h', 0)
            else:
                weather_data['rain'] = 0
                
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return self._get_simulation_weather(city)
        except (KeyError, json.JSONDecodeError) as e:
            print(f"❌ Data Parsing Error: {e}")
            return self._get_simulation_weather(city)
    
    def get_forecast(self, city: str, days: int = 5) -> Optional[List[Dict]]:
        """
        Fetch weather forecast for a given city
        
        Args:
            city: City name
            days: Number of days for forecast (max 5)
            
        Returns:
            List of daily forecast data or None if error
        """
        if self.simulation_mode or not self.api_key:
            return self._get_simulation_forecast(city, days)
        
        try:
            # Build API URL
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 readings per day (3-hour intervals)
            }
            
            # Make API request
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Process forecast data (daily aggregation)
            daily_forecast = {}
            
            for item in data['list']:
                date = item['dt_txt'].split()[0]
                
                if date not in daily_forecast:
                    daily_forecast[date] = {
                        'temps': [],
                        'humidity': [],
                        'rain': 0,
                        'description': item['weather'][0]['description']
                    }
                
                daily_forecast[date]['temps'].append(item['main']['temp'])
                daily_forecast[date]['humidity'].append(item['main']['humidity'])
                
                if 'rain' in item and '3h' in item['rain']:
                    daily_forecast[date]['rain'] += item['rain']['3h']
            
            # Create forecast list
            forecast = []
            for date, data in list(daily_forecast.items())[:days]:
                forecast.append({
                    'date': date,
                    'temp_max': max(data['temps']),
                    'temp_min': min(data['temps']),
                    'temp_avg': sum(data['temps']) / len(data['temps']),
                    'humidity_avg': sum(data['humidity']) / len(data['humidity']),
                    'rain_mm': data['rain'],
                    'description': data['description']
                })
            
            return forecast
            
        except Exception as e:
            print(f"❌ Forecast Error: {e}")
            return self._get_simulation_forecast(city, days)
    
    def _get_simulation_weather(self, city: str) -> Dict:
        """
        Generate simulated weather data for demo purposes
        
        Args:
            city: City name
            
        Returns:
            Simulated weather data dictionary
        """
        import random
        
        # Simulate different weather patterns based on city name
        city_hash = sum(ord(c) for c in city) % 10
        
        weather_conditions = [
            {"main": "Clear", "desc": "clear sky", "temp": 22, "humidity": 55, "rain": 0, "wind": 3},
            {"main": "Clouds", "desc": "scattered clouds", "temp": 18, "humidity": 65, "rain": 0, "wind": 5},
            {"main": "Rain", "desc": "light rain", "temp": 15, "humidity": 85, "rain": 2.5, "wind": 7},
            {"main": "Thunderstorm", "desc": "thunderstorm", "temp": 12, "humidity": 90, "rain": 15, "wind": 12},
            {"main": "Snow", "desc": "light snow", "temp": -2, "humidity": 75, "rain": 0, "wind": 4}
        ]
        
        condition = weather_conditions[city_hash % len(weather_conditions)]
        
        # Add some randomness
        temp_variation = random.uniform(-3, 3)
        
        return {
            'city': city,
            'temperature': round(condition['temp'] + temp_variation, 1),
            'feels_like': round(condition['temp'] + temp_variation - 1, 1),
            'humidity': condition['humidity'] + random.randint(-10, 10),
            'pressure': 1013 + random.randint(-20, 20),
            'wind_speed': condition['wind'] + random.uniform(-2, 2),
            'description': condition['desc'],
            'main_condition': condition['main'],
            'rain': condition['rain'] * random.uniform(0, 1.5),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _get_simulation_forecast(self, city: str, days: int) -> List[Dict]:
        """
        Generate simulated forecast data
        
        Args:
            city: City name
            days: Number of days
            
        Returns:
            List of simulated forecast data
        """
        import random
        from datetime import datetime, timedelta
        
        forecast = []
        current_date = datetime.now()
        
        for i in range(days):
            date = current_date + timedelta(days=i)
            
            # Simulate weather patterns
            temp_base = 20 if i % 2 == 0 else 15
            temp_variation = random.uniform(-5, 5)
            
            forecast.append({
                'date': date.strftime("%Y-%m-%d"),
                'temp_max': round(temp_base + temp_variation + 5, 1),
                'temp_min': round(temp_base + temp_variation - 3, 1),
                'temp_avg': round(temp_base + temp_variation, 1),
                'humidity_avg': random.randint(50, 90),
                'rain_mm': round(random.uniform(0, 20), 1),
                'description': random.choice(['clear sky', 'few clouds', 'scattered clouds', 'light rain', 'moderate rain'])
            })
        
        return forecast