import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import pandas as pd
import numpy as np
import csv
import math

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'Exmf1lXUqO89Sm1tIk62CH8mc'
        consumer_secret = 'Q6GLPLRmkX1XOljSl02Zb2x0YSdXxP28D2L3Wkw1e6RUgxCovu'
        access_token = '1111728489164615682-JVqhenKoMkuvsNM60m9vJqHTOc8YbV'
        access_token_secret = 'W8W0aKrrZ6i9N619jh4nJtXbFzS4150QmT01bMonpZNXT'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split()) )

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


# def main():
#     # creating object of TwitterClient Class
#     api = TwitterClient()
#     # calling function to get tweets
#     tweets = api.get_tweets(query='Donald Trump', count=200)
#
#     # picking positive tweets from tweets
#     ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
#     # percentage of positive tweets
#     print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
#     # picking negative tweets from tweets
#     ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
#     # percentage of negative tweets
#     print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
#     # percentage of neutral tweets
#     print("Neutral tweets percentage: {} % \
#           ".format(100 * len(tweets - ntweets - ptweets) / len(tweets)))
#
#     # printing first 5 positive tweets
#     print("\n\nPositive tweets:")
#     for tweet in ptweets[:10]:
#         print(tweet['text'])
#
#     # printing first 5 negative tweets
#     print("\n\nNegative tweets:")
#     for tweet in ntweets[:10]:
#         print(tweet['text'])

if __name__ == "__main__":
    # calling main function
    #main()
    # creating object of TwitterClient Class
    # api = TwitterClient()
    # # calling function to get tweets
    # tweets = api.get_tweets(query='Donald Trump', count=200)
    #
    # # picking positive tweets from tweets
    # ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # # percentage of positive tweets
    # print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # # picking negative tweets from tweets
    # ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # # percentage of negative tweets
    # print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # # percentage of neutral tweets
    # print("Neutral tweets percentage: {} % \
    #       ".format(100 * len(tweets - ntweets - ptweets) / len(tweets)))
    #
    # # printing first 5 positive tweets
    # print("\n\nPositive tweets:")
    # for tweet in ptweets[:10]:
    #     print(tweet['text'])
    #
    # # printing first 5 negative tweets
    # print("\n\nNegative tweets:")
    # for tweet in ntweets[:10]:
    #     print(tweet['text'])


    file = "Sentiment_Analysis_Dataset.csv"
    #df = pd.read_csv(file, sep=',', header=None)
    sh = TwitterClient()
    with open(file, 'r') as dest_f:
        data_iter = csv.reader(dest_f,
                               delimiter=",",
                               quotechar='"')
        data = [data for data in data_iter]
    data_array = np.asarray(data)
    data_array = np.delete(data_array, (0), axis=0)
    
    percentage = 0.2 # What portion of data you want to analyze??
    for i in range( math.floor( percentage*np.shape(data_array)[0]) ):
        sent = sh.get_tweet_sentiment(data_array[i][3])
        if sent == "positive":
            data_array[i][1] = 1
        elif sent =="neutral":
            data_array[i][1] = 0.5
        elif sent == "negative":
            data_array[i][1] = 0

        if i%100 == 0:
             print (i)

    np.save("data", data_array)





print("done")