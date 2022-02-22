"""
This script queries Twitter for tweets using their API.
The results are saved in a .csv file in a formatted way.
Various filters are applied to find the desired tweets.
"""

from os import getenv
from argparse import ArgumentParser
from dotenv import load_dotenv
from tweepy import OAuthHandler, Cursor, API
from helpers import tweets_to_df


software_ver = "1.0.0"
# Set up CLI with arguments
parser = ArgumentParser(
    usage="python %(prog)s query number [-f filename] [-t type] [-r regex]...",
    description="This script queries Twitter for tweets using their API."
                "Visit https://github.com/ivandimitrovkyulev/TwitterBot.git for more info.",
    epilog=f"Version - %(prog)s {software_ver}",
)

parser.add_argument(
    "query", action="store", type=str, nargs='?', metavar="query",
    help="Query to search for. For more than 1 word, enclose string in quotes. For example: "
         "'Elon Musk min_faves:20 -Tesla -filter:retweets lang:en' searches for tweets that "
         "contain Elon Musk, have minimum 20 likes, do NOT contain Tesla, are NOT retweeted, "
         "and are written in english.",
)
parser.add_argument(
    "number", action="store", type=int, nargs='?', metavar="number",
    help="Number of queries to request from Twitter. Limits may apply.",
)
parser.add_argument(
    "-f", action="store", type=str, dest="filename", nargs='?', metavar="filename", default="tweets.csv",
    help="Name of the file to save the results in. search_tweets.csv for example.",
)
parser.add_argument(
    "-t", action="store", type=str, dest="search_type", nargs='?', metavar="type",
    choices=["search_tweets", "search_30_day", "search_full_archive"], default="search_tweets",
    help="Choose between search_tweets, search_30_day, search_full_archive. "
         "Full archive is a premium type of search. Defaults to search_tweets.",
)
parser.add_argument(
    "-s", action="store", type=str, dest="sort_results", nargs='?', metavar="column",
    choices=["User", "Date", "Tweet Text", "Retweet?", "Hashtags", "Followers", "Tweet ID"],
    help="Sorts the the .csv file with the specified column. Choose from: 'User', 'Date', 'Tweet Text', "
         "'Retweet?', 'Hashtags', 'Followers', 'Tweet ID'.",
)
parser.add_argument(
    "-r", action="store", type=str, dest="regex", nargs='?', metavar="regex", default="",
    help="Filters out tweets which do not match the regular expression provided. "
         "Enclose in quotes.",
)
parser.add_argument(
    "-m", action="store", type=str, dest="mode", nargs='?', metavar="mode",
    choices=['a', 'w'], default="a",
    help="File mode, default is 'a', which appends if file exists, otherwise creates it.",
)
parser.add_argument(
    "-V", "--version", action="version", version=software_ver,
    help="Prints the current version of the script."
)
# Parse provided arguments
args = parser.parse_args()

# Load .env with Tweeter keys and tokens
load_dotenv()
KEY = getenv("API_KEY")
SECRET = getenv("API_SECRET_KEY")
ACCESS_TOKEN = getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = getenv("ACCESS_TOKEN_SECRET")
# Authorise and configure
auth = OAuthHandler(KEY, SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True)

# Assign arguments
query = args.query
number = args.number
filename = args.filename
search_type = args.search_type
regex = args.regex
mode = args.mode
sort_results = args.sort_results

# Create pagination for querying tweets
tweets = Cursor(getattr(api, search_type), q=query).items(number)

# Construct the API query with the given parameters and return results
if query and number:
    tweet_info = tweets_to_df(tweets, api, regex)
else:
    parser.exit(message="Please provide query string and number.")

# Get Pandas DataFrame and save it to file
if tweet_info is None:
    parser.exit(message="No results found with provided parameters, please try something else.")
else:
    # Get DataFrame
    df = tweet_info[0]
    # Get number of returned tweets and those filtered out
    tweets_returned = tweet_info[1]
    tweets_omitted = tweet_info[2]

if args.sort_results:
    df.sort_values(by=f"{sort_results}", inplace=True, ascending=False)

# Save DataFrame to .csv file
df.to_csv(filename, float_format="{:,.2f}".format, mode=mode)


print(f"Number of tweets requested:  {number}")
print(f"Number of tweets returned: {tweets_returned}")
print(f"Number of tweets matching regex: {tweets_returned - tweets_omitted}")
print(f"Tweets saved in ./{filename}")
