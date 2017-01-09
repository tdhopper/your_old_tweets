import twitter as tw
import datetime as dt
import urllib
import json
import logging

from dateutil.relativedelta import relativedelta


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def yearsago(years, from_date=None):
    if from_date is None:
        from_date = dt.datetime.now()
    return from_date - relativedelta(years=years)


def dates(n=12):
    for i in range(1, n+1):
        d1 = yearsago(i).strftime("%Y-%m-%d")
        d2 = (yearsago(i) + dt.timedelta(days=1)).strftime("%Y-%m-%d")
        yield "(since:{} until:{})".format(d1, d2)


def get_api():
    with open("twitter_credentials.json", "r") as f:
        credentials = json.load(f)
    return tw.Api(**credentials)


def get_followers(api):
    for f in api.GetFollowers():
        yield f


def make_tweet(follower):
    base = "https://twitter.com/search?"
    date_list = " OR ".join(dates())
    encoded = urllib.urlencode({"q": "from:{} ({})".format(follower.screen_name, date_list)})
    return "@{}: {}{}".format(follower.screen_name, base, encoded)


def go_time(follower, event_time):
    try:
        return -follower.utc_offset/3600 + 5 == event_time
    except:
        logger.error("Error computing go time for user %s", follower)
        return False


def send_tweet(event, context):
    """Post tweet"""
    event_time = (event or {}).get('time', '2017-01-09T00:00:00Z')
    event_hour = (dt.datetime
                  .strptime(event_time, "%Y-%m-%dT%H:%M:%SZ")
                  .hour)
    api = get_api()
    for f in get_followers(api):
        if not go_time(f, event_hour):
            logger.debug("Not go time for %s %s with offset of %s",
                         f.screen_name, f.id, f.utc_offset)
            continue
        logger.debug("Sending tweet for %s, %s with offset of %s",
                     f.screen_name, f.id, f.utc_offset)

        update = make_tweet(f)
        api.PostUpdate(update, verify_status_length=False)

if __name__ == '__main__':
    print send_tweet(None, None)
