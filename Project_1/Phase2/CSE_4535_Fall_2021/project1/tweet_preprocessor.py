'''
@author: Souvik Das
Institute: University at Buffalo
'''

import demoji, re, datetime
import preprocessor


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet, type):

        # if(tweet.full_text.startswith("RT @") or tweet.full_text.startswith("rt @") ):
        #     processed_tweet = {
        #     "poi_name": None,
        #     "poi_id": None,
        #     "verified": None,
        #     "id": None,
        #     "replied_to_tweet_id": None,
        #     "replied_to_user_id" : None,
        #     "reply_text" : None,
        #     "tweet_text" : None,
        #     "tweet_lang" : None,
        #     "hashtags" : None,
        #     "mentions" : None,
        #     "tweet_urls" : None,
        #     "tweet_emoticons" : None,
        #     "tweet_date" : None,
        #     "tweet_en" : None,
        #     "tweet_es" : None,
        #     "tweet_hi" : None,
        #     "country" : None,
        # }

        #else :

        if(type == "POI"):
            poi_name = tweet.user.screen_name
            poi_id = tweet.user.id
        elif(type == "general" or type == "reply"):
            poi_name = None
            poi_id = None

        verified = tweet.user.verified
        id = tweet.id

        if(type == "POI" or type == "general") :
            replied_to_tweet_id = None
            replied_to_user_id = None
            reply_text = None
        elif(type == "reply"):
            replied_to_tweet_id = tweet.in_reply_to_status_id
            replied_to_user_id = tweet.in_reply_to_user_id
            reply_text = tweet.full_text

    # "in_reply_to_status_id": null,
    # "in_reply_to_status_id_str": null,
    # "in_reply_to_user_id": null,
    # "in_reply_to_user_id_str": null,
    # "in_reply_to_screen_name": null,

        tweet_text_raw = tweet.full_text
        tweet_text_cleaned, tweet_emoticons =  _text_cleaner(tweet.full_text)
        tweet_lang = tweet.lang
        hashtags = _get_entities(tweet._json, 'hashtags')
        mentions = _get_entities(tweet._json, 'mentions')
        tweet_urls = _get_entities(tweet._json, 'urls')
        tweet_date = str(_get_tweet_date(tweet.created_at.strftime('%a %b %d %H:%M:%S +0000 %Y')))
        #geolocation = tweet.geo
        tweet_xx = ""
        country = ""

        if(tweet.lang == "hi"):
            tweet_xx = "tweet_hi"
            country = "India"
        elif(tweet.lang == "es"):
            tweet_xx = "tweet_es"
            country = "Mexico"
        elif(tweet.lang == "en"):
            tweet_xx = "tweet_en"
            country = "USA"

        processed_tweet = {
            "poi_name": poi_name,
            "poi_id": poi_id,
            "verified": verified,
            "id": id,
            "replied_to_tweet_id": replied_to_tweet_id,
            "replied_to_user_id" : replied_to_user_id,
            "reply_text" : reply_text,
            "tweet_text" : tweet_text_raw,
            "tweet_lang" : tweet_lang,
            "hashtags" : hashtags,
            "mentions" : mentions,
            "tweet_urls" : tweet_urls,
            "tweet_emoticons" : tweet_emoticons,
            "tweet_date" : tweet_date,
            "country" : country,
            tweet_xx : tweet_text_cleaned,
            
        }

        return processed_tweet

        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''

        #raise NotImplementedError


def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet['entities']['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet['entities']['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet['entities']['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))
