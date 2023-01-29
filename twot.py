""""
    Twot - The Twitter Bot

    gpl27
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TwitterAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged = False
        # Start the webdriver
        service = Service(executable_path="driver/chromedriver")
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, timeout=5)

    
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
        self.wait.until(EC.title_contains("Explore"))
        self.logged = False
        return True


    def post_tweet(self, message):
        if not self.logged:
            print(f"[TwitterAPI:post_tweet] Must log in first")
            return ""
        self.driver.get("https://twitter.com/compose/tweet")
        text_input = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@aria-label="Tweet text"]'))
        text_input.click()
        text_input.send_keys(message)
        tweet_button = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@data-testid="tweetButton"]'))
        tweet_button.click()
        alert = self.wait.until(lambda d: d.find_element(By.XPATH, '//div[@role="alert" and @data-testid="toast"]'))
        tweet_link = alert.find_element(By.TAG_NAME, 'a').get_attribute("href")
        return tweet_link

    
    # def reply_to_tweet(self, tweet_id, message):
    #     tweet_url = tweet_id_to_url(tweet_id)
    #     self.driver.get(tweet_url)


    # def like_tweet(self, tweet_id):
    #     tweet_url = tweet_id_to_url(tweet_id)
    #     self.driver.get(tweet_url)

    
    # def retweet(self, tweet_id):
    #     tweet_url = tweet_id_to_url(tweet_id)
    #     self.driver.get(tweet_url)


    def quit(self):
        self.driver.quit()



# Convert a tweet id to a url
# NOTE: this is for future compatibility with
# twitter APIs like twint
def tweet_id_to_url(tweet_id):
    tweet_url = tweet_id
    return tweet_url