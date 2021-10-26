'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("O6MeDnEEsDIXaF49jRmpnZnLH", "I4qgALKl9xAAwUSLa70o7i6PJaIN3V47XLXF3FjSQ2Vk9B7nBw")
        self.auth.set_access_token("1432557018670317568-b1MHevdUIZW3KYLb1dJomYiPyQGaVu", "JQLiqSbukDcGTNWp2xROjb52HdSNk2JWlml8vo5XmuN71")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    

    def get_tweets_by_poi_screen_name(self, name, count_no):
        print("collecting tweets..." + str(count_no))
        #tweets_by_poi = self.api.user_timeline(screen_name=name, count=count_no, include_rts = False, tweet_mode = 'extended')
        tweets_by_poi = tweepy.Cursor(self.api.user_timeline,screen_name=name, tweet_mode = 'extended', timeout=999999, count=count_no, include_rts = False).items(count_no)
        return tweets_by_poi

    def get_tweets_by_lang_and_keyword(self, keyword, lang_code, count_no):
        print("collecting tweets..."+ str(count_no))
        #date_since = "2021-09-01"
        tweets_by_keywords = tweepy.Cursor(self.api.search, q=keyword, lang=lang_code, tweet_mode='extended', include_rts = False, count=count_no).items(count_no)
        return tweets_by_keywords

    def get_replies(self, name, count_no):

        #print("collecting tweets in replies..." + str(count_no))
        #tweets_for_replies = tweepy.Cursor(self.api.search,q='to:'+name,result_type='recent',timeout=999999, tweet_mode = 'extended', include_rts = False, count=100).items(count_no)
        #return tweets_for_replies

#tweet_id = ['1440064291143442435' , '1439620763837886466' , '1439270211874529285' , '1438584801678659585' , '1438330243811463170' , '1435963500405276672' , '1433488717780422659']
        # name = "SSalud_mx"
        # tweet_id = "1440767863774658566"

        # replies=[]
        replies = tweepy.Cursor(self.api.search,q='to:'+name, timeout=999999, count=count_no, include_rts = False, tweet_mode='extended').items(count_no)
        #     #print("inside for loop")
        #     if hasattr(tweet, 'in_reply_to_status_id_str'):
        #         if (tweet.in_reply_to_status_id_str==tweet_id):
        #             print("got reply")
        #             replies.append(tweet)
        # print(len(replies))
        return replies            

        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        #raise NotImplementedError
    #def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        #raise NotImplementedError
