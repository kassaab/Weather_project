import datetime
import requests
import json
from django.shortcuts import render
import environ

env = environ.Env()
environ.Env.read_env()

API_KEY = env('MY_API_KEY')

if API_KEY is None:
    raise ValueError("API key not found")

def index(request):
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=imperial&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        if city1:
            weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data1, daily_forecasts1 = None, None
        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2,
        }

        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'], 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    daily_forecasts = []
    previous_day = []
    for daily_data in forecast_response['list']:
        day_of_week = datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A")
        if day_of_week not in previous_day:
            daily_forecasts.append({
                # "day": datetime.datetime.strptime(daily_data['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%A"),
                # "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
                "day": day_of_week,
                "min_temp": round(daily_data['main']['temp_min'], 2),
                "max_temp": round(daily_data['main']['temp_max'], 2),
                "description": daily_data['weather'][0]['description'],
                "icon_url": f"http://openweathermap.org/img/w/{daily_data['weather'][0]['icon']}.png"
            })
            previous_day.append(day_of_week)

    return weather_data, daily_forecasts[:5]
