#Flask application is created in three steps
#Step 1 : Import package
#Step 2 : Create Falsk Application
#step 3 : Run the aplication

from flask import Flask
from Server import connection
from Validator import generalvalidation
from Config import ApplicationProperty
from Validator import pincodevalidation
import random
from flask import jsonify
from Operation import insertdata
import datetime
from Server import logcapture
import firebase_admin
from firebase_admin import credentials, auth
if not firebase_admin._apps:
    cred = credentials.Certificate("ServiceAccountKey.json")
    firebase_admin.initialize_app(cred)


app=Flask(__name__)
#Create API to add two number
@app.route('/add/<a>/<b>')
def summ(a,b):
    try:
        #VAlidate the request
        #Perform operation
        #Return the result
        if(generalvalidation.check_is_digit(a) and generalvalidation.check_is_digit(b)):
            c=int(a)+int(b)
            print(c)
            return ApplicationProperty.SUCCESS
        return ApplicationProperty.BADREQUEST
    except:
        return ApplicationProperty.ERROR

#Create signup API
@app.route('/createaccount/<name>/<userid>/<contact>/<dob>/<email>/<password>')
def createaccount(name,userid,contact,dob,email,password):
    try:
        if(generalvalidation.check_is_alpha(name) and generalvalidation.check_is_validcontact(contact) and generalvalidation.check_is_validdob(dob) and generalvalidation.check_is_valid_email(email) and generalvalidation.check_is_valid_userid(userid) and generalvalidation.check_is_valid_password(password)):
            #conmnect to the server
            firebase=connection.establish_connection()
            #create auth object
            authobject=firebase.auth()
            authobject.create_user_with_email_and_password(userid+"@app.in",password)
            log(userid,"data inserted in auth table","200")
            data={
                 'name':name,
                 'userid':userid,
                 'contact':contact,
                 'dob':dob,
                 'email':email
                 }
            message=insertdata.insert_data_in_generic("personaldata",data)
            log(userid,"data inserted in realtime table","200")
            print(message)
            if(message=="SUCCESS"):
                log(userid,"account creation successfull","200")
                return "Success"
        log(userid,"bad request for account creation","400")
        return ApplicationProperty.BADREQUEST
    except:
        log(userid,"internal server error for account creation","500")
        return ApplicationProperty.ERROR

#Create login API
@app.route('/loginaccount/<userid>/<password>/<captcha>')
def loginaccount(userid,password,captcha):
    try:
        firebase=connection.establish_connection()
        database=firebase.database()
        count=logcapture.log_capture(userid,database)
        print(count)
        if(count<3):
            if(generalvalidation.check_is_valid_userid(userid) and generalvalidation.check_is_valid_password(password) and generalvalidation.check_is_captcha(captcha,ApplicationProperty.SYSTEMCAPTCHA)):
                #conmnect to the server
                #write down the code to fetch the number of invalid login
                
                if(True):
                    #create auth object
                    authobject=firebase.auth()
                    firebase=connection.establish_connection()
                    try:
                        authobject.sign_in_with_email_and_password(userid+"@app.in",password)
                        log(userid,"Login success","200")
                        return "Success"
                    except:
                        log(userid,"Bad request for login","400")
                        return ApplicationProperty.BADREQUEST
               
            log(userid,"Bad request for login","400")
            return ApplicationProperty.BADREQUEST
        else:
            return ApplicationProperty.LIMIT
    except:
        log(userid,"login failed","500")
        return ApplicationProperty.ERROR   
    
@app.route('/checkvaliduserid/<userid>')
def checkvaliduserid(userid):
    firebase=connection.establish_connection()
    database=firebase.database()
    data=database.child("personaldata").get()
    for eachdata in data.each():
        Vid=eachdata.val()['userid']
        if(userid==Vid):
            return "UserID is present"
    return "Invalid UserID"


@app.route('/generatecaptcha')
def generatecaptcha():
    #generate 4 digit random number
    captcha=str(random.randint(1000,9999))
    ApplicationProperty.SYSTEMCAPTCHA=captcha
    return ApplicationProperty.SYSTEMCAPTCHA

@app.route('/kyc/<userid>/<name>/<address>')
def kyc(userid,name,address):
    try:
        if(generalvalidation.check_is_alpha(name)):
            firebase=connection.establish_connection()
            database=firebase.database()
            data=database.child("personaldata").get()
            for eachdata in data.each():
                Did=eachdata.val()['userid']
                #print(Did,userid)
                if(Did==userid):
                    #Connect to the local database and validate pincode
                    data=address.split(',')[3]
                    print(data)
                    message=pincodevalidation.validate_pincode(data,address)
                    print(message)
                    if(message!="INVALID PIN" and message!="INVALID FORMAT"):
                        #check that userid must be unique
                        firebase=connection.establish_connection()
                        database=firebase.database()
                        data=database.child("KYC").get()
                        found=0
                        for eachdata in data.each():
                            Kid=eachdata.val()['userid']
                            if(Kid==userid):
                                found=1
                        print(found)
                        if(found==0):
                            #insert the data in a KYC table
                            data={
                                'name':name,
                                'userid':userid,
                                'address':address
                                }
                            insertdata.insert_data_in_generic("KYC",data)
                            return "Success"
                                
                        return "ADDRESS FOUND" 
        return ApplicationProperty.BADREQUEST
    except:
        return ApplicationProperty.ERROR
    
    
@app.route('/log/<user>/<operation>/<status>')
def log(user,operation,status):
    #no need to add validation
    #insert the data into log table
    data={
        'timestamp':str(datetime.datetime.now()),
        'user':user,
        'operation':operation,
        'status':status
        }
    insertdata.insert_data_in_generic("log", data)
    return ApplicationProperty.SUCCESS

@app.route('/security/<userid>/<securityquestion>/<securityanswer>')
def security(userid,securityquestion,securityanswer):
    try:
        data={
            'userid':userid,
            'securityquestion':securityquestion,
            'securityanswer':securityanswer
            }
        insertdata.insert_data_in_generic("Security", data)
        return ApplicationProperty.SUCCESS
    except:
        return ApplicationProperty.ERROR
  
@app.route('/security_ques/<userid>')
def security_ques(userid):
    firebase=connection.establish_connection()
    database=firebase.database()
    data=database.child("Security").get()
    for eachdata in data.each():
        Qid=eachdata.val()['userid']
        if(Qid==userid):
           securityquestion = eachdata.val().get('securityquestion')
           return jsonify(securityquestion)
      
    result="Absent"
    return jsonify(result)
       
        
       
@app.route('/security_validation/<userid>/<securityquestion>/<securityanswer>')
def security_validation(userid,securityquestion,securityanswer):
    try:
        firebase=connection.establish_connection()
        database=firebase.database()
        data=database.child("Security").get()
        for eachdata in data.each():
            Vid=eachdata.val()['userid']
            Vquestion=eachdata.val()['securityquestion']
            Vanswer=eachdata.val()['securityanswer']
            if(Vid==userid and Vquestion==securityquestion and Vanswer==securityanswer):
                return "Success"
        return "Fail"
    except:
        return "Fail"
 

       
@app.route('/raise_asset/<userid>/<softwareasset>/<hardwareasset>')
def raise_asset(userid,softwareasset,hardwareasset):
    try:
        reqid=str(random.randint(100000,999999))
        time=str(datetime.datetime.now())
        time=time[:16]
        data={
            'userid':userid,
            'softwareasset':softwareasset,
            'hardwareasset':hardwareasset,
            'reqid':reqid,
            'status':"pending",
            'time':time
            }
        insertdata.insert_data_in_generic("Asset", data)
        result={
               'reqid': reqid,
               'status': "pending",
               'time': time
            }
        return result
    except:
        return "FAIL"
  
    
@app.route('/asset_status/<reqid>')
def asset_status(reqid):
    firebase=connection.establish_connection()
    database=firebase.database()
    data=database.child("Asset").get()
    for eachdata in data.each():
        Rid=eachdata.val()['reqid']
        if(reqid==Rid):
           status = eachdata.val().get('status')
           time = eachdata.val().get('time')
           result = {
               'reqid': Rid,
               'status': status,
               'time': time
           }
           return jsonify(result)
    return "Reqid is not present"
            

        
    
@app.route('/validate_asset/<userid>')
def validate_asset(userid):
    firebase=connection.establish_connection()
    database=firebase.database()
    data=database.child("Asset").get()
    for eachdata in data.each():
        Aid=eachdata.val()['userid']
        if(userid==Aid):
            return "Present"
    return "Empty"


    
@app.route('/complain/<userid>/<issues>')
def complain(issues,userid):
    try:
        comid=str(random.randint(100000,999999))
        time=str(datetime.datetime.now())
        time=time[:16]
        data={
            'userid':userid,
            'comid':comid,
            'issues':issues,
            'time':time,
            'status':'pending'
            }
        insertdata.insert_data_in_generic("Complaints", data)
        result={
               'comid': comid,
               'status': "pending",
               'time': time
            }
        return result
    except:
        return "FAIL"


@app.route('/complain_status/<comid>')
def complain_status(comid):
    firebase=connection.establish_connection()
    database=firebase.database()
    data=database.child("Complaints").get()
    for eachdata in data.each():
        Cid=eachdata.val()['comid']
        if(comid==Cid):
           status = eachdata.val().get('status')
           time = eachdata.val().get('time')
           result = {
               'comid': Cid,
               'status': status,
               'time': time
           }
           return jsonify(result)
    return "Comid is not present" 


@app.route('/asset_presence/<userid>')
def asset_presence(userid):
    firebase=connection.establish_connection()
    database=firebase.database()
    data=database.child("Asset").get()
    for eachdata in data.each():
        Uid=eachdata.val()['userid']
        if(userid==Uid):
           print(userid,Uid)
           reqid = eachdata.val().get('reqid')
           status = eachdata.val().get('status')
           time = eachdata.val().get('time')
           result = {
               'reqid': reqid,
               'status': status,
               'time': time
           }
           return jsonify(result)
        else:
           result = {
               'reqid': "none",
               'status': "none"
               }
    return jsonify(result)

    

@app.route('/complain_presence/<userid>')
def complain_presence(userid):
    firebase=connection.establish_connection()
    database=firebase.database()
    data=database.child("Complaints").get()
    for eachdata in data.each():
        Uid=eachdata.val()['userid']
        if(userid==Uid):
           comid = eachdata.val().get('comid')
           status = eachdata.val().get('status')
           time = eachdata.val().get('time')
           result = {
               'comid': comid,
               'status': status,
               'time': time
           }
           return jsonify(result)
        else:
              result = {
                  'comid': "none",
                  'status':"none"
                  }
    return jsonify(result)


@app.route('/validate_admin/<userid>')
def validate_admin(userid):
    try:
        firebase=connection.establish_connection()
        database=firebase.database()
        data=database.child("admin").get()
        for eachdata in data.each():
            Adid=eachdata.val()['userid']
            if(Adid==userid):
                return "AdminLogin"
            return "Fail"
        return "Fail"
    except:
        return "Error"
    

@app.route('/requested_asset')
def requested_asset():
    firebase = connection.establish_connection()
    database = firebase.database()
    data = database.child("Asset").get()
    data_list = []
    
    for asset in data.each():
        values = asset.val()
        data_list.append([
            values.get('reqid', ''),
            values.get('userid', ''),
            values.get('hardwareasset', ''),
            values.get('softwareasset', ''),
            values.get('time', ''),
            values.get('status', '')
        ])
    
    return jsonify(data_list)

@app.route('/assetid')
def assetid():
    firebase = connection.establish_connection()
    database = firebase.database()
    data = database.child("Asset").get()
    data_list = []
    for asset in data.each():
        values = asset.val()
        if(values.get('status', '') != "Resolved"):
            data_list.append([
                values.get('reqid', '')
            ])
    return jsonify(data_list)
     
    
@app.route('/update_asset/<reqid>/<status>')
def update_asset(reqid,status):
        firebase = connection.establish_connection()
        database = firebase.database()
        data = database.child("Asset").get()
        for eachdata in data.each():
            key = eachdata.key()  
            Rid = eachdata.val().get('reqid')
            if (Rid == reqid):
                database.child("Asset").child(key).update({"status": status})
                return "success"
        return "error: request ID not found"
           


@app.route('/submitted_complaints')
def submitted_complaints():
    firebase = connection.establish_connection()
    database = firebase.database()
    data = database.child("Complaints").get()
    data_list = []
    for asset in data.each():
        values = asset.val()
        data_list.append([
            values.get('comid', ''),
            values.get('userid', ''),
            values.get('issues', ''),
            values.get('time', ''),
            values.get('status','')
            
        ])
    return jsonify(data_list)    

@app.route('/complainid')
def complainid():
    firebase = connection.establish_connection()
    database = firebase.database()
    data = database.child("Complaints").get()
    data_list = []
    for asset in data.each():
        values = asset.val()
        if values.get('status', '') != 'resolved':
            data_list.append([
                values.get('comid', '')
            ])
    return jsonify(data_list)   

@app.route('/update_complaint/<comid>/<status>')
def update_complaint(comid,status):
        firebase = connection.establish_connection()
        database = firebase.database()
        data = database.child("Complaints").get()
        for eachdata in data.each():
            key = eachdata.key()  
            Cid = eachdata.val().get('comid')
            if (Cid == comid):
                database.child("Complaints").child(key).update({"status": status})
                return "success"
        return "error: complaint ID not found"

    
@app.route('/active_complaints/<userid>')
def active_complaints(userid):
    firebase = connection.establish_connection()
    database = firebase.database()
    data = database.child("Complaints").get()
    for eachdata in data.each():
        uid=eachdata.val()['userid']
        if(uid==userid):
            return "present"
    return "error"

@app.route('/active_asset/<userid>')
def active_asset(userid):
    firebase = connection.establish_connection()
    database = firebase.database()
    data = database.child("Complaints").get()
    for eachdata in data.each():
        uid=eachdata.val()['userid']
        if(uid==userid):
            return "present"
    return "error"


@app.route('/update_password/<userid>/<new_password>')
def update_password(userid, new_password):
    try:
        firebase = connection.establish_connection()
        database = firebase.database()
        data = database.child("personaldata").get()

        for eachdata in data.each():
            key = eachdata.key()
            Usid = eachdata.val().get('userid')

            if Usid == userid:
                email = Usid + "@app.in"
                user_record = auth.get_user_by_email(email)
                auth.update_user(
                        user_record.uid,
                        password=new_password
                    )

                database.child("personaldata").child(key).update({"password": new_password})

                return "Password"
                

        return "FAIL"
    except Exception as e:
        return f"Error: {str(e)}"

       

if __name__ == '__main__':
    app.run()
    
