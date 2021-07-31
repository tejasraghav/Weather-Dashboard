import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def weather_dashboard():
    return render_template("home.html")


@app.route("/weather", methods=["POST"])
def render_result():
    city = request.form["cityName"]
    api_key = get_api_key()
    data = get_weather_results(city, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["description"].capitalize()
    location = data["name"]
    return render_template("weather.html", location=location,
                           temp=temp, weather=weather, feels_like=feels_like)


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["weather_dashboard"]["api_key"]


def get_weather_results(city_name, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city_name, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == "__main__":
    app.run()
