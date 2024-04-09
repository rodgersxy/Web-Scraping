# Importing required modules and initializing variables

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
string = ''
# ______________________________________

# Opening thetypingcat.com on firefox

firefox = webdriver.Firefox()
firefox.get('https://thetypingcat.com/typing-speed-test/1m')
# ______________________________________

# Using javascript to get the typing content from the website and storing value in "string" variable

for i in range(firefox.execute_script('return document.querySelectorAll(".line").length')):
	string += firefox.execute_script('return document.querySelectorAll(".line")['+str(i)+'].innerHTML')

string = re.sub(r'<[^>]*>','',string) #This line is just delete tags present inside string
# ______________________________________

# Selenium commands to type what is stored inside string variable on the focused screen

action = ActionChains(firefox)
action.send_keys(string)
action.perform()

# ______________________________________ END ______________________________________