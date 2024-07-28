from customtkinter import *
import requests
import json
import datetime
from PIL import ImageTk, Image
 

set_appearance_mode("Dark")
set_default_color_theme("green")

window = CTk()
window.title("Weather App")
window.geometry("550x850")
window.resizable(False, False)

dt = datetime.datetime.now()

# Images

cloudy_img = CTkImage(Image.open("Images/cloud.png"), size=(200,200))
sunny_img = CTkImage(Image.open("Images/sun.png"), size=(200,200))
rainy_img = CTkImage(Image.open("Images/heavy-rain.png"), size=(200,200))
api_key = "" # Your OpenWeatherMap API key
 
 
def city_name():
 
    api_request = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+ city_entry.get() + "&units=metric&appid="+api_key)
 
    api = json.loads(api_request.content)
 
    y = api['main']
    temprature = y['temp']
    humidity = y['humidity']

    x = api['coord']
    longtitude = x['lon']
    latitude = x['lat']
 
    z = api['sys']
    country = z['country']
    city = api['name']

    weather = api["weather"]
    weather_main = weather[0]["main"]
    weather_description = weather[0]["description"]

    visibility = api["visibility"]
    wind_speed = api["wind"]["speed"]

    if weather_main == "Rain":
        img_label.configure(image=rainy_img)
    elif weather_main == "Clouds":
        img_label.configure(image=cloudy_img)
    elif weather_main == "Clear":
        img_label.configure(image=sunny_img)

    temp_label.configure(text=f"{temprature}°C")
    humidity_value_label.configure(text=f"{humidity} %")
    longitude_value_label.configure(text=longtitude)
    latitude_value_label.configure(text=latitude)
    country_value_label.configure(text=country)
    city_value_label.configure(text=city)
    hour_value_label.configure(text=dt.strftime('%I : %M %p'))
    date_value_label.configure(text=dt.strftime('%A'))
    month_value_label.configure(text=dt.strftime('%m %B'))
    weather_value_label.configure(text=weather_main)
    weather_desc_value_label.configure(text=weather_description)
    visibility_value_label.configure(text=f"{visibility/1000} KM")
    wind_speed_value_label.configure(text=f"{wind_speed} m/s")
 

city_entry = CTkEntry(window, width=380, height=40)
city_entry.place(x=10,y=20)

city_name_btn = CTkButton(window, text="Search", command=city_name, height=40)
city_name_btn.place(x=400,y=20)
 
city_label = CTkLabel(window, text="City: ", font=("Raleway", 20))
city_label.place(x=25, y=90)

city_value_label = CTkLabel(window, text="", font=("Raleway", 20))
city_value_label.place(x=80, y=90)
 
country_label = CTkLabel(window, text="Country: ", font=("Raleway", 20))
country_label.place(x=350, y=90)

country_value_label = CTkLabel(window, text="", font=("Raleway", 20))
country_value_label.place(x=450, y=90)

date_label = CTkLabel(window, text="Day: ", font=("Raleway", 20))
date_label.place(x=25, y=130)

date_value_label = CTkLabel(window, text="", font=("Raleway", 20))
date_value_label.place(x=80, y=130)

month_label = CTkLabel(window, text="Date: ", font=("Raleway", 20))
month_label.place(x=350, y=130)

month_value_label = CTkLabel(window, text="", font=("Raleway", 20))
month_value_label.place(x=450, y=130)

hour_label = CTkLabel(window, text="Time: ", font=("Raleway", 20))
hour_label.place(x=25, y=170)

hour_value_label = CTkLabel(window, text="", font=("Raleway", 20))
hour_value_label.place(x=80, y=170)

humidity_label = CTkLabel(window, text="Humidity: ", font=("Raleway", 20))
humidity_label.place(x=350, y=170)
 
humidity_value_label = CTkLabel(window, text="", font=("Raleway", 20))
humidity_value_label.place(x=450, y=170)
 
longitude_label = CTkLabel(window, text="Longitude: ", font=("Raleway", 20))
longitude_label.place(x=25, y=210)

longitude_value_label = CTkLabel(window, text="", font=("Raleway", 20))
longitude_value_label.place(x=130, y=210)

latitude_label = CTkLabel(window, text="Latitudes: ", font=("Raleway", 20))
latitude_label.place(x=350, y=210)

latitude_value_label = CTkLabel(window, text="", font=("Raleway", 20))
latitude_value_label.place(x=450, y=210)

weather_desc_label = CTkLabel(window, text="Description: ", font=("Raleway", 20))
weather_desc_label.place(x=25, y=250)

weather_desc_value_label = CTkLabel(window, text="", font=("Raleway", 20))
weather_desc_value_label.place(x=150, y=250)

weather_label = CTkLabel(window, text="Weather: ", font=("Raleway", 20))
weather_label.place(x=350, y=250)

weather_value_label = CTkLabel(window, text="", font=("Raleway", 20))
weather_value_label.place(x=450, y=250)

wind_speed_label = CTkLabel(window, text="Wind Speed: ", font=("Raleway", 20))
wind_speed_label.place(x=30, y=290)

wind_speed_value_label = CTkLabel(window, text="", font=("Raleway", 20))
wind_speed_value_label.place(x=150, y=290)

visibility_label = CTkLabel(window, text="Visibility: ", font=("Raleway", 20))
visibility_label.place(x=350, y=290)

visibility_value_label = CTkLabel(window, text="", font=("Raleway", 20))
visibility_value_label.place(x=450, y=290)
 
temp_label = CTkLabel(window, text="",font=("Helvetica", 100))
temp_label.place(x=85, y=400)

img_label = CTkLabel(window, text="")
img_label.place(x=160, y=550)

note_label = CTkLabel(window, text="All temperatures in degree celsius", font=("Raleway", 20))
note_label.place(x=115, y=800)
 
window.mainloop()
