import json
import requests
import sys
import pytemperature
import twilio_send_message

# Compute location from command line arguments.
if len(sys.argv) < 2:
    print('Usage: quickWeather.py location')
    sys.exit()


def get_weather(lat, lon):
    # Download the JSON data from OpenWeatherMap.org's API
    url = """http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=""".format(
        sys.argv[1], sys.argv[2])

    response = requests.get(url)
    response.raise_for_status()

    # Load JSON data into a Python variable.
    weatherData = json.loads(response.text)
    #print(json.dumps(weatherData, indent=4, sort_keys=True))
    relevant_temp = {}
    relevant_weather = {}

    for w, v in weatherData.items():
        if w == 'list':
            for w1 in v:
                for w2, w3 in w1.items():
                    if w2 == 'dt_txt':
                        for w4, w5 in w1.get("main").items():
                            if w4 == 'temp':
                                relevant_temp[w3] = w5

    for w, v in weatherData.items():
        if w == 'list':
            for w1 in v:
                for w2, w3 in w1.items():
                    if w2 == 'dt_txt':
                        relevant_weather[w3] = ''
                    elif w2 == 'weather':
                        for k, v in relevant_weather.items():
                            relevant_weather[k] = w3

    # print(relevant_weather)
    my_message = ""
    for k, v in relevant_weather.items():
        if k.endswith('20 09:00:00'):
            for k1, v1 in v[0].items():
                if k1 == 'description':
                    my_message = v1

    if my_message == 'broken clouds':
        my_message = ("В Києві завтра зранку мінлива хмарність, ")

    for k, v in relevant_temp.items():
        if k.endswith('20 09:00:00'):
            my_message += ("температура повітря %s" % str(round(pytemperature.k2c(v))) + "C")

    return my_message


#get_weather(sys.argv[1], sys.argv[2])
twilio_send_message.textmyself(get_weather(sys.argv[1], sys.argv[2]))
