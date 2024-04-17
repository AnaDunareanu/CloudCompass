from models.SearchLog import SearchLog
from config.__init__ import search_collection
from bson import json_util
from geopy.geocoders import Nominatim
from folium import Map, Marker, PolyLine, Icon
from service.weatherService import get_weather
import python_weather
import asyncio

#Mock data
flights = [
    {'origin': 'NYC', 'destination': 'LAX', 'date': '2024-04-01', 'airline': 'Delta', 'price': 300},
    {'origin': 'LAX', 'destination': 'NYC', 'date': '2024-04-02', 'airline': 'United', 'price': 350},
    {'origin': 'ORD', 'destination': 'IAD', 'date': '2024-04-03', 'airline': 'Delta', 'price': 320},
    {'origin': 'NYC', 'destination': 'LAX', 'date': '2024-04-04', 'airline': 'Delta', 'price': 320},
    {'origin': 'ATL', 'destination': 'ABY', 'date': '2024-04-05', 'airline': 'Delta', 'price': 420},
]

recommendations = {
        'NYC': 'Try the famous pizza at Joe\'s Pizza in Manhattan.',
        'LAX': 'Visit the iconic Hollywood Walk of Fame.',
        'ORD': 'Explore Millennium Park and see the Cloud Gate sculpture in Chicago.',
        'ATL': 'Experience the Georgia Aquarium, one of the largest in the world.'
    }



geolocator = Nominatim(user_agent="CloudCompass")

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
    results = []

    if not origin or not destination or not date or not airline:
        return 'Origin, destination, date, and airline are required'

    for flight in flights:
        if flight['origin'] == origin and flight['destination'] == destination and flight['date'] == date and flight['airline'] == airline:
            results.append(flight)

    if not results:
        return 'No flights found'
    
    #Define the location of the origin and destination
    locatie_origine = geolocator.geocode(origin + ', USA')
    locatie_destinatie = geolocator.geocode(destination + ', USA')

    orignCity = get_city_from_coordinates(locatie_origine.latitude, locatie_origine.longitude)
    destinationCity = get_city_from_coordinates(locatie_destinatie.latitude, locatie_destinatie.longitude)

    #Get the recommendation for the destination
    recommendation = get_recommendation(destination)

    # Fetch the weather forecast for both origin and destination
    origin_forecast = asyncio.run(get_weather(orignCity))
    destination_forecast = asyncio.run(get_weather(destinationCity))

    #Create a map centered between the origin and destination
    m = Map(location=[(locatie_origine.latitude + locatie_destinatie.latitude) / 2, (locatie_origine.longitude + locatie_destinatie.longitude) / 2], zoom_start=5)

    #Add a marker for the origin
    Marker([locatie_origine.latitude, locatie_origine.longitude], tooltip='Origine', icon=Icon(color='green')).add_to(m)

    #Add a marker for the destination
    Marker([locatie_destinatie.latitude, locatie_destinatie.longitude], tooltip='Destinație', icon=Icon(color='red')).add_to(m)

    #Add a line between the origin and destination
    PolyLine([(locatie_origine.latitude, locatie_origine.longitude), (locatie_destinatie.latitude, locatie_destinatie.longitude)], color='blue').add_to(m)

    #Save the map to an HTML file
    m.save('map.html')

    #Add the weather forecast to the results
    for flight in results:
        flight['origin_forecast'] = origin_forecast
        flight['destination_forecast'] = destination_forecast
        flight['recommendation'] = recommendation

    return results



def log_search_history(user_id, origin, destination, date, airline):
    search_entry = SearchLog(user_id, origin, destination, date, airline)
    SearchLog.save(search_entry)



def get_search_history(user_id):
    search_history = search_collection.find({'user_id': user_id})

    # Convert ObjectId to string representation
    search_history_serialized = [json_util.dumps(record) for record in search_history]
    return search_history_serialized

