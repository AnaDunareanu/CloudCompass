import python_weather
import asyncio


async def get_weather(city):
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

    # fetch a weather forecast from a city
        weather = await client.get(location=city)

        forecast = {
            "temperature": f"{weather.temperature}°F",
            "daily_forecasts": [{"date": daily.date, "temperature": f"{daily.temperature}°F"} for daily in weather.daily_forecasts]
        }

        return forecast
    
