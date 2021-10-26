'''
@author: Souvik Das
Institute: University at Buffalo
'''

import json
import datetime
import pandas as pd
from twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer

reply_collection_knob = False


def read_config():
    with open("config.json") as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json", 'w') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("data/" + filename)


def read_file(type, id):
    return pd.read_pickle(f"data/{type}_{id}.pkl")


def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()

    pois = config["pois"]
    keywords = config["keywords"]
    tweet_count = 0


    # processed_replies = []
    # #name = 'GavinNewsom'
    

    # processed_replies = []
    # replies = twitter.get_replies()

    # for tweet in replies:
    #     processed_replies.append(TWPreprocessor.preprocess(tweet, "reply"))     

    # indexer.create_documents(processed_replies)

    # write_config({
    #     "pois": pois, "keywords": keywords
    # })

    # save_file(processed_replies, f"GavinNewsom_replies.pkl")
    # print("------------ process complete -----------------------------------")
    # print("Collected tweets: "+str(tweet_count)) 




    # replies=[]
    # processed_tweets = []
    # processed_replies = []
    # name = "narendramodi"
    # count = 50
    # for full_tweets in twitter.get_tweets_by_poi_screen_name(name, count):
    #     tweet_count = 0
    #     processed_tweets.append(TWPreprocessor.preprocess(full_tweets, "POI"))
    #     for tweet in twitter.get_replies(name, 60):
    #         if hasattr(tweet, 'in_reply_to_status_id_str'):
    #             if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
    #                 processed_replies.append(TWPreprocessor.preprocess(tweet, "reply"))
    #                 tweet_count += 1
        
    # print("Collected tweets: "+str(tweet_count))

    # indexer.create_documents(processed_tweets)
    # indexer.create_documents(processed_replies)


    # write_config({
    #     "pois": pois, "keywords": keywords
    # })

    #save_file(processed_tweets, f"MoHFW_INDIA_replies.pkl")
    #print("------------ process complete -----------------------------------")
    #print("Collected tweets: "+str(tweet_count))
    #print(processed_tweets)  

    
    # tweet_count = 0
    # poi_tweets = twitter.get_tweets_by_poi_screen_name(name, count)
    # raw_tweets=[]
    # for tweet in raw_tweets:
    #     if("RT @" not in tweet.full_text) and ("rt @" not in tweet.full_text) and (not tweet.retweeted) and tweet.in_reply_to_status_id != None:
    #         poi_tweets.append(TWPreprocessor.preprocess(tweet, "reply"))
    #         tweet_count += 1

    # indexer.create_documents(poi_tweets)

    # pois[i]["finished"] = 1
    # pois[i]["collected"] = len(processed_tweets)

    # write_config({
    #     "pois": pois, "keywords": keywords
    # })

    # save_file(processed_tweets, f"replies_1.pkl")
    # print("------------ process complete -----------------------------------")
    # print("Collected tweets: "+str(tweet_count))

    name = "mrkate"
    count = 2000
    tweet_count = 0
    raw_tweets = twitter.get_tweets_by_poi_screen_name(name, count)  # pass args as needed

    processed_tweets = []
    for tw in raw_tweets:
        if(("RT @" not in tw.full_text) and ("rt @" not in tw.full_text) and (not tw.retweeted) and (tw.in_reply_to_status_id != None)):
            processed_tweets.append(TWPreprocessor.preprocess(tw, "reply"))
            tweet_count += 1

    indexer.create_documents(processed_tweets)

    save_file(processed_tweets, f"reply_1.pkl")
    print("------------ process complete -----------------------------------")
    print("Collected tweets: "+str(tweet_count))






    # for i in range(len(pois)):
    #     tweet_count = 0
    #     if pois[i]["finished"] == 0:
    #         print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")

    #         raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i]['screen_name'], pois[i]['count'])  # pass args as needed

    #         processed_tweets = []
    #         for tw in raw_tweets:
    #             processed_tweets.append(TWPreprocessor.preprocess(tw, "POI"))
    #             tweet_count += 1

    #         indexer.create_documents(processed_tweets)

    #         pois[i]["finished"] = 1
    #         pois[i]["collected"] = len(processed_tweets)

    #         write_config({
    #             "pois": pois, "keywords": keywords
    #         })

    #         save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
    #         print("------------ process complete -----------------------------------")
    #         print("Collected tweets: "+str(tweet_count))
    #         #print(processed_tweets)

            
    # for i in range(len(keywords)):
    #     tweet_count = 0
    #     if keywords[i]["finished"] == 0:
    #         print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")

    #         raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]['name'], keywords[i]['lang'], keywords[i]['count'])  # pass args as needed

    #         processed_tweets = []
    #         for tw in raw_tweets:
    #             if(not(tw.full_text.startswith("RT @") or tw.full_text.startswith("rt @")) ):
    #                 processed_tweets.append(TWPreprocessor.preprocess(tw, "general"))
    #                 tweet_count += 1

    #         indexer.create_documents(processed_tweets)

    #         keywords[i]["finished"] = 1
    #         keywords[i]["collected"] = len(processed_tweets)

    #         write_config({
    #             "pois": pois, "keywords": keywords
    #         })

    #         save_file(processed_tweets, f"keywords_{keywords[i]['id']}.pkl")

    #         print("------------ process complete -----------------------------------")
    #         print("Collected tweets: "+str(tweet_count))
    #         #print(processed_tweets)


    #if reply_collection_knob:
        # Write a driver logic for reply collection, use the tweets from the data files for which the replies are to collected.

        #raise NotImplementedError


if __name__ == "__main__":
    main()
