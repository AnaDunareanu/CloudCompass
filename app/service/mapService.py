from geopy.geocoders import Nominatim
from folium import Map, Marker, PolyLine, Icon


#from models.SearchLog import SearchLog
geolocator = Nominatim(user_agent="CloudCompass")


origin_location = geolocator.geocode('LAX, USA')
destination_location = geolocator.geocode('NYC, USA')

print(origin_location.latitude, origin_location.longitude)
print(destination_location.latitude, destination_location.longitude)





# Creează o hartă centrată între origine și destinație
m = Map(location=[(origin_location.latitude + destination_location.latitude) / 2, (origin_location.longitude + destination_location.longitude) / 2], zoom_start=5)

# Adaugă un marcator pentru origine
Marker([origin_location.latitude, origin_location.longitude], tooltip='Origine', icon=Icon(color='green')).add_to(m)

# Adaugă un marcator pentru destinație
Marker([destination_location.latitude, destination_location.longitude], tooltip='Destinație', icon=Icon(color='red')).add_to(m)

# (Opțional) Adaugă o linie între origine și destinație
PolyLine([(origin_location.latitude, origin_location.longitude), (destination_location.latitude, destination_location.longitude)], color='blue').add_to(m)

# Salvează harta într-un fișier HTML
m.save('ruta_aeriana_orase.html')
