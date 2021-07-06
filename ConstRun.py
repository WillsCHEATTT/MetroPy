# This version just runs every 10 mins (This is technecly what the "Main" script should be)
# Oh and sorry for lack of comments in this code. main.py and mainWITHusr_input.py Have comments for this code if you would like them : )
import re
from datetime import datetime
import bs4
import requests
import time

zipCode = "Put Zipcode Here"
try: 
    def main():
        req = requests.get('https://weather.com/weather/today/l/' + zipCode + ':4:US')
        try:
            req.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % exc)
            return
        weatherSoup = bs4.BeautifulSoup(req.text, features="html.parser")
        div = weatherSoup.findAll("div", {"class": "CurrentConditions--header--3-4zi"})
        place = div[0].getText()
        div = weatherSoup.findAll("div", {"class": "CurrentConditions--primary--3xWnK"})
        weather = div[0].getText()
        weatherDetails = weatherSoup.findAll("div", {"class": "WeatherDetailsListItem--wxData--23DP5"})
        humidity = ""
        humidityRegEx = re.compile(r'\d{1,3}\%')
        hum = ""
        for i, j in enumerate(weatherDetails):
            if True if "PercentageValue" in str(j) else False:
                hum = humidityRegEx.search(str(j))
                humidity = str(j)[hum.start():hum.end()]
                break
        windspeed = ""
        windspeedRegEx = re.compile(r'\d{1,3} mph')
        wind = ""
        for i in weatherDetails:
            if True if "Wind" in str(i) else False:
                wind = windspeedRegEx.search(str(i))
                windspeed = str(i)[wind.start():wind.end()]
                break
        div = weatherSoup.findAll("div", {"class": "SunriseSunset--sunriseDateItem--2ATeV"})
        sunrise = div[0].getText()
        div = weatherSoup.findAll("div", {"class": "SunriseSunset--sunsetDateItem--2_gJb SunriseSunset--sunriseDateItem--2ATeV"})
        sunset = div[0].getText()
        div = weatherSoup.findAll("div", {"class": "CurrentConditions--primary--3xWnK"})
        temperature = ""
        temperatureRegEx = re.compile(r'\d{1,3}')
        temp = ""
        for i in div:
            if True if "TemperatureValue" in str(i) else False:
                temp = temperatureRegEx.search(str(i))
                temperature = str(i)[temp.start():temp.end()]
                break
        div = weatherSoup.findAll("div", {"class": "TodayDetailsCard--feelsLikeTemp--2GFqN"})
        RealFeel = ""
        realfeelRegEx = re.compile(r'\d{1,3}°')
        temp = ""
        for i in div:
            if True if "TemperatureValue" in str(i) else False:
                temp = realfeelRegEx.search(str(i))
                RealFeel = str(i)[temp.start():temp.end()]
                break
        div = weatherSoup.findAll("div", {"class": "CurrentConditions--phraseValue--2xXSr"})
        weatherOb = div[0].getText()
        now = datetime.now()
        date_string = now.strftime("%m/%d/%Y")
        time_string = now.strftime("%H:%M")
        formatted_text = [date_string, time_string, weatherOb, temperature, windspeed, humidity, RealFeel, sunrise[8:], sunset[6:]]
        formatted_text = ','.join(formatted_text) + "\n"
        file = open("Weather Observation.csv", "a")
        file.write(formatted_text)
        file.close()


    while True:
        t = datetime.now()
        time.sleep(60*10)  # I'm up at 2 in the morning this line remindes me to sleep
        print(t.now())
        main()
except:
    print('Error occured. Probably a connection error')
