#!/usr/bin/env

"""
    Sample script of twot usage
    
    Logs in to an account, gets latest tweets and engages with them


    gpl27
"""

import logging
import time
from twot import *

# Sets ups console and file logging

# Get twots logger
logger = logging.getLogger('twot')
logger.setLevel(logging.DEBUG)

# Add a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(ch_format)
logger.addHandler(ch)

# Add a file handler
fh = logging.FileHandler('main.log', mode='w')
fh.setLevel(logging.DEBUG)
fh_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fh_format)
logger.addHandler(fh)


# Runs code using the TwitterAPI
api = TwitterAPI('TheTwotBot', 'twotthetwitterbot')

api.login()
api.login()
my_tweet = api.post_tweet(time.strftime('%H:%M:%S', time.localtime()))

api.like_tweet(my_tweet)
my_tweet = api.reply_to_tweet(my_tweet, time.strftime('%H:%M:%S', time.localtime()))
api.retweet(my_tweet)
api.follow('elonmusk')

api.logout()
api.quit()