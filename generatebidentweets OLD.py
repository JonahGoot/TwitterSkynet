# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:53:44 2020

@author: JonahG
"""
import _thread
import sys
import time
import tweepy
import markovify
import tweetreply
import re
import random

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





with open('tweetdata.txt', 'r', encoding='utf-8') as f:
    textfile = f.read()
    f.seek(0, 0)
    lines = f.readlines()



TEXT_LENGTH = len(textfile)
LINENUM = len(lines)

print(f'Number of characters in text: {TEXT_LENGTH}')
print(f'Number of lines in text: {LINENUM}')

lastid = 1

text_model = markovify.Text(textfile)
con = 1
#change init to true to bake post at start of looping phase
init = False




class bidenbot: 
    
    def checknewR():
        newr = api.mentions_timeline(count=1) 
        new = newr[0].id
        return new

    
    def genpost(kind):
        post = text_model.make_sentence(tries=50)
        if post == None:
            return bidenbot.genpost()

        #for generating regular posts
        if kind == "p":  
            #strip all but the first url out
            print(post)
            lurl = re.search("(?P<url>https?://[^\s]+)", post)
            if lurl != None:
                lurl = lurl.group("url")
                a,b = post.split(lurl, 1)
                oneUrl = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', b, flags=re.MULTILINE)
                post = a + lurl + oneUrl
                post = post.replace('  ', ' ')
            #check length
            if len(post) > 280:
                return bidenbot.genpost("p")  
            
        #for generating replies
        if kind == "r":
            post = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', post, flags=re.MULTILINE)
            if len(post) > 264:
                return bidenbot.genpost("r")
        return post

#for sending actual post
    def makepost(post): 
       global init
       if init == True:
           api.update_status(post)
       if init == False:
           init = True
       
      # print("making post filler")
  
        
    def makereply(post, postid):
        
        randomInt = random.randint(0, 2)
        if randomInt == 0:
            rpost = "look here jack, " + post
        if randomInt == 1:
            rpost = "Come on maaan, " + post
        if randomInt == 2:
            rpost = "look here fat, " + post
        
        api.update_status(status = rpost, in_reply_to_status_id = postid , auto_populate_reply_metadata=True)      

    
                      

    def yes_or_no(question):
        post = bidenbot.genpost("p")
        print('\n' + post + '\n')
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            bidenbot.makepost(post)
            sys.exit()
        if reply[0] == 'n':
            return bidenbot.yes_or_no('how about this one?')
        else:
            return bidenbot.yes_or_no("Uhhhh... please enter ")
        
    def looping(looptime):
        global con
        global lastid
        global check
        
        while con == 1:
            post = bidenbot.genpost("p")
            print(post)
            bidenbot.makepost(post)
            
            for i in range(looptime):
              #  print("starting replyin loop") 

                print("checknewR: " + str(bidenbot.checknewR()))
                
                print("lastreplyid: " + str(lastid))
                
     #1           print("replyin loop2")
     
                if bidenbot.checknewR() != lastid:
                    lastid = bidenbot.checknewR() 
                    tweetreplyV = tweetreply.checkanreply()
                    print ("tweet to reply to: " + str(tweetreplyV[1]))
                    
                    if tweetreplyV[1] == True:
                        makeTWEE = tweetreplyV[0]
                        print ("999" + str(makeTWEE))
                        for TWEE in makeTWEE:
                            post = bidenbot.genpost("r")
                            bidenbot.makereply(post, TWEE)
                        
                for i in range(30):
                    time.sleep(1)
                    if con != 1:
                        break
                if con != 1:
                        break
                    
        print("exiting looping")
        sys.exit()
            

        
        
  #  def listenforexit():       
 #       input('press enter to exit')
  #      sys.exit()
            
        

def wait():
    sys.sleep(1)    



def main():
    print ("Auto run or select single post?\n 1:autorun\n 2:single post")
    reply = int(input('(1/2): '))
    if reply == 2:
        bidenbot.yes_or_no("would you like Simulation Biden to make this post")
    if reply == 1:
        print ("Enter time frame betwen posts in minutes:")
        looptime = int(input(': '))*2
        
        global con
        looptime = looptime*2
        _thread.start_new_thread(bidenbot.looping, (looptime,)) 
        input('press enter to exit') 
        con = con+1       
        sys.exit()
                 
    else: 
        return main()
        
       
        
if __name__ == "__main__":
    main()







    

