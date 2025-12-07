import sys
import json
import requests
import textwrap
import datetime
import configparser
from pathlib import Path

city = "Belgrade"

config = configparser.ConfigParser()
config.read(Path(__file__).with_name('settings.cfg'))
api_key = config.get('API', 'api_key')

# forecast izbacuje detaljnu prognozu
# weather samo trenutnu

url_info = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

httpResponse = requests.get(url_info)

# print(json.dumps(httpResponse.json(), indent=3))

if httpResponse.status_code == 200:
    data = httpResponse.json()
    if len(data):
        coordinates = dict()
        coordinates['lat'] = data["coord"]["lat"]
        coordinates['lon'] = data["coord"]["lon"]
    else:
        sys.exit(f"Location not found for {city}")
else:
    sys.exit(f"{httpResponse.status_code} {httpResponse.reason}")


latitude = str(coordinates['lat'])
longitude = str(coordinates['lon'])

# print(f"{latitude}; {longitude}")

count = 8  # json odgovor mi vraca inkremente od 3h, 3h*8 znaci imam prognozu za 24h

url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&cnt={count}&lat={latitude}&lon={longitude}&appid={api_key}"

httpResponseForecast = requests.get(url_forecast)

if httpResponseForecast.status_code != 200:
    sys.exit(f"{httpResponseForecast.status_code} {httpResponseForecast.reason}")

print(json.dumps(httpResponseForecast.json(), indent=3))
