"""Coordinates the twitter api with the markov chain models"""
import json
from pprint import pprint

import time
from threading import Thread

from tweepy import Stream, OAuthHandler, API
from tweepy.streaming import StreamListener

from holy_markov import BiblePassagesMarkov
from twitter_secrets import api_tokens as at


class HolyListener(StreamListener):

    bible = BiblePassagesMarkov()
    bot_name = 'HolyStupidArt'

    def send_passage(self, screen_name, name, text):

        if screen_name != self.bot_name:
            print('Passage sent to @' + screen_name)
            seed_words = [screen_name, name] + text.split()
            passage = self.bible.twitter_message(seed_words=seed_words,
                                                 line_length=(140 - len(screen_name) - 2))
            tweet = ''.join(['@', screen_name, ' ', passage])

            self.api.update_status(tweet)

    def on_connect(self):
        print("Connection established!!")

    def on_disconnect(self, notice):
        print("Connection lost!! : ", notice)

    def on_direct_message(self, status):
        try:
            dm = status._json['direct_message']
            self.send_passage(screen_name=dm['sender_screen_name'],
                              name='',
                              text='')
        except BaseException as e:
            print("Failed on_direct_message()", str(e))
            pprint(status._json)

        return True

    def on_event(self, status):
        try:
            event = status._json['event']
        except BaseException as e:
            print("Failed on_event()", str(e))
            pprint(status._json)
        else:
            if event == 'follow':
                self.send_passage(screen_name=status._json['source']['screen_name'],
                                  name='',
                                  text='')

    def on_status(self, status):
        print('Entered on_status()')
        try:
            self.send_passage(screen_name=status._json['user']['screen_name'],
                                  name='',
                                  text='')
        except BaseException as e:
            print("Failed on_status()", str(e))
            pprint(status._json)
        return True

    def on_error(self, status):
        print('Entered on_error()')
        pprint(status._json)


def main():
    """The main event loop for the holy twitter bot

    It watches for twitter events, and posts randomly generated holy text to twitter.
    """
    def passageEvery15():
        old_testa = BiblePassagesMarkov()
        while True:
            time.sleep(15*60)
            passage = old_testa.twitter_message()
            api.update_status(passage)
            print('Posted Tweet at {}'.format(time.localtime()[3:6]))


    auth = OAuthHandler(at['CONSUMER_KEY'], at['CONSUMER_SECRET'])
    auth.secure = True
    auth.set_access_token(at['ACCESS_KEY'], at['ACCESS_SECRET'])
    api = API(auth)

    # If the authentication was successful, you should
    # see the name of the account print out
    print(api.me().name)

    regular_thread = Thread(target=passageEvery15)
    regular_thread.start()

    stream = Stream(auth, HolyListener(api=api))
    stream.userstream()


if __name__ == '__main__':
    main()
