#!/usr/bin/env python
import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

reader=SimpleMFRC522()
print("Scan RFID to check attendance")
try:
   id,text=reader.read()
   print("\nHello "+ text)

finally:
   GPIO.cleanup()


import pyrebase   
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
print("Logging in to database")
user = auth.sign_in_with_email_and_password("abc@gmail.xyz", "test123")#add your own credentials here


print("\n Requesting data from database")
n1= db.child("attendance").child(id).child("OOPS").get(user['idToken']).val()
n2= db.child("attendance").child(id).child("Crypto").get(user['idToken']).val()
n3= db.child("attendance").child(id).child("CAO").get(user['idToken']).val()
n4= db.child("attendance").child(id).child("FDA").get(user['idToken']).val()
n5= db.child("attendance").child(id).child("STS").get(user['idToken']).val()
n6= db.child("attendance").child(id).child("Microcontrollers").get(user['idToken']).val()

print(str(n1+" : OOPS\n"+n2+" : Crypto\n"+n3+" : CAO\n"+n4+" : FDA\n"+n5+" : STS\n"+n6+" : Microcontrollers\n"))