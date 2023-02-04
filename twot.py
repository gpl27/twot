""""Twot - The Twitter Bot API

Access Twitter functionality through code. To use this module you must
first make sure you have selenium installed as well as chrome and the
correct chromedrivers. For more information see the selenium site.
You can, and should, use the python `logging` library.

NOTE: Make sure the chromedriver is installed at ./driver

NOTE: For the time being you must provide the url to the tweet you
want to interact with. In the future this will change to actually
use the ID of the tweet, this way it is easier to integrate with
other libraries such as twint and tweepy

NOTE:
    DEBUG - Everything, including funtion returns
    INFO  - Standard messages
    WARN  - Solvable errors
    ERROR - Unknown errors

Author: gpl27
"""


import logging

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class TwitterAPI:
    """Interface to Twitter

    Attributes
    ----------
    username : str
        string that holds the current users @
    password : str
        string that holds the current users password

    Methods
    -------
    status()
        Prints general info about the class state
    login()
        Uses `username` and `password` to login to Twitter
    logout()
        Logs out from Twitter
    post_tweet(message)
        Posts a tweet to users timeline
    reply_to_tweet(tweet_id, message)
        Posts a reply to the specified tweet
    like_tweet(tweet_id)
        Likes/Unlikes the tweet
    retweet(tweet_id)
        Retweets/Unretweets the tweet
    quote_retweet(tweet_id, message)
        Quote retweets the tweet with the specified message
    follow(user_handle)
        Follows the user with the specified handle
    unfollow(user_handle)
        Unfollows the user with the specified handle
    quit()
        Ends the browser session
    """

    def __init__(self, username, password):
        """
        Parameters
        ----------
        username : str
            The username/@ to be used
        password : str
            The password associated with `username`
        """

        self.username = username
        self.password = password
        self.__logged = False
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, timeout=5)
        logger.info('TwitterAPI initialized with user @%s', username)

    def _post(self, message):
        """Post a tweet in the current browser state

        It is assumed that there is a tweet text input and tweet button
        Only call in that given context
        """

        text_input = self.wait.until(
            lambda d: d.find_element(By.XPATH,
                                     '//div[@aria-label="Tweet text"]'))
        text_input.click()
        text_input.send_keys(message)
        tweet_button = self.wait.until(
            lambda d: d.find_element(By.XPATH,
                                     '//div[@data-testid="tweetButton"]'))
        tweet_button.click()
        alert = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//div[@role="alert" and @data-testid="toast"]'))
        tweet_link = alert.find_element(By.TAG_NAME, 'a').get_attribute("href")
        return tweet_link

    def status(self):
        """Prints current `username`, `password` (in *), and log status"""

        print(f"Username: {self.username}")
        print(f"Password: {'*'*len(self.password)}")
        print(f"Logged: {self.__logged}")

    def login(self):
        """Uses `username` and `password` to login to Twitter

        Returns whether the operation was successfull
        """

        logger.info('Logging in as @%s', self.username)
        if self.__logged:
            logger.warning('Already logged in as %s', self.username)
            return False
        self.driver.get("https://twitter.com/i/flow/login")
        username_input = self.wait.until(
            lambda d: d.find_element(By.NAME, "text"))
        username_input.click()
        username_input.send_keys(self.username + Keys.ENTER)
        try:
            passwd_input = self.wait.until(
                lambda d: d.find_element(By.NAME, "password"))
        except TimeoutException:
            logger.warning('Username not found!')
            return False
        passwd_input.send_keys(self.password + Keys.ENTER)
        try:
            self.wait.until(EC.title_contains("Home"))
        except TimeoutException:
            logger.warning('Wrong password!')
            return False
        self.__logged = True
        return True

    def logout(self):
        """Logs out from twitter. Browser session remains

        Returns whether the operation was successfull
        """

        logger.info('Logging out')
        if not self.__logged:
            logger.warning('Must log in first')
            return False
        self.driver.get("https://twitter.com/logout")
        logout_button = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
        logout_button.click()
        self.wait.until(EC.url_contains("?"))
        self.__logged = False
        return True

    def post_tweet(self, message):
        """Posts a tweet to the timeline

        `message` should be a string exactly as you want your tweet to be.
        Returns the tweets ID
        """

        if not self.__logged:
            logger.warning('Must log in first')
            return ""
        self.driver.get("https://twitter.com/compose/tweet")
        post_link = self._post(message)
        logger.debug('Tweeted %s', post_link)
        return post_link

    def reply_to_tweet(self, tweet_id, message):
        """Posts a reply to the tweet

        `message` should be a string exactly as you want your reply to be
        Returns the reply's ID, or None if fail
        """

        if not self.__logged:
            logger.warning('Must log in first')
            return None
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        try:
            reply_button = self.wait.until(
                lambda d: d.find_element(By.XPATH,
                                         '//div[@aria-label="Reply"]'))
        except TimeoutException:
            logger.warning('Tweet does not exist: %s', tweet_id)
            return None
        try:
            reply_button.click()
        except ElementClickInterceptedException:
            return self.reply_to_tweet(tweet_id, message)

        post_link = self._post(message)
        logger.debug('Replied %s', post_link)
        return post_link

    def like_tweet(self, tweet_id):
        """Likes/Unlikes the tweet

        Returns whether the tweet is now Liked (True) or
        Unliked/default (False) or None if fail
        """

        if not self.__logged:
            logger.warning('Must log in first')
            return None
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        try:
            like_button = self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    '//div[@aria-label="Like" or @aria-label="Liked"]'))
        except TimeoutException:
            logger.warning('Tweet does not exist: %s', tweet_id)
            return None
        try:
            like_button.click()
        except ElementClickInterceptedException:
            return self.like_tweet(tweet_id)
        like_label = like_button.get_attribute("aria-label")
        like_status = True if like_label == "Liked" else False
        log_msg = like_label if like_status else "Unliked"
        log_msg += f' {tweet_id}'
        logger.debug(log_msg)
        return like_status

    def retweet(self, tweet_id):
        """Retweets/Unretweets the tweet

        Returns whether the tweet is Retweeted (True) or
        Unretweeted/default (False) or None if fail
        """

        if not self.__logged:
            logger.warning('Must log in first')
            return None
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        try:
            retweet_button = self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    '//div[@aria-label="Retweet" or @aria-label="Retweeted"]'))
        except TimeoutException:
            logger.warning('Tweet does not exist: %s', tweet_id)
            return None
        try:
            retweet_button.click()
        except ElementClickInterceptedException:
            return self.retweet(tweet_id)
        confirm_button = self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                ('//div[@data-testid="retweetConfirm" or '
                 '@data-testid="unretweetConfirm"]')))
        self.wait.until(EC.element_to_be_clickable(confirm_button))
        confirm_button.click()
        retweet_label = retweet_button.get_attribute("aria-label")
        retweet_status = True if retweet_label == "Retweeted" else False
        log_msg = retweet_label if retweet_status else "Unretweeted"
        log_msg += f' {tweet_id}'
        logger.debug(log_msg)
        return retweet_status

    def quote_retweet(self, tweet_id, message):
        """Quote Retweets the tweet with the message

        Returns the Quote Retweet's ID or None if fail
        """

        if not self.__logged:
            logger.warning('Must log in first')
            return None
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        try:
            retweet_button = self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    '//div[@aria-label="Retweet" or @aria-label="Retweeted"]'))
        except TimeoutException:
            logger.warning('Tweet does not exist: %s', tweet_id)
            return None
        try:
            retweet_button.click()
        except ElementClickInterceptedException:
            return self.quote_retweet(tweet_id, message)
        confirm_button = self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                ('//div[@data-testid="retweetConfirm" or '
                 '@data-testid="unretweetConfirm"]')))
        qrt_locator = locate_with(By.TAG_NAME, 'div').below(confirm_button)
        qrt = self.driver.find_element(qrt_locator)
        self.wait.until(EC.element_to_be_clickable(qrt))
        qrt.click()
        post_link = self._post(message)
        logger.debug('QuoteRetweeted %s', post_link)
        return post_link

    def _get_follow_button(self, user_handle):
        if not self.__logged:
            logger.warning('Must log in first')
            return None

        user_url = self.handle_to_url(user_handle)
        self.driver.get(user_url)
        try:
            follow_button = self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    (f'//div[@aria-label="Follow @{user_handle}" or '
                     f'@aria-label="Following @{user_handle}"]')
                )
            )
        except TimeoutException:
            logger.warning('User @%s does not exist', user_handle)
            return None
        return follow_button

    def follow(self, user_handle):
        """Follows the user

        Must provide the handle without '@'
        Returns whether the operation was successfull
        """

        follow_button = self._get_follow_button(user_handle)
        if follow_button is None:
            return False
        if "Following" in follow_button.get_attribute('aria-label'):
            logger.warning('You already follow @%s', user_handle)
            return False
        try:
            follow_button.click()
        except ElementClickInterceptedException:
            return self.follow(user_handle)
        try:
            self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    f'//div[@aria-label="Following @{user_handle}"]'
                )
            )
        except TimeoutException:
            logger.error('Something went wrong...')
            return False
        logger.debug('Followed @%s', user_handle)
        return True

    def unfollow(self, user_handle):
        """Unfollows the user

        Must provide the handle without '@'
        Returns whether the operation was successfull
        """

        follow_button = self._get_follow_button(user_handle)
        if follow_button is None:
            return False
        if "Following" not in follow_button.get_attribute('aria-label'):
            logger.warning('You do not follow @%s', user_handle)
            return False
        try:
            follow_button.click()
        except ElementClickInterceptedException:
            return self.unfollow(user_handle)
        confirm_button = self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                '//div[@data-testid="confirmationSheetConfirm"]'
            )
        )
        confirm_button.click()
        try:
            self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    f'//div[@aria-label="Follow @{user_handle}"]'
                )
            )
        except TimeoutException:
            logger.error('Something went wrong...')
            return False
        logger.debug('Unfollowed @%s', user_handle)
        return True

    def quit(self):
        """Ends the selenium driver session"""

        logger.info('Ending session')
        self.driver.quit()

    @staticmethod
    def tweet_id_to_url(tweet_id):
        """Convert tweet ID to a URL

        To be implemented...
        """

        tweet_url = tweet_id
        return tweet_url

    @staticmethod
    def handle_to_url(user_handle):
        """Convert @ to a URL"""

        return f"https://twitter.com/{user_handle}"
