# dailygammon-championship

This script is supposed to help with the result administration. It collects match results based on match IDs and saves the results to an Excel file. Results are also output to the console, as shown in the picture below. For now, it works for finished matches only. 

![results](pics/group_results.png)

## installation (Linux)
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
* Create your .env file (see below)
* Now you can run the script: `python match_results.py test_input.txt`

## installation (Windows)

## .env
* The program uses your DailyGammon credentials to fetch the results, which is stored in a file called .env
* Log in to DailyGammon
* Press F12 to open Dev Tools (in case of Chrome and variants)
* Select Application at the top
* Select Coockies at the left
* Select dailygammon.com
* Now you see your cookie with two parameters: USERID and PASSWORD
* A template is available in the project as .env-example
* Rename it to .env
* Enter your USERID and PASSWORD between the single quotes
* Save the .env file

![Cookie.png](pics/Cookie.png)

## usage
* Make sure that you are logged in to DailyGammon
* Your authentication token is stored in a cookie you receive from DailyGammon
* Rename .env-example to .env, and fill USERID and PASSWORD according to the cookie 
* Add the match-IDs to input.txt. Each ID shall go to a separate line (see input.txt as an example)
    * If you open a match export or review in DailyGammon, the URL will look like `http://dailygammon.com/bg/export/4311203` or `http://dailygammon.com/bg/game/4311742/1/list`. The 7 digit number in the url is the match-ID
* Once you execute match_result.py, the output should be something like this
    * If you make it executable (`chmod +x match_result.py`), it can run on any Linux machine
    * For Windows, you have to change the first line of the script to `#! python3`
    * Start it from the command line: `./match_result.py` (in case of Linux, I am not sure about Windows)
    * Be patient, execution can take up to 30 seconds
    * Nan indicates unfished matches
    
