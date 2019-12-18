import twitter as tw
import datetime as dt
from urllib.parse import urlencode
import os
import logging

from dateutil.relativedelta import relativedelta


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def yearsago(years, from_date=None):
    if from_date is None:
        from_date = dt.datetime.now()
    return from_date - relativedelta(years=years)


def dates(n=12):
    for i in range(1, n + 1):
        d1 = yearsago(i).strftime("%Y-%m-%d")
        d2 = (yearsago(i) + dt.timedelta(days=1)).strftime("%Y-%m-%d")
        yield "(since:{} until:{})".format(d1, d2)


def get_api():
    credentials = {
        "consumer_key": os.environ["CONSUMER_KEY"].strip(),
        "consumer_secret": os.environ["CONSUMER_SECRET"].strip(),
        "access_token_key": os.environ["TOKEN"].strip(),
        "access_token_secret": os.environ["TOKEN_SECRET"].strip(),
    }
    return tw.Api(**credentials)


def get_followers(api):
    for f in api.GetFollowers():
        yield f


def make_tweet(follower):
    base = "https://twitter.com/search?"
    date_list = " OR ".join(dates())
    encoded = urlencode(
        {
            "f": "tweets",
            "vertical": "default",
            "q": "from:{} ({})".format(follower.screen_name, date_list),
        }
    )
    return "@{}: {}{}".format(follower.screen_name, base, encoded)


def go_time(follower, event_time):
    try:
        return -follower.utc_offset / 3600 + 5 == event_time
    except:
        logger.error("Error computing go time for user %s", follower)
        return False


def send_tweet(event, context):
    """Post tweet"""
    api = get_api()
    for f in get_followers(api):
        update = make_tweet(f)
        api.PostUpdate(update, verify_status_length=False)


if __name__ == "__main__":
    send_tweet(None, None)
