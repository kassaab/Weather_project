import requests
import tkinter as tk
import json
import re

# Load API keys from configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

IPBASE_API_ENDPOINT = "https://api.ipbase.com/v2/info"
IPBASE_API_KEY = config['IPBASE_API_KEY']
WEATHER_MAP_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_MAP_API_KEY = config['WEATHER_MAP_API_KEY']

IP_ADDRESS_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def get_weather():
    input_value = input_field.get()

    if IP_ADDRESS_REGEX.match(input_value):
        ipbase_query_params = {'apiKey': IPBASE_API_KEY, 'ip': input_value}
        response = requests.get(IPBASE_API_ENDPOINT, params=ipbase_query_params)
        ip_data = response.json()
        city_name = ip_data['data']['location']['city']['name']
    else:
        city_name = input_value

    weather_query_params = {
        'q': city_name,
        'appid': WEATHER_MAP_API_KEY,
        'units': 'imperial'
    }
    response = requests.get(WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
    weather_data = response.json()

    if 'name' in weather_data:
        weather_label.config(text=f"{weather_data['name']}: {weather_data['main']['temp']}°F", fg='white')
    else:
        weather_label.config(text="Error: Weather data not available for the entered location.", fg='red')

def get_location_weather():
    query_params = {
        "apiKey": IPBASE_API_KEY
    }
    response = requests.get(IPBASE_API_ENDPOINT, params=query_params)
    city_name = response.json()["data"]["location"]["city"]["name"]

    weather_query_params = {
        'q': city_name,
        'appid': WEATHER_MAP_API_KEY,
        'units': 'imperial'
    }
    response = requests.get(WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
    weather_data = response.json()

    if 'name' in weather_data:
        weather_label.config(text=f"{weather_data['name']}: {weather_data['main']['temp']}°F", fg='white')
    else:
        weather_label.config(text="Error: Weather data not available for the current location.", fg='red')

root = tk.Tk()
root.title("Weather Forecasting App")
root.geometry("400x200")

input_label = tk.Label(root, text="Enter city or IP address:")
input_label.pack()

input_field = tk.Entry(root)
input_field.pack()

submit_button = tk.Button(root, text="Get Weather", command=get_weather)
submit_button.pack()

location_button = tk.Button(root, text="Use Current Location", command=get_location_weather)
location_button.pack()

weather_label = tk.Label(root, text="")
weather_label.pack()

root.mainloop()