#!/usr/bin/env python
from __future__ import print_function 
import os
import pyrebase
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import (MessagingResponse,Message,Body,Media)
# In python 2.7
import sys

config = {
  "apiKey": "",#add your own api key here
  "authDomain": "rfidvit-33af5.firebaseapp.com",
  "databaseURL": "https://rfidvit-33af5.firebaseio.com/",
  "storageBucket": "rfidvit-33af5.appspot.com",
  "serviceAccount": "key.json"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()
#authenticate a user
user = auth.sign_in_with_email_and_password("abc@gmail.xyz", "test123")#add your own credentials here


app = Flask(__name__)

@app.route("/sms",methods=['GET','POST'])
def sms_reply():
     resp=MessagingResponse()
     message1=str(request.form['Body'])
     if message1=="History":
         
     #print(resp, file=sys.stderr)
     #fromno=request.form['']
      phno1=request.form['From']
      str1=""
      phno1=phno1.replace("whatsapp:","")
      data = db.child("transactions").child(phno1).shallow().get().val()


      data=list(data)

      numofelem=len(data)

   #  numofelem=0
      for i in range(1,numofelem+1):
           
             str1= "Cost: "+str(db.child("transactions").child(phno1).child(str(i)).child('cost').get().val())+" "
             str2= "Date&time: "+str(db.child("transactions").child(phno1).child(str(i)).child('date').get().val())+" "
             str3= "Location "+ str(db.child("transactions").child(phno1).child(str(i)).child('location').get().val())+" "
    
     #resp.message(request.form['From'])
      resp.message(str1+str2+str3)
      

      return str(resp)
if __name__ =="__main__":
   app.run(host='127.0.0.1',port='8080',debug=True)#!/usr/bin/python
