# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:14:15 2020

@author: JonahG
"""

import tweepy
import json
import random




def main(name,allbots, replyOrCom):
    b = []
    name = TweetReply(name, allbots)
    if replyOrCom == "reply":
        return name.checkanreply()
    if replyOrCom == "com":
        return name.check(b)
       





class TweetReply:
    def __init__(self, name, allbots):
        self.name = name
        self.allbots = allbots
        #set access keys from text file
        Ckeys = []
        with open(self.name + 'BotKeys.txt', 'r', encoding='utf-8') as f:
            keys = f.readlines() 
        for key in keys:
            
            key = key.replace('\n', "")
            a,b = key.split(" ", 1)
            Ckeys.append(b)
        consumer_key = Ckeys[0]
        consumer_secret_key = Ckeys[1]
        bearer_token = Ckeys[2]
        access_token = Ckeys[3]
        access_token_secret = Ckeys[4]        
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        
        # Create API object
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
   #     self.api.search(me)
   #     screen_name = str(self.api.me()).split('',)
        self.screen_name = self.api.me()._json['screen_name']
       # print(self.screen_name)

    def checkanreply(self):
        mentions = self.api.mentions_timeline(count=3)
        return self.check(mentions)
        

    def check(self, mentions):
        twlist = []
        idlist = []
        commenting = True # pass this var as an option later
        
        
        if commenting==True:   
            com_post=self.getComPosts(self.allbots)
            if com_post != None:
                mentions.append(com_post)
        #mention = mentions[0]
        if mentions == None:
            return None, None
        for mention in mentions:
            
            tweet_id = mention.id
            user_name = mention.user.screen_name
            already_replied = False
            print("\n\n1" + user_name)
            
            
       #     print ("2" + str(mention.id))
       #     print('\n')
    
            replies = tweepy.Cursor(self.api.search, q='to:' + user_name, since_id=tweet_id, max_id=None, tweet_mode='extended').items()
            for reply in replies:
          #      print("3" + reply.user.screen_name)   
        #    print (reply.in_reply_to_status_id)
        #    print('\n')
                if(reply.in_reply_to_status_id == tweet_id):
           #         print ("4" + reply.user.screen_name) 
                    twlist.append(reply.user.screen_name)
           #         print("5" + str(twlist))
            
            if not twlist:     
                for tw in twlist:
                    if tw == self.screen_name:
                        already_replied = True
                                
                ranint = random.randint(0,4)
                if ranint == 4:
                    already_replied = True 

                if user_name in ('cybrDonaldTrump', 'Fanged_Joemena'):          
                    already_replied = True

                            
                if already_replied == False:
                   already_replied = True
            #       print("6" + "replying")
            #   print (tweet_id)
                   idlist.append(tweet_id)
             #      print("7" + str(idlist))
               #    return tweet_id, True
            twlist = []
            
        if idlist:
          #  print("returning this:")
          #  print(idlist)
            return idlist, True
        return None, None  
    
    def getComPosts(self, allbots):
        randomInt = random.randint(0, 15)
        Tposts = []
        allbots.append('benshapiro')
        if randomInt == 10:
            for name in allbots:
                posts = tweepy.Cursor(self.api.search, q='to:' + name, since_id=None, max_id=None, tweet_mode='extended').items(20)
                for post in posts:
                    Tposts.append(post)
            randomInt2 = random.randint(0,59)
            print (Tposts[randomInt2].full_text)
            return Tposts[randomInt2]
        return None
        
            
        
        
        
  
if __name__ == "__main__":
    main("Joebiden", ('JoeBiden', 'realDonaldTrump'))
    
    
    
    
    

#with open('bidenreplied.txt', 'r', encoding='utf-8') as f:
 #   textfile = f.read()
  #  f.seek(0, 0)
#  lines = f.readlines()
#  lines = f.readlines()
