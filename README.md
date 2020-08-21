# dailygammon-championship

This package is supposed to help with the result administration. It collects match results based on match IDs and saves the results to an Excel file. Results are also output to the console, as shown in the picture below. For now, it works for finished matches only. 

![results](pics/group_results.png)

## no need to install
Clone or download the whole project. In the dist folder, there is an exe and a Linux executable with all the dependencies, you do not have to have even Python installed.

## usage
* Create a working directory
* Copy the executable into it (from the project's dist folder)
* Create your .env file in the same directory (see below - you have to do this only once)
* Create your input file in the same directory (see below - you have to do this only once per season)
* Start the program from the command line, with adding the input file name as a command line argument, like below:
    * Linux: `./dg-results input.txt`
    * Windows: `dg-results.exe input.txt`
* Be patient, execution can take up to 30 seconds
* NaN indicates unfished matches

## .env
* The program uses **your** DailyGammon credentials to fetch the results, which is stored in a file called .env
* Log in to DailyGammon
* Press F12 to open Dev Tools (in case of Chrome and variants)
* Select Application at the top
* Select Coockies at the left
* Select dailygammon.com
* Now you see your authentication cookie with two parameters: USERID and PASSWORD
* A .env template is available in the project as .env-example
* Rename it to .env
* Enter your USERID and PASSWORD between the single quotes
* Save the .env file

![Cookie.png](pics/Cookie.png)

## create your input
* The program fetches the match results based on the match-IDs. The mathc-ID is the 7 digit number in the url if you open a match in your browser. E.g. `http://dailygammon.com/bg/export/4311203` or `http://dailygammon.com/bg/game/4311742/1/list`
* Create a simple text file with all the match ID-s you are interested in
* Every match ID goes to a separate line. See `test_input.txt` as an example.

## if you want to avoid using the binary executables
* Prerequisites:
    * Python: most Linux distributions come with Python preisntalled
    * pip (or pip3): `sudo apt install python3-pip`
    * git: `sudo apt install git-all`
* Navigate to any dictionary you want to use as a working directory
* Clone the project: `git clone https://github.com/dzsobacsi/dailygammon-championship.git` 
* `cd dailygammon-championship`
* Install virtualenv: `pip install virtualenv` (use pip3 if necessary)
* Create a virtual environment: `virtualenv venv`
* Activate it: `source venv/bin/activate`
* Install all the requirements: `pip install -r requirements.txt`
* Create your .env file
* Now you can run the script: `python dailygammon-championship test_input.txt`
