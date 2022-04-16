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

    contents = []
    
    for i in file.readlines():
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

def parse_spans(spans):

    # Insert regex magic here, because birdy is a regex wizard
    return []


def main():
    while True:
        print("What is your zip code?")
        zipCode = input().strip()
                            
        # build regex parser for zipcode
        zipcodeRegEx = re.compile(r'^\d{5}$')
        check = zipcodeRegEx.search(zipCode)
        # "Basic" Zipcode Check
        if check is None:
            print("Hmm.. I don't recognize " + zipCode + " as a proper zipcode. Use digit like 75115")
            continue
        break
    
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
    
    
    spans = weatherSoup.find_all("span")
    formatted_data = parse_spans(spans)
    
    file = open("Weather Observation.csv", "a")
    file.write(formatted_data)
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
