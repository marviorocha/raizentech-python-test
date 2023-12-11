from flask import Flask, abort, jsonify
import os
import requests

app = Flask(__name__)


def get_weather_data(city):
    apiKey = os.environ.get("APPID")
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.route("/weather/<string:city>")
def get_weather(city):
    apiKey = os.environ.get("APPID")
    weather_data = get_weather_data(city)

    lat = weather_data["coord"]["lat"]
    lon = weather_data["coord"]["lon"]

    api_forecast = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apiKey}"
    response = requests.get(api_forecast)

    if response.status_code == 200:
        return response.json()
    else:
        return abort(404, "City not found")


app.run(debug=True)
