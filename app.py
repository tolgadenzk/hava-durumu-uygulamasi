import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests

load_dotenv()  # .env dosyasını yükle
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # API anahtarını güvenli şekilde al

app = Flask(__name__)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        weather = get_weather(city)
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)