#!/usr/bin/env

""""
    Twot - The Twitter Bot

    gpl27
"""

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup


class TwitterAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Start the webdriver
        service = Service(executable_path="driver/chromedriver")
        self.driver = webdriver.Chrome(service=service)

    
    def login(self):
        self.driver.get("https://twitter.com/i/flow/login")


    def post_tweet(self, message):
        self.driver.get("https://twitter.com/compose/tweet")

    
    def reply_to_tweet(self, tweet_url, message):
        self.driver.get(tweet_url)


    def like_tweet(self, tweet_url):
        self.driver.get(tweet_url)

    
    def retweet(self, tweet_url):
        self.driver.get(tweet_url)



# Convert a tweet id to a url
def tweet_id_to_url(tweet_id):
    tweet_url = ""
    return tweet_url