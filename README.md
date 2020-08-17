# TwitterSkynet

This is the first thing I've made in python, I learn better by doing so I just wanted to kinda jump right in and try to do something fun.
It's an automatic twitter parody bot generator, that scrapes anyones tweets and runs them through markovify(markov chain) 
to generate new tweets and automatically post them(you set the time frame between new posts for each bot, each time you launch the bots)
currently all bots occasionally randomly reply to the replies of any of the original accounts they are parodying, Im going to add an option to turn commenting on or off
in the gui later


1) add any account name as a new line in the TweetsToScrape file
2) run the scraper, and the last couple thousand tweets from the account will be scraped into a tweetdata file, exluding retweets
3) create a new "username you scraped from"BotKeys.txt, with the keys from a new twitter account that will be your bot
4) your parody bot is ready, run as many bots as you want through the gui, or directly through the generatebidentweets.py file 


(the main file name is generatebidentweets because that's what i started with and i haven't bothered to change it yet but it works with any bot, and currently I have it running 
bot a trump and a biden parody bot. this is not a partisan project in any way)











