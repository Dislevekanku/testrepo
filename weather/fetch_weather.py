import datetime
import json
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

api_key = '0c1d440522e06f812858f8f9fbb9ba52'
lat = '38.8951'
lon ='-77.0364'


# If folder is not present, create it

data_folder = 'openweathermap_data/raw_data'
if not os.path.isdir(data_folder):
    os.makedirs(data_folder)


# Generate the URL

url = 'https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&appid={2}&units=imperial'.format(
    lat, lon, api_key)

response = requests.get(url)
weather_data = response.json()
#current = datetime.current()
current_datetime = datetime.datetime.fromtimestamp(weather_data["current"]["dt"]).strftime('%Y_%m_%d_%H_%M')
filename = os.path.join(data_folder, 'weather_{0}.json'.format(current_datetime))

with open(filename, 'w+') as f:
    f.write(json.dumps(weather_data))

latest_filename = os.path.join(data_folder, 'weather.json')
with open(latest_filename, 'w+') as f:
    f.write(json.dumps(weather_data))


current_date_time = None
def get_latest_weather_data():
    global current_date_time
    filename = 'openweathermap_data/raw_data/weather.json'
    with open(filename) as f:
        data = json.load(f)
    df = pd.DataFrame(data['hourly'])

        # convert time into a proper datetime object
    df['time'] = pd.to_datetime(df['dt'])

    # set the current date time of the data in the global variable. This will be accessed later
    current_date_time = datetime.datetime.fromtimestamp(data['current']['dt']).strftime('%Y_%m_%d_%H_%M')
    return df

df = get_latest_weather_data()



def write_csv_file(dataframe):
    folder_name ='openweathermap_data/output_data/{0}'.format(current_date_time)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
        
    filename = os.path.join(folder_name, 'output.csv')
    dataframe.to_csv(filename, index=False)
write_csv_file(df)

def calculate_temperature_stats(dataframe):
    temperature_data = {'stat':'temp'}
    temperature_data['max'] = dataframe['temp'].max()
    temperature_data['min'] = dataframe['temp'].min()
    temperature_data['average'] = dataframe['temp'].mean()
    return temperature_data


stats = []
stats.append(calculate_temperature_stats(df))
stats

def calculate_windspeed_stats(dataframe):
    temperature_data = {'stat':'wind_speed'}
    temperature_data['max'] = dataframe['wind_speed'].max()
    temperature_data['min'] = dataframe['wind_speed'].min()
    temperature_data['average'] = dataframe['wind_speed'].mean()
    return temperature_data

stats.append(calculate_windspeed_stats(df))
stats

# Write the stats to a csv file
folder_name = 'openweathermap_data/output_data/{0}'.format(current_date_time)
filename = os.path.join(folder_name, 'output.csv')
pd.DataFrame(stats).to_csv(filename, index=False)


def plot_temperature(dataframe):
    folder_name = 'openweathermap_data/output_data/{0}'.format(current_date_time)
    filename = os.path.join(folder_name, 'temperature.png')
    df.plot.line(x='time', y='temp')
    plt.savefig(filename)
    
plot_temperature(df)

def plot_wind_speed(dataframe):
    folder_name = 'openweathermap_data/output_data/{0}'.format(current_date_time)
    filename = os.path.join(folder_name, 'wind_speed.png')
    df.plot.line(x='time', y='wind_speed')
    plt.savefig(filename)
    
plot_wind_speed(df)