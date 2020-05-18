import config
import pandas as pd
import praw
import datetime as dt

# Creates empty list for full data set.
full_data_set = []

# API access.
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)

# Subreddits to be scraped.
subreddits = ['conspiracy', 'politics']

# Tag the subreddits here (must correspond with object position in subreddits list).
# 0 = political posts ; 1 = conspiracy posts ; 2 = other
classifiers = [1, 0]

# Sets up a dictionary to store the subreddit data.
subreddit_dict = {"title": [],
                  "score": [],
                  "id": [], "url": [],
                  "comms_num": [],
                  "created": [],
                  "body": [],
                  "classifier": [],
                  "comms_word_count": []}

# Iterative script to scrape targeted subreddits.
for post in subreddits:
    select_subreddit = reddit.subreddit(str(post))
    top_posts = select_subreddit.top('month', limit=50)
    for submission in top_posts:
        subreddit_dict["title"].append(submission.title)
        subreddit_dict["score"].append(submission.score)
        subreddit_dict["id"].append(submission.id)
        subreddit_dict["url"].append(submission.url)
        subreddit_dict["comms_num"].append(submission.num_comments)
        subreddit_dict["created"].append(submission.created)
        subreddit_dict["body"].append(submission.selftext)
        subreddit_dict["classifier"].append(classifiers[(subreddits.index(post))])

# Word counter
for post_id in subreddit_dict["id"]:
    post_comment_word_count = 0
    submission = reddit.submission(id=str(post_id))
    for top_level_comment in submission.comments:
        submission.comments.replace_more()
        words = top_level_comment.body
        words_countable = words.split()
        post_comment_word_count += len(words_countable)
    subreddit_dict["comms_word_count"].append(post_comment_word_count)


# Function converts from Reddit's UNIX date format to Year-Month-Day-Time
def get_date(created):
    return dt.datetime.fromtimestamp(created)


subreddit_data = pd.DataFrame(subreddit_dict)
_timestamp = subreddit_data["created"].apply(get_date)
subreddit_data_fixed = subreddit_data.assign(timestamp=_timestamp)
full_data_set.append(subreddit_data_fixed)

# Joins all of the data sets into a single, concatenated set.
full_post_data_set_merged = pd.concat(full_data_set)

# Exports to .csv
full_post_data_set_merged.to_csv('subreddit_data_set.csv', index=False)
