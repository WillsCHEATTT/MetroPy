###########################################################################     
#                                                                         #     
#             MetroPY ("Weather" you like this script or not)             #     
#                                                                         #     
#                                                                         #     
#  Copyright (c) 2020, Zackery .R. Smith <zackery.smith@hsdgreenbush.org>.#     
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


# **Additional Notes
# Please understand i'm very new to website stuff so please bear in mind that my var names may be named improperly named.

import requests
import bs4
import re
from datetime import date, time, datetime
from time import gmtime, strftime

def log_check():
    print("Opening Weather Observation.csv")
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
    choice = 0
    list_index = -1
    for i in range(9):
        i += 1
        choice += 1
        list_index += 1
        if usr_input == str(choice):
            for i in contents:
                print(i[list_index])
            break
    else:
        pass
    print("Closing Weather Observation.csv")
    file.close()


def main():
    while True:
        print("What is your zip code?")
        zipCode = input()
        # build regex parser for zipcode
        zipcodeRegEx = re.compile(r'^\d{5}$')
        check = zipcodeRegEx.search(zipCode)
        # "Basic" Zipcode Check
        if check is None:
            print("Hmm.. I don't recognize " + zipCode + " as a proper zipcode. Use digit like 75115")
            continue
        break
    
    ## Making Quality Of Life Functions
    # Get Item In Class
    def get_class(class_name, index, regex = None):
        # req will request the websites source                                      
        req = requests.get('https://weather.com/weather/today/l/' + zipCode + ':4:US')
                                                                                  
        # Check if any errors occurred                                              
        try:                                                                        
            req.raise_for_status()                                                  
        except Exception as exc:                                                    
            print('There was a problem: %s' % exc)                                  
            return                                                                  
                                                                                    
        # This will tell BS4 that we are reading html                               
        weatherSoup = bs4.BeautifulSoup(req.text, features="html.parser")
   
        try:
            # If this code functions we know that the div has multi classes so we deal with it diffrently
            div = weatherSoup.findAll("div", {"class": f"{class_name}"})
            div[index + 1].getText()  # This will run a error if the div does not contain multi classes (Everything past this is the real deal)
            class_data = div[index].getText()
            regex = re.compile(regex)
            temp_data = regex.search(str(class_data))
            return str(class_data)[temp_data.start():temp_data.end()]
        except:
            div = weatherSoup.findAll("div", {"class": f"{class_name}"})
            return div[index].getText()
    
    ## Creating Variables
    # Place Your At
    place = get_class("CurrentConditions--header--1NDhO", 0)

    # Weather
    weather = get_class("CurrentConditions--phraseValue--17s79", 0)

    # Humidity
    humidity = get_class("ListItem--listItem--Gcuav WeatherDetailsListItem--WeatherDetailsListItem--2Coc5", 2, r'\d{1,3}\%')
    
    # Wind Speed
    windspeed = get_class("ListItem--listItem--Gcuav WeatherDetailsListItem--WeatherDetailsListItem--2Coc5", 1, r'\d{1,3} mph')
    
    # Sunrise Time
    sunrise = get_class("SunriseSunset--sunriseDateItem--3PunQ", 0)

    # Sunset Time
    sunset = get_class("SunriseSunset--sunsetDateItem--3zmvo SunriseSunset--sunriseDateItem--3PunQ", 0)

    # Temperature
    temperature = get_class("CurrentConditions--dataWrapperInner--3Cwsl", 0)
    # Manual RegEx Because I Suck At Programing                                 
    # To elaborate on that dumbness I mean that my func 'get_class' doesnt see it as a multi class div well... because it's not but I dont know ho
    temperatureregex = re.compile(r'\d{1,3}°')                                  
    temp_temperature = temperatureregex.search(temperature)                     
    temperature = str(temperature)[temp_temperature.start():temp_temperature.end()]
    
    # Real Feel
    realfeel = get_class("TodayDetailsCard--feelsLikeTemp--2hhSJ", 0)        
    # Manual RegEx Because I Suck At Programing                                 
    # To elaborate on that dumbness I mean that my func 'get_class' doesnt see it as a multi class div well... because it's not but I dont know ho
    realfeelregex = re.compile(r'\d{1,3}°')                                  
    temp_realfeel = temperatureregex.search(temperature)                     
    realfeel = str(realfeel)[temp_realfeel.start():temp_realfeel.end()]
    

    # Weather Observation
    weather = get_class("CurrentConditions--phraseValue--17s79", 0)

    # Pretty much just a block of redundant code I don't ever use Prediction but i'll keep the code here
    try:
        prediction = get_class("CurrentConditions--precipValue--1RgXi", 0)
    except:
        pass

    # Date & Time
    now = datetime.now()
    # dd/mm/YY H:M
    date_string = now.strftime("%m/%d/%Y")
    time_string = now.strftime("%H:%M")

    ## datetime import fix
    # date_string = strftime("%Y-%m-%d", gmtime())
    #time_string = strftime("%H:%M", gmtime())

    # The file building.
    formatted_text = [date_string, time_string, weather, temperature, windspeed, humidity, realfeel, sunrise[8:],sunset[6:]]
    formatted_text = ','.join(formatted_text) + "\n"
    file = open("Weather Observation.csv", "a")
    file.write(formatted_text)
    file.close()
    print("Successfully Collected Data From " + zipCode)


# Menu loop
while True:
    choice = input("\n1:   Check Logs\n2:   Get Data\n: ")
    if choice == '1':
        log_check()
    elif choice == '2':
        main()
    else:
        continue
