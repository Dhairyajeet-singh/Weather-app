import requests
import json
import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
def create_database(report):
    conn=sqlite3.connect('weather_data.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather
            (date TEXT, city TEXT, temp REAL, humidity REAL, pressure REAL, wind_speed REAL)''')
    c.execute("INSERT INTO weather (date, city, temp, humidity, pressure, wind_speed) VALUES (?, ?, ?, ?, ?, ?)",
            (report['Date'], report['City'], report['Temperature'], report['Humidity'], report['Pressure'], report['Wind']))
    conn.commit()
    conn.close()
def weather_app(api_key, city):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather"
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"

    try:
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            return f"City {city} not founded"
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']


        prms = {
            "lat": lat,
            "lon": lon,
            'appid': api_key,
            'units': 'metric'
        }


        weather_response = requests.get(weather_url, params=prms)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        main = weather_data['main']
        weather = weather_data['weather'][0]
        wind = weather_data['wind']
        clouds = weather_data['clouds']

        report = {
             'City': city,
             'Temperature': main['temp'],
             'Weather': weather['description'],
             'Humidity': main['humidity'],
             'Pressure': main['pressure'],
             'Wind': wind['speed'],
             'Cloud': clouds['all']
        }
        conn=sqlite3.connect('weather_data2.db')
        c=conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS weather
                (city TEXT, temp REAL, humidity REAL, pressure REAL, wind_speed REAL)''')
        c.execute("INSERT INTO weather (city, temp, humidity, pressure, wind_speed) VALUES (?, ?, ?, ?, ?)",
                (report['City'], report['Temperature'], report['Humidity'], report['Pressure'], report['Wind']))
        conn.commit()
        conn.close()
        return report
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occured: {conn_err}")
    except requests.exceptions.Timeout as tm_error:
        print(f"Timeout error occurred: {tm_error}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        
def weather_for_some_date(api_key, city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"

    dates = []
    date = input("Enter dates seprated by a commas (for ex 'YYYY-MM-DD','YYYY-MM-DD',....):")
    date_list = date.split(',')
   
    for date_str in date_list:
        try:
            date_datetime = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
            dates.append(date_datetime)
        except ValueError: 
            print(f"Entered date {date} is in wrong format use format 'YYYY-MM-DD','YYYY-MM-DD'...")
    try:
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            return f"City {city} not founded"
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        print("----------------WEATHER REPORT--------------------")
        for date in dates:
            timestamp = int(datetime.datetime(date.year, date.month, date.day).timestamp())

            prms = {
                "lat": lat,
                "lon": lon,
                'appid': api_key,
                'units': 'metric',
                'dt':timestamp
            }


            weather_response = requests.get(weather_url, params=prms)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            main = weather_data['main']
            weather = weather_data['weather'][0]
            wind = weather_data['wind']
            clouds = weather_data['clouds']

            report = {
                'City': city,
                'Date': date.strftime('%Y-%m-%d'),
                'Temperature': main['temp'],
                'Weather': weather['description'],
                'Humidity': main['humidity'],
                'Pressure': main['pressure'],
                'Wind': wind['speed'],
                'Cloud': clouds['all']
            }
            for key, value in report.items():
                print(f"{key}: {value}")
            print('\n')
            create_database(report)
            return report
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occured: {conn_err}")
    except requests.exceptions.Timeout as tm_error:
        print(f"Timeout error occurred: {tm_error}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
def hist_weather(API_key,city):
    url=f"https://api.weatherbit.io/v2.0/history/daily"
    prms = {
        'city': city,
        'start_date': '2024-06-01',
        'end_date': '2024-08-01',
        'key': API_key
    }
    response = requests.get(url, params=prms)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()
def prediction(data):
    df = pd.DataFrame(data)

if __name__=='__main__':
    print("WEATHER STATION")
    print("1. Weather report for a city")
    print("2. Predictive Analysis for future weather prediction")
    print("3. Weather for a specific or multiple dates")
    print("4. Check database")
    print("5. EXIT ")
    choice = input("Select Feature ['1','2','3','4','5']\n")
    
    if choice == '1':
        city = input("Enter your city: ")
        api_key = '5f74547800ab55e06053217dbdc5eb3d' #create your own api over openweatherapp website and use it sign up in the website then click over your profile a dropdown menu will open
                                #go to api key make your api key
        weather = weather_app(api_key,city)

        if isinstance(weather, dict):
            print("\nWeather Report:")
            for key, value in weather.items():
                print(f"{key}: {value}")
        else:
            print(weather)
    elif choice=='2':
        city=input("enter city")
        API_key="4df673486bee46629b534df494a08e1f"
        weather_data = hist_weather(API_key,city)
        print(weather_data)
        print('\n')
        print('\n')
        print('above mentioned data is historical data for the city provided for prediction, though I am unable to finish rest of the prediciton model')
    elif choice=='3':
        city = input("Enter your city: ")
        api_key = '5f74547800ab55e06053217dbdc5eb3d' #create your own api over openweatherapp website and use it sign up in the website then click over your profile a dropdown menu will open
                                #go to api key make your api key
        weather = weather_for_some_date(api_key,city)

        if isinstance(weather, dict):
            print("\nWeather Report:")
            for key, value in weather.items():
                print(f"{key}: {value}")
        else:
            print(weather)

    elif choice=='4':
        def get_weather_data():
            conn = sqlite3.connect('weather_data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM weather")
            data = c.fetchall()
            conn.close()
            return data
        def get_weather_data_two():
            conn = sqlite3.connect('weather_data2.db')
            c = conn.cursor()
            c.execute("SELECT * FROM weather")
            data = c.fetchall()
            conn.close()
            return data
        def show_data():
            weather_data = get_weather_data()
            for row in weather_data:
                tree.insert("", "end", values=row)
        def show_data_two():
            weather_data=get_weather_data_two()
            for row in weather_data:
                tree.insert("","end",values=row)

        subchoice = input("Enter '1' for weather data with date or '2' for weather data without date: ")
        if subchoice == '1':
            app = tk.Tk()
            app.title("Weather Database")

            # Treeview to display data
            tree = ttk.Treeview(app, columns=("City", "Temperature", "Humidity", "Pressure", "Wind Speed"), show='headings')
            tree.heading("City", text="City")
            tree.heading("Temperature", text="Temperature")
            tree.heading("Humidity", text="Humidity")
            tree.heading("Pressure", text="Pressure")
            tree.heading("Wind Speed", text="Wind Speed")
            tree.pack()
            load_button = tk.Button(app, text="Load Weather Data", command=show_data)
            load_button.pack()

            app.mainloop()
            
        elif subchoice == '2':
            app = tk.Tk()
            app.title("Weather Database 2")

            # Treeview to display data
            tree = ttk.Treeview(app, columns=("City", "Temperature", "Humidity", "Pressure", "Wind Speed"), show='headings')
            tree.heading("City", text="City")
            tree.heading("Temperature", text="Temperature")
            tree.heading("Humidity", text="Humidity")
            tree.heading("Pressure", text="Pressure")
            tree.heading("Wind Speed", text="Wind Speed")
            tree.pack()
            load_button = tk.Button(app, text="Load Weather Data", command=show_data_two)
            load_button.pack()

            app.mainloop()
    elif choice=='5':
        print("EXITING IN 3 2 1...")
