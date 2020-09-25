from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import requests
import json



driver = webdriver.Firefox()
driver.get("https://www.instagram.com")

username = "smb__h"
password = "3!M>Z*(VhZkB"



