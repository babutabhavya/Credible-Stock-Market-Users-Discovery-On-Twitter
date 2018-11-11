#Created By Bhavya Babuta 
#YEAR 2018
#Credible Twitter User Discovery
#IF TWEEPY THROWS AN ERROR PLEASE CHANGE ALL THE async to async_it in python3.7/site-packages/tweepy/streaming.py and execute using python3
#This Project Trains the Model Based on names of Twitter Users that are extracted from a .TXT FILE.
#NAIVES BAYES CLASSIFICATION USING SCI KIT LEARN
#FOR ANY SUGGESTIONS AND CORRECTIONS PLEASE WRITE TO BABUTABHAVYA@GMAIL.COM
import tkinter as tk
import tweepy
import sys
import time
import numpy as np
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import SSLError,ReadTimeoutError
from sklearn.naive_bayes import GaussianNB

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def exit():
            sys.exit(-1)
        start_label = tk.Label(self, text="Welcome To Our Final Year Project. Hit Enter To Experience The Awesomeness That Follows.",width=500,height=20,font=("Courier", 20))
        page_1_button = tk.Button(self, text="Enter",command=lambda: master.switch_frame(PageOne),width=50)
        quit = tk.Button(self, text="Quit",command=exit,width=50)
        start_label.pack(side="top", fill="x", pady=10)
        page_1_button.pack(pady=100)
        quit.pack(pady=20)
        
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global ratio
        global ids
        ratio=[]
        def exit():
            sys.exit(-1)
        header = tk.Label(self, text="Credibility Analysis For Twitter Stock Market Users",width=500,height=5,font=("Courier", 15))
        test_label = tk.Label(self, text="Enter The Stock Market Handle to Check For Its Credibility",width=500,height=5,font=("Courier", 15))
        quit_one = tk.Button(self, text="Quit",command=exit,width=50)
        def train():
            global auth
            global api
            auth = tweepy.AppAuthHandler('kHxhJj4BXE25KiG8ebLJbMDsk', 's7Jgq6VvHkDSO0AF1dycTfTJbzSIp0BFUm7lIMSPYNrTiAyxHQ')
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
            if (not api):
                tk.messagebox.showinfo(message="Can't Authenticate",title="Tweepy Authentication")
                sys.exit(-1)
            else:
                tk.messagebox.showinfo(message="Successfull Authentication.Let's Go Ahead and Train",title="Tweepy Authentication")
            myList=[]
            stck_tweet_no=[]
            tk.messagebox.showinfo(message="Please Select A Text File Containing The Raw Twitter Handles of Twitter Users That Have To Be Used To Train Our Model")
            filename = filedialog.askopenfilename()
            fileid=open(filename,'r+')
            for line in fileid:
                myList.append(line)
            tk.messagebox.showinfo(message=myList,title="Train")
            try:
                for index in myList:
                    stckk=0
                    ids=[]
                    tk.messagebox.showinfo(message=index)
                    try:
                        for page in tweepy.Cursor(api.followers_ids, screen_name=str(index)).pages():
                            ids.extend(page)
                        tk.messagebox.showinfo(message=len(ids))
                        if(len(ids)>=1000000):
                            tk.messagebox.showwarning(message="This User Has More than 1 Million Followers.Skipping User:"+index)
                            break
                        if(len(ids)<=20):
                            tk.messagebox.showwarning(message="This User Has Less Than 20 Followers. Skipping User :"+index)
                    except tweepy.TweepError as ww:
                            print("Skipping. Un-Authorised USER in Dataset")   
                    for id in ids:
                        try:
                            u=api.get_user(id)
                            print(u.screen_name)
                            testTweet = api.user_timeline(id=id,count=200)
                        except tweepy.TweepError as ww:
                            print("Skipping. Un-Authorised User \n")
                        try:
                            for tweet in testTweet:
                                for word in (tweet.text).split():
                                    if(re.match("\$[A-Z]+",word)):
                                        stckk=stckk+1
                                        print(tweet.text)
                                        break
                                    else:
                                        continue 
                        except tweepy.TweepError as ww:
                            print("Skipping. Un-Authorised Tweet")    
                    try:
                        stck_tweet_no.append([stckk])
                        print(stckk)
                        ratio.append([stckk/len(ids)])
                        print(ratio)
                        tk.messagebox.showinfo(message=ratio)
                    except ZeroDivisionError:
                        tk.messagebox.showerror(message="This User Has No Stock Market Related Tweets")  
            except tweepy.TweepError as ww:
                tk.messagebox.showerror(message=ww)
            except SSLError as ssl1:
                tk.messagebox.showerror(message=ssl1)
            except ReadTimeoutError as rerror:
                tk.messagebox.showerror(message=rerror)
            except ConnectionError as conerror:
                tk.messagebox.showerror(message=conerror)
        def test():
            Y=[]
            global input_user
            global input_ratio
            ids=[]
            stckk=0
            input_user=e.get()
            input_ratio=[]
            if (not api):
                tk.messagebox.showinfo(message="Not Authenticated Authenticate",title="Tweepy Authentication")
                sys.exit(-1)
            else:
                tk.messagebox.showinfo(message="Already Authenticated.Let's Go Ahead and Test.",title="Tweepy Authentication")
            try:
                for page in tweepy.Cursor(api.followers_ids, screen_name=str(input_user)).pages():
                    ids.extend(page)
                    tk.messagebox.showinfo(message=len(ids))   
                for id in ids:
                    try:
                        u=api.get_user(id)
                        print(u.screen_name)
                        testTweet = api.user_timeline(id=id,count=200)
                    except tweepy.TweepError as ww:
                        print("Skipping. Un-Authorised User \n")
                    try:
                        for tweet in testTweet:
                            for word in (tweet.text).split():
                                if(re.match("\$[A-Z]+",word)):
                                    stckk=stckk+1
                                    print(tweet.text)
                                    break
                                else:
                                    continue 
                    except tweepy.TweepError as ww:
                        print("Skipping. Un-Authorised Tweet")    
                try:
                    input_ratio.append([stckk/len(ids)])
                except ZeroDivisionError:
                    tk.messagebox.showerror(message="This User Has No Stock Market Related Tweets")  
            except tweepy.TweepError as ww:
                tk.messagebox.showerror(message=ww)
            except SSLError as ssl1:
                tk.messagebox.showerror(message=ssl1)
            except ReadTimeoutError as rerror:
                tk.messagebox.showerror(message=rerror)
            except ConnectionError as conerror:
                tk.messagebox.showerror(message=conerror)
            tk.messagebox.showinfo(message="The User Under Credibility Analysis is "+input_user)
            tk.messagebox.showinfo(message="The User Under Credibility Analysis has a RATIO "+(str(input_ratio)))
            
            threshold=np.median(input_ratio)
            
            for ratio_val in ratio:
                if ratio_val>threshold:
                    Y.append(1)
                else:
                    Y.append(0)    
            X=[[0.00028],[0.00061],[0.00064],[0.0011],[0.01],[0.008],[0.00191],[0.00455],[0.0061]]
            YY=[0,0,0,0,1,1,0,1,1]   
            model=GaussianNB()
            model.fit(X,YY)
            predicted=model.predict(input_ratio)
            if(predicted==1):
                tk.messagebox.showinfo(message=""+input_user+"is a Credible User.")
            else:
                tk.messagebox.showinfo(message=""+input_user+"is not a Credible Twitter User")

        train = tk.Button(self, text="Train",command=train,width=50)
        test = tk.Button(self, text="Test",command=test,width=50)
        header.pack(side="top", fill="x", pady=5)
        train.pack(pady=50)
        test_label.pack()
        e = tk.Entry(self)
        e.pack(pady=15)
        test.pack(pady=50)
        quit_one.pack(side="bottom",pady=50)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()