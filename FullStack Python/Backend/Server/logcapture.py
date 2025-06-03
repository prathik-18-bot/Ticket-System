
import datetime
def log_capture(value,database):
    count=0
    data=database.child("log").get()
    for eachdata in data.each():
        Lid=eachdata.val()['user']
        status=eachdata.val()['status']
        opertion=eachdata.val()['operation']
        timestamp=eachdata.val()['timestamp']
       # print(timestamp.split(' ')[0],str(datetime.datetime.now()).split(' ')[0])
        if(Lid==value and status=="400" and opertion=="Bad request for login" and timestamp.split(' ')[0]==str(datetime.datetime.now()).split(' ')[0]):
            count+=1
    print(count)
    return count
               
            