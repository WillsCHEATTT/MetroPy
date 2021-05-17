                                                                      
I8,        8        ,8I  88  88  88                                   
`8b       d8b       d8'  ""  88  88                                   
 "8,     ,8"8,     ,8"       88  88                                   
  Y8     8P Y8     8P    88  88  88  ,adPPYba,  ,adPPYba,  ,adPPYba,  
  `8b   d8' `8b   d8'    88  88  88  I8[    ""  I8[    ""  I8[    ""  
   `8a a8'   `8a a8'     88  88  88   `"Y8ba,    `"Y8ba,    `"Y8ba,   
    `8a8'     `8a8'      88  88  88  aa    ]8I  aa    ]8I  aa    ]8I  
     `8'       `8'       88  88  88  `"YbbdP"'  `"YbbdP"'  `"YbbdP"'  
                                                                      
^ Logo doesnt look good in GitHub :(
--------------------------------------------------------------------

Hello everyone reading this!! This is my 7th grade science fair project that I decided
to put on Github.

Im not going to put a licence on this code so feel free to take it! If you do
want to credit me here is my info : )


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
