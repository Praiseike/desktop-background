#!/usr/bin/python

import os
import requests
import random
import json
import time
from colorama import Fore as color

class Offline:

    # init the class
    def __init__(self,mode = "scale",random = True,pathName = "/home/praise/Pictures/pics",time = 60):
        self.os = __import__("os")
        self.defaultMode = mode
        self.random = random
        self.path = pathName
        self.time = time

        try:
            self.generateFileList()
            self.changeBackground()
        except KeyboardInterrupt:
            print color.RED+"[Ctr+c]"+color.GREEN+" Exiting"

    def generateFileList(self):
        g = __import__("glob")
        # generate a list of image paths from self.path
        self.list = g.glob(self.path+"/*")

    def changeBackground(self):
        if(self.random): # if random is set to true
            while(True):
                self.ExecString = "feh --bg-%s --randomize %s"%(self.defaultMode,self.path)  
                self.os.system(self.ExecString)
                time.sleep(self.time)
        else:
            while(True):
                
                # loop through all in the images in the list 
                for i in range(0,len(self.list)):
                    # generate executing string for bash shell
                    self.ExecString = "feh --bg-%s %s"%(self.defaultMode,self.list[i])
                    self.os.system(self.ExecString)
                    time.sleep(self.time)   # sleep self.time seconds

    def __str__(self):
        return "A class to handle background image changing and display"





class Online(object):
    json_file_name = "anime.json"
    image_list_file = "image_urls.txt"
    cat_url = "https://wall.alphacoders.com/api2.0/get.php?auth=YOUR_KEY&method=category_list"
    api_key = "01c321d43be9b5200c24478a0687ce17"
    anime_list_string = ""
    cat_url = cat_url.replace("YOUR_KEY",api_key)

    def __init__(self,mode = "scale",random = True,time = 10):
        self.random = random
        self.defaultMode = mode
        self.time = time
        self.get_json_data()
        self.save_json_data()
        self.save_image_list()
        try:
            self.changeBackground()
        except KeyboardInterrupt:
            print color.RED+"[Ctr+c]"+color.GREEN+" Exiting"

    def get_json_data(self):
        try:
            self.req = requests.get(self.cat_url)    
        except Exception as e:
            print(e)

        self.cat_json = self.req.json()

        if(self.req.status_code == 200 and self.cat_json['success']):
            print("Connection to image server successful")
        else:
            print("Unable to get data: %s"%cat_json['error'])

        self.categories = self.cat_json['categories']
        # scan for anime
        for i in range(len(self.categories)):
            if(self.categories[i]['name'].lower() == "anime" or "anime" in self.categories[i]['name'].lower()):
                self.anime_id = self.categories[i]['id']
                break  # don't go further

        self.page_number = random.randint(0,10)
        self.anime_url = "https://wall.alphacoders.com/api2.0/get.php?auth=01c321d43be9b5200c24478a0687ce17&method=category&id=%i&page=%i&info_level=2"%(self.anime_id,self.page_number)
        
        try:
            self.req = requests.get(self.anime_url)
        except Exception as e:
            print(e)

        if(self.req.status_code == 200):
            self.anime_list = self.req.json()
            if(self.anime_list['success']):
                print("Finished populating anime list")
            else:
                print("Unable to get data:",self.anime_list['error'])
    
    def save_json_data(self):
        with open(self.json_file_name,"w") as file:
            json_data = json.dumps(self.anime_list)
            file.write(json_data)

    def save_image_list(self):
        for i in range(len(self.anime_list['wallpapers'])):
            self.anime_list_string += self.anime_list['wallpapers'][i]['url_image']+"\n"
        with open(self.image_list_file,'w') as file:
            file.write(self.anime_list_string)

    def check_load_save(self):
        if(os.path.exists(self.json_file_name)):
            return True
        else:
            return False


    def changeBackground(self):
        image_list = self.anime_list_string.split("\n")

        if(self.random):
            while(True):
                ExecString = "feh --bg-%s %s"%(self.defaultMode,image_list[random.randint(0,len(image_list)-1)])  
                os.system(ExecString)
                time.sleep(self.time)
        else:
            while(True):
                
                # loop through all in the images in the list 
                for i in range(len(image_list)):
                    # generate executing string for bash shell
                    ExecString = "feh --bg-%s %s"%(self.defaultMode,self.image_list[i])
                    os.system(ExecString)
                    time.sleep(self.time)   # sleep self.time seconds



def check_internet_connection():
    url = "http://www.google.com"
    try:
        req = requests.get(url,timeout=5)
        print("Connecting to the internet")
        return True
    except(requests.ConnectionError,requests.Timeout) as e:
        print("No internet connection")
        return False

if(check_internet_connection()):
    app = Online()
else:
    app = Offline()