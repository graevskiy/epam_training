from functools import wraps

from flask import Flask, jsonify, session
from flask_session import Session
from stocks import StockCollector, StockDataAggregator, TweetsCollector

STOCK_NUM_LIMIT = 10
app = Flask(__name__)

# as this is just test project not going to Prod,
# assume it's ok to let it be here
app.config["SECRET_KEY"] = b"youllneverguessasitssoeasy"

# this is not following RESTful spirit,
# but client-side stored session didn't work out of the box
app.config["SESSION_TYPE"] = "filesystem"
app.config["JSON_SORT_KEYS"] = False
Session(app)

# set up collectors and collectors' aggregator
stock_col = StockCollector()
tweet_col = TweetsCollector()
stock_aggr = StockDataAggregator(stock_col, tweet_col)


def session_exists(func):
    """wraps route function if it has to deal with stock watchlist"""

    @wraps(func)
    def session_wrapper(*args, **kwargs):
        if "stocks" not in session:
            session["stocks"] = []
        return func(*args, **kwargs)

    return session_wrapper


@app.route("/")
@app.route("/stocks/")
@session_exists
def index():
    return jsonify(stock_aggr.collect(session["stocks"]))


@app.route("/stocks/<string:stock_name>", methods=["POST"])
@session_exists
def stock_add(stock_name):
    stocks = session["stocks"]
    if len(stocks) >= STOCK_NUM_LIMIT:
        # not sure which code would be correct
        return {"error": "Max limit of tickers in watchlist exceeded"}, 406
    # also, not sure what is correct way if no body should be there
    # but just a proper status code
    if stock_name not in stocks:
        stocks.append(stock_name)
        return "201", 201
    return "200"


@app.route("/stocks/<string:stock_name>", methods=["GET"])
def stock_show(stock_name):
    return jsonify(stock_aggr.collect(stock_name))


@app.route("/stocks/<string:stock_name>", methods=["DELETE"])
@session_exists
def stock_delete(stock_name):
    stocks = session["stocks"]
    if stock_name in stocks:
        stocks.remove(stock_name)
    return "204", 204


if __name__ == "__main__":
    app.run(debug=True)
