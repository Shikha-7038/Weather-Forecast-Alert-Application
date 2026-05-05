"""
Simulation Module
Provides simulated weather data for testing without API
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List
import json

class WeatherSimulator:
    """Simulates weather data for testing and demonstration"""
    
    def __init__(self):
        """Initialize the weather simulator"""
        self.cities_db = {
            'london': {'lat': 51.5074, 'lon': -0.1278, 'climate': 'temperate'},
            'new york': {'lat': 40.7128, 'lon': -74.0060, 'climate': 'continental'},
            'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'climate': 'humid_subtropical'},
            'sydney': {'lat': -33.8688, 'lon': 151.2093, 'climate': 'oceanic'},
            'mumbai': {'lat': 19.0760, 'lon': 72.8777, 'climate': 'tropical'},
            'dubai': {'lat': 25.2048, 'lon': 55.2708, 'climate': 'desert'},
            'moscow': {'lat': 55.7558, 'lon': 37.6173, 'climate': 'continental'},
            'cairo': {'lat': 30.0444, 'lon': 31.2357, 'climate': 'desert'},
            'mexico city': {'lat': 19.4326, 'lon': -99.1332, 'climate': 'highland'},
            'berlin': {'lat': 52.5200, 'lon': 13.4050, 'climate': 'temperate'}
        }
        
        # Weather condition templates with realistic values
        self.weather_templates = {
            'sunny': {
                'temp_range': (20, 35),
                'humidity_range': (30, 50),
                'wind_range': (0, 5),
                'rain_chance': 0.05,
                'description': 'clear sky, sunny',
                'main': 'Clear'
            },
            'cloudy': {
                'temp_range': (15, 28),
                'humidity_range': (50, 70),
                'wind_range': (3, 8),
                'rain_chance': 0.20,
                'description': 'overcast clouds',
                'main': 'Clouds'
            },
            'rainy': {
                'temp_range': (10, 22),
                'humidity_range': (75, 95),
                'wind_range': (5, 12),
                'rain_chance': 0.90,
                'description': 'light rain',
                'main': 'Rain'
            },
            'stormy': {
                'temp_range': (8, 20),
                'humidity_range': (80, 98),
                'wind_range': (10, 20),
                'rain_chance': 0.95,
                'description': 'thunderstorm',
                'main': 'Thunderstorm'
            },
            'cold': {
                'temp_range': (-10, 10),
                'humidity_range': (60, 85),
                'wind_range': (4, 10),
                'rain_chance': 0.30,
                'description': 'cold weather',
                'main': 'Clear'
            }
        }
    
    def get_simulated_weather(self, city: str) -> Dict:
        """
        Get simulated weather for a city
        
        Args:
            city: City name
            
        Returns:
            Simulated weather data
        """
        city_key = city.lower().strip()
        
        # Get city climate or use default
        city_info = self.cities_db.get(city_key, {'climate': 'temperate'})
        climate = city_info['climate']
        
        # Select weather based on climate
        if climate == 'desert':
            weather_type = 'sunny'
            temp_adjust = 5
        elif climate == 'tropical':
            weather_type = random.choices(['sunny', 'cloudy', 'rainy'], weights=[0.3, 0.4, 0.3])[0]
            temp_adjust = 0
        elif climate == 'continental':
            weather_type = random.choices(['sunny', 'cloudy', 'rainy', 'cold', 'stormy'], 
                                         weights=[0.2, 0.3, 0.25, 0.2, 0.05])[0]
            temp_adjust = -5
        else:  # temperate
            weather_type = random.choices(['sunny', 'cloudy', 'rainy', 'stormy'], 
                                         weights=[0.25, 0.35, 0.3, 0.1])[0]
            temp_adjust = 0
        
        template = self.weather_templates[weather_type]
        
        # Generate realistic values
        temp_min, temp_max = template['temp_range']
        temp = round(random.uniform(temp_min, temp_max) + temp_adjust, 1)
        
        hum_min, hum_max = template['humidity_range']
        humidity = random.randint(hum_min, hum_max)
        
        wind_min, wind_max = template['wind_range']
        wind_speed = round(random.uniform(wind_min, wind_max), 1)
        
        # Rain amount
        if template['rain_chance'] > random.random():
            rain = round(random.uniform(0.5, 15), 1)
        else:
            rain = 0
        
        return {
            'city': city.title(),
            'temperature': temp,
            'feels_like': round(temp - random.uniform(0, 3), 1),
            'humidity': humidity,
            'pressure': random.randint(990, 1030),
            'wind_speed': wind_speed,
            'description': template['description'],
            'main_condition': template['main'],
            'rain': rain,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'simulation': True
        }
    
    def get_simulated_forecast(self, city: str, days: int = 5) -> List[Dict]:
        """
        Get simulated forecast for a city
        
        Args:
            city: City name
            days: Number of days
            
        Returns:
            List of forecast data
        """
        forecast = []
        current_date = datetime.now()
        
        # Create a realistic trend
        base_temp = None
        trend_direction = random.choice(['up', 'down', 'stable'])
        
        for i in range(days):
            date = current_date + timedelta(days=i)
            
            # Get current weather for this day (using simulation)
            weather = self.get_simulated_weather(city)
            
            if base_temp is None:
                base_temp = weather['temperature']
            
            # Apply trend
            if trend_direction == 'up':
                temp_adjust = i * random.uniform(0.5, 2)
            elif trend_direction == 'down':
                temp_adjust = -i * random.uniform(0.5, 2)
            else:
                temp_adjust = random.uniform(-2, 2)
            
            forecast.append({
                'date': date.strftime("%Y-%m-%d"),
                'temp_max': round(weather['temperature'] + random.uniform(2, 5) + temp_adjust, 1),
                'temp_min': round(weather['temperature'] - random.uniform(3, 8) + temp_adjust, 1),
                'temp_avg': round(weather['temperature'] + temp_adjust, 1),
                'humidity_avg': min(100, max(0, weather['humidity'] + random.randint(-10, 10))),
                'rain_mm': round(max(0, weather['rain'] + random.uniform(-2, 5)), 1),
                'description': weather['description']
            })
        
        return forecast
    
    def get_all_cities(self) -> List[str]:
        """Get list of all available cities"""
        return [city.title() for city in self.cities_db.keys()]
    
    def generate_sample_data_file(self, filename: str = "sample_weather_data.json"):
        """Generate a sample data file for testing"""
        sample_data = {}
        
        for city in self.cities_db.keys():
            sample_data[city] = {
                'current': self.get_simulated_weather(city),
                'forecast': self.get_simulated_forecast(city, 5)
            }
        
        with open(filename, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"✅ Sample data saved to {filename}")
        return filename