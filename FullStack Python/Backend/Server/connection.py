#this file is resposible for connecting to the server
import pyrebase
def establish_connection():
    #connect to datbase server
    databaseinformation={
      "apiKey": "***************************************",
      "authDomain": "firstproject-6b23d.firebaseapp.com",
      "databaseURL": "https://firstproject-6b23d-default-rtdb.firebaseio.com/",
      "projectId": "firstproject-6b23d",
      "storageBucket": "firstproject-6b23d.firebasestorage.app",
      "messagingSenderId": "887652328217",
      "appId": "1:887652328217:web:990528742a942b5b76db88",
      "measurementId": "G-XKCH531T1W"
        
        
        }
    firebase=pyrebase.initialize_app(databaseinformation)
    return firebase