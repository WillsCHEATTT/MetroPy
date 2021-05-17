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
    humidityRegEx = re.compile(
        r'\d{1,3}\%')  # This will search for a num (Only three) if it ends with % it will store it
    hum = ""  # This var is made here but assigned later

    for i, j in enumerate(weatherDetails):  # enumerate() will make I the index of and J the actual output
        if True if "PercentageValue" in str(
                j) else False:  # If the str is found anywhere in J if True it will do the IF
            hum = humidityRegEx.search(str(j))  # Searches for '\d{1,3}\%' in J
            # print(i, str(j)[hum.start():hum.end()])
            humidity = str(j)[hum.start():hum.end()]
            break
        # print(i, j, "\n\n\n\n")

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
    div = weatherSoup.findAll("div",
                              {"class": "SunriseSunset--sunsetDateItem--2_gJb SunriseSunset--sunriseDateItem--2ATeV"})
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

    # Pretty much just a block of redundant code I don't ever use Prediction but i'll keep the code here
    try:
        div = weatherSoup.findAll("div", {"class": "CurrentConditions--precipValue--RBVJT"})
        prediction = div[0].getText()
    except:
        pass

    # The file building

    now = datetime.now()
    # dd/mm/YY H:M
    date_string = now.strftime("%m/%d/%Y")
    time_string = now.strftime("%H:%M")

    ## datetime import fix
    # date_string = strftime("%Y-%m-%d", gmtime())
    #time_string = strftime("%H:%M", gmtime())

    formatted_text = [date_string, time_string, weatherOb, temperature, windspeed, humidity, RealFeel, sunrise[8:],
                      sunset[6:]]
    formatted_text = ','.join(formatted_text) + "\n"
    file = open("Weather Observation.csv", "a")
    file.write(formatted_text)
    file.close()
    print("Successfully Collected Data From " + zipCode)


while True:
    choice = input("\n1:   Check Logs\n2:   Get Data\n: ")
    if choice == '1':
        log_check()
    if choice == '2':
        main()
    else:
        continue
