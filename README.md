# twot - The Twitter Bot API
![PyPI](https://img.shields.io/pypi/v/twot)
![GitHub](https://img.shields.io/github/license/gpl27/twot)
## About
This is a Python package that provides an easy-to-use interface to 
Twitter using Selenium to emulate actions that a Twitter user might make,
such as liking, following, and tweeting. In addition, it provides a 
Tweet Search implementation that uses Twitter's Advanced Search to
scrape for tweets.

## Getting Started
### Prerequisites
To use this package, you will need:
- Python 3.7+
- Selenium 4.0+
- Chrome Browser
- Twitter Account
### Installation
1. `pip install twot`
### Usage
2. Import `TwitterAPI` class, create an instance and login:
```python
from twot.classes import TwitterAPI

api = TwitterAPI('my_username', 'my_password')
api.login()
```
3. Use the `TwitterAPI` instance to interact with Twitter:
```python
# Tweet something
api.post_tweet('Hello World!')

# Like a tweet
api.like_tweet('https://twitter.com/twitter/status/1234567890')

# Quote retweet a tweet
api.quote_retweet('https://twitter.com/twitter/status/1234567890', 'Foo bar')

```
4. Scrape for tweets:
```python
# First five options are required for every search
OPTIONS = {
    "limit": 500,
    "replies": False,
    "only-replies": False,
    "links": True,
    "only-links": False,
    "from": ['BarackObama']
}
# Links to the last 500 tweets from Obama
obama_tweets = api.search(OPTIONS)

```
## Features
You must have a Twitter account to use all features (including search).
Class methods return the results of their actions. For example, methods
that post a tweet return a link to the new tweet. Likeing and following
return whether that tweet/account is now liked/followed or unliked/unfollowed
(true/false).
```
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
    search(options)
        Searches for tweets using Advanced Search
    quit()
        Ends the browser session

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.
