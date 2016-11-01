AG_CLIENT_KEY = ''
AG_CACHE_SECONDS = 60*60*24*7
AG_ALGORITHM_ANALYZE_KEYWORD = 'nlp/AnalyzeTweets/0.1.8'
AG_ALGORITHM_ANALYZE_USER = 'diego/AnalyzeTwitterUser/0.1.3'

TWITTER_APP_KEY = ''
TWITTER_APP_SECRET = ''
TWITTER_OAUTH_TOKEN = ''
TWITTER_OAUTH_SECRET = ''

MOCK_RESPONSE_USER = {"followers":11308,"following":571,"is negative about":[{"negfoo":13,"negbar":11}],"is positive about":[{"posfoo":14,"posbar":12}],"screen_name":"FooBar"}
MOCK_RESPONSE_KEYWORDS = {"posLDA":[{"posfoo":1}, {"posbar":1, "poscat":1}], "negLDA":[{"negfoo":1}, {"negbar":1, "negcat":1}], "allTweets":[{"text": "sometext", "created_at": "Mon Oct 24 22:04:00 +0000 2016", "negative_sentiment":0, "tweet_url": "https://twitter.com/statuses/790675235980865536", "positive_sentiment":0.244, "overall_sentiment":0.4404, "neutral_sentiment":0.756}, {"text": "moretext", "created_at": "Mon Oct 24 20:23:12 +0000 2016", "negative_sentiment":0, "tweet_url": "https://twitter.com/statuses/790649868314415104", "positive_sentiment":0, "overall_sentiment":0, "neutral_sentiment":1}], "posTweets":[], "negTweets":[]}