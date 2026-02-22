from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Mapping Open-Meteo codes to Lucide Icon names
ICON_MAP = {
    0: "sun", 1: "cloud-sun", 2: "cloud-sun", 3: "cloud",
    45: "cloud-fog", 48: "cloud-fog", 51: "cloud-drizzle",
    61: "cloud-rain", 71: "snowflake", 95: "cloud-lightning"
}

def get_weather_data(city):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_data = requests.get(geo_url).json()

        if not geo_data.get("results"):
            return {"error": "Location not found"}

        loc = geo_data["results"][0]
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['latitude']}&longitude={loc['longitude']}&current_weather=true&hourly=relative_humidity_2m"
        w_data = requests.get(weather_url).json()
        
        current = w_data["current_weather"]
        
        return {
            "city": loc["name"],
            "country": loc.get("country_code", ""),
            "temp": round(current["temperature"]),
            "wind": current["windspeed"],
            "icon": ICON_MAP.get(current["weathercode"], "cloud"),
            "success": True
        }
    except:
        return {"error": "Connection lost"}

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        weather = get_weather_data(city)
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)