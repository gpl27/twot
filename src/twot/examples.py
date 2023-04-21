""" Examples
Samples search options for Twitter Search
Samples functions
"""

REQUIRED_OPTIONS = {
    'limit': 100,
    'replies': True,
    'only-replies': False,
    'links': True,
    'only-links': False
}

ALL_OPTIONS = {
    'limit': 200,          
    'words': "foo",
    'phrase': "bar",
    'any': "yam",
    'none': ["zoo"],
    'hashtags': ["dum"],
    'from': ['TheTwotBot'],
    'to': ['BarackObama'],
    'mentions': ['POTUS'],
    'replies': True,      
    'only-replies': False, 
    'links': True,         
    'only-links': False,   
    'min-replies': 20,
    'min-likes': 100,
    'min-rt': 10,
    'start': "2023-01-01",
    'end': "2023-03-20"

}

def like_recent(handle, api):
    """Likes the last 30 tweets"""

    OPTIONS = REQUIRED_OPTIONS.copy()
    OPTIONS['limit'] = 30
    OPTIONS['from'] = [handle]
    tweets = api.search(OPTIONS)
    for tweet in tweets:
        api.like_tweet(tweet)
    return
