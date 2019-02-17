import datetime as dt

import markdown2
import praw
from psaw import PushshiftAPI

reddit = praw.Reddit(
    client_id="XXX",
    client_secret="XXX",
    user_agent="reddot",
    username="XXX",
    password="XXX",
)

start_epoch = int(dt.datetime(2017, 1, 1).timestamp())
end_epoch = int(dt.datetime(2017, 1, 31).timestamp())
api = PushshiftAPI(reddit)


def get_top(start_date):
    end_date = (start_date.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
    top_list = list(
        api.search_submissions(
            after=int(start_date.timestamp()),
            before=int(end_date.timestamp()),
            subreddit="gonewildstories",
            filter=["url", "author", "title", "subreddit"],
            sort="desc",
            sort_type="score",
            limit=30,
        )
    )
    top_list = [
        post for post in top_list if post.selftext not in ["[removed]", "[deleted]"]
    ]
    return top_list[:10]


def output_list(submissions):
    for post in submissions:
        print("* {}: [{}](<{}>)".format(post.score, post.title, post.url))


for year in range(2011, 2018):
    print("# {}".format(year))
    for month in range(1, 13):
        start_date = dt.datetime(year, month, 1)
        print("## {} {}".format(year, start_date.strftime("%b")))
        output_list(get_top(start_date))
        print("\n___\n")
