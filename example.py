#!/usr/bin/env

"""
Sample script of twot usage

Logs in to an account, tweets, quote retweets, likes, and follows

USAGE:
$ ./example.py [username] [password]

Author: gpl27
"""

import logging
import time
from sys import argv

from twot import TwitterAPI

# Sets ups console and file logging
logger = logging.getLogger('twot')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(ch_format)
logger.addHandler(ch)
fh = logging.FileHandler('main.log', mode='w')
fh.setLevel(logging.DEBUG)
fh_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fh_format)
logger.addHandler(fh)


def main(username, password):
    # Runs code using the TwitterAPI
    api = TwitterAPI(username, password)

    api.login()
    message = f"{time.strftime('%H:%M:%S', time.localtime())} - This is a sample tweet that was posted using twot-TheTwitterAPI"
    my_tweet = api.post_tweet(message)

    api.like_tweet(my_tweet)

    message = f"{time.strftime('%H:%M:%S', time.localtime())} - This is a sample quote retweet"
    my_tweet = api.quote_retweet(my_tweet, message)

    api.like_tweet(my_tweet)

    api.follow('TheTwotBot')

    api.logout()
    api.quit()


if __name__ == "__main__":
    main(argv[1], argv[2])
