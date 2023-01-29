""""
    Twot - The Twitter Bot

    gpl27
"""

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with


class TwitterAPI:
    # TODO:
    #   * optional username and password on constructor
    #   * make self.logged private
    #   * add set_user() function to change user&pwd
    #   * add error handling to login (wrong user|pwd)
    #   * add error handling to undefined tweet_ids
    #   * add status() function
    #   * add logger

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged = False
        # Start the webdriver
        service = Service(executable_path="driver/chromedriver")
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, timeout=5)


    def _post(self, message):
        text_input = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@aria-label="Tweet text"]'))
        text_input.click()
        text_input.send_keys(message)
        tweet_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@data-testid="tweetButton"]'))
        tweet_button.click()
        alert = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@role="alert" and @data-testid="toast"]'))
        tweet_link = alert.find_element(By.TAG_NAME, 'a').get_attribute("href")
        return tweet_link
    

    def login(self):
        if (self.logged):
            print(f"[TwitterAPI:login] Already logged in as {self.username}")
            return False
        self.driver.get("https://twitter.com/i/flow/login")
        username_input = self.wait.until(lambda d: d.find_element(By.NAME, "text"))
        username_input.click()
        username_input.send_keys(self.username + Keys.ENTER)
        passwd_input = self.wait.until(lambda d: d.find_element(By.NAME, "password"))
        passwd_input.send_keys(self.password + Keys.ENTER)
        self.wait.until(EC.title_contains("Home"))
        self.logged = True
        return True

    def logout(self):
        if not self.logged:
            print(f"[TwitterAPI:logout] Must log in first")
            return False
        self.driver.get("https://twitter.com/logout")
        logout_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
        logout_button.click()
        self.wait.until(EC.url_contains("?"))
        self.logged = False
        return True


    def post_tweet(self, message):
        if not self.logged:
            print(f"[TwitterAPI:post_tweet] Must log in first")
            return ""
        self.driver.get("https://twitter.com/compose/tweet")
        return self._post(message)
        
    
    def reply_to_tweet(self, tweet_id, message):
        if not self.logged:
            print(f"[TwitterAPI:reply_to_tweet] Must log in first")
            return ""
        tweet_url = tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        reply_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@aria-label="Reply"]'))
        try:
            reply_button.click()
        except:
            return self.reply_to_tweet(tweet_id, message)
        
        return self._post(message)


    def like_tweet(self, tweet_id):
        if not self.logged:
            print(f"[TwitterAPI:like_tweet] Must log in first")
            return None
        tweet_url = tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        like_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@aria-label="Like" or @aria-label="Liked"]'))
        try:
            like_button.click()
        except:
            return self.like_tweet(tweet_id)
        like_label = like_button.get_attribute("aria-label")
        like_status = True if like_label == "Liked" else False
        return like_status

    
    def retweet(self, tweet_id):
        if not self.logged:
            print(f"[TwitterAPI:like_tweet] Must log in first")
            return None
        tweet_url = tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        retweet_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@aria-label="Retweet" or @aria-label="Retweeted"]'))
        try:
            retweet_button.click()
        except:
            return self.retweet(tweet_id)
        confirm_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@data-testid="retweetConfirm" or @data-testid="unretweetConfirm"]'))
        self.wait.until(EC.element_to_be_clickable(confirm_button))
        confirm_button.click()
        retweet_label = retweet_button.get_attribute("aria-label")
        retweet_status = True if retweet_label == "Retweeted" else False
        return retweet_status


    def quote_retweet(self, tweet_id, message):
        if not self.logged:
            print(f"[TwitterAPI:quote_retweet] Must log in first")
            return None
        tweet_url = tweet_id_to_url(tweet_id)
        self.driver.get(tweet_url)
        retweet_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@aria-label="Retweet" or @aria-label="Retweeted"]'))
        try:
            retweet_button.click()
        except:
            return self.quote_retweet(tweet_id, message)
        confirm_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@data-testid="retweetConfirm" or @data-testid="unretweetConfirm"]'))
        qrt_locator = locate_with(By.TAG_NAME, 'div').below(confirm_button)
        qrt = self.driver.find_element(qrt_locator)
        self.wait.until(EC.element_to_be_clickable(qrt))
        qrt.click()
        return self._post(message)


    def quit(self):
        self.driver.quit()

    def shutdown(self):
        self.logout()
        self.quit()



# Convert a tweet id to a url
# NOTE: this is for future compatibility with
# twitter APIs like twint
def tweet_id_to_url(tweet_id):
    tweet_url = tweet_id
    return tweet_url