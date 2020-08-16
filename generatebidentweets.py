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
import os
import tkinter






class TwitterBot:    
    def __init__(self, name):
        self.con = True
        self.lastid = 1
        self.init = False
        self.name = name
        
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
        
        #Generate Markov Model

        with open('tweetdata' + self.name + '.txt', 'r', encoding='utf-8') as f:
            textfile = f.read()      
        TEXT_LENGTH = len(textfile)            
        print(f'Number of characters in text: {TEXT_LENGTH}')               
        self.text_model = markovify.Text(textfile)
 
    
            
        
        
#Check the bots most recent mention, returns post id    
    def checknewR(self):
        newr = self.api.mentions_timeline(count=1)
        try:
            new = newr[0].id
        except:
            new = newr
        return new

    
    def genpost(self, kind):
        post = self.text_model.make_sentence(tries=50)
        if post == None:
            return self.genpost()

        #for generating regular posts
        if kind == "p":  
            #strip all but the first url out
            
            lurl = re.search("(?P<url>https?://[^\s]+)", post)
            if lurl != None:
                lurl = lurl.group("url")
                a,b = post.split(lurl, 1)
                oneUrl = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', b, flags=re.MULTILINE)
                post = a + lurl + oneUrl
                post = post.replace('  ', ' ')
            #check length
            if len(post) > 280:
                return self.genpost("p")  
            
        #for generating replies
        if kind == "r":
            post = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', post, flags=re.MULTILINE)
            if len(post) > 227:
                return self.genpost("r")
        print(post)    
        return post

#for sending actual post
    def makepost(self, post): 
           self.api.update_status(post)
       
       
      # print("making post filler")
  
        
    def makereply(self, post, postid):
        print(postid)
        randomInt = random.randint(0,1)
        if randomInt == 1:
            post = post.lower()
            post = "Because of how short ben shapiro is, "+post
        
        
        
        randomInt = random.randint(0, 2)
        if self.name == "JoeBiden":
            if randomInt == 0:
                post = post.lower()
                rpost = "Look here jack, " + post
            elif randomInt == 1:
                post = post.lower()
                rpost = "Come on maaan, " + post
            else:
                post = post.lower()
                rpost = "Look here fat, " + post
                
        if self.name == "realDonaldTrump":
            if randomInt == 0:
                post = post.lower()
                rpost = "Listen, " + post
            elif randomInt == 1:
                rpost =  post + ", TRUST ME!"
            else:
                post = post.lower()
                rpost = "FAKE NEWS! " + post
        
        
        self.api.update_status(status = rpost, in_reply_to_status_id = postid , auto_populate_reply_metadata=True)      

    
                      
        #selecting a post if you choose to only make one
    def yes_or_no(self, question):
        post = self.genpost("p")
        reply = str(input(question+' (y/n): ')).lower().strip()
        
        if reply == 'y':
            self.makepost(post)
            return
        elif reply == 'n':
            return self.yes_or_no('how about this one?')
        else:
            return self.yes_or_no("Uhhhh... please enter ")
        
        #continual looping in seperate thread to make periodic posts and scan for any new replies
    def looping(self, looptime):
       
        
        #Main Loop                
        
        while self.con == True:
            post = self.genpost("p")     
            if self.init == True:
                 self.makepost(post)
            if self.init == False:
                self.init = True
            
            for i in range(looptime):
              #  print("starting replyin loop") 

                print("checknewR: " + str(self.checknewR()))
                
                print("lastreplyid: " + str(self.lastid))
                
     #1           print("replyin loop2")
     
                if self.checknewR() != self.lastid:
                    self.lastid = self.checknewR() 
                    tweetreplyV = tweetreply.main(self.name, allbotnames(), "reply")
                    print ("tweet to reply to: " + str(tweetreplyV[1]))
                    
                    if tweetreplyV[1] == True:
                        makeTWEE = tweetreplyV[0]
                        print ("999" + str(makeTWEE))
                        for TWEE in makeTWEE:
                            post = self.genpost("r")
                            self.makereply(post, TWEE)
                            
                tweetcom = tweetreply.main(self.name, allbotnames(), "com") 
                if tweetcom[1] == True:
                    
                    makeTWE = tweetcom[0]
                    for TWE in makeTWE:
                        post = self.genpost("r")
                        self.makereply(post, TWE)
                            
                            
                            
                            
                        
                for i in range(30):
                    time.sleep(1)
                    if self.con == False:
                        break
                if self.con == False:
                        break
                    
        print("exiting looping")
        sys.exit()
            

        
        
  #  def listenforexit():       
 #       input('press enter to exit')
  #      sys.exit()
            
        

def wait():
    sys.sleep(1)    



def main():
    Bots = []
    print ("Select one or more bots:\n 1:All\n 2:Bidenbot\n 3:Trumpbot")
    reply = int(input('(1/2/3): '))
    if reply == 1:
        allnames = allbotnames()
        for name in allnames:
            Bots.append(TwitterBot(name))       
    elif reply == 2:
        Bots[0] = TwitterBot("JoeBiden")
    elif reply == 3:
        Bots[0] = TwitterBot("realDonaldTrump")
    else: return main
    
    print ("Auto run or select single post?\n 1:autorun\n 2:single post")
    reply = int(input('(1/2/3): '))
    
    #if you choose autorun
    if reply == 1:
        for bot in Bots:
            print ("Enter time frame betwen posts in minutes for "+ bot.name +":")
            looptime = int(input(': '))*2
            print('initiating' + bot.name)
            _thread.start_new_thread(bot.looping, (looptime,)) #Initiates bot loops for continual posting
        input('press enter to exit')
        for bot in Bots:
            bot.con = False     
        sys.exit()
        
    elif reply == 2:
        for bot in Bots:
            bot.init = True
            bot.yes_or_no("would you like "+ bot.name +" to make this post")
    else: 
        return main()
    
    

    
    
    
    
    
    
    #return names of all bots
def allbotnames():
    file_names = os.listdir()
    files = []
    for file in file_names:
        if "BotKeys" in file:
            files.append(file.replace('BotKeys.txt',''))
    return files

        
       
        
if __name__ == "__main__":
    main()






    







    

