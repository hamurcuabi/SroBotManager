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
WelcomeText = QtBind.createLabel(gui, 'Veri',20, 20)
InfoText = QtBind.createLabel(gui, 'text',20, 200)
InfoCloseText = QtBind.createLabel(gui, 'text',20, 250)
sendDataButton=QtBind.createButton(gui, 'stop_sending', 'Stop to send',20, 220)

MailText = QtBind.createLabel(gui, 'Your email:',20, 110)
MainInput = QtBind.createLineEdit(gui,"",100,105,120,20)

PasswordText = QtBind.createLabel(gui, 'Your password:',20, 135)
PasswordInput = QtBind.createLineEdit(gui,"",100,130,120,20)
LoginButton=QtBind.createButton(gui, 'login_button_clicked', 'Login',155, 155)

loopCount = 1
partyMessage = {"partyMessage":[]};
guildMessage = {"guildMessage":[]};
isSending = False
QtBind.setText(gui,WelcomeText, "Welcome to Silkroad Mobile App plugin. \n \n1- Download app, https://sroph.emrehamurcu.com/ \n2- Create an account from mobile app.\n3- Enter your account email and password.\n4- After that, click to 'Login button' and wait a few minutes")
QtBind.setText(gui,InfoText, "Silkroad api is not sendind data.")
QtBind.setText(gui,InfoCloseText, "WARNING: Before closing or reloding phBot ,if data is sending PLEASE STOP by clicking button. ")
sendAllDataThread = None
accesToken=''
tokenIdSended=False
#___________________LOGIN___________________# 
def login_button_clicked():
    
    if sendAllDataThread!=None:
        sendAllDataThread.cancel()
   
    email = QtBind.text(gui,MainInput)
    password = QtBind.text(gui,PasswordInput)
    if email=='':
        log("Please enter your email")
        return
    if password=='':
        log("Please enter your password")   
        return

    Login(password,email)   


#___________________BACK_END_DATA___________________# 
def sendAllData():
    global sendAllDataThread
    global accesToken
    global tokenIdSended
    global isSending

    if isSending==False:
        if sendAllDataThread!=None:
            sendAllDataThread.cancel()
        else:
            sendAllDataThread=None
        QtBind.setText(gui,InfoText, "Please Login, to start data.")
        return

    if accesToken=='':
        QtBind.setText(gui,InfoText, "Please Login, to start data.")
        return

    headersApi={'Content-Type': 'application/json','Authorization':'Bearer '+accesToken}
    tokenTest = get_character_data().copy()
    tokenData = {'tokenId':str(tokenTest['account_id'])}
    if tokenTest['account_id']==0:
        log("After player join the game data will be send")
        return
    else:
        pass  

    try:
        if tokenIdSended==False:
            character_data = get_character_data().copy()
            character_data.update(tokenData)
            character_data_encoded_data = json.dumps(character_data).encode('utf-8')
            urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/User/addToken/'+str(tokenTest['account_id'])
            resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)
            tokenIdSended=True
    except Exception as e:
        tokenIdSended=False
        log(str(e))
        pass   


    try:
        setTrainigArea()
    except Exception as e:
        log(str(e))
        pass

    try:
        
        character_data = get_character_data().copy()
        character_data.update(tokenData)
        character_data_encoded_data = json.dumps(character_data).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/character_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)
    except Exception as e:
        log(str(e))
        pass

    try:
        character_data_encoded_data = json.dumps(get_position()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/position_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

    except Exception as e:
        log(str(e))
        pass

    try:
        character_data_encoded_data = json.dumps(get_training_position()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/training_position_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

    except Exception as e:
        log(str(e))
        pass
  
    try:
        character_data_encoded_data = json.dumps(get_party()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/party_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

    except Exception as e:
        log(str(e))
        pass

    try:
        character_data_encoded_data = json.dumps(get_inventory()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/inventory_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

    except Exception as e:
        log(str(e))
        pass
    
    try:
        character_data_encoded_data = json.dumps(get_storage()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/storage_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

    except Exception as e:
        log(str(e))
        pass

    try:
        character_data_encoded_data = json.dumps(get_guild()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/guild_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

    except Exception as e:
        log(str(e))
        pass
    
    try:
        character_data_encoded_data = json.dumps(get_guild_union()).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/guild_union_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

    except Exception as e:
        log(str(e))
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
       
#___________________STOP_THREAD_DATA___________________# 
def stop_sending():
    global isSending
    global sendAllDataThread
    global accesToken
    
    if isSending==False:
        QtBind.setText(gui,InfoText, "Please Login, to start data.")
        return

    if accesToken=='':
        QtBind.setText(gui,InfoText, "Please Login, to start data.")
        return

    QtBind.setText(gui,InfoText, "Silkroad api is not sendind data.")
    isSending=False
    QtBind.setText(gui,InfoText, "Please Login, to start data again.")
    log("Sending data canceled.Please wait at least 5 seconds")
    sendAllDataThread.cancel()   

#___________________START_THREAD_DATA___________________# 
def start_sending():
    global sendAllDataThread
    global isSending
    global accesToken

    if accesToken=='':
        QtBind.setText(gui,InfoText, "Please Login, to start data.")
        return

    if sendAllDataThread==None:
        sendAllDataThread=perpetualTimer(5,sendAllData)

    else:
        sendAllDataThread.cancel()
        sendAllDataThread=None
        sendAllDataThread=perpetualTimer(5,sendAllData)

    if isSending==False:
        QtBind.setText(gui,InfoText, "Silkroad api is sending data look at your phone.")
        isSending=True
        log("Data will send after 5 seconds please wait...")
        sendAllDataThread.start()  
                
#___________________CHAT___________________#      
def handle_chat(t, player, msg):
    global partyMessage
    global guildMessage

    headersApi={'Content-Type': 'application/json','Authorization':'Bearer '+accesToken}

    tokenTest = get_character_data().copy()
    if tokenTest['account_id']==0:
        return
            
    try:
        message = {'type':str(t),'player':player,'msg':msg}
        message_data = json.dumps(message).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/message_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=message_data)
        
    except:
        pass 

#___________________EVENT___________________#   
def handle_event(t, data):
    headersApi={'Content-Type': 'application/json','Authorization':'Bearer '+accesToken}
    tokenTest = get_character_data().copy()
    if tokenTest['account_id']==0:
        return
    try:
        message = {'type':str(t),'data':data}
        message_data = json.dumps(message).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/notification_data/'+str(tokenTest['account_id'])
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=message_data)
        
    except:
        pass  
    
#___________________PLEYER_LOGIN___________________# 
def Login(password,email):
    try:
        headersApi={'Content-Type': 'application/json'}
        message = {'email':email,'password':password}
        message_data = json.dumps(message).encode('utf-8')
        urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/User/getToken'
        resp = http.request('POST',urlcharacter_data, headers=headersApi, body=message_data)
        LoginRes(resp.data)

    except Exception as e:
        log("Something wrong, pleaser try again."+str(e))
        pass 

def LoginRes(isExistResponse):
    global accesToken
    data = json.loads(isExistResponse)
    result=data["success"]
    accesToken=data["data"]
    if result==True:
        QtBind.setText(gui,PasswordInput,"")
        log("Success!.Your data will be sending in every 5 seconds..")
        isSending=False 
        start_sending()
    else:
        log("We didnt find your account,please try again...")

#___________________MESSAGE_API___________________# 
def getAllMessage():
    headersApi={'Content-Type': 'application/json','Authorization':'Bearer '+accesToken}
    try:
        urlIsExist = 'https://silkroad.emrehamurcu.com/api/Message/getMessages'
        respIsExist = http.request('GET', urlIsExist,headers=headersApi)
        send_message(respIsExist.data)
    except:
        pass  

#___________________Booting___________________# 
def startOrStopBoot(tokenId):
    headersApi={'Content-Type': 'application/json','Authorization':'Bearer '+accesToken}

    try:
        urlIsExist = 'https://silkroad.emrehamurcu.com/api/Boot/getBooting/'+tokenId
        respIsExist = http.request('GET', urlIsExist,headers=headersApi)
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

    headersApi={'Content-Type': 'application/json','Authorization':'Bearer '+accesToken}
    try:
        tokenTest = get_character_data().copy()
        urlIsExist = 'https://silkroad.emrehamurcu.com/api/TrainingArea/getTrainigArea/'+str(tokenTest['account_id'])
        respIsExist = http.request('GET', urlIsExist,headers=headersApi)
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
    if accesToken==None:
        return
    loopCount=loopCount+1
    if loopCount%3==0:
        try:
            headersApi={'Content-Type': 'application/json','Authorization':'Bearer '+accesToken}
            getAllMessage()
            tokenTest = get_character_data().copy()
            if tokenTest['account_id']!=0:
                 startOrStopBoot(str(tokenTest['account_id']))
            tokenData = {'booting':str(get_status())}
            character_data_encoded_data = json.dumps(tokenData).encode('utf-8')
            urlcharacter_data = 'https://silkroad.emrehamurcu.com/api/Silkroad/booting/'+str(tokenTest['account_id'])
            resp = http.request('POST',urlcharacter_data, headers=headersApi, body=character_data_encoded_data)

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