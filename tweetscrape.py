# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:35:22 2020

@author: JonahG
"""

import json
import csv
import tweepy
import re

Ckeys = []
with open('ScanKeys.txt', 'r', encoding='utf-8') as f:
    keys = f.readlines() 
for key in keys:            
    key = key.replace('\n', "")
    a,b = key.split(" ", 1)
    Ckeys.append(b)
consumer_key = Ckeys[0]
consumer_key_secret = Ckeys[1]
bearer_token = Ckeys[2]
access_token = Ckeys[3]
access_token_secret = Ckeys[4]

    #create authentication for accessing Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
    
    #initialize Tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    

def main():
    with open('ProfilesToScrape.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print("Extracting tweets from " + str(len(lines)) + " profiles:")
    for line in lines:
        line = line.replace('\n', "")
        print(line)   
        line = ScrapeInstance(line)
        line.createfile()
        line.ScrapeIntoFile()
        




class ScrapeInstance:
    def __init__(self, name):
        self.name = name
        self.f = None
    
    
    def createfile(self):
        filename = "tweetdata" + self.name + ".txt"
        self.f = open(filename, "w", encoding='utf-8')

    def ScrapeIntoFile(self): 
        for tweet in tweepy.Cursor(api.user_timeline,id=self.name, tweet_mode='extended', include_rts=False).items():
            text = tweet.full_text 
            self.f.write(text.replace('\n',' ').replace('&amp', '') + ('\n'))
        self.f.close()
    
    
if __name__ == "__main__":
    main()
#JoeBiden = ScrapeInstance("JoeBiden")
#JoeBiden.createfile()
#JoeBiden.scrapeintofile()





