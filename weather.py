import requests

def get_location():
    # Get the user's IP address and location
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data['status'] == 'success':
            return data['city'], data['lat'], data['lon']
        else:
            print("Could not retrieve location.")
            return None, None, None
    except Exception as e:
        print(f"Error retrieving location: {e}")
        return None, None, None

def get_weather_and_aqi():
    # Replace these with your actual API keys and URLs
    weather_api_key = "2321b3b8fff8cce73315c7759b112276"
    aqi_api_key = "4082a24fbd9f92c377a45bfbd9782ebdbbdcbf4b"

    # Get the user's location
    city, lat, lon = get_location()
    if city is None:
        return "Location not found."

    # Use the city name and coordinates to fetch weather and AQI data
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    aqi_url = f"http://api.waqi.info/feed/geo:{lat};{lon}/?token={aqi_api_key}"

    # Get weather data
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    if weather_response.status_code == 200:
        temp = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
    else:
        temp = "N/A"
        weather_description = "N/A"

    # Get AQI data
    aqi_response = requests.get(aqi_url)
    aqi_data = aqi_response.json()
    if aqi_response.status_code == 200 and aqi_data['status'] == 'ok':
        aqi = aqi_data['data']['aqi']
    else:
        aqi = "N/A"

    return f"Temp: {temp}°C, Weather: {weather_description}, AQI: {aqi}"