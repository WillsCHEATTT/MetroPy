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
####     Huge thanks to mrHeavenli for updated webscraping method!     ####
###########################################################################
import requests
import bs4
import re
from datetime import date, time, datetime
from time import gmtime, strftime

regexes = {
	"temp" : r"tempValue.*(?P<tempature>\b([0-9]|[1-9][0-9]|1[0-9]{2}|200)°)",
	"windspeed" : r"(?P<windspeed>([0-9]|[1-9][0-9]|100).mph)",
	"humidity" : r"PercentageValue.*(?P<humidity>\d([0-9]|[1-9][0-9]|100)%)",
	"realfeel" : r"feelsLikeTempValue.*(?P<realfeel>\d([0-9]|[1-9][0-9]|1[0-9]{2}|200)°)"
}
		

def log_check():
    with open('Weather Observation.csv', 'r') as logfile:                       
        contents = [x.strip("\n").split(",") for x in logfile.readlines()]      
        userinput = input()                                                     
        try:                                                                    
            if int(userinput)-1 <= len(contents):                               
                for i in range(0, len(contents)): print(contents[i][int(userinput)-1])
        except (ValueError, IndexError): return                                 

def get_sky_observation():
    DOM = etree.HTML(str(other))
    # Grabs the text from the Xpath
    return DOM.xpath("/html/body/div[1]/main/div[2]/main/div[1]/div/section/div/div[2]/div[1]/div[1]/div[1]/text()")[0]


def parse_spans(spans):  # Unfinished
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
    other = bs4.BeautifulSoup(req.text, 'lxml')

    
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
