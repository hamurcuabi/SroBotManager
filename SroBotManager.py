from phBot import *
from tkinter import *  
import phBotChat
import QtBind
import json
import threading 
import urllib3
import shutil
import os
from random import randint
import pyqrcode
import sys
from threading import Timer,Thread,Event

http = urllib3.PoolManager()
gui = QtBind.init(__name__, 'SroBot Manager')
String1 = QtBind.createLabel(gui, 'Veri',20, 20)
String2 = QtBind.createLabel(gui, 'text',20, 100)
sendDataButton=QtBind.createButton(gui, 'karakter_data_button_clicked', 'Start to send',120, 70)
send = QtBind.createButton(gui, 'createQR', 'Create QR Code', 20, 70)
loopCount = 1
partyMessage = {"partyMessage":[]};
guildMessage = {"guildMessage":[]};
oneClick = True
isSending = False
QtBind.setText(gui,String1, "Welcome to Silkroad Mobile App plugin. To connect your bot to the mobile app, please click 'Create QR Code' button and scan it with your phone.")
QtBind.setText(gui,String2, "Silkroad api is not sendind data.")
sendAllDataThread = None

#___________________BACK_END_DATA___________________# 
def sendAllData():
    tokenTest = get_character_data().copy()
    tokenData = {'tokenId':str(tokenTest['account_id'])}
    if tokenTest['account_id']==0:
        log("After player join the game data will be send")
        return
    else:
        pass  

    try:
        setTrainigArea()

    except:
        pass

    try:
        
        character_data = get_character_data().copy()
        character_data.update(tokenData)
        character_data_encoded_data = json.dumps(character_data).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/character_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)
    except:
        pass

    try:
        character_data_encoded_data = json.dumps(get_position()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/position_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

    except:
        pass

    try:
        character_data_encoded_data = json.dumps(get_training_position()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/training_position_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

    except:
        pass
  
    try:
        character_data_encoded_data = json.dumps(get_party()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/party_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

    except:
        pass

    try:
        character_data_encoded_data = json.dumps(get_inventory()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/inventory_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

    except:
        pass
    
    try:
        character_data_encoded_data = json.dumps(get_storage()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/storage_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

    except:
        pass

    try:
        character_data_encoded_data = json.dumps(get_guild()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/guild_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

    except:
        pass
    
    try:
        character_data_encoded_data = json.dumps(get_guild_union()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/guild_union_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

    except:
        pass    

#___________________MESSAGE___________________# 
def send_message(data):
    jsondata = json.loads(data)
    result=jsondata["data"]
    for item in result:
        player=str(item["player"])
        message=str(item["text"])
        mtype=item["type"]
        if mtype==1:
            phBotChat.All(message)
        if mtype==2:
            phBotChat.Private(player,message)
        if mtype==4:
            phBotChat.Party(message)
        if mtype==5:
            phBotChat.Guild(message)
        if mtype==6:
            phBotChat.Global(message)
        if mtype==7:
            phBotChat.Stall(message)
        if mtype==11:
            phBotChat.Union(message)                        
       
#___________________THREAD_DATA___________________# 
def karakter_data_button_clicked():
    global sendAllDataThread
    global isSending
    global sendAllDataThread
    if sendAllDataThread==None:
        sendAllDataThread=perpetualTimer(5,sendAllData)

    if isSending==True:
        oneClick=True
        QtBind.setText(gui,String2, "Silkroad api is not sendind data.")
        isSending=False
        QtBind.setText(gui, sendDataButton,"Start to send")
        log("Sending data canceled.Please wait at least 5 seconds")
        sendAllDataThread.cancel()
    else:
        QtBind.setText(gui,String2, "Silkroad api is sending data look at your phone.")
        isSending=True
        log("Data will send after 5 seconds please wait...")
        QtBind.setText(gui, sendDataButton,"Stop to send")
        sendAllDataThread.start()   
        
#___________________CHAT___________________#      
def handle_chat(t, player, msg):
    global partyMessage
    global guildMessage
    tokenTest = get_character_data().copy()
    if tokenTest['account_id']==0:
        return
            
    try:
        message = {'type':str(t),'player':player,'msg':msg}
        message_data = json.dumps(message).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/message_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=message_data)
        
    except:
        pass 

#___________________EVENT___________________#   
def handle_event(t, data):
    tokenTest = get_character_data().copy()
    if tokenTest['account_id']==0:
        return
            
    try:
        message = {'type':str(t),'data':data}
        message_data = json.dumps(message).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/notification_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=message_data)
        
    except:
        pass  
    
#___________________QR CODE___________________# 
def createQR():
    global oneClick
    tokenTest = get_character_data().copy()
    if tokenTest['account_id']==0:
        log("Your player is not ready. Please be sure your bot joined the game!")
        return
    if oneClick == True:
        oneClick = False
        try:
            createQRCodeShow(tokenTest['account_id'])
            
        except:
            log('QR Code could not be sent. Please try again...')
            oneClick=True
            pass

def createQRCodeShow(creatingQR):
    global oneClick
    global window
    if creatingQR != 0:
        window = Tk()
        window_height = 500
        window_width = 500
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        window["bg"] = "#ffffff"
        window["bd"] = 1
        window.overrideredirect(1)
        
        notificationLabel= Label(window)
        notificationLabel.grid(row= 1, column=0, sticky= N+S+E+W)

        tokenData = {'tokenId':str(creatingQR)}
        tokenData_encoded_data = json.dumps(tokenData).encode('utf-8')

        myQr = pyqrcode.create(str(creatingQR))

        qrImage = myQr.xbm(scale=6)
        photo = BitmapImage(data=qrImage)
        notificationLabel.config(image= photo,width=400, bg='#ffffff',borderwidth=2, relief="ridge")
        
        lab1 = Label(window, text="Please scan the QR Code",  font=("Helvetica", 16,),bg='#ffffff',fg='black',borderwidth=2, relief="ridge")
        lab1.grid(row=0, column= 0, sticky= N+S+E+W)

        #Making responsive layout:
        totalRows= 2
        totalCols = 1

        for row in range(totalRows+1):
            window.grid_rowconfigure(row, weight=1)

        for col in range(totalCols+1):
            window.grid_columnconfigure(col, weight=1)

        #looping the GUI
        timerCount("Closing in 3..")
        window.after(1000, lambda: timerCount("Closing in 2.."))  # 2
        window.after(2000, lambda: timerCount("Closing in 1.."))  # 1 
        window.after(3000, lambda: timerCount("Closing in 0.."))  # 0
        log("Your device will be checking in a few seconds later...")
        window.after(4000, lambda:isPlayerExist(str(creatingQR))) 
        window.after(5000, lambda: window.destroy()) 
        
        window.mainloop()    
        
def timerCount(countText):
    global window
    lab2 = Label(window, text = countText,  font=("Helvetica", 18,),bg='#111111',fg='#ffffff',borderwidth=2, relief="ridge")
    lab2.grid(row=2, column= 0, sticky= N+S+E+W)

#___________________PLEYER_API___________________# 
def isPlayerExist(qrcode):
    try:
        urlIsExist = 'https://silkroad.emrehamurcu.com/api/Silkroad/isPlayerExist?tokenId='+qrcode
        respIsExist = http.request('GET', urlIsExist)
        isExistResponseFunc(respIsExist.data)

    except Exception as e:
        log("Something wrong, pleaser try again.")
        oneClick=True
        pass 

def isExistResponseFunc(isExistResponse):
    data = json.loads(isExistResponse)
    result=data["success"]
    if result==False:
        log("We didnt find your id,please try again...")
        oneClick == True
    else:
        log("Your data will be sending in every 5 seconds..")
        isSending=False 
        karakter_data_button_clicked()

#___________________MESSAGE_API___________________# 
def getAllMessage():
    try:
        urlIsExist = 'https://silkroad.emrehamurcu.com/api/Message/getMessages'
        respIsExist = http.request('GET', urlIsExist)
        send_message(respIsExist.data)
    except:
        pass  

#___________________Booting___________________# 
def startOrStopBoot(tokenId):
    try:
        urlIsExist = 'https://silkroad.emrehamurcu.com/api/Boot/getBooting/'+tokenId
        respIsExist = http.request('GET', urlIsExist)
        jsondata = json.loads(respIsExist.data)
        result=jsondata["data"]
        succes=jsondata["success"]
        if succes==True:
            shouldStart=result["booting"]
            if shouldStart ==True:
                start_bot()
            else:
                stop_bot()     


    except Exception as e:
        pass         

#___________________Trainig Area___________________# 
def setTrainigArea():
    try:
        tokenTest = get_character_data().copy()
        urlIsExist = 'https://silkroad.emrehamurcu.com/api/TrainingArea/getTrainigArea/'+str(tokenTest['account_id'])
        respIsExist = http.request('GET', urlIsExist)
        jsondata = json.loads(respIsExist.data)
        result=jsondata["data"]
        succes=jsondata["success"]
        if succes==True:
            stop_bot()
            x=result["x"]
            y=result["y"]
            z=result["z"]
            radius=result["radius"]
            set_training_position(0, x, y, z)
            set_training_radius(radius)
            start_bot()

    except:
        pass 

#___________________EVENT_LOOP___________________#  
def event_loop():
    global loopCount
    loopCount=loopCount+1
    if loopCount%3==0:
        try:
            getAllMessage()
            tokenTest = get_character_data().copy()
            if tokenTest['account_id']!=0:
                 startOrStopBoot(str(tokenTest['account_id']))
            tokenData = {'booting':str(get_status())}
            character_data_encoded_data = json.dumps(tokenData).encode('utf-8')
            urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/booting/'+str(tokenTest['account_id'])
            resp = http.request('POST',urlcharacter_data, headers={'Content-Type': 'application/json'}, body=character_data_encoded_data)

        except:
            pass

#___________________TIMER_THREAD___________________# 
class perpetualTimer():

   def __init__(self,t,hFunction):
       self.t=t
       self.hFunction = hFunction
       self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
       self.hFunction()
       self.thread = Timer(self.t,self.handle_function)
       self.thread.start()

   def start(self):
       self.thread.start()

   def cancel(self):
       self.thread.cancel()