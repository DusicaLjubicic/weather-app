import sys
import json
import requests
import textwrap
import datetime
import configparser
from tkinter import *
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


def search():
    pass


app = Tk()
app.title("Weather App")
app.geometry('700x350')

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()  # pack smesti na ekran

search_btn = Button(app, text="Search weather", width=12, command=search)
search_btn.pack()

location_lbl = Label(app, text='', font=('bold', 20))
location_lbl.pack()

image = Label(app, bitmap='')
image.pack()

temp_lbl = Label(app, text='')
temp_lbl.pack()

weather_lbl = Label(app, text='')
weather_lbl.pack()


app.mainloop()
