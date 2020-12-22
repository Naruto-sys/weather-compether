import requests
from flask import Flask, render_template, request


def get_weather(town):
    response = {}
    openweathermap_url_api = "http://api.openweathermap.org/data/2.5/weather/"
    weatherapi_url = "http://api.weatherapi.com/v1/current.json"
    weatherbit_url = "https://api.weatherbit.io/v2.0/current/"
    params_openweathermap = {"APPID": "b99acbecb6f7073cec5096866817cd5c", "q": town}
    params_weatherbit = {"key": "eab701c961cc45b8921548a11213f7f3", "city": town}
    try:
        open_weather = requests.get(openweathermap_url_api, params=params_openweathermap).json()
        lon, lat = open_weather['coord']['lon'], open_weather['coord']['lat']
        weatherbit = requests.get(weatherbit_url, params=params_weatherbit).json()
        params_weatherapi = {"key": "0f2b5a1e0da84e0a946155242202910", "q": town}
        weatherapi = requests.get(weatherapi_url, params=params_weatherapi).json()
        temp_weatherbit = weatherbit['data'][0]['temp']
        temp_weatherapi = weatherapi['current']['temp_c']
        temp_open = -272.15 + open_weather["main"]["temp"]  # Перевод из Кельвинов в Цельсии
        response["openweather"] = round(temp_open, 1)
        response["weatherapi"] = temp_weatherapi
        response["weatherbit"] = temp_weatherbit
    except KeyError:
        return {"error": 1}

    return response


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index(dictionary={}):
    sites = []
    if dictionary != {}:
        if "error" in dictionary.keys():
            sites.append("Простите, но нам не удалось найти информацию об этом городе,"
                         " проврьте правильность написания")
        else:
            for key in dictionary.keys():
                a = "По сайту " + key[0].upper() + key[1:] + " сейчас в этом городе " + str(dictionary[key])
                sites.append(a)
            a = "Средняя оценка температуры по всем данным: " + str(round(sum(dictionary.values()) / len(dictionary.keys()), 1))
            sites.append(a)
    return render_template('main_page.html', sites=sites, length=len(sites))


@app.route('/', methods=['POST'])
def index_post():
    city = request.form['form-control']
    return index(dictionary=get_weather(city))


if __name__ == '__main__':
    app.run(port=8006, host='127.0.0.1')
