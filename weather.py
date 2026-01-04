import sys
import json
import requests
import textwrap
import datetime
import configparser
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path


config = configparser.ConfigParser()
config.read(Path(__file__).with_name('settings.cfg'))
api_key = config.get('API', 'api_key')

# The forecast provides a detailed weather prediction,
# while the weather field gives a simplified version that I will use in this application
# (the example using the forecast is commented out and was implemented for practice purposes)

# API call

url_info = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"


# httpResponse = requests.get(url_info)

# # print(json.dumps(httpResponse.json(), indent=3))

# if httpResponse.status_code == 200:
#     data = httpResponse.json()
#     if len(data):
#         coordinates = dict()
#         coordinates['lat'] = data["coord"]["lat"]
#         coordinates['lon'] = data["coord"]["lon"]
#     else:
#         sys.exit(f"Location not found for {city}")
# else:
#     sys.exit(f"{httpResponse.status_code} {httpResponse.reason}")


# latitude = str(coordinates['lat'])
# longitude = str(coordinates['lon'])

# # print(f"{latitude}; {longitude}")

# count = 8  # json gives us 3-hour increments, 3h*8 means that we have a 24-hour forecast

# url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&cnt={count}&lat={latitude}&lon={longitude}&appid={api_key}"

# httpResponseForecast = requests.get(url_forecast)

# if httpResponseForecast.status_code != 200:
#     sys.exit(f"{httpResponseForecast.status_code} {httpResponseForecast.reason}")

# print(json.dumps(httpResponseForecast.json(), indent=3))


def get_weather(city):
    result = requests.get(url_info.format(city, api_key))
    if result:
        json = result.json()
        # I want to extract the forecast information and store it in a tuple
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin-273.15
        temp_fahrenheit = (temp_kelvin-273.15)*9/5+32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']

        info = (city, country, temp_celsius, temp_fahrenheit, icon, weather)

        return info

    else:
        return None


def search():
    city = city_text.get()
    weather_final = get_weather(city)
    if weather_final:
        location_lbl['text'] = f"{weather_final[0]}, {weather_final[1]}"

        img = Image.open(f"./icons/{weather_final[4]}.png")
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)

        image.config(image=photo)
        image.image = photo

        temp_lbl['text'] = f"{weather_final[2]:.2f}°C, {weather_final[3]:.2f}°F"
        weather_lbl['text'] = weather_final[5]
    else:
        messagebox.showerror("Error", f"Cannot find {city}")

# App UI


app = Tk()
app.title("Weather App")
app.geometry('700x350')

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

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
