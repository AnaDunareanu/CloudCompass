from models.SearchLog import SearchLog
from config.__init__ import search_collection
from bson import json_util
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from folium import Map, Marker, PolyLine, Icon
from service.weatherService import get_weather
from ai_model.aiModel import predict_price
import python_weather
import datetime
import asyncio


recommendations = {
        'JFK': 'Try the famous pizza at Joe\'s Pizza in Manhattan.',
        'LAX': 'Visit the iconic Hollywood Walk of Fame.',
        'ORD': 'Explore Millennium Park and see the Cloud Gate sculpture in Chicago.',
        'ATL': 'Experience the Georgia Aquarium, one of the largest in the world.'
    }



geolocator = Nominatim(user_agent="CloudCompass")

def get_geocode(place_name):
    try:
        location = geolocator.geocode(place_name)
        if location:
            return {'lat': location.latitude, 'lng': location.longitude}
        else:
            return {'lat': 0, 'lng': 0}  # Return a default coordinate if location is not found
    except Exception as e:
        return {'error': str(e)}

def get_city_from_coordinates(latitude, longitude):
    # Reverse geocode the coordinates to get location details
    location = geolocator.reverse((latitude, longitude), language='en')
    
    # Extract the city from the location details
    city = location.raw['address'].get('city', '')
    
    return city


#Return a recommendation for a given destination
def get_recommendation(destination):
    return recommendations.get(destination, 'No recommendation available for this destination.')


def search_flights(origin, destination, date, airline):
    loc_origin = geolocator.geocode(f"{origin}, USA")
    loc_destination = geolocator.geocode(f"{destination}, USA")
    
    if not loc_origin or not loc_destination:
        return "Location information could not be retrieved."
    
    origin_coord = (loc_origin.latitude, loc_origin.longitude)
    destination_coord = (loc_destination.latitude, loc_destination.longitude)
    miles = geodesic(origin_coord, destination_coord).miles
    
    if isinstance(date, str):
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    else:
        date_obj = date
        
    year = date_obj.year
    quarter = (date_obj.month - 1) // 3 + 1
    
    predicted_price = predict_price(year, quarter, origin, destination, miles, 1, airline, date_obj)
    
    return predicted_price



def log_search_history(user_id, origin, destination, date, airline):
    search_entry = SearchLog(user_id, origin, destination, date, airline)
    SearchLog.save(search_entry)



# Function to fetch search history from the database
def get_search_history(user_id):
    search_history = search_collection.find({'user_id': user_id})
    
    # Serialize the search history for use in the template
    search_history_serialized = []
    for record in search_history:
        record['_id'] = str(record['_id'])
        record['timestamp'] = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        search_history_serialized.append(record)
    
    return search_history_serialized

