# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 02:15:23 2020

@author: JonahG
"""


import tkinter as tk
import _thread

from PIL import ImageTk, Image
import generatebidentweets as Gen


#from tkinter import messagebox

class Window1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        filename = tk.PhotoImage(file = "Terminator.png")
#background image       
        self.master.grid_propagate(False)
        background = tk.Label(self.master, image=filename)
        background.place(x=0, y=0, relwidth=1, relheight=1)
        background.image = filename   
        

        

        
#get name of all bots for drop down option        
        self.BotList = Gen.allbotnames()
        self.BotList.append("All Bots")
        self.BotList.insert(0,"Select Bots")        
        
#select which bot to run        
        self.botvar = tk.StringVar(self.master)
        
        
        print(self.BotList)
        self.botvar.set(self.BotList[0])
        
        botopt = tk.OptionMenu(self.master, self.botvar, *self.BotList)
        
        botopt.config(width=15, font=('Helvetica', 12))
        botopt.grid(column=0,row=0,pady=10,padx=10)
        
#pre-initialize auto or single list and launch button   
        self.AorSlist = None
        self.lbutt = None
        self.BOTS = []
        self.botvar.trace("w", self.autoOrSingle)
       
     
    def autoOrSingle(self, *args):
        try:
            if self.aorsvar != None:
                self.whipe(3)
        except AttributeError: pass
        
        print(self.botvar.get())
        if self.AorSlist == None:
            self.AorSlist = ('Select', 'Auto Post', 'Single Post')
            self.aorsvar = tk.StringVar(self.master)
            self.aorsvar.set(self.AorSlist[0])
            self.aorsopt = tk.OptionMenu(self.master, self.aorsvar, *self.AorSlist )
            self.aorsopt.config(width=15, font=('Helvetica', 12))
            self.aorsvar.trace("w", self.launchButton)
        
        
        
        if self.botvar.get() != "Select Bots":
            self.aorsopt.grid(column=1,row=0, padx=20)
            
        else:         
            self.whipe(2)
                
            
#create launch button to run bot in either single or looped mode            
    def launchButton(self, *args):        
        if self.lbutt == None:           
            self.lbutt = tk.Button(self.master, text="LAUNCH", command=self.launch)
            
        if self.aorsvar.get() == 'Single Post':
            self.whipe(1)
            self.lbutt.grid(column=2,row=0)            
        elif self.aorsvar.get() == 'Auto Post':
            self.lbutt.grid_forget()
            print("autoposting")
            self.AutopostB()
        else:           
            self.whipe(1)
        
        print(self.aorsvar.get())
        
    def whipe(self, pos):
        if pos >= 2:
            try:
                self.aorsopt.grid_forget()
            except AttributeError: pass
        if pos >= 1:
            try:
                self.lbutt.grid_forget()
            except AttributeError: pass               
                
        try:    
            for label in self.labels:
                label.grid_forget()
            for entry in self.entries:
                entry.grid_forget()
        except AttributeError: pass
        if pos == 3:
            self.launchButton()
        
        
        
        
#when launch button is pressed       
    def launch(self):
        self.exitBs = []
        self.BOTS = []
        self.inputs = []
        if self.botvar.get() == 'All Bots':
            for bot in Gen.allbotnames():
                self.BOTS.append(Gen.TwitterBot(bot))
        else:
            self.BOTS.append(Gen.TwitterBot(self.botvar.get()))
                
        if self.aorsvar.get() == "Single Post":
            for bot in self.BOTS:
                bot.init = True
                post = bot.genpost("p")
                pop=tk.messagebox.askquestion(bot.name, 'Make post: \n"'+post)
                if pop == 'yes' :
                    bot.makepost(post)
        elif self.aorsvar.get() == "Auto Post":
            # for entry in self.entries:
            #     inputs.append(entry.get())
            self.lbutt.grid_forget()
            count = 0
            
            for bot in self.BOTS:
               _thread.start_new_thread(bot.looping, (int(self.entries[count].get()),))
               self.exitBs.append(tk.Button(self.master, text="Stop", command=lambda b=bot,c=count: self.stopping(b,c)))
               count = count+1
            count=0   
            for b in self.exitBs:
                b.grid(column=3,row=count)
                count=count+2
     
    def stopping(self, bot, count):  
        bot.con=False     
        self.exitBs[count].grid_forget()
#        self.exitBs[count].grid_forget()            
          
            
                
 #when autopost is selected             
    def AutopostB(self):
        count = 0
        self.entries = []
        self.labels = []
     ####   self.exitB = []
        #If all bots are selected
        if self.botvar.get() == "All Bots":
            for g in Gen.allbotnames():
                label = tk.Label(self.master, text=g+"Looptime(minutes):")
                self.labels.append(label)
                label.grid(column=2,row=count,pady=10,sticky=tk.W)
                self.entries.append(tk.Entry(self.master))       
                count = count+2
         #If only one bot is selected        
        else:   
            label = tk.Label(self.master, text=self.botvar.get()+"Looptime(minutes):")
            label.grid(column=2,row=count,pady=10,sticky=tk.W)
            self.labels.append(label)                
            self.entries.append(tk.Entry(self.master)) 
            count = count+2
        count=1
        for entry in self.entries:
            entry.grid(column=2,row=count, sticky=tk.W)
            count = count+2
        self.lbutt.grid(column=3,row=1,padx=30)   
          
        
        
            
        
            
            
            
        
        
        



def main(): #run mainloop 
    root = tk.Tk()
    app = Window1(root)
    root.geometry('740x370')
    root.mainloop()

if __name__ == '__main__':
    main()










