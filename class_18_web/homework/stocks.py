import base64
import json
import os

import requests
from alpha_vantage.timeseries import TimeSeries

TWEETS_TYPES = ("recent", "popular")

# for proper working there should be following env variable set up
# it's of concatenated API key and API secret
# os.environ["TWITTER_API"] = f"{_key}:{_sec}"

# it is not that secure as twitter's one
ALPHAVANTAGE_API_KEY = "YG3GMROI3RPTIZ23"


class StockCollector:
    """Gets daily stock data from AlphaVantage API (via python driver).
    Main usage is to call `collect` with provided ticker(s).
    You will get back last close, max and min for last 100 days

    """

    name = "price_data"

    def __init__(self):
        self.key = ALPHAVANTAGE_API_KEY

    def collect(self, ticker):
        try:
            data, _ = TimeSeries(key=self.key).get_daily(ticker)
        except ValueError:
            return {}
        data = [float(val["4. close"]) for val in data.values()]
        return {
            "last_price": data[0],
            "p100d_min": min(data),
            "p100d_max": max(data),
        }


class TweetsCollector:
    """Collects tweets for a given stock ticker where if was mentions
    in hash tag.
    Requires env var TWITTER_API set up. It has to be a string as following:
    'app API key' + ':' + 'app API secret'
    TODO: check if Bearer token expired and request a new one (check on exp policy)

    """

    name = "tweets"

    def __init__(self):
        self.session = requests.Session()
        self.auth_url = "https://api.twitter.com/oauth2/token"
        self.tweets_url = "https://api.twitter.com/1.1/search/tweets.json"
        self._api_creds = self._get_twit_api_creds()
        self.bearer = self._get_bearer()

    def _get_twit_api_creds(self):
        # not sure this is secure to store it this way
        api_key_secret = os.getenv("TWITTER_API", None)
        if not api_key_secret:
            raise AttributeError("'TWITTER_API' env var not set up")
        return base64.b64encode(api_key_secret.encode())

    def _get_bearer(self):
        headers = {
            "Authorization": f"Basic {self._api_creds.decode()}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        data = {
            "grant_type": "client_credentials",
        }
        res = self.session.post(self.auth_url, headers=headers, data=data)
        if res.status_code != 200:
            raise ConnectionError(f"Cannot get Twitter bearer token: {res}")
        return json.loads(res.content.decode())["access_token"]

    def collect(self, stock_ticker, tweets_type="recent"):
        if tweets_type not in TWEETS_TYPES:
            raise TypeError(f"'{tweets_type}' is not supported type")
        headers = {
            "Authorization": f"Bearer {self.bearer}",
        }
        params = {
            "q": f"#{stock_ticker}",
            "count": "5",
            "result_type": tweets_type,
            "lang": "en",
        }
        res = self.session.get(self.tweets_url, headers=headers, params=params)
        if res.status_code == 200:
            return [t["text"] for t in res.json()["statuses"]]
        return []


class StockDataAggregator:
    def __init__(self, *collectors):
        self.collectors = collectors

    def collect(self, tickers):
        if type(tickers) == str:
            tickers = [tickers]
        res = []
        for t in tickers:
            res.append(
                dict(
                    **{"ticker": t},
                    **{type(c).name: c.collect(t) for c in self.collectors},
                )
            )
        return res
