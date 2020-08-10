#This is a very basic Aritificial Intelligence I have created, hence the name 'Basic', which was inspired by assistants such as Siri and Google Assistant.
#The main purpose of this side-project was to gain an understanding of how an artificial intelligence like this could be achieved and implemented in a python
#'Basic' has been implemented on a Raspberry Pi Model 3B+ so that it could become a tangible household item like Alexa or Google Assitant
#This program covers how a basic version of this could be implemented for my own self-learning, however it could very easily be upgraded to enhance its capabilities 

import requests
import time
connection = False
while connection == False:
     try:
          x = requests.get('https://www.google.com').status_code#Attempts to connect to google and returns a status code
          if x == 200:#A status code of 200 indicates a good connection but more importantly indicates that the Pi has successfully connected to WiFi, which is essential for this program
               print("Connection Established")
               connection = True #Breaks the loop and continues with the programme
     except Exception as e: #Catches any exceptions, such as WiFi connection not yet being established which would have otherwise toppled the program
          time.sleep(10)#Waits 10 seconds before executing the loop and re-attempting to connect to google.com
          pass
#libraries
from gtts import gTTS #Text to Speech
import os
import speech_recognition as sr #Used to take voice commands
from time import ctime
import wikipedia
import sys
import random
import os.path
import pytube
from pytube import YouTube
from youtubesearchpython import searchYoutube
import geocoder
import geopy
from geopy.geocoders import Nominatim
import pyowm
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound

#defining lists and variables
#The items in these lists consist of words and phrases which can be found in regular speech patterns to execute certain commands that 'Basic' is capable of 
shutDown_words = ["shut down","stop","close","done","finished","bye","goodbye","shutdown"]
timePhrases = ["tell me the time","what is the time","what's the time","what time is it"]
wikiPhrases = ["what is", "tell me about", "who is", "information on ", "you know about"]
datePhrases = ["day is it today", "the date", "day of the week"]
rpsPhrases = ["rock paper scissors","rock,paper,scissors","play a game of", "game", "play"]
make_listWords = ["create", "make", "start", "compose", "generate", "prepare"]
add_listWords = ["add","append","insert","annex","enter","fill in"]
view_listWords = ["read","view","see","show","display","bring","open","say","recite"]
delete_itemWords = ["delete","remove","erase","discard","get rid of","take"]
deleteItem_listIdentifiers = ["an","from","in","inside","within"]
songPhrases = ["play","listen to", "search youtube","song"]
weatherPhrases = ["weather", "temperature","climate","degrees","climate"]
weather_locationIdentifiers = ["in","near","around"]

#converts command from user into list
def string_to_list(string):
     li = list(string.split(" "))
     return li

def speaking(string):#Allows 'Basic' to speak to the user through Text to Speech 
     print(string)
     ((gTTS(text = string, lang = 'en'))).save("x.mp3")
     sound = AudioSegment.from_mp3("x.mp3")
     play(sound)
     os.remove("x.mp3")

def listening():#Allows a microphone to be used for audio input from the user
     r = sr.Recognizer()
     with sr.Microphone() as source:
          r.adjust_for_ambient_noise(source)
          userInput = r.recognize_google((r.listen(source)),language = 'en').lower()#stores command as a variable
          print(userInput)
          return userInput

def youtubeSong():
     #Due to YouTube's ever-changing nature, there is a chance that this module may no longer be viable by the time you see this
     #If you intend to use this code, check https://github.com/alexmercerind/youtube-search-python for any updates which could fix the problem at hand
     if os.path.exists("YouTube.mp4"):#Checks to see if file already exists
          os.remove("YouTube.mp4")#Deletes file to avoid any further complications

     speaking("Enter Song Name: ")#Prompts user
     cont = False
     while cont == False:#Creates a loop in case of an error 
          try:
               searchQuery = listening()#Stores audio input from user as variable
          except sr.UnknownValueError:
               cont = False
               speaking("I Couldn't Quite Understand That ...")#In the case that the audio input from the user was unclear, this will be fed back to the user
          else:
               cont = True
          #Loop allows user to enter song name again in the case of an error 
     speaking("Please Bear With Me Whilst I Fetch Your Request ...")#Informs the user that there is a possibility this may take some time to execute 
     search = searchYoutube(searchQuery,offset = 1,mode = 'dict',max_results = 1)#makes use of youtubesearchpython to return top video in regards to user's search terms
     ytResult = search.result()#saves result as a dictionary in variable 'ytResult'
     print("Result Found")
     ytResult = ytResult.get('search_result')#Gets the value in correspondence with the key 'search_result'
     ytLink = ytResult[0].get('link')#Gets the value in correspondence with the key 'link', which could be found in the first value of ytResult
     print("Link Found")
     ytName = ytResult[0].get('title')#Gets the value in correspondence with the key 'title' which could be found in the first value of ytResult

     url = ytLink
     ytVideo = pytube.YouTube(url)
     ytVideo.streams.get_highest_resolution().download()#Downloads video from youtube as a mp4 file 
     print("Video Downloaded")

     speaking("Now Playing: " + ytName)#Prompts the user that the command has been executed and the song can now be played 

     playsound("YouTube.mp4")
     os.remove("YouTube.mp4")

def RPS():#subroutine for rock paper scissors game
     num = random.randint(1,3)#generates random number between 1&3 inclusive w/ each number corresponding to rock, paper or scissors
     speaking("Rock, Paper, Scissors, Shoot! ")
     r = sr.Recognizer()
     play = False
     while play == False:
          try:
               userChoice = listening()#Accepts user input for RPS as audio input     
          except sr.UnknownValueError:
               speaking("I Couldn't Quite Understand What You Said There ...")
               play = False
          else:
               play = True
     
     if num == 1:
          speaking("Rock!")
          #All possible events are accounted for, in accordance with the rules of RPS
          if "paper" in userChoice:
               speaking("You Win!")
          elif "scissors" in userChoice:
               speaking("I Win!")
          elif "rock" in userChoice:
               speaking("It's A Draw!")
          else:
               speaking("That's Not In The Guidelines Of Traditional Rock Paper Scissors! ")#Accounts for a input from the user which may not rock, paper or scissors             
     elif num == 2:
          speaking("Paper!")
          if "scissors" in userChoice:
               speaking("You Win!")
          elif "rock" in userChoice:
               speaking("I Win!")
          elif "paper" in userChoice:
               speaking("It's A Draw!") 
          else:
               speaking("That's Not In The Guidelines Of Traditional Rock Paper Scissors! ")
     elif num == 3:
          speaking("Scissors!")
          if "rock" in userChoice:
               speaking("You Win!")
          elif "paper" in userChoice:
               speaking("I Win!")  
          elif "scissors" in userChoice:
               speaking("It's A Draw!")
          else:
               speaking("That's Not In The Guidelines Of Traditional Rock Paper Scissors! ")
          
     
def phraseCheck():
     commandDone = False #Ensures only one command is done at a time, there were some instances where two phrases matched for two commands
     #how are you phrase
     if commandDone == False:
          if "how are you" in variable:
               speaking("I Am Perfectly Fine Thank You, How Are You? ...")
               commandDone = True
     #time phrase
     if commandDone == False:
          for i in range(len(timePhrases)):
               phrase = timePhrases[i]
               if phrase in variable:#Checks if a phrase in the timePhrases list is in the command 
                    lstTime = string_to_list(ctime())
                    timeReturn =  "The Time Is Currently: " + str(lstTime[3][:2]) + ":" + str(lstTime[3][3:5])
                    speaking(timeReturn)
                    commandDone = True
     #date phrase
     if commandDone == False:
          for i in range(len(datePhrases)):
               phrase = datePhrases[i]#checks if a phrase in the datePhrases list is in the command 
               if phrase in variable:
                    lstDate = string_to_list(ctime())
                    del lstDate[3]
                    del lstDate[3]
                    todayDate = " ".join(lstDate)
                    speaking("The Date Today Is: " + todayDate)#Outputs date to user 
                    commandDone = True
     #weather phrase
     if commandDone == False:
          weatherMatch = False
          locationMatch = False
          owm = pyowm.OWM('ec7e84c838666b3ba623f01cd83f1650')#connects to API
          mgr = owm.weather_manager()
          for i in range(len(weatherPhrases)):
               if weatherPhrases[i] in variable:#Checks if a phrase in weatherPhrases is in the command
                    weatherMatch = True
          for i in range(len(weather_locationIdentifiers)):
               if weather_locationIdentifiers[i] in variable:#Checks if a location has been specified 
                    locationIndicator = weather_locationIdentifiers[i]
                    locationMatch = True

          if weatherMatch == True and locationMatch == False:
               g = geocoder.ip('me')#Finds the ip address of the current location of the device
               location = str(g[0])
               location = location[1:]
               num = location.index(",")
               location = location[:num]
               latlng = g.latlng#Finds latitude and longitude of the area 
               lat = latlng[0]
               lng = latlng[1]
          
               weather = mgr.weather_at_coords(lat,lng)#Returns weather information for specified coordinates 
          elif weatherMatch == True and locationMatch == True:
               commandLst = string_to_list(variable)
               identifierIndex = commandLst.index(locationIndicator) + 1#finds the location specified in the command, based on regular speech pattersn 
               location = commandLst[identifierIndex]
               locationQuery = commandLst[identifierIndex] + ",UK"
               weather = mgr.weather_at_place(locationQuery)#Returns weather information at specified location 
          if weatherMatch == True:
               getWeather = weather.weather
               temp = getWeather.temperature('celsius').get('temp')#Returns value in correspondence to key 'temp' from pyowm module 
               degreeSign = u"\N{DEGREE SIGN}" + "C"
               speaking("The Temperature In " + location.capitalize() + " Is Currently " + str(temp) + degreeSign + " ...")#Returns the temperature to the user
               commandDone = True                       
     #what is your name name phrase
     if commandDone == False:
          if "your name" in variable:
               speaking("My Name Is Basic ...")
               commandDone = True
     #make_list phrase
     if commandDone == False:
          makeMatch = False
          listMatch = True
          for i in range(len(make_listWords)):
               phrase = make_listWords[i]
               if phrase in variable:#checks if a phrase from make_listWords is in the command
                    makeMatch = True    
          if makeMatch == True:
               if "list" in variable:#checks if the word 'list' is in the command
                    listMatch = True
               else:
                    listMatch = False
          if makeMatch == True and listMatch == True:
               speaking("What Would You Like To Name This List?")
               nameMatch = False
               while nameMatch == False:#Creates loop in case of error
                    try:
                         listName = listening()#Accepts listName as audio input from user
                    except sr.UnknownValueError:#Catches error which would otherwise topple program
                         nameMatch = False
                         speaking("I Couldn't Quite Understand That ...")#Notifies User of error
                    else:
                         nameMatch = True
                    
               f = open("{}.txt".format(listName),"a+") #Creates a new list as a txt file in append format
               f.close()
               speaking("List Created Successfully")#Notifies user that a list has sucessfully been created 
               commandDone = True
     #add_list phrase
     if commandDone == False:
          addMatch = False
          listMatch = False
          for i in range(len(add_listWords)):#Checks if a phrase from add_listWords is in the command
               phrase = add_listWords[i]
               if phrase in variable:
                    addMatch = True
          if addMatch == True:
               if "list" in variable:#Checks if the word 'list' is in the command
                    listMatch = True
               else:
                    listMatch = False
          if addMatch == True and listMatch == True:
               speaking("Which List Would You Like To Append?")
               nameMatch = False
               while nameMatch == False:
                    try:
                         listName = listening()#Accepts listName as audio input from the user
                    except sr.UnknownValueError:#Catches error
                         nameMatch = False
                         speaking("I Couldn't Quite Understand That ...")
                    else:
                         nameMatch = True
               if os.path.exists("{}.txt".format(listName)):#Checks if the file to which the user is referring to exists
                    speaking("What Would You Like To Add To {}".format(listName))
                    speaking("Please Only Add One Item At A Time: ")#This allows each item to be written individually
                    cont = False
                    while cont == False:
                         try:
                              listItem = listening()#Accepts listItem as audio input from the user
                         except sr.UnknownValueError:
                              cont = False
                              speaking("I Couldn't Quite Understand That ...")
                         else:
                              cont = True    
                    f = open("{}.txt".format(listName),"a+")#Opens the specified txt file in append format 
                    f.write("\n")#Adds a new line, thus there will not be two items of the list written on the same line which allows for easier reading of the file
                    f.write(listItem)#Writes specified item to txt file
                    f.write("\n")
                    f.close()
                    speaking("{} Added Successfully".format(listItem))#Notifies reader that the command was executed successfully
                    commandDone = True
               else:
                    speaking("Sorry I Could Not Find An Existing List Called {}".format(listName))#Notifies the reader if the specified list does not exist
                    commandDone = True
                    
     #view_list phrase
     if commandDone == False:
          viewMatch = False
          listMatch = False
          for i in range(len(view_listWords)):
               phrase = view_listWords[i]
               if phrase in variable:#checks if a phrase from view_listWords can be found in the command
                    viewMatch = True
          if viewMatch == True:
               if "list" in variable:#checks if the word 'list' can be found in the command
                    listMatch = True
               else:
                    listMatch = False
          if viewMatch == True and listMatch == True:
               speaking("Which List Would You Like Me To Read?")
               nameCont = False
               while nameCont == False:
                    try:
                         listName = listening()
                    except:
                         nameCont = False
                         speaking("I Couldn't Quite Understand That ...")
                    else:
                         nameCont = True
               if os.path.exists("{}.txt".format(listName)):#Checks if list exists 
                    f = open("{}.txt".format(listName),"r+")#Opens txt file in read format 
                    listContents = f.readlines()#Returns values of txt file as list in python 
                    f.close()
                    listContents = [x.strip() for x in listContents]#Removes any blank spaces in the form of new lines (/n) 
                    emptySpaces = True
                    while emptySpaces == True:
                         if "" in listContents:#Checks to see if there are any more blank spaces 
                              listContents.remove("")#Removes blank spaces if found
                         else:
                              emptySpaces = False
                    for i in range(len(listContents)):
                         speaking(listContents[i])#Reads out each item in the list
                    
                    commandDone = True
               else:
                    speaking("Sorry I Could Not Find An Existing List Called {}".format(listName))#Notifies user if list could not be found
                    commmandDone = True 
     #delete_listItem phrase
     if commandDone == False:
          delMatch = False
          itemMatch = False
          listMatch = False
          for i in range(len(delete_itemWords)):
               phrase = delete_itemWords[i]
               if phrase in variable:#checks if a phrase from delete_itemWords can be found in the command
                    delMatch = True
          if delMatch == True:
               for i in range(len(deleteItem_listIdentifiers)):
                    phrase = deleteItem_listIdentifiers[i]
                    if phrase in variable:#Finds the specified item which needs to be deleted from the list 
                         itemMatch = True
          if delMatch == True and itemMatch == True:
               if "list" in variable:#Checks if the word 'list' is in the command 
                    listMatch = True
          if delMatch == True and itemMatch == True and listMatch == True:
               speaking("Which List Would You Like Me To Delete An Item From?")
               nameCont = False
               while nameCont == False:
                    try:
                         listName = listening()
                    except:
                         nameCont = False
                         speaking("I Couldn't Quite Understand That ...")
                    else:
                         nameCont = True
               if os.path.exists("{}.txt".format(listName)):
                    speaking("What Item Would You Like Me To Delete From {}".format(listName))
                    speaking("Please Delete Only One Item At A Time: ")
                    itemCont = False
                    while itemCont == False:
                         try:
                              delItem = listening()
                         except:
                              itemCont = False
                              speaking("I Couldn't Quite Understand That ...")
                         else:
                              itemCont = True
                    f = open("{}.txt".format(listName),"r")#opens txt file in read format
                    listContents = f.readlines()#stores contents of the txt file as a python list
                    f.close()
                    listContents = [x.strip() for x in listContents]#removes empty spaces from list caused by /n
                    if delItem in listContents:
                         listContents.remove(delItem)#removes the specified item from the python list
                    f = open("{}.txt".format(listName),"w+")#opens txt file in write format
                    for i in range(len(listContents)):
                         f.write(listContents[i])#Rewrites txt file with new list without the deleted item
                         f.write("\n")#Adds new line after every item 
                    f.close()#Closes txt file
                    speaking("{} Deleted From {} Successfully".format(delItem,listName))#Notifies user that the command has been executed successfully
                    commandDone = True
               else:
                    speaking("Sorry I Could Not Find An Existing List Called {}".format(listName))#Notifies the user if the txt file could not be found 
                    commandDone = True
     #delete list phrase
     if commandDone == False:
          delMatch = False
          listMatch = False
          for i in range(len(delete_itemWords)):
               phrase = delete_itemWords[i]
               if phrase in variable:#checks if a phrase from delete_itemWords could be found in the command
                    delMatch = True
          if "list" in variable:#checks if the word 'list' could be found in the command
               listMatch = True
          if delMatch == True and listMatch == True:
               speaking("Which List Would You Like Me To Delete? ")
               nameCont = False
               while nameCont == False:
                    try:
                         listName = listening()
                    except:
                         nameCont = False
                         speaking("I Couldn't Quite Understand That ...")
                    else:
                         nameCont = True
               if os.path.exists("{}.txt".format(listName)):#Checks if txt file exists
                    os.remove("{}.txt".format(listName))#Deletes txt file
                    speaking("{} Deleted Successfully".format(listName))#Notifies user that command has been executed successfully 
                    commandDone = True
               else:
                    speaking("Sorry I Could Not Find An Existing List Called {}".format(listName))
                    commandDone = True
     #song phrase
     if commandDone == False:
          for i in range(len(songPhrases)):
               if songPhrases[i] in variable:#Checks if a phrase from songPhrases is in the command
                    if "display" or "rock paper scissors" in variable:#checks if the words 'display' or 'rock paper scissors' are in the command, as to avoid confusion with other executable commands
                         commandDone = False
                    elif "display" or "rock paper scissors" not in variable:
                         try:
                              youtubeSong()#Calls youtubeSong subroutine
                         except Exception:#Catches any possible errors
                              speaking("An Error Occurred")#Notifies user of an error
                         commandDone = True
     #rock,paper,scissors phrase
     if commandDone == False:
          for i in range(len(rpsPhrases)):
               phrase = rpsPhrases[i]
               if phrase in variable:#Checks if a phrase from rpsPhrases is in the command 
                    if "game" in variable:#checks if the word 'game' is in the command 
                         RPS()#Calls RPS subroutine 
                         commandDone = True
                         break
                    
     #wikipedia definitions phrase
     if commandDone == False:
          for i in range(len(wikiPhrases)):
               try:
                    phrase = wikiPhrases[i]
                    if phrase in variable:#checks if a phrase from wikiPhrases is in the command
                         lst = string_to_list(variable)
                         phraseLst = string_to_list(phrase)
                         for x in range(len(lst)):
                              if lst[x] == phraseLst[-1]:#finds position of identifier within command
                                   num = x + 1
                                   break
                              else:
                                   x += 1
                         y = lst[num:]#Stores the search term as variable 'y', which would be found after the identifier as would be the case in everyday speech patterns 
                         searchTerm = ' '.join(item for item in y)#Joins items in the list to create a string 
                         desc = wikipedia.summary(searchTerm)#Finds wikipedia information for searchTerm through wikipedia module
                         descLst = string_to_list(desc)#Converts wikipedia description into list
                         a = 0 
                         for i in range(len(descLst)):
                              if "." in descLst[i]:
                                   a += 1
                              if a == 3:#Looks for 3 full stops which can be used to identify the first 3 sentences
                                   b = i +  1
                                   break
                         if "your name" in variable:#Checks if the phrase 'your name' is in the command which can cause confusion with other commands 
                              pass
                         else:
                              del descLst[b:]#Removes description following the third full stop 
                              description = ' '.join(item for item in descLst)#Converts remaining list items into a string 
                              speaking(description)#Reads out description to the user
               except Exception:
                    speaking("Sorry, I Wasn't Entirely Sure What You Were Referring To There... Please Be More Specific ... ")
                    #Notifies user that a wikipedia definition for their search term could not be found
               else:
                    pass
     #shutdown phrase
     if commandDone == False:
          for i in range(len(shutDown_words)):
               phrase = shutDown_words[i]
               if phrase in variable:#checks if a phrase from shutDown_words could be found in the command 
                    speaking("Shutting Down ...")
                    start = False
                    commandDone = True
                    os.system("sudo shutdown -h now")#Accesses raspberry pi terminal and shuts down raspberry pi 

def RPS():#subroutine for rock paper scissors game
     num = random.randint(1,3)
     speaking("Rock, Paper, Scissors, Shoot! ")
     r = sr.Recognizer()
     play = False
     while play == False:
          try:
               userChoice = listening()    
          except sr.UnknownValueError:
               speaking("I Couldn't Quite Understand What You Said There ...")
               play = False
          else:
               play = True
     
     if num == 1:
          speaking("Rock!")
          if "paper" in userChoice:
               speaking("You Win!")
          elif "scissors" in userChoice:
               speaking("I Win!")
          elif "rock" in userChoice:
               speaking("It's A Draw!")
          else:
               speaking("That's Not In The Guidelines Of Traditional Rock Paper Scissors! ")                 
     elif num == 2:
          speaking("Paper!")
          if "scissors" in userChoice:
               speaking("You Win!")
          elif "rock" in userChoice:
               speaking("I Win!")
          elif "paper" in userChoice:
               speaking("It's A Draw!") 
          else:
               speaking("That's Not In The Guidelines Of Traditional Rock Paper Scissors! ")
     elif num == 3:
          speaking("Scissors!")
          if "rock" in userChoice:
               speaking("You Win!")
          elif "paper" in userChoice:
               speaking("I Win!")  
          elif "scissors" in userChoice:
               speaking("It's A Draw!")
          else:
               speaking("That's Not In The Guidelines Of Traditional Rock Paper Scissors! ")
               
speaking("I'm Ready ...")
#Notifies the user that the modules have successfully been imported and the program is ready to use as I found it would take some time for the modules to be imported when using raspberry pi
start = False
while start == False:
     try:
          a = listening()
     except sr.UnknownValueError:
          start = False
     else:
          if "basic" in a:#Checks if the name of the ai, 'basic' has been said by the user and thus the program becomes 'activated'
               start = True
               output = "Welcome ..."#Acknowledges the user 
               speaking(output)
          else:
               start = False
while start == True:     
     try:
          speaking("Enter Command: ")#Prompts the user to enter a command
          variable = listening()
          command = string_to_list(variable)
     except sr.UnknownValueError:
          speaking("I Couldn't Quite Understand That ...")
     else:
          phraseCheck()#Calls phraseCheck subroutine to analyse the speech patterns within the user's command
          
          
               
     
                    
          
