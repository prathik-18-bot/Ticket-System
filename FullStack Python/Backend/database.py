#Extract the data from database
import pyrebase
def fetchData():
     firebaseconfiguration={ 
       "apiKey": "AIzaSyCOD0VCBf1HYGGLKXo0TNbwew9pqFh39cs",
       "authDomain": "firstproject-6b23d.firebaseapp.com",
       "databaseURL": "https://firstproject-6b23d-default-rtdb.firebaseio.com/",
       "projectId": "firstproject-6b23d",
       "storageBucket": "firstproject-6b23d.firebasestorage.app",
       "messagingSenderId": "887652328217",
       "appId": "1:887652328217:web:990528742a942b5b76db88",
       "measurementId": "G-XKCH531T1W"
         }
     firebase=pyrebase.initialize_app(firebaseconfiguration)
     database=firebase.database()
     data=database.child("personaldata").get()
     print(data)
     
print(fetchData())


    