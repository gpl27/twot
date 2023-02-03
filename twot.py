""""Twot - The Twitter Bot API

Access Twitter functionality through code. To use this module you must
first make sure you have selenium installed as well as chrome and the
correct chromedrivers. For more information see the selenium site.

NOTE: Make sure the chromedriver is installed at ./driver

NOTE: For the time being you must provide the url to the tweet you
want to interact with. In the future this will change to actually 
use the ID of the tweet, this way it is easier to integrate with
other libraries such as twint and tweepy

Author: gpl27
"""

# TODO:
#   * add error handling to undefined tweet_ids
#   * add logger
#   * add send dm
#   * add check notifications/mentions

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait


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
        service = Service(executable_path="driver/chromedriver")
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, timeout=5)


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

        if (self.__logged):
            print(f"[TwitterAPI:login] Already logged in as {self.username}")
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
            print(f"[TwitterAPI:login] Username not found!")
            return False
        passwd_input.send_keys(self.password + Keys.ENTER)
        try:
            self.wait.until(EC.title_contains("Home"))
        except TimeoutException:
            print(f"[TwitterAPI:login] Wrong password!")
            return False
        self.__logged = True
        return True


    def logout(self):
        """Logs out from twitter. Browser session remains
        
        Returns whether the operation was successfull
        """

        if not self.__logged:
            print(f"[TwitterAPI:logout] Must log in first")
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
            print(f"[TwitterAPI:post_tweet] Must log in first")
            return ""
        self.driver.get("https://twitter.com/compose/tweet")
        return self._post(message)
        
    
    def reply_to_tweet(self, tweet_id, message):
        """Posts a reply to the tweet
        
        `message` should be a string exactly as you want your reply to be
        Returns the reply's ID
        """

        if not self.__logged:
            print(f"[TwitterAPI:reply_to_tweet] Must log in first")
            return ""
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        reply_button = self.wait.until(
            lambda d: d.find_element(By.XPATH, '//div[@aria-label="Reply"]'))
        try:
            reply_button.click()
        except:
            return self.reply_to_tweet(tweet_id, message)
        
        return self._post(message)


    def like_tweet(self, tweet_id):
        """Likes/Unlikes the tweet
        
        Returns whether the tweet is now Liked (True) or
        Unliked/default (False)
        """

        if not self.__logged:
            print(f"[TwitterAPI:like_tweet] Must log in first")
            return None
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        like_button = self.wait.until(
            lambda d: d.find_element(
                By.XPATH, '//div[@aria-label="Like" or @aria-label="Liked"]'))
        try:
            like_button.click()
        except:
            return self.like_tweet(tweet_id)
        like_label = like_button.get_attribute("aria-label")
        like_status = True if like_label == "Liked" else False
        return like_status

    
    def retweet(self, tweet_id):
        """Retweets/Unretweets the tweet
        
        Returns whether the tweet is Retweeted (True) or
        Unretweeted/default (False)
        """

        if not self.__logged:
            print(f"[TwitterAPI:like_tweet] Must log in first")
            return None
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        retweet_button = self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                '//div[@aria-label="Retweet" or @aria-label="Retweeted"]'))
        try:
            retweet_button.click()
        except:
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
        return retweet_status


    def quote_retweet(self, tweet_id, message):
        """Quote Retweets the tweet with the message
        
        Returns the Quote Retweet's ID
        """

        if not self.__logged:
            print(f"[TwitterAPI:quote_retweet] Must log in first")
            return None
        tweet_url = self.tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        retweet_button = self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                '//div[@aria-label="Retweet" or @aria-label="Retweeted"]'))
        try:
            retweet_button.click()
        except:
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
        return self._post(message)


    def _get_follow_button(self, user_handle):
        if not self.__logged:
            print(f"[TwitterAPI:_get_follow_button] Must log in first")
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
            print(f"[TwitterAPI:_get_follow_button] User @{user_handle} does not exist")
            return None
        return follow_button


    def follow(self, user_handle):
        """Follows the user

        Must provide the handle without '@'
        Returns whether the operation was successfull
        """

        follow_button = self._get_follow_button(user_handle)
        if follow_button == None:
            return False
        if "Following" in follow_button.get_attribute('aria-label'):
            print(f"[TwitterAPI:follow] You already follow @{user_handle}")
            return False
        try:
            follow_button.click()
        except:
            return self.follow(user_handle)
        try:
            self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    f'//div[@aria-label="Following @{user_handle}"]'
                )
            )
        except:
            print(f"[TwitterAPI:follow] Something went wrong...")
            return False
        return True


    def unfollow(self, user_handle):
        """Unfollows the user
        
        Must provide the handle without '@'
        Returns whether the operation was successfull
        """

        follow_button = self._get_follow_button(user_handle)
        if follow_button == None:
            return False
        if "Following" not in follow_button.get_attribute('aria-label'):
            print(f"[TwitterAPI:follow] You do not follow @{user_handle}")
            return False
        try:
            follow_button.click()
        except:
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
        except:
            print(f"[TwitterAPI:follow] Something went wrong...")
            return False
        return True

        
    def quit(self):
        """Ends the selenium driver session"""

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
