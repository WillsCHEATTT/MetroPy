## MetroPy <sub>The program that sits here to "weather" and never be used</sub>

Hello everyone reading this!! This is my 7th grade science fair project that I decided to put on Github.

Now that summer break is coming to an end, so has my laziness so I decided to fix some projects. This being one of them from what I know this script was broken since 5-7-2021 or around there. The issue was the developers of weather.com had made some changes to the website, causing my script to stop working. After some revisions I have simplified most of the code :)

No matter how good I've made it there are some issues and improvements and I have learned from my mistake and I will list those issues now.

1. get_class() when called opens the website (This means when called it will just make a new website request making the script slower)
2. 2 parts of data specifically temperature & real feel have to be manually RegEx'ed because of the way "get_class()" determines how to deal with the request. 

Because I plan on updating this in the future i've put a licence on MetroPy 1.1. Feel  free to use 1.0 without credit as only 1.1+ will have a licence

(C) 2021 Zackery .R. Smith MetroPy
Code is protected by the GNU3 GPL Licence

- Zackery .R. Smith
- github.com/WillsCHEATTT
 
--------------------------------------------------------------------

When using older versions of python mainly 3.0 - 3.6 datetime does not exist so some fixes are due below is more info

Python 3.7 - 3.9 (Works just fine) 

Python 3.0 - 3.6 (Small and easy fix)


	Because datetime does not exsist on older versions of python we need to fix 
	the date and time code. This is a simple two line fix replace the code listed below.

	
	Replace date_string and time_string with

		date_string = strftime("%Y-%m-%d", gmtime())
   		time_string = strftime("%H:%M", gmtime()) 

	Remove this line
	
		now = datetime.now()



That will fix the datetime issue. If gmtime and strftime are not imported from time do so.

Python 2.9 or below will not function from my tests. If you would like to add 2.9 or below support please, make a pull request so people can also use your modifications!

--------------------------------------------------------------------
