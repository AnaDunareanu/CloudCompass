def get_recommendation(destination):
    recommendations = {
        'NYC': 'Try the famous pizza at Joe\'s Pizza in Manhattan.',
        'LAX': 'Visit the iconic Hollywood Walk of Fame.',
        'ORD': 'Explore Millennium Park and see the Cloud Gate sculpture in Chicago.',
        'ATL': 'Experience the Georgia Aquarium, one of the largest in the world.'
    }
    
    return recommendations.get(destination, 'No recommendation available for this destination.')


destination = 'NYC'
recommendation = get_recommendation(destination)
print(recommendation)
