'''
Hello you scripters that are reading this !!!
My code is really wack there are some improvements that I already know I have to make.
This is my first time using beautifulSoup4 so I dont know much. Thus most of my code is stiched together :)
This was tested on linux but because this is python we are talking about it should work on Windows and Mac.
'''
import re
from datetime import datetime
import bs4
import requests

zipCode = "Your Zip Code In Here"

def log_check():  # Not needed but it may help to be able to look at logs
    # Read csv and extract all the data inside it
    file = open('Weather Observation.csv', 'r')
    temp_list = []
    contents = []
    for l in file.readlines():
        temp_list.append(l)
    for i in temp_list:
        contents.append(i.strip('\n').split(','))
    ## User Input Section
    usr_input = input(": ")
    if usr_input == '0':
        for i in contents:
            print(i)
    # If statement shorter
    choice_loop = 0
    list_index = -1
    for i in range(9):
        i += 1
        choice_loop += 1
        list_index += 1
        if usr_input == str(choice_loop):
            for i in contents:
                print(i[list_index])
            break
    else:
        pass
    file.close()


def main():
    # req will request the websites source
    req = requests.get('https://weather.com/weather/today/l/' + zipCode + ':4:US')
    # Raise any errors that may have occurred
    try:
        req.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % exc)
        return
        # This will tell BS4 that we are reading html
    weatherSoup = bs4.BeautifulSoup(req.text, features="html.parser")
    ## Creating Variables
    # Place Your At
    div = weatherSoup.findAll("div", {"class": "CurrentConditions--header--3-4zi"})
    place = div[0].getText()
    # Weather
    div = weatherSoup.findAll("div", {"class": "CurrentConditions--primary--3xWnK"})
    weather = div[0].getText()
    weatherDetails = weatherSoup.findAll("div", {"class": "WeatherDetailsListItem--wxData--23DP5"})
    # Humidity
    humidity = ""
    humidityRegEx = re.compile(r'\d{1,3}\%')  # This will allow us to search for a number with three or less chars
    hum = ""  # This var is made here but assigned later
    for i in enumerate(weatherDetails):
        if True if "PercentageValue" in str(i) else False:  # If the str is found anywhere in i then its true else its false
            hum = humidityRegEx.search(str(i))  # Searches for '\d{1,3}\%' in i
            humidity = str(i)[hum.start():hum.end()]
            break
    # Wind Speed
    windspeed = ""
    windspeedRegEx = re.compile(r'\d{1,3} mph')
    wind = ""
    for i in weatherDetails:
        if True if "Wind" in str(i) else False:
            wind = windspeedRegEx.search(str(i))
            windspeed = str(i)[wind.start():wind.end()]
            break
    # Sunrise Time
    div = weatherSoup.findAll("div", {"class": "SunriseSunset--sunriseDateItem--2ATeV"})
    sunrise = div[0].getText()
    # Sunset Time
    div = weatherSoup.findAll("div", {"class": "SunriseSunset--sunsetDateItem--2_gJb SunriseSunset--sunriseDateItem--2ATeV"})
    sunset = div[0].getText()

    # Temperature
    div = weatherSoup.findAll("div", {"class": "CurrentConditions--primary--3xWnK"})
    temperature = ""
    temperatureRegEx = re.compile(r'\d{1,3}°')
    temp = ""
    for i in div:
        if True if "TemperatureValue" in str(i) else False:
            temp = temperatureRegEx.search(str(i))
            temperature = str(i)[temp.start():temp.end()]
            break
    # Real Feel
    div = weatherSoup.findAll("div", {"class": "TodayDetailsCard--feelsLikeTemp--2GFqN"})
    RealFeel = ""
    realfeelRegEx = re.compile(r'\d{1,3}°')
    temp = ""
    for i in div:
        if True if "TemperatureValue" in str(i) else False:
            temp = realfeelRegEx.search(str(i))
            RealFeel = str(i)[temp.start():temp.end()]
            break
    # Weather Observation
    div = weatherSoup.findAll("div", {"class": "CurrentConditions--phraseValue--2xXSr"})
    weatherOb = div[0].getText()
    # The file building
    now = datetime.now()
    # dd/mm/YY H:M
    date_string = now.strftime("%m/%d/%Y")
    time_string = now.strftime("%H:%M")
    formatted_text = [date_string, time_string, weatherOb, temperature, windspeed, humidity, RealFeel, sunrise[8:], sunset[6:]]
    formatted_text = ','.join(formatted_text) + "\n"
    file = open("Weather Observation.csv", "a")
    file.write(formatted_text)
    file.close()


main()
