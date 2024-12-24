import requests
import json
import os
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError
from pprint import pprint
load_dotenv('config.env')

accuweather_token = os.getenv('accuweather_token')


class MyError(Exception):
    def __init__(self, name, desc):
        super().__init__(self, name)
        self.name = name
        self.desc = desc


class Weather:
    def __init__(self, location):
        self.location = location
        self.location_key = self.get_key()

    def get_key(self):
        """
        Searching the AccuWeather location key

        Args:
            location: The query string of the location (e.g., "London", "New York")

        Returns:
            accuweather location key(string) if found location,
            or None if there is an error or loc is not found
        """
        search_url = 'http://dataservice.accuweather.com/locations/v1/search'

        params = {'q': self.location,
                  'apikey': accuweather_token}
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            return response.json()[0]['Key']
        except IndexError as e:
            print(f'IndexError: {e}')
            raise MyError(f'city {self.location} not found',
                          desc='Проверьте правильность введенных данных')
        except HTTPError as e:
            if e.response.status_code == 503:
                txt = json.loads(e.response.text)
                msg = txt.get('Message')
                if msg:
                    raise MyError(
                        'wrong API key', desc='Возможно ваш API-ключ достиг лимита, или неверный')
                else:
                    raise e
            else:
                raise e
        except ConnectionError:
            raise MyError(
                'API unavailable', desc='Возможно у вас отсутствует соединение, или недоступен API-сервис ')

    def get_forecast(self, days_nums=1):
        weather_url = f'http://dataservice.accuweather.com/forecasts/v1/daily/{
            days_nums}day/{self.location_key}'
        params = {'apikey': accuweather_token, 'details': True, 'metric': True}
        try:
            response = requests.get(weather_url, params=params)
            response.raise_for_status()
            forecast_data = response.json()['DailyForecasts']
            return [
                {
                    'date': day['Date'],
                    'temperature': day['Temperature']['Minimum']['Value'],
                    'wind_speed': day['Day']['Wind']['Speed']['Value'],
                    'humidity': day['Day']['RelativeHumidity']['Average'],
                    'rain_chance': day['Day']['RainProbability']
                } for day in forecast_data
            ]
        except HTTPError as e:
            raise MyError('API Error', desc=str(e))
        except ConnectionError:
            raise MyError(
                'API unavailable', desc='Проблемы с соединением или недоступен API сервис')


class BadWeatherModel:
    temp_thresholds = (-7, 29)
    wind_speed_threshold = 50
    humidity_threshold = 65
    rain_chance_threshold = 80

    @classmethod
    def is_weather_bad(cls, weather_data):
        if all(key in weather_data for key in ['temperature', 'wind_speed', 'humidity', 'rain_chance']):
            is_temp_bad = weather_data['temperature'] not in range(
                *cls.temp_thresholds)
            is_wind_bad = weather_data['wind_speed'] > cls.wind_speed_threshold
            is_humidity_bad = weather_data['humidity'] > cls.humidity_threshold
            is_rain_bad = weather_data['rain_chance'] > cls.rain_chance_threshold
            return any((is_temp_bad, is_wind_bad, is_humidity_bad, is_rain_bad))
        return True


if __name__ == '__main__':
    accuweather_token = os.getenv('accuweather_token')
    weather_loc = Weather('London')
    # print(weather_loc.get_one_day_forecast())
    print(BadWeatherModel.is_weather_bad({'temperature': 20,
                                          'wind_speed': 40,
                                          'humidity': 40,
                                          'rain_chance': 1000}))
