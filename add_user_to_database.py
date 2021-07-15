#!/usr/bin/env python
import pyrebase
import hashlib 

import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

reader=SimpleMFRC522()
print("Hold a tag near the reader")
try:
   id,text=reader.read()
   print("Processing card data")

finally:
   GPIO.cleanup()
   
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



ans=input("Do you want to add a new user to the database?")
if ans=='y' or ans=='yes':
    print("Name of the person is :"+text)
    cash1=input("Cash while opening account: ")
    phno1=int(input("Enter phone number: "))
    pass1=str(input("Set password for transactions: "))
    n1=str(input("OOPS attendance: "))
    n2=str(input("Crypto attendance: "))
    n3=str(input("CAO attendance: "))
    n4=str(input("FDA attendance: "))
    n5=str(input("STS attendance: "))
    n6=str(input("Microcontrollers attendance: "))




 
    pass1 = hashlib.md5(pass1.encode()) 

    pass1=pass1.hexdigest() 

             
    data1 = {'cash':cash1,'name':text,'phno':phno1, 'password':pass1}
             #adding data
    db.child("accounts").child(id).set(data1, user['idToken'])
    db.child("attendance").child(id).child("OOPS").set(n1,user['idToken'])
    db.child("attendance").child(id).child("Crypto").set(n2,user['idToken'])
    db.child("attendance").child(id).child("CAO").set(n3,user['idToken'])
    db.child("attendance").child(id).child("FDA").set(n4,user['idToken'])
    db.child("attendance").child(id).child("STS").set(n5,user['idToken'])
    db.child("attendance").child(id).child("Microcontrollers").set(n6,user['idToken'])
