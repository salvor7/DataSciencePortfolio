"""Coordinates the twitter api with the markov chain models"""

from tweepy import Stream, OAuthHandler, API
from tweepy.streaming import StreamListener

from twitter_secrets import api_tokens as at


class HolyListener(StreamListener):
    def __init__(self):
        self.tweetCount = 0

    def on_connect(self):
        print("Connection established!!")

    def on_disconnect(self, notice):
        print("Connection lost!! : ", notice)

    def on_data(self, status):
        print("Entered on_data()")
        print(status, flush=True)
        return True

    def on_direct_message(self, status):
        print("Entered on_direct_message()")
        try:
            print(status, flush=True)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))

    def on_error(self, status):
        print(status)


def main():
    """The main event loop for the holy twitter bot

    It watches for twitter events, and posts randomly generated holy text to twitter.
    """
    try:
        auth = OAuthHandler(at['CONSUMER_KEY'], at['CONSUMER_SECRET'])
        auth.secure = True
        auth.set_access_token(at['ACCESS_KEY'], at['ACCESS_SECRET'])

        api = API(auth)

        # If the authentication was successful, you should
        # see the name of the account print out
        print(api.me().name)


        stream.userstream()

    except BaseException as e:
        print("Error in main()", e)


if __name__ == '__main__':
    main()
