import os
import re
from dotenv import load_dotenv
import pandas as pd
import tweepy
import helpers


load_dotenv()
KEY = os.getenv("API_KEY")
SECRET = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(KEY, SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#Configure to wait on rate limit if necessary
api = tweepy.API(auth, wait_on_rate_limit=True, )

filename = "tweets.csv"
number_of_tweets = 800
query_type = "search_tweets"

query = "cosmos atom " \
        " -nft -doge -shiba -moon -meme min_faves:20" \
        " -filter:retweets lang:en"

# Regex for $BTC-$MATIC. [$]?[A-Z]+.?[-–/].?[$]?[A-Z]+
regex_token = re.compile("")

if query_type == "search_tweets":
    tweets = tweepy.Cursor(api.search_tweets, q=query, count=100, result_type='top'
                           ).items(number_of_tweets)
elif query_type == "search_30_day":
    tweets = tweepy.Cursor(api.search_30_day, label="dev", query=query,
                           ).items(number_of_tweets)


data = {"User":[], "Date":[], "Tweet Text":[], "Retweet?":[], "Hashtags":[], "Followers":[]}
omitted_tweets = 0
tweets_returned = 0
for tweet in tweets:

    #Count the number of returned tweets
    tweets_returned += 1
    status = api.get_status(tweet.id, tweet_mode="extended")

    try:
        # If retweeted get the text
        tweet_text = "Tweet ID: {0}\n{1}".format(
            tweet.id_str, status.retweeted_status.full_text)

        # Omit tweet if it does not match the Regex provided
        if regex_token.search(tweet_text) is None:
            omitted_tweets += 1
            continue

        data["Tweet Text"].append(helpers.reduce_text_len(tweet_text, 70))
        data["Retweet?"].append("Yes")

        hashtags = ""
        for tag in status.retweeted_status.entities["hashtags"]:
            hashtags += tag['text'] + "\n"
        data["Hashtags"].append(hashtags)

    except AttributeError:
        tweet_text = "Tweet ID: {0}\n{1}".format(
            tweet.id_str, status.full_text)

        # Omit tweet if it does not match the Regex provided
        if regex_token.search(tweet_text) is None:
            omitted_tweets += 1
            continue

        data["Tweet Text"].append(helpers.reduce_text_len(tweet_text, 60))
        data["Retweet?"].append("No")

        hashtags = ""
        for tag in status.entities["hashtags"]:
            hashtags += tag['text'] + "\n"
        data["Hashtags"].append(hashtags)

    #Adding User name and follower count and the Tweet's ID
    followers_count = "{:,}".format(status.user.followers_count)

    if status.user.description == "":
        user_description = "None"
    else:
        user_description = helpers.reduce_text_len(status.user.description, 30)

    user_info = "{0}\nFollowers: {1}\n\nDescription: {2}".format(
        status.user.name, followers_count, user_description)
    data["User"].append(user_info)

    #Adding Tweet Date in day-month-year, hour-minute-second format
    date = status.created_at.strftime('%d-%m-%Y') + "\n" + status.created_at.strftime('%X')
    data["Date"].append(date)

    data["Followers"].append(followers_count)


df = pd.DataFrame(data)
df.to_csv(filename, float_format="{:,.2f}".format)

print("Number of tweets queried:  {}".format(number_of_tweets))
print("Number of tweets returned: {}".format(tweets_returned))
print("Number of tweets omitted:  {}".format(omitted_tweets))
print("Number of tweets exported: {} to {} file.".format(
    tweets_returned - omitted_tweets, filename))