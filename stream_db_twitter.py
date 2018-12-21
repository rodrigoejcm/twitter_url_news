import json
import db_init
import datetime
from pony.orm import *
from dateutil import parser


from birdy.twitter import StreamClient
import pass_tw ## twitter credentials
#import unicodedata
#from unidecode import unidecode
#import timeline
from data_vars import follow
import re



client = StreamClient(pass_tw.CONSUMER_KEY,
                    pass_tw.CONSUMER_SECRET,
                    pass_tw.ACCESS_TOKEN,
                    pass_tw.ACCESS_TOKEN_SECRET)

resource = client.stream.statuses.filter.post(follow=follow)


@db_session
def save_data(json_data):

    #id = None
    if 'id' in json_data:

        
        id = json_data['id']

        if not db_init.Tweet.exists(id=id): 
            id_str = json_data['id_str']
            created_at = parser.parse(json_data['created_at'])
            

            truncated = json_data['truncated']
            if truncated : 
                text_full =  json_data['extended_tweet']['full_text'] 
            else:
                text_full =  json_data['text']
            
            ### To check if it is a retweet
            retweet_from_tweet_id = json_data['retweeted_status']['id'] if 'retweeted_status' in json_data else None 
            ### To check if it is a reply
            in_reply_to_user_id = json_data['in_reply_to_user_id'] if 'in_reply_to_user_id' in json_data else None 
            in_reply_to_status_id = json_data['in_reply_to_status_id'] if 'in_reply_to_status_id' in json_data else None 
            in_reply_to_screen_name = json_data['in_reply_to_screen_name'] if 'in_reply_to_screen_name' in json_data else None 

            #USER
            id_user = json_data['user']['id']
            id_str_user = json_data['user']['id_str'] if 'id_str' in json_data['user'] else None 
            screen_name = json_data['user']['screen_name'] if 'screen_name' in json_data['user'] else None  
            name = json_data['user']['name'] if 'name' in json_data['user'] else None  
            
            
            if(id_str_user in follow ):
                
                ### SAVE TWEET NA BASE DE ORIGINAL TWEETS                
                if(not retweet_from_tweet_id and not(in_reply_to_status_id or in_reply_to_screen_name or in_reply_to_user_id)):
                    ## SAVE USER
                    if not db_init.User.exists(id=id_user): 
                        db_init.User(
                            id = id_user,
                            screen_name_usuario = screen_name,
                            name_usuario = name
                        )
                    ## SAVE TWEET
                    tweet = db_init.Tweet(
                        id = id,
                        id_str = id_str,
                        id_usuario = id_user,
                        id_str_usuario = id_str_user,
                        created_at = created_at,
                        name_usuario = name,
                        text_full = text_full,
                    )

                    print("ORIGINAL -> ",text_full)

                    ### URL ###    

                    if truncated:
                        urls = json_data['extended_tweet']['entities']['urls']
                    else:
                        urls = json_data['entities']['urls']

                    for url in urls:
                        db_init.Url(tweet = tweet, 
                                    expanded_url = url['expanded_url'],
                                    url = url['url'],
                                    display = url['display_url'])
                        #print(url['expanded_url'])
                        #print(url['url'])
                        #print(url['display_url'])
                        #print("--------")

                        #with open("temp_data/"+str(id)+'.json', 'w') as outfile:
                        #    json.dump(json_data, outfile)

                    
                    

            elif(in_reply_to_status_id or in_reply_to_screen_name or in_reply_to_user_id ):
        
                ### SAVE TWEET NA BASE DE REPLIES
                if in_reply_to_status_id:
                    tw_id = in_reply_to_status_id
                    
                    if db_init.Tweet.exists(id=tw_id): 
                        ### USER
                        if not db_init.User.exists(id=id_user): 
                            db_init.User(
                                id = id_user,
                                screen_name_usuario = screen_name,
                                name_usuario = name
                            )
                            
                        ### TWEET_REPLY
                        if not db_init.Tweet_Reply.exists(id=id):
                            db_init.Tweet_Reply(
                                id = id,
                                id_str = id_str,
                                id_usuario = id_user,
                                id_str_usuario = id_str_user,
                                created_at = created_at,
                                text_full = text_full,
                                in_reply_to_user_id = in_reply_to_user_id, 
                                in_reply_to_status_id = in_reply_to_status_id
                                
                            )
                            print("REPLY -> ",id_user," - ", text_full)
                            #timeline.find_user_tweets(id_user)
                    else:
                        print("tweet original nao existe")
                                        
                
                #line = ' '.join(re.sub("([@#][A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text_full).split())
                #total_words = len(re.findall(r'\w+', line))

for data in resource.stream():
    save_data(data)
    commit()

