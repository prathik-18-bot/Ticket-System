
from firebase import firebase        
    
def insert_data_in_generic(table,data):
    try:
        database=firebase.FirebaseApplication("https://firstproject-6b23d-default-rtdb.firebaseio.com/",authentication=None)
        database.post(table,data)
        return "SUCCESS"
    except:
        return "FAIL"