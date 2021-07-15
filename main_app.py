#!/usr/bin/env python
import pyrebase
import RPi.GPIO as GPIO
import sys
import time
import hashlib
import os
from datetime import datetime
from twilio.rest import Client


sys.path.append('/home/pi/MFRC522-python')



account_sid = ''#Enter your own sid here
auth_token = ''#Enter your own auth_token here
client = Client(account_sid, auth_token)




from mfrc522 import SimpleMFRC522
class keypad():
    def __init__(self, columnCount = 3):
        GPIO.setmode(GPIO.BOARD)

        # CONSTANTS 
        if columnCount is 3:
            self.KEYPAD = [
                [1,2,3],
                [4,5,6],
                [7,8,9],
                ["*",0,"#"]
            ]

            self.ROW         = [38,37,36,35]
            self.COLUMN      = [13,12,11]
        
        elif columnCount is 4:
            self.KEYPAD = [
                [1,2,3,"A"],
                [4,5,6,"B"],
                [7,8,9,"C"],
                ["*",0,"#","D"]
            ]

            self.ROW         = [18,23,24,25]
            self.COLUMN      = [4,17,22,21]
        else:
            return
     
    def getKey(self):
         
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
         
        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
         
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
                 
        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return
         
        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         
        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
 
        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j
                 
        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal <0 or colVal >2:
            self.exit()
            return
 
        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]
         
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
print("Name of the person is :"+text)
user = auth.sign_in_with_email_and_password("abc@gmail.xyz", "test123")#add your own credentials here
from_whatsapp_number='whatsapp:+14155238886'
x=db.child("accounts").child(id).child('phno').get(user['idToken']).val()
to_whatsapp_number='whatsapp:'+x


ans=int(input("Cost of item being bought: "))
#querying/reading of data
print("Retrieving cash balance")
n= int(db.child("accounts").child(id).child("cash").get(user['idToken']).val())

password1= db.child("accounts").child(id).child("password").get(user['idToken']).val()

print("Enter password for the transaction")
kp = keypad()
num1=""
break1=0
    # Loop while waiting for a keypress
digit = None
digit = kp.getKey()
while len(num1)<4:
        
        if digit != None:
            num1=num1+str(digit)
            time.sleep(0.3)
            
        digit = kp.getKey()
num1=hashlib.md5(num1.encode())
num1=num1.hexdigest()
print("Password entered")
if password1==num1:
    if ans<n:
        n=n-ans
        db.child("accounts").child(id).update({"cash": str(n)}, user['idToken'])
        today= datetime.now()
        text2="You have made a transaction of Rs."+str(ans)+" on " +str(today) +"\n and your balance is" +str(n)
        client.messages.create(body=text2, from_=from_whatsapp_number, to=to_whatsapp_number)
        data1 = {'location':"cafeteria",'cost':str(ans),'date':str(today)}
             #adding data
        phno1=str(db.child("accounts").child(id).child("phno").get(user['idToken']).val())
        data = db.child("transactions").child(phno1).shallow().get().val()
        try:
            data=list(data)
            numofelem=len(data)
        except:
            numofelem=0
        db.child("transactions").child(phno1).child(str(numofelem+1)).set(data1, user['idToken'])
    else:
         print("Not enough balance")
else:
    print("Wrong password")
#updation
GPIO.cleanup()
