###########################################################################
#                                                                         #
#             MetroPY ("Weather" you like this script or not)             #
#                                                                         #
#                                                                         #
#  Copyright (c) 2022, Zackery .R. Smith <zackery.smith@hsdgreenbush.org>.#
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.   #
#                                                                         #
###########################################################################
####     Huge thanks to mrHeavenli for updated webscraping method!     ####
###########################################################################

import requests
import bs4
import re
from typing import Optional
from datetime import date, time, datetime
from time import gmtime, strftime, sleep

regexes = {
	"tempature" : r"tempValue.*(?P<tempature>\b([0-9]|[1-9][0-9]|1[0-9]{2}|200)°)",
	"windspeed" : r"(?P<windspeed>([0-9]|[1-9][0-9]|100).mph)",
	"humidity" : r"PercentageValue.*(?P<humidity>\d([0-9]|[1-9][0-9]|100)%)",
	"realfeel" : r"feelsLikeTempValue.*(?P<realfeel>\d([0-9]|[1-9][0-9]|1[0-9]{2}|200)°)",
	"weatherob" : r"CurrentConditions--phraseValue--.+?>(?P<weatherob>.+?(?=<))"
}

def log_check():
    with open('Weather Observation.csv', 'r') as logfile:
        contents = [x.strip("\n").split(",") for x in logfile.readlines()]
        userinput = input()
        try:
            if int(userinput)-1 <= len(contents):
                for i in range(0, len(contents)): print(contents[i][int(userinput)-1])
        except (ValueError, IndexError): return

def parse_site(
        weathersoup: bs4.BeautifulSoup,
    ) -> list:
    weatherdata = [date.today().strftime("%m/%d/%y"), datetime.now().strftime("%H:%M")]+[""]*7

    span_string = "".join([str(span) for span in weathersoup.find_all("span")])
    data = [re.search(regex, span_string) for regex in regexes.values()]

    # Weather Observation
    weatherdata[2] = re.search(
            r"CurrentConditions--phraseValue--.+?>(?P<weatherob>.+?(?=<))", 
            "".join([str(div) for div in weathersoup.find_all("div")])
    ).group("weatherob")
    # Temperature, Windspeed, Humidity, and Realfeel
    for i in range(3, 6+1): weatherdata[i] = data[i-3].group(list(regexes.keys())[i-3])

    # Sunset & Sunrise
    matches = [
            re.sub(r"[apm\s]", "", i.text)
            for i in weathersoup.find_all("p")
            if re.match(".*SunriseSunset--dateValue.*", str(i))
    ]
    weatherdata[7], weatherdata[8] = matches[0], matches[1]
    

    return weatherdata


def main(zipcode: Optional[str]=None):
    # "Basic" Zipcode Check
    if zipcode == None:
        while True:
            if re.compile(r"^\d{5}$").search(zipcode := input("What is your zip code?\n:").strip()) is None:
                print("Hmm.. I don't recognize that as a proper zipcode (example zipcode: 75115)")
                continue
            break


    # req will request the websites source
    req = requests.get('https://weather.com/weather/today/l/' + zipcode + ':4:US')

    # Check if any errors occurred
    try: req.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % exc)
        return

    weathersoup = bs4.BeautifulSoup(req.text, features="html.parser")
    weatherdata = parse_site(weathersoup)

    try:
        with open("Weather Observation.csv", "a") as log_file: log_file.write(",".join(weatherdata)+"\n")
    except: pass

    print("Successfully Collected Data From " + zipcode)

    return zipcode

# Menu loop
while True:
    choice = input("\n1:   Check Logs\n2:   Get Data\n: ")
    if choice == '1': log_check()
    elif choice == '2': 
        zipcode = main()
        if input("Would you like to loop this process? [y, N]").lower() == "y":
            print("Ok, press ctrl+c to cancel")
            while True:
                try: main(str(zipcode)); sleep(60*10)
                except: sleep(60*5); continue
    else: continue
