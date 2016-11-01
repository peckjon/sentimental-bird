## Synopsis

A tool to inspect the most recent Tweets by (and about) specific Twitter users.

Uses [AnalyzeTweets](http://algorithmia.com/algorithms/nlp/AnalyzeTweets) and [AnalyzeTwitterUser](http://algorithmia.com/algorithms/diego/AnalyzeTwitterUser) to retrieve tweets, run sentiment analysis, and extract keywords.

## Sample

[sentimental-bird.appspot.com](http://sentimental-bird.appspot.com/)

## Contributors

Jon Peck: [github.com/peckjon](https://github.com/peckjon)

## License

[WTFPL v2](http://en.wikipedia.org/wiki/WTFPL)

## Structure

The frontend is fairly straightforward AngularJS.  The backend is set up to run on Google App Engine, but doesn't use any GAE-specific frameworks, so you can easily port the Python to another platform.

This application uses [algorithmia-python](https://github.com/algorithmiaio/algorithmia-python) and dependent libraries (enum, requests, and six), included for simplicity.

'app' contains all frontend code (JS, HTML, and CSS).

'main.py' contains all backend code, mostly simple handlers to pull and restructure data from Algorithmia.

'settings.py' contains API keys and other constants.

## Installation

You will need to obtain an account and API keys from [Algorithmia](http://developers.algorithmia.com/basics/customizing-api-keys/), and to create a [Twitter app](https://apps.twitter.com/) to obtain app and OAuth tokens
  
Modify the API keys in settings.py accordingly.

To run in Google App Engine, [create a new project](http://developers.google.com/ad-exchange/rtb/open-bidder/google-app-guide), adjust the application param in app.yaml, and deploy.