import requests

def get_location():
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        if data['status'] == 'success':
            location = f"{data['city']}, {data['regionName']}, {data['country']}"
            return location
        else:
            return "Location: Unknown"
    except Exception as e:
        return f"Location: Error {e}"