from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests

@api_view(['GET'])
def get_weather(request):
    city = request.GET.get('city', '')
    if not city:
        return Response({'error': 'City parameter is required'}, status=400)

    api_key = settings.OPENWEATHERMAP_API_KEY
    coordinates = get_coordinates(city)

    if 'error' in coordinates:
        return Response(coordinates, status=404)

    weather_data = get_current_weather(coordinates['lat'], coordinates['lon'], api_key)

    if 'error' in weather_data:
        return Response(weather_data, status=500)

    return Response(weather_data)

@api_view(['GET'])
def get_pollution(request):
    city = request.GET.get('city', '')
    if not city:
        return Response({'error': 'City parameter is required'}, status=400)

    api_key = settings.OPENWEATHERMAP_API_KEY
    coordinates = get_coordinates(city)
    if 'error' in coordinates:
        return Response(coordinates, status=404)
    print(coordinates)
    overview_data = current_overview(coordinates['lat'], coordinates['lon'], api_key)
    
    
    if 'error' in overview_data:
        return Response(overview_data, status=500)
    
    return Response(overview_data)
    

def get_coordinates(city):
    api_key = settings.OPENWEATHERMAP_API_KEY
    base_url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        'q': city,
        'limit': 1,
        'appid': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200 and data:
            return {
                'name': data[0]['name'],
                'lat': data[0]['lat'],
                'lon': data[0]['lon'],
                'country': data[0]['country'],
                'state': data[0].get('state', 'N/A')
            }
        else:
            return {'error': 'City not found'}
    except Exception as e:
        return {'error': str(e)}

def get_current_weather(lat, lon, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
            }
        else:
            return {'error': 'Weather data not available'}
    except Exception as e:
        return {'error': str(e)}
    
def current_overview(lat, lon, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"

    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                'pollution': data['list'][0]['components'].get('o3')
            }
        else:
            return {'error': 'Weather data not available'}
    except Exception as e:
        return {'error': str(e)}
    pass

