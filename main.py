import Algorithmia
import collections
from google.appengine.api import memcache, urlfetch
import itertools
import json
import os
import settings
import webapp2


TWITTER_AUTH_DICT = {"app_key": settings.TWITTER_APP_KEY,
                     "app_secret": settings.TWITTER_APP_SECRET,
                     "oauth_token": settings.TWITTER_OAUTH_TOKEN,
                     "oauth_token_secret": settings.TWITTER_OAUTH_SECRET}

IS_LOCAL = os.environ["SERVER_NAME"] in ("localhost", "127.0.0.1")


class AlgorithmiaRequestHandler(webapp2.RequestHandler):

    def process_post(self, algorithm, useAt, data={}.copy()):
        """
        handle POST to run the specified algorithm
        :param algorithm: algorithm to run ("user/algorithm/version")
        :param useAt: should '@' be prefixed to 'uid' (in POST body JSON)
        :param data: additional params to send to the algorithm
        :return:
        """
        urlfetch.set_default_fetch_deadline(120)
        uid = extract_uid(self.request.body)
        if not uid:
            return {'error':'Invalid Twitter Username'}
        try:
            data["query"] = '@'+uid if useAt else uid
            cache_key = algorithm+' '+json.dumps(collections.OrderedDict(sorted(data.items())))
            result = memcache.get(cache_key)
            if result is None:
                data["auth"] = TWITTER_AUTH_DICT
                result = call_algorithmia(algorithm, data).result
                memcache.add(cache_key, result, settings.AG_CACHE_SECONDS)
            return result
        except Exception as x:
            return {'error': str(x)}


class AnalyzeUserHandler(AlgorithmiaRequestHandler):

    def post(self):
        '''
        Analyze the provided twitter username ('uid') via https://algorithmia.com/algorithms/diego/AnalyzeTwitterUser
        :return: JSON of the form:
            {"following": Int,
            "is negative about": [{String:Int}],
            "followers": Int,
            "screen_name": String,
            "is positive about": [{String:Int}]}
        '''
        result = settings.MOCK_RESPONSE_USER if IS_LOCAL \
            else super(self.__class__, self).process_post(settings.AG_ALGORITHM_ANALYZE_USER, False)
        if "is positive about" in result:
            result = {
                "screen_name": result["screen_name"],
                "followers": result["followers"],
                "following": result["following"],
                "positive": flatten_list_of_pairs(result["is positive about"]),
                "negative": flatten_list_of_pairs(result["is negative about"])
            }
        self.response.write(json.dumps(result))


class AnalyzeMentionsHandler(AlgorithmiaRequestHandler):

    def post(self):
        '''
        Analyze the last 100 tweets containing 'uid' as a keyword
        as per https://algorithmia.com/algorithms/nlp/AnalyzeTweets
        TBD: this doesn't remove retweets, and breaks down when uid is also a natural language word
        :return: JSON of the form:
            {"posLDA": [{String: Int}],
            "negLDA": [{String: Int}],
            "allTweets": [{
                "text": String,
                "created_at": Date,
                "tweet_url": String,
                "overall_sentiment": Float,
                "positive_sentiment": Float,
                "neutral_sentiment": Float,
                "negative_sentiment": Float
            }],
            "posTweets": <AS ABOVE>,
            "negTweets": <AS ABOVE>}
        '''
        result = settings.MOCK_RESPONSE_KEYWORDS if IS_LOCAL \
            else super(self.__class__, self).process_post(settings.AG_ALGORITHM_ANALYZE_KEYWORD, True, {"numTweets": "100"})
        if "posLDA" in result:
            result = {
                "allTweets": remove_duplicate_tweet_texts(result["allTweets"]),
                "posTweets": remove_duplicate_tweet_texts(result["posTweets"]),
                "negTweets": remove_duplicate_tweet_texts(result["negTweets"]),
                "positive": flatten_list_of_pairs(result["posLDA"]),
                "negative": flatten_list_of_pairs(result["negLDA"])
            }
        self.response.write(json.dumps(result))


def flatten_list_of_pairs(list_of_pairs):
    """
    given a list of items containing key-value pairs, flatten into a sorted list of unique key-value pairs
    :param list_of_pairs:
    :return:
    """
    return sorted(list(set(itertools.chain.from_iterable([elem.keys() for elem in list_of_pairs]))))


def remove_duplicate_tweet_texts(tweets):
    """
    deduplicate a set of tweets based on 'text' value
    :param tweets:
    :return:
    """
    return {t['text']: t for t in tweets}.values()


def extract_uid(body):
    """
    load body as JSON and extract the 'uid' value, trimming and removing '@'
    :param body:
    :return:
    """
    uid = json.loads(body).get('uid', None)
    return uid.strip().lstrip('@') if uid and not ' ' in uid else None


def call_algorithmia(algorithm, data):
    """
    call Algorithmia to run a specific algorithm
    :param algorithm: algorithm to run ("user/algorithm/version")
    :param data: params to send to algorithm
    :return:
    """
    client = Algorithmia.client(settings.AG_CLIENT_KEY)
    algo = client.algo(algorithm)
    return algo.pipe(data)


app = webapp2.WSGIApplication([
    ('/json/analyze_user', AnalyzeUserHandler),
    ('/json/analyze_mentions', AnalyzeMentionsHandler),
], debug=True)