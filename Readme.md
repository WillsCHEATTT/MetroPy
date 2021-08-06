
Hello everyone reading this!! This is my 7th grade science fair project that I decided
to put on Github.

Code is protected by the GNU3 GPL Licence

- Zackery .R. Smith
- github.com/WillsCHEATTT
 
--------------------------------------------------------------------

This script is really simple and small, and if you would like to use this on a older 
version of python some changes are due. All the versions i've tested and fixed are listed below.

Python 3.7 - 3.9 (Works just fine) 

Python 3.0 - 3.6 (Small and easy fix)


	Because datetime does not exsist on older versions of python we need to fix 
	the date and time code. This is a simple two line fix replace the code listed below.

	
	Replace date_string and time_string with

		date_string = strftime("%Y-%m-%d", gmtime())
   		time_string = strftime("%H:%M", gmtime()) 

	Remove this line
	
		now = datetime.now()



That should fix the issue if gmtime and strftime are not imported from time do so


Python 2.9 or Below (Python 2.9 and below have never been tested but the 3.0 - 3.6 fix might work if you have issues)
--------------------------------------------------------------------
