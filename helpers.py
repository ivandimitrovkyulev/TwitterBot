from re import compile
from typing import Tuple, Iterator, Any
from pandas import DataFrame


def reduce_text_len(
        text: str,
        max_len: int,
) -> str:
    """Takes a string as input and returns a reduced line length string, where
    each line has a maximum specified character length. Achieved by inserting \n

    :param text: String to be transformed
    :param max_len: Maximum number of characters per line returned
    """

    if type(text) != str:
        raise Exception("Parameters text & max_len must be str & int respectively.")

    reduced_text = ""
    text_len = len(text)
    if text_len <= max_len:
        return text
    else:
        count = 1
        current_word = ""
        for char in text:

            if char.isspace():
                reduced_text += current_word
                current_word = ""

                if count >= max_len:
                    reduced_text += "\n"
                    count = 0  # Reset counter
                else:
                    reduced_text += char
                    count += 1  # Increment

            else:
                current_word += char
                count += 1  # Increment

        reduced_text += current_word

        return reduced_text


def tweets_to_df(
        tweets: Iterator,
        twitter_api: Any,
        regex: str = "",
) -> Tuple[DataFrame, int, int]:
    """Iterates through all the tweets and extracts the tweet info, which is combined in a
    Pandas DataFrame object.

    :param tweets: Tweepy's tweet collection
    :param twitter_api: Twitter's API Interface
    :param regex: Regular expression pattern for filtering out tweets, eg '[0-9]'
    """

    data = {"User": [], "Date": [], "Tweet Text": [], "Retweet?": [],
            "Hashtags": [], "Followers": [], "Tweet ID": []}

    regex_token = compile(regex)
    tweets_omitted = 0
    tweets_returned = 0

    for tweet in tweets:

        # Count the number of returned tweets
        tweets_returned += 1

        status = twitter_api.get_status(tweet.id, tweet_mode="extended")

        try:
            # If retweeted get the text
            tweet_text = status.retweeted_status.full_text

            # Omit tweet if it does not match the Regex provided
            if regex_token.search(tweet_text) is None:
                tweets_omitted += 1
                continue

            data["Tweet Text"].append(reduce_text_len(tweet_text, 70))
            data["Retweet?"].append("Yes")
            data["Tweet ID"].append(tweet.id_str)

            hashtags = ""
            for tag in status.retweeted_status.entities["hashtags"]:
                hashtags += tag['text'] + "\n"

            if hashtags == "":
                data["Hashtags"].append("None")
            else:
                data["Hashtags"].append(hashtags)

        except AttributeError:
            # Get string repr of tweet
            tweet_text = status.full_text

            # Omit tweet if it does not match the Regex provided
            if regex_token.search(tweet_text) is None:
                tweets_omitted += 1
                continue

            data["Tweet Text"].append(reduce_text_len(tweet_text, 60))
            data["Retweet?"].append("No")
            data["Tweet ID"].append(tweet.id_str)

            hashtags = ""
            for tag in status.entities["hashtags"]:
                hashtags += tag['text'] + "\n"

            if hashtags == "":
                data["Hashtags"].append("None")
            else:
                data["Hashtags"].append(hashtags)

        # Adding User name and follower count and the Tweet's ID
        followers_count = "{:,}".format(status.user.followers_count)

        if status.user.description == "":
            user_description = "None"
        else:
            user_description = reduce_text_len(status.user.description, 30)

        user_info = "{0}\nFollowers: {1}\n\nDescription: {2}".format(
            status.user.name, followers_count, user_description)
        data["User"].append(user_info)

        # Adding Tweet Date in day-month-year, hour-minute-second format
        date = status.created_at.strftime('%d-%m-%Y') + "\n" + status.created_at.strftime('%X')
        data["Date"].append(date)

        data["Followers"].append(followers_count)

    # Construct DataFrame with dict Data
    df = DataFrame(data)
    return df, tweets_returned, tweets_omitted


class TextF:
    """Class that implements different text formatting styles."""

    B = '\033[1m'
    U = '\033[4m'  # Underline
    IT = '\x1B[3m'  # Italic
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'  # Every style must have an 'END' at the end

    @staticmethod
    def format(
            text: str,
            style: str = 'U',
    ) -> str:
        """Re formats the Text with the specified style.
        Defaults to bold.

        :param text: text to be formatted
        :param style: the style to re-format to, eg. bold, underline, etc. All available options can be
        found in the TextFormat class using the dot operator"""

        style = style.upper()

        try:
            styled_text = "{0}{1}{2}".format(TextF.__dict__[style], text, TextF.END)

        except KeyError as Err:
            # get a list of all available styles
            style_keys = [k for k, v in TextF.__dict__.items()
                          if k[0] != '_' and type(v) == str]

            print(f"{Err} not available, please choose style from: {style_keys}")
            raise

        return styled_text


if __name__ == "__main__":
    pass
