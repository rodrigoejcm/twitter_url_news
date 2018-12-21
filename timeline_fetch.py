import json
import db_init
import datetime
import time
from pony.orm import *
from dateutil import parser


from birdy.twitter import UserClient, TwitterApiError

import pass_tw ## twitter credentials
#import unicodedata
#from unidecode import unidecode

client2 = UserClient(pass_tw.CONSUMER_KEY_2,
                    pass_tw.CONSUMER_SECRET_2,
                    pass_tw.ACCESS_TOKEN_2,
                    pass_tw.ACCESS_TOKEN_SECRET_2)

resource_timeline = client2.api.statuses.user_timeline

@db_session
def find_tweets_to_fecth():
    to_fetch = db_init.Tweet_Reply.select(lambda p: p.fetch_status == "To Fetch")[:]
    return to_fetch

@db_session
def update_tweets(list_tweets):
    for tweet in list_tweets:
        print(tweet.id) #id_usuario
        status = find_user_tweets(tweet.id_usuario, tweet.id)
        db_init.Tweet_Reply[tweet.id].fetch_status = status
        commit()

@db_session
def find_user_tweets(id_user, id_reply_ref):
    try:
        response_timeline = resource_timeline.get(user_id=id_user, count=100, include_rts=False,  tweet_mode='extended')
        for tweet in response_timeline.data:
            if 'id' in tweet:

                truncated = tweet['truncated']
                if truncated : 
                    text_full =  tweet['full_text']
                else:
                    text_full =  tweet['full_text']
                    
                    db_init.Extra_User_Tweet(
                        #id=tweet['id'],
                        id_usuario=id_user,
                        text_full=text_full,
                        created_at= parser.parse(tweet['created_at']),
                        tweet_reply_ref = id_reply_ref
                    )
                    print("tweet do usuario -> " ,id_user)
                    status = "OK"
        time.sleep(1)
    except TwitterApiError:
        status = "Erro"

    return status

    

    #commit()

#find_user_tweets(281827460)


while True:

    to_fetch = find_tweets_to_fecth()
    if to_fetch:
        update_tweets(to_fetch)
    else: 
        print("Não existem tweets novos")
        time.sleep(5)





