import datetime
from flask import Flask, abort, jsonify
import os
import requests
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


app = Flask(__name__)


def get_weather_data(city):
    apiKey = os.environ.get("APPID")
    api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}&units=metric"
    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()

        forecasts = []
        for day in weather_data["list"]:
            if day["dt_txt"].split()[1] == "12:00:00":
                nextDate = day["dt_txt"]
                temperature = day["main"]["temp"]
                weather = day["weather"][0]["main"]
                forecasts.append(
                    {
                        "date": nextDate,
                        "temperature": temperature,
                        "weather": weather,
                        "created_at": datetime.datetime.now(),
                    },
                )

        return {
            "city": weather_data["city"]["name"],
            "forecasts": forecasts,
        }
    else:
        return None


@app.route("/api/v1/weather/<string:city>")
def get_weather(city):
    weather_data = get_weather_data(city)

    if weather_data:
        for forecast in weather_data["forecasts"]:
            data = {
                "city": weather_data["city"],
                "temperature": forecast["temperature"],
                "weather": forecast["weather"],
                "created_at": forecast["date"],
            }
            supabase.table("weather_data").insert(data).execute()

        return jsonify({"city": city, "weather_data": weather_data})
    else:
        return abort(404, "City not found")


app.run()
