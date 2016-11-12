"""Coordinates the twitter api with the markov chain models"""
import json

from tweepy import Stream, OAuthHandler, API
from tweepy.streaming import StreamListener

from holy_markov import OldTestaPassagesMarkov
from twitter_secrets import api_tokens as at


class HolyListener(StreamListener):

    old_testa = OldTestaPassagesMarkov()

    def on_connect(self):
        print("Connection established!!")

    def on_disconnect(self, notice):
        print("Connection lost!! : ", notice)

    def on_direct_message(self, status):
        dm = status._json['direct message']
        screen_name = dm['sender_screen_name']

        print("Entered on_direct_message().", 'Passage sent to @' + screen_name)

        passage = self.old_testa.twitter_message(line_length=(140 - len(screen_name) - 2))
        tweet = ''.join(['@', screen_name, ' ', passage])
        try:
            self.api.update_status(tweet)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))

    def on_event(self, status):
        print('Entered on_event()')
        print(status)

    def on_error(self, status):
        print('Entered on_error()')
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

        stream = Stream(auth, HolyListener(api=api))

        stream.userstream()

    except BaseException as e:
        print("Error in main()", e)


if __name__ == '__main__':
    main()
