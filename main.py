import requests


if __name__ == '__main__':
    openweathermap_url_api = "http://api.openweathermap.org/data/2.5/weather/"
    weatherapi_url = "http://api.weatherapi.com/v1/current.json"
    weatherbit_url = "https://api.weatherbit.io/v2.0/current/"
    town = input("Введите город (желательно на английском):")

    params_openweathermap = {"APPID": "b99acbecb6f7073cec5096866817cd5c", "q": town}
    params_weatherbit = {"key": "eab701c961cc45b8921548a11213f7f3", "city": town}

    open_weather = requests.get(openweathermap_url_api, params=params_openweathermap).json()
    lon, lat = open_weather['coord']['lon'], open_weather['coord']['lat']
    weatherbit = requests.get(weatherbit_url, params=params_weatherbit).json()
    print(weatherbit)

    params_weatherapi = {"key": "0f2b5a1e0da84e0a946155242202910", "q": town}
    weatherapi = requests.get(weatherapi_url, params=params_weatherapi).json()

    temp_weatherbit = weatherbit['data'][0]['temp']
    temp_weatherapi = weatherapi['current']['temp_c']
    temp_open = -272.15 + open_weather["main"]["temp"]  # Перевод из Кельвинов в Цельсии

    print("Openweather:", round(temp_open, 1), "\nWeatherApi:",
          temp_weatherapi, "\nWeatherBit:",
          temp_weatherbit)

