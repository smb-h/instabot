from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import requests
import json
import logging.config
import sys



driver = webdriver.Firefox()
driver.get("https://www.instagram.com")

username = ""
password = ""

with open('static/jquery-3.5.1.min.js', 'r') as jquery_js: 
    jquery = jquery_js.read()
    driver.execute_script(jquery)

    

