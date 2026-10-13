from django.shortcuts import render
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def weather_view(request):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = request.GET.get("city", "Puerto Princesa")

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            url,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric",
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
        }

    except (requests.RequestException, KeyError):
        weather_data = {
            "error": f"Could not get weather information for '{city}'."
        }

    return render(request, "weather.html", {
        "weather": weather_data,
        "city": city,
    })