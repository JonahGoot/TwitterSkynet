# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:14:15 2020

@author: JonahG
"""
import json
import _thread
from threading import Thread, currentThread, activeCount
import sys
import time
import tweepy
import markovify
import multiprocessing


consumer_key = "sl9PVFa9aaTohRkIJyy1p7tl8"
consumer_secret_key = "LvcdbNWR3ls1Ns9tg7FB3dHTsuC0sVrfeLmPPGMrI4IZpaN2UH"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAJl0GgEAAAAANayCdDRak31lyGmibVooze4xEHM%3DDlUFrwX6tgM9uvVgTsmAJ58ZkzlVKiyZFcbFMf79i2w9z7MCdv"
access_token = "1291219258593153024-oPTaCp2echfcbfDFeJaJY6vB7KPBzL"
access_token_secret = "PAMBBGj7jpSwAP4abzxYMjOPbadU27RCQJBDyZOGnqs21"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)










def checkanreply():
    twlist = []
    idlist = []
    mentions = api.mentions_timeline(count=3) 
    #mention = mentions[0]

    for mention in mentions:
        
        tweet_id = mention.id
        user_name = mention.user.screen_name
        already_replied = False
        print("\n\n1" + user_name)
        print ("2" + str(mention.id))
        print('\n')

        replies = tweepy.Cursor(api.search, q='to:' + user_name, since_id=tweet_id, max_id=None, tweet_mode='extended').items()
        for reply in replies:
            print("3" + reply.user.screen_name)   
    #    print (reply.in_reply_to_status_id)
    #    print('\n')
            if(reply.in_reply_to_status_id == tweet_id):
                print ("4" + reply.user.screen_name) 
                twlist.append(reply.user.screen_name)
                print("5" + str(twlist))
        
        if not twlist:     
            for tw in twlist:
                if tw == 'Fanged_Joemena':
                    already_replied = True        
            if already_replied == False:
               already_replied = True
               print("6" + "replying")
        #   print (tweet_id)
               idlist.append(tweet_id)
               print("7" + str(idlist))
           #    return tweet_id, True
        twlist = []
        
    if idlist:
      #  print("returning this:")
      #  print(idlist)
        return idlist, True
    return None, None  
        
  
if __name__ == "__main__":
    checkanreply()
    
    
    

#with open('bidenreplied.txt', 'r', encoding='utf-8') as f:
 #   textfile = f.read()
  #  f.seek(0, 0)
#  lines = f.readlines()