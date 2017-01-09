from __future__ import absolute_import

import tweet
import datetime as dt

from collections import namedtuple


User = namedtuple("User", "ID ScreenName utc_offset")

def test_go_time():
    f = User(89249164, "tdhopper", -18000)
    event_time = dt.datetime(2017, 1, 1, 0, 0, 0)
    assert tweet.go_time(f, event_time.hour) == False
    event_time = dt.datetime(2017, 1, 1, 10, 0, 0)
    assert tweet.go_time(f, event_time.hour) == True