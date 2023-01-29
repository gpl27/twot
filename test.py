#!/usr/bin/env

"""
    Test script for learning Selenium and BSoup
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup


service = Service(executable_path="driver/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://twitter.com/i/flow/login")
driver.implicitly_wait(10)

driver.find_element(By.NAME, "text").click()
driver.find_element(By.NAME, "text").send_keys("gubthebug")
driver.find_element(By.NAME, "text").send_keys(Keys.ENTER)
driver.find_element(By.NAME, "password").send_keys("testpass")
driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

time.sleep(3)

driver.quit()