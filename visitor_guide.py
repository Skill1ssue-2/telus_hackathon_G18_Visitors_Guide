import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta

class TorontoVisitorGuide:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.concert_time = pd.Timestamp('2024-11-14 19:00:00')  # Example date/time for Taylor Swift
        
    def load_and_train_model(self, subway_data_path):
        # Load historical concert data and train the model
        subway_dataset = pd.read_csv(subway_data_path)
        
        # Similar to your existing model training code
        tor_core_data = subway_dataset[subway_dataset['output_geoid'] == 'Tor-Core']
        # ... model training code ...
        
    def predict_subway_traffic(self, station, hour, day, weekday):
        if not self.model:
            return "Model not trained yet"
            
        example_data = pd.DataFrame({
            'input_geoid_encoded': [self.label_encoder.transform([station])[0]],
            'hour': [hour],
            'day': [day],
            'weekday': [weekday]
        })
        return self.model.predict(example_data)[0]

    def get_arrival_recommendation(self, origin_region):
        # Real data-based arrival patterns
        arrival_patterns = {
            'ON1': {'peak_hour': 17, 'free_hours': 4},
            'ON2': {'peak_hour': 16, 'free_hours': 5},
            'ON3': {'peak_hour': 13, 'free_hours': 8},
            'ON4': {'peak_hour': 12, 'free_hours': 9}
        }
        
        pattern = arrival_patterns.get(origin_region)
        if not pattern:
            return {
                'recommended_arrival_time': None,
                'reason': "Region not found in data"
            }
        
        # Recommend arriving 1 hour before peak
        recommended_hour = pattern['peak_hour'] - 1
        recommended_time = self.concert_time.replace(hour=recommended_hour)
        
        return {
            'recommended_arrival_time': recommended_time,
            'peak_arrival_time': self.concert_time.replace(hour=pattern['peak_hour']),
            'free_hours': pattern['free_hours'],
            'reason': f"Based on data, most visitors from {origin_region} arrive at {pattern['peak_hour']}:00. "
                     f"We recommend arriving at {recommended_hour}:00 to avoid peak crowds and have {pattern['free_hours']} hours to explore Toronto."
        }

    def get_tourist_suggestions(self, available_hours):
        suggestions = {
            'very_short': {  # 2-3 hours
                'activities': [
                    {'name': 'CN Tower', 'duration': '1 hour', 'type': 'Landmark', 
                     'description': 'Iconic tower with glass floor and observation deck'},
                    {'name': 'Rogers Centre Area', 'duration': '30 mins', 'type': 'Sports/Entertainment',
                     'description': 'Home of Blue Jays, walking distance to concert venue'},
                    {'name': 'Steam Whistle Brewery', 'duration': '1 hour', 'type': 'Food & Drink',
                     'description': 'Historic roundhouse with brewery tours and tastings'}
                ],
                'description': 'Quick city highlights near the concert venue',
                'food_suggestions': ['Steam Whistle Biergarten', 'Loose Moose', 'The Fox']
            },
            'short': {  # 4-5 hours
                'activities': [
                    {'name': "Ripley's Aquarium", 'duration': '2 hours', 'type': 'Attraction',
                     'description': 'Underwater tunnel and marine life exhibits'},
                    {'name': 'St. Lawrence Market', 'duration': '1.5 hours', 'type': 'Food & Shopping',
                     'description': 'Historic market with local foods and crafts'},
                    {'name': 'Harbourfront Walk', 'duration': '1 hour', 'type': 'Outdoor',
                     'description': 'Scenic waterfront promenade with shops and cafes'}
                ],
                'description': 'Popular downtown attractions with food options',
                'food_suggestions': ['St. Lawrence Market Food Court', 'Pearl Harbourfront', 'Amsterdam BrewHouse']
            },
            'medium': {  # 6-7 hours
                'activities': [
                    {'name': 'Royal Ontario Museum', 'duration': '2.5 hours', 'type': 'Museum',
                     'description': 'Natural history and world cultures museum'},
                    {'name': 'Yorkville', 'duration': '2 hours', 'type': 'Shopping/Entertainment',
                     'description': 'Upscale shopping district with restaurants'},
                    {'name': 'Graffiti Alley', 'duration': '1 hour', 'type': 'Art/Culture',
                     'description': 'Colorful street art in Fashion District'},
                    {'name': 'Kensington Market', 'duration': '1.5 hours', 'type': 'Neighborhood',
                     'description': 'Eclectic neighborhood with vintage shops and food'}
                ],
                'description': 'Mix of culture, shopping, and local flavor',
                'food_suggestions': ['Seven Lives Tacos', 'Pai', 'Mother\'s Dumplings']
            },
            'long': {  # 8+ hours
                'activities': [
                    {'name': 'Casa Loma', 'duration': '2.5 hours', 'type': 'Historic Site',
                     'description': 'Gothic Revival castle with gardens'},
                    {'name': 'Art Gallery of Ontario', 'duration': '2.5 hours', 'type': 'Art Museum',
                     'description': 'Canadian and international art collections'},
                    {'name': 'Toronto Islands Ferry', 'duration': '3 hours', 'type': 'Outdoor/Adventure',
                     'description': 'Island park with beaches and great city views'},
                    {'name': 'Distillery District', 'duration': '2 hours', 'type': 'Historic/Entertainment',
                     'description': 'Victorian architecture with shops and restaurants'}
                ],
                'description': 'Comprehensive Toronto experience',
                'food_suggestions': ['El Catrin', 'Richmond Station', 'Lee Restaurant']
            }
        }
        
        if available_hours <= 3:
            return suggestions['very_short']
        elif available_hours <= 5:
            return suggestions['short']
        elif available_hours <= 7:
            return suggestions['medium']
        else:
            return suggestions['long']

# Example usage
def main():
    guide = TorontoVisitorGuide()
    
    # Example: Get recommendations for a visitor
    origin = 'ON2'
    arrival_info = guide.get_arrival_recommendation(origin)
    print(f"\nArrival Recommendation for {origin}:")
    print(f"Arrive at: {arrival_info['recommended_arrival_time'].strftime('%I:%M %p')}")
    print(f"Reason: {arrival_info['reason']}")
    
    # Example: Get tourist suggestions
    free_time = 5  # hours
    suggestions = guide.get_tourist_suggestions(free_time)
    print(f"\nSuggested Activities for {free_time} hours:")
    print(f"Description: {suggestions['description']}")
    print("Activities:")
    for activity in suggestions['activities']:
        print(activity) 