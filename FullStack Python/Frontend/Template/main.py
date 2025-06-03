#Front end development done in 3 steps
#Step1: Importing the packages
import json
from gettext import textdomain
from http.client import responses
from pickle import GLOBAL
from urllib.parse import quote
from tkinter import *
from tkinter import messagebox, ttk
from unittest import enterModuleContext

import requests
import random

from flask import Request
from pyexpat.errors import messages

#Step2 : Design the application
app=Tk()
#Configure the screen
app.state('zoomed')


def validateuserid():
    #fetch the userid
    userid=useridentry.get()
    #validate empty condition
    if(userid==""):
        messagebox.showwarning('Warning','Details are missing')
    else:
        url="http://127.0.0.1:5000/checkvaliduserid/"+userid
        responses=requests.get(url)
        responses=responses.text
        if(responses=="UserID is present"):
            messagebox.showinfo('info','Valid UserID')
            loginstep1.place_forget()
            loginstep2.place(x=35, y=15, height=750, width=1450)
            url="http://127.0.0.1:5000/generatecaptcha"
            responses=requests.get(url)
            responses=responses.text
            givencaptcha.configure(text=responses)
        else:
            messagebox.showerror('Error','Invalid UserID')


def refresh():
    url="http://127.0.0.1:5000/generatecaptcha"
    responses=requests.get(url)
    responses=responses.text
    givencaptcha.configure(text=responses)

def forgot_password():
    userid = useridentry.get()
    url="http://127.0.0.1:5000/security_ques/"+userid
    responses = requests.get(url)
    json_data = json.loads(responses.text)
    json_data1 = json_data + '?'
    global Sques
    Sques= json_data
    Sques = quote(Sques)
    loginstep2.place_forget()
    securityques.place(x=35, y=15, height=750, width=1450)
    newsecurityqlabel.configure(text=json_data1)

def Submit1():
    Ques = Sques
    Ans = newsecuritya.get()
    userid = useridentry.get()
    url = "http://127.0.0.1:5000/security_validation/" +userid+ "/" +Ques+ "/" +Ans
    print(url)
    responses = requests.get(url)
    responses = responses.text
    if(responses == "Success"):
        messagebox.showinfo('Info', 'Your answer is correct')
        securityques.place_forget()
        passwordupdate.place(x=35,y=15,height=750,width=1450)
    else:
        messagebox.showwarning('Warning','Your answer is incorrect')

def reset_password():
    userid = useridentry.get()
    passwordnew =  newpasswordentry.get()
    passwordnew1 = newpasswordentry1.get()
    if( passwordnew1 == passwordnew):
        url = "http://127.0.0.1:5000/update_password/" +userid+"/" +passwordnew
        print(url)
        responses = requests.get(url)
        responses = responses.text
        if (responses == "Password"):
            messagebox.showinfo('Info', 'Password changed successfully,Login with new password')
            passwordupdate.place_forget()
            loginstep2.place(x=35, y=15, height=750, width=1450)
        else:
            messagebox.showwarning('Warning','Your password is not valid')
    else:
        messagebox.showwarning('Warning','Your password is not matching!')
def login():
    userid = useridentry.get()
    password = passwordentry.get()
    captcha = captchaentry.get()
    if (password == "" and captcha == ""):
        messagebox.showwarning('Warning','Please Enter the Password and Captcha')
    elif (captcha == ""):
        messagebox.showwarning('Warning', 'Please Enter Captcha')
    elif(password == ""):
        messagebox.showwarning('Warning', 'Please Enter Password')
    else:
        url="http://127.0.0.1:5000/loginaccount/"+userid+"/"+password+"/"+captcha
        responses = requests.get(url)
        responses = responses.text
        print(responses)
        if(responses=="Success"):
            url1="http://127.0.0.1:5000/validate_admin/" +userid
            responses1 = requests.get(url1)
            responses1 = responses1.text
            if(responses1=="AdminLogin"):
                messagebox.showinfo('Info', 'You have successfully logged in as an administrator.')
                loginstep2.place_forget()
                Adminpage.place(x=35, y=15, height=750, width=1450)
            else:
                messagebox.showinfo('Info','You have successfully logged in as a user')
                loginstep2.place_forget()
                homepage.place(x=35, y=15, height=750, width=1450)
        else:
            messagebox.showerror('Error', 'Login Failed')


def create():
    loginstep1.place_forget()
    createstep1.place(x=35, y=15, height=750, width=1450)


def next():
    Userid = userid.get()
    Password = password.get()
    Password1 = password1.get()
    if (Userid == "" and Password == "" and Password1 ==""):
        messagebox.showwarning('Warning', 'Please Enter a UserID  and Password')
    elif (Userid == ""):
        messagebox.showwarning('Warning', 'Please Enter a UserID')
    elif (Password == ""):
        messagebox.showwarning('Warning', 'Please Enter a Password')
    elif(Password != Password1):
        messagebox.showwarning('Warning', 'Password is Not Matching')
    elif(len(Userid)<5):
        messagebox.showwarning('Warning','UserId is too short')
    else:
        messagebox.showinfo('Info','Please Enter Your Personal Details')
        createstep1.place_forget()
        createstep2.place(x=35, y=15, height=750, width=1450)


def next1():
    Name = name.get()
    Userid = userid.get()
    Password = password.get()
    Contact = contact.get()
    Dob = dob.get()
    Email = email.get()
    if (Name== "" and Contact == "" and Dob == "" and Email ==""):
        messagebox.showwarning('Warning', 'Please Enter your Personal Details')
    elif (Name == ""):
        messagebox.showwarning('Warning', 'Please Enter your Name')
    elif (Contact == ""):
        messagebox.showwarning('Warning', 'Please Enter your Contact')
    elif (Dob == ""):
        messagebox.showwarning('Warning', 'Please Enter your Date of Birth')
    elif (Email == ""):
        messagebox.showwarning('Warning', 'Please Enter your Email')
    elif (Name== "" and Contact == ""):
        messagebox.showwarning('Warning', 'Please Enter your Name and Contact')
    elif (Name == "" and Dob == ""):
        messagebox.showwarning('Warning', 'Please Enter your Name and Date of Birth')
    elif (Contact == "" and Dob == ""):
        messagebox.showwarning('Warning', 'Please Enter your Contact and Date of Birth')
    else:
        url = "http://127.0.0.1:5000/createaccount/" +Name+"/" +Userid+ "/" +Contact+ "/" +Dob+ "/" +Email+ "/" +Password
        responses = requests.get(url)
        responses = responses.text
        if (responses == "Success"):
            messagebox.showinfo('Info','Personal Details Filled Successfully')
            createstep2.place_forget()
            createstep3.place(x=35, y=15, height=750, width=1450)
        else:
            messagebox.showerror('Error','Your Credentials are not Valid')
            createstep2.place_forget()
            createstep1.place(x=35, y=15, height=750, width=1450)


def Address():
    details=address.get()
    Name = name.get()
    Userid = userid.get()
    if(details == ""):
        messagebox.showwarning('Warning','Enter your Address')
    else:
        url = "http://127.0.0.1:5000/kyc/"+Userid+ "/" +Name+ "/" +details
        responses=requests.get(url)
        responses=responses.text
        print(responses)
        if(responses == "Success"):
            messagebox.showinfo('Info', 'Address Filled Successfully')
            createstep3.place_forget()
            createstep4.place(x=35, y=15, height=750, width=1450)
            get_random_security_question()
        else:
            messagebox.showerror('Error', 'Your Address is not Valid')
            createstep3.place_forget()
            createstep3.place(x=35, y=15, height=750, width=1450)


def Finish():
    Userid = userid.get()
    SecurityQ=msg
    SecurityA=securitya.get()
    if(SecurityA == ""):
       messagebox.showwarning('Warning','Please Answer the Question')
    else:
        url="http://127.0.0.1:5000/security/" +Userid+ "/" +SecurityQ+ "/"+SecurityA
        responses = requests.get(url)
        responses = responses.text
        print(responses)
        messagebox.showinfo('Info','Account Created Successfully')
        messagebox.showinfo('Info','Please log in to the application to gain access ')
        createstep4.place_forget()
        loginstep1.place(x=35, y=15, height=750, width=1450)

def Reset():
    get_random_security_question()

security_questions = [
    "What is your Best Friend Name?",
    "What is your Pet Name?",
    "What is your Favourite Sports?",
    "What is your Class Teacher Name?"
]

msg = ""
question = ""

def get_random_security_question():
    global msg, question
    question = random.choice(security_questions)
    securityqlabel.configure(text=question)
    msg = quote(question)
    msg = msg[:-1]

def Logout():
    decision= messagebox.askyesno('Info', 'Do you really want to Logout?')
    if decision:
        homepage.place_forget()
        app.destroy()
        import main
        loginstep1.place(x=35, y=15, height=750, width=1450)
    else:
        homepage.place(x=35, y=15, height=750, width=1450)

def Asset():
    Userid=useridentry.get()
    msg= messagebox.askyesno('Info','Do you want to request Asset?')
    url="http://127.0.0.1:5000/asset_presence/" +Userid
    responses = requests.get(url)
    json_data = json.loads(responses.text)
    print(json_data)
    rid = json_data['reqid']
    sts = json_data['status']
    if(rid=="none"):
        if msg:
            child2.place_forget()
            child3.place_forget()
            child1.place(x=350, y=150, height=500, width=1000)
            requestabutton = Button(child1, bg='green', fg='white', text="Request", font=("Arial", 12),command=Request_Asset)
            requestabutton.place(x=300, y=380, height=50, width=200)
        else:
            homepage.place(x=35, y=15, height=750, width=1450)
    elif(sts == "Resolved"):
        child2.place_forget()
        child3.place_forget()
        child1.place(x=350, y=150, height=500, width=1000)
        requestabutton = Button(child1, bg='green', fg='white', text="Request", font=("Arial", 12),command=Request_Asset)
        requestabutton.place(x=300, y=380, height=50, width=200)
    else:
        child2.place_forget()
        child3.place_forget()
        child1.place(x=350, y=150, height=500, width=1000)
        tme = json_data['time']
        sentence = "You are requested the Asset with Request ID " + rid + " at " + tme + ", which is under " + sts + " Status"
        assetmsg1 = Label(child1, bg='gray', fg='black', text=sentence, font=("Arial", 15))
        assetmsg1.place(x=30, y=400)


def Request_Asset():
    Userid=useridentry.get()
    print(userid)
    SoftA=sofassetentry.get()
    HardA=harassetentry.get()
    if (SoftA== "" and HardA == ""):
        messagebox.showwarning('Warning', 'Please Enter your Required asset')
    elif (SoftA == ""):
        messagebox.showwarning('Warning', 'Please Enter your Required Software asset')
    elif (HardA == ""):
        messagebox.showwarning('Warning', 'Please Enter your Required Hardware asset')
    else:
        url="http://127.0.0.1:5000/raise_asset/"+Userid+"/"+SoftA+"/"+HardA
        responses = requests.get(url)
        json_data = json.loads(responses.text)
        rid = json_data['reqid']
        sts = json_data['status']
        tme = json_data['time']
        child1.place(x=350,y=150,height=500,width=1000)
        sentence = "You are requested the asset with Request ID "+rid+" at "+tme+", which is under "+sts+" Status"
        messagebox.showinfo('Info', 'Assets requested successfully')
        assetmsg=Label(child2, bg='gray', fg='white', text=sentence, font=("Arial", 15))
        assetmsg.place(x=300,y=450)


def Com_Status():
    Userid = useridentry.get()
    url = "http://127.0.0.1:5000/validate_asset/" + Userid
    responses = requests.get(url)
    responses = responses.text
    if (responses == "Present"):
        child3.place_forget()
        child1.place_forget()
        child2.place(x=350,y=150,height=500,width=1000)
    else:
        messagebox.showwarning('Warning',"You don't have any requested asset!")

def Submitted_asset():
    Reqid = identry.get()
    if (Reqid == ""):
        messagebox.showwarning('Warning', 'Enter the Request ID!')
    else:
        url = "http://127.0.0.1:5000/asset_status/" + Reqid
        responses = requests.get(url)
        json_data = json.loads(responses.text)
        rid = json_data['reqid']
        sts = json_data['status']
        if(Reqid==rid):
            sentence = "Your request with request Id " + rid + " under " + sts + " status"
            reqlabel=Label(child2, bg='gray', fg='white', text=sentence, font=("Arial", 15))
            reqlabel.place(x=250,y=250)
        else:
            messagebox.showwarning('Warning', 'You entered invalid Request ID!')

def Submitted_complain():
    Comid=identry.get()
    if(Comid==""):
        messagebox.showwarning('Warning','Enter the Complain ID!')
    else:
        url = "http://127.0.0.1:5000/complain_status/" +Comid
        responses = requests.get(url)
        json_data = json.loads(responses.text)
        cid=json_data['comid']
        sts=json_data['status']
        if(Comid==cid):
            sentence="The complaint with complaint Id "+cid+" is under "+sts+ "status"
            comlabel=Label(child2, bg='gray', fg='white', text=sentence, font=("Arial", 15))
            comlabel.place(x=250, y=250)
        else:
            messagebox.showwarning('Warning','You entered invalid Complain ID!')

def Complain():
    Userid=useridentry.get()
    url="http://127.0.0.1:5000/validate_asset/" +Userid
    responses = requests.get(url)
    responses = responses.text
    if(responses=="Present"):
        url1 = "http://127.0.0.1:5000/complain_presence/" + Userid
        responses1 = requests.get(url1)
        json_data1 = json.loads(responses1.text)
        cid = json_data1['comid']
        sts = json_data1['status']
        if(cid=="none"):
            child1.place_forget()
            child2.place_forget()
            child3.place(x=350,y=150,height=500,width=1000)
            submitbutton = Button(child3, bg='green', fg='white', text='Submit', font=("Arial", 12), command=Submit)
            submitbutton.place(x=340, y=380, height=50, width=210)
        elif(sts == "Resolved"):
            msg = "Your Complaint with Complaint ID "+cid+" is solved"
            messagebox.showinfo('Info',msg)
            child1.place_forget()
            child2.place_forget()
            child3.place(x=350, y=150, height=500, width=1000)
            submitbutton = Button(child3, bg='green', fg='white', text='Submit', font=("Arial", 12), command=Submit)
            submitbutton.place(x=340, y=380, height=50, width=210)
        else:
            child1.place_forget()
            child2.place_forget()
            tme = json_data1['time']
            sentence = "You are complained with complaint Id "+cid+" at " + tme + ", which is under " + sts + " Status"
            child3.place(x=350, y=150, height=500, width=1000)
            compmsg2 = Label(child3, bg='gray', fg='black', text=sentence, font=("Arial", 15))
            compmsg2.place(x=80, y=400)
    else:
        messagebox.showwarning('Warning',"You don't have any requested asset!")

def Submit():
    Userid=useridentry.get()
    Complaints=complainentry.get()
    if(Complaints==""):
        messagebox.showwarning('Warning','Please mention complaints!')
    else:
        complaints=Complaints.split(" ")
        print(complaints)
        msg=""
        for i in range(len(complaints)):
            complain=complaints[i]+"%20"
            print(complain)
            msg+=complain
        msg=msg[0:len(msg)-3]
        url="http://127.0.0.1:5000/complain/" +Userid+ "/" +msg
        responses = requests.get(url)
        json_data = json.loads(responses.text)
        cid = json_data['comid']
        sts = json_data['status']
        tme = json_data['time']
        sentence = "You are complained with the complain ID " + cid + " at " + tme + " which is under " + sts + " Status"

        messagebox.showinfo('Info', 'Complain submitted successfully')
        compmsg = Label(child3, bg='gray', fg='black', text=sentence, font=("Arial", 15))
        compmsg.place(x=340, y=400)


def AssetReq():
   Adminchild2.place_forget()
   Adminchild3.place_forget()
   Adminchild1.place(x=350,y=150,height=500,width=1000)
   for widget in Adminchild1.winfo_children():
       widget.destroy()
   url="http://127.0.0.1:5000/requested_asset"
   responses = requests.get(url)
   data = json.loads(responses.text)
   reqlabel = Label(Adminchild1, bg='orange', fg='white', text="Requested Assets are below", font=("Arial", 20))
   reqlabel.pack(pady=10)
   columns = ["Request ID", "User ID", "Hardware Asset", "Software Asset", "Time", "Status"]
   tree = ttk.Treeview(Adminchild1, columns=columns, show="headings")
   for col in columns:
       tree.heading(col, text=col)
       tree.column(col, width=150, anchor='center')
   for row in data:
       tree.insert("", "end", values=row)
   scrollbar = ttk.Scrollbar(Adminchild1, orient="vertical", command=tree.yview)
   tree.configure(yscrollcommand=scrollbar.set)
   tree.pack(side="left", fill="both", expand=True)
   scrollbar.pack(side="right", fill="y")


def Adm_Status():
    Adminchild1.place_forget()
    Adminchild3.place_forget()
    Adminchild2.place(x=350,y=150,height=500,width=1000)

def update_asset():
    Assetid=reqid.get()
    Sts=status1.get()
    url="http://127.0.0.1:5000/update_asset/"+Assetid+"/"+Sts
    responses = requests.get(url)
    responses = responses.text
    if(responses=="success"):
        messagebox.showinfo('Info','Asset updated successfully')
    else:
        messagebox.showerror("Error","Internal Error")
def update_complain():
    Compid = compid.get()
    Sts1 = status1.get()
    url = "http://127.0.0.1:5000/update_complaint/" + Compid + "/" + Sts1
    responses = requests.get(url)
    responses = responses.text
    if (responses == "success"):
        messagebox.showinfo('Info', 'Complaint updated successfully')
    else:
        messagebox.showerror("Error", "Internal Error")

def Complaints():
    Adminchild1.place_forget()
    Adminchild2.place_forget()
    Adminchild3.place(x=350,y=150,height=500,width=1000)
    for widget in Adminchild3.winfo_children():
        widget.destroy()
    url = "http://127.0.0.1:5000/submitted_complaints"
    responses = requests.get(url)
    data = json.loads(responses.text)
    reqlabel = Label(Adminchild3, bg='orange', fg='white', text="Submitted complaints are below", font=("Arial", 20))
    reqlabel.pack(pady=10)
    columns = ["Complain ID", "User ID","Complaints","Time", "Status"]
    tree = ttk.Treeview(Adminchild3, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')
    for row in data:
        tree.insert("", "end", values=row)
    scrollbar = ttk.Scrollbar(Adminchild3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def LogoutA1():
    decision= messagebox.askyesno('Info', 'Do you really want to Logout?')
    if decision:
        Adminpage.place_forget()
        app.destroy()
        import main
        loginstep1.place(x=35, y=15, height=750, width=1450)
    else:
        Adminpage.place(x=35, y=15, height=750, width=1450)



#Create login step1 frame
loginstep1=Frame(app,bg='blue')
loginstep1.place(x=35,y=15,height=750,width=1450)
head=Label(loginstep1,bg='blue',fg='white',text="First Step of Login",font=("Arial",30))
head.place(x=20,y=20)
heading=Label(loginstep1,bg='blue',text="What is  your userid?",font=('Arial',30),fg='white')
heading.place(x=250,y=250)
useridentry=Entry(loginstep1,)
useridentry.place(x=650,y=240,height=80,width=400)
nextbutton=Button(loginstep1,bg='green',fg='white',text="Next",font=("Arial",12),command=validateuserid)
nextbutton.place(x=1100,y=600,height=80,width=200)
newbutton=Button(loginstep1,bg='blue',fg='white',text="New to Application? Create account",font=("Arial",12),command=create)
newbutton.place(x=600,y=650,height=50,width=300)
########################################################ENd of loginstep1


loginstep2=Frame(app,bg='blue')
#loginstep2.place(x=35,y=15,height=750,width=1450)
head1=Label(loginstep2,bg='blue',fg='white',text="Final Step of Login",font=("Arial",30))
head1.place(x=20,y=20)
passwordlabel=Label(loginstep2,bg='blue',fg='white',text='Please enter your password',font=('Arial',15))
passwordlabel.place(x=600,y=180)
passwordentry=Entry(loginstep2,show='*')
passwordentry.place(x=600,y=220,height=60,width=250)
passwordbutton=Button(loginstep2,bg='green',fg='white',text="Forgot password",font=("Arial",12),command=forgot_password)
passwordbutton.place(x=600,y=290,height=30,width=250)
refreshbutton=Button(loginstep2,bg='green',fg='white',text="Refresh",font=("Arial",12),command=refresh)
refreshbutton.place(x=750,y=355,height=50,width=100)
givencaptcha=Label(loginstep2,bg='blue',fg='white',font=("Italian",20))
givencaptcha.place(x=650,y=360)
captchalabel=Label(loginstep2,bg='blue',fg='white',text='Please enter the captcha',font=('Arial',15))
captchalabel.place(x=600,y=425)
captchaentry=Entry(loginstep2)
captchaentry.place(x=600,y=460,height=60,width=250)
loginbutton=Button(loginstep2,bg='green',fg='white',text="Login",font=("Arial",12),command=login)
loginbutton.place(x=620,y=600,height=80,width=200)
###########################################################End of login step2


securityques=Frame(app,bg='blue')
#securityques.place(x=35, y=15, height=750, width=1450)
head5=Label(securityques,bg='blue',fg='white',text="Security question",font=("Arial",30))
head5.place(x=20,y=20)
newsecurityqlabel=Label(securityques,bg='blue',fg='white',font=("Arial",15))
newsecurityqlabel.place(x=600,y=240)
newsecuritya=Entry(securityques)
newsecuritya.place(x=600,y=280,height=60,width=250)
newfinalbutton=Button(securityques,bg='green',fg='white',text="Submit",font=("Arial",12),command=Submit1)
newfinalbutton.place(x=625,y=380,height=80,width=200)




passwordupdate=Frame(app,bg='blue')
#passwordupdate.place(x=35,y=15,height=750,width=1450)
passhead1=Label(passwordupdate,bg='blue',fg='white',text="For password change",font=("Arial",30))
passhead1.place(x=20,y=20)
newpasswordlabel=Label(passwordupdate,bg='blue',fg='white',text='Please enter your new password',font=('Arial',15))
newpasswordlabel.place(x=600,y=180)
newpasswordentry=Entry(passwordupdate,show='*')
newpasswordentry.place(x=600,y=220,height=60,width=250)
newpasswordlabel1=Label(passwordupdate,bg='blue',fg='white',text='Please re-enter your new password',font=('Arial',15))
newpasswordlabel1.place(x=600,y=300)
newpasswordentry1=Entry(passwordupdate,show='*')
newpasswordentry1.place(x=600,y=340,height=60,width=250)
newpassbutton=Button(passwordupdate,bg='green',fg='white',text="Reset",font=("Arial",12),command=reset_password)
newpassbutton.place(x=620,y=600,height=80,width=200)
#################################################


createstep1=Frame(app,bg='blue')
#createstep1.place(x=35,y=15,height=750,width=1450)
head2=Label(createstep1,bg='blue',fg='white',text="First Step of Account Creation",font=("Arial",30))
head2.place(x=20,y=20)
useridlabel=Label(createstep1,bg='blue',fg='white',text="Enter a userid",font=("Arial",15))
useridlabel.place(x=600,y=150)
useridformatlabel=Label(createstep1,bg='blue',fg='white',text="(User ID needs uppercase, lowercase, and a number)",font=("Arial",12))
useridformatlabel.place(x=600,y=175)
userid=Entry(createstep1)
userid.place(x=600,y=200,height=60,width=250)
passwordlabel1=Label(createstep1,bg='blue',fg='white',text="Enter a password",font=("Arial",15))
passwordlabel1.place(x=600,y=280)
passwordformat=Label(createstep1,bg='blue',fg='white',text="(Password with at least 8 characters, including uppercase and lowercase letters, numbers, and special symbols)",font=("Arial",12))
passwordformat.place(x=600,y=310)
password=Entry(createstep1,show='*')
password.place(x=600,y=340,height=60,width=250)
passwordlabel2=Label(createstep1,bg='blue',fg='white',text="Re-enter your password",font=("Arial",15))
passwordlabel2.place(x=600,y=420)
password1=Entry(createstep1,show='*')
password1.place(x=600,y=460,height=60,width=250)
nextbutton1=Button(createstep1,bg='green',fg='white',text="Next",font=("Arial",12),command=next)
nextbutton1.place(x=1100,y=600,height=80,width=200)
###############################################################End of 1st page of creation


createstep2=Frame(app,bg='blue')
#createstep2.place(x=35,y=15,height=750,width=1450)
head3=Label(createstep2,bg='blue',fg='white',text="Second Step of Account Creation",font=("Arial",30))
head3.place(x=20,y=20)
namelabel=Label(createstep2,bg='blue',fg='white',text="Enter Your Name",font=("Arial",15))
namelabel.place(x=600,y=120)
name=Entry(createstep2)
name.place(x=600,y=160,height=60,width=250)
emaillabel=Label(createstep2,bg='blue',fg='white',text="Enter Your Email",font=("Arial",15))
emaillabel.place(x=600,y=240)
email=Entry(createstep2)
email.place(x=600,y=280,height=60,width=250)
contactlabel=Label(createstep2,bg='blue',fg='white',text="Enter Your Contact Number",font=("Arial",15))
contactlabel.place(x=600,y=360)
contactformatlabel=Label(createstep2,bg='blue',fg='white',text="(must be 10 digits)",font=("Arial",12))
contactformatlabel.place(x=720,y=390)
contact=Entry(createstep2)
contact.place(x=600,y=420,height=60,width=250)
doblabel=Label(createstep2,bg='blue',fg='white',text="Enter Your Date of Birth",font=("Arial",15))
doblabel.place(x=600,y=500)
dobformatlabel=Label(createstep2,bg='blue',fg='white',text="(dd-mm-yyyy)",font=("Arial",12))
dobformatlabel.place(x=750,y=530)
dob=Entry(createstep2)
dob.place(x=600,y=560,height=60,width=250)
addressbutton=Button(createstep2,bg='green',fg='white',text="Next",font=("Arial",12),command=next1)
addressbutton.place(x=1100,y=600,height=80,width=200)
############################################################# End of 2nd step of creation


createstep3=Frame(app,bg='blue')
#createstep3.place(x=35,y=15,height=750,width=1450)
head4=Label(createstep3,bg='blue',fg='white',text="Third Step of Account Creation",font=("Arial",30))
head4.place(x=20,y=20)
addresslabel=Label(createstep3,bg='blue',fg='white',text="Enter Your Address",font=("Arial",15))
addresslabel.place(x=600,y=160)
addressformat=Label(createstep3,bg='blue',fg='white',text="(Address should be in :[House No], [Nearby Place], [Locality], [PIN Code], [City], [State], [Country]. format)",font=("Arial",12))
addressformat.place(x=600,y=190)
address=Entry(createstep3)
address.place(x=600,y=230,height=200,width=300)
addressbutton1=Button(createstep3,bg='green',fg='white',text="Next",font=("Arial",12),command=Address)
addressbutton1.place(x=1100,y=600,height=80,width=200)
###########################################################End of 3rd stage of creation

createstep4=Frame(app,bg='blue')
#createstep4.place(x=35,y=15,height=750,width=1450)
head5=Label(createstep4,bg='blue',fg='white',text="Fourth Step of Account Creation",font=("Arial",30))
head5.place(x=20,y=20)
securityqlabel=Label(createstep4,bg='blue',fg='white',font=("Arial",15))
securityqlabel.place(x=600,y=240)
securitya=Entry(createstep4)
resetbutton=Button(createstep4,bg='green',fg='white',text="Change",font=("Arial",12),command=Reset)
resetbutton.place(x=620,y=360,height=50,width=210)
securitya.place(x=600,y=280,height=60,width=250)
resetlabel=Label(createstep4,bg='blue',fg='white',text="(Press 'Change' Button for Changing The Security Question)" ,font=("Arial",12))
resetlabel.place(x=530,y=600)
finalbutton=Button(createstep4,bg='green',fg='white',text="Finish",font=("Arial",12),command=Finish)
finalbutton.place(x=1100,y=600,height=80,width=200)
###############################################################End of 4th stage of creation


homepage=Frame(app,bg='blue')
#homepage.place(x=35,y=15,height=750,width=1450)
head6=Label(homepage,bg='blue',fg='white',text="Welcome To User Dash Board Page",font=("Arial",30))
head6.place(x=20,y=20)
reqassetbutton=Button(homepage,bg='green',fg='white',text='For Assets',font=("Arial",12),command=Asset)
reqassetbutton.place(x=40,y=150,height=50,width=210)
statusbutton=Button(homepage,bg='green',fg='white',text='Status',font=("Arial",12),command=Com_Status)
statusbutton.place(x=40,y=250,height=50,width=210)
complainbutton=Button(homepage,bg='green',fg='white',text='Complain',font=("Arial",12),command=Complain)
complainbutton.place(x=40,y=350,height=50,width=210)
logoutbutton=Button(homepage,bg='green',fg='white',text='Logout',font=("Arial",12),command=Logout)
logoutbutton.place(x=40,y=650,height=50,width=210)
###########################################################################################
global child1
child1=Frame(homepage,bg='gray')
#child1.place(x=350,y=150,height=500,width=1000)
sofasset=Label(child1,bg='gray',fg='white',text="Kindly specify the Software assets you require",font=("Arial",15))
sofasset.place(x=300,y=60)
sofassetentry=Entry(child1)
sofassetentry.place(x=300,y=100,height=100,width=200)
harasset=Label(child1,bg='gray',fg='white',text="Kindly specify the Hardware assets you require",font=("Arial",15))
harasset.place(x=300,y=220)
harassetentry=Entry(child1)
harassetentry.place(x=300,y=260,height=100,width=200)


##############################################################################################

child2=Frame(homepage,bg='gray')
#child2.place(x=350,y=150,height=500,width=1000)
idslabel=Label(child2,bg='gray',fg='white',text="Kindly enter your Request/Complain ID",font=("Arial",15))
idslabel.place(x=300,y=60)
identry=Entry(child2)
identry.place(x=400,y=100,height=50,width=150)
assetstatus=Button(child2,bg='green',fg='white',text="Asset",font=("Arial",12),command=Submitted_asset)
assetstatus.place(x=300,y=180,height=50,width=200)
comstatus=Button(child2,bg='green',fg='white',text="Complain",font=("Arial",12),command=Submitted_complain)
comstatus.place(x=520,y=180,height=50,width=200)

###################################################################

child3=Frame(homepage,bg='gray')
#child3.place(x=350,y=150,height=500,width=1000)
complainlabel=Label(child3,bg='gray',fg='white',text="Write down your complaints",font=("Arial",20))
complainlabel.place(x=300,y=100)
complainentry=Entry(child3)
complainentry.place(x=300,y=150,height=200,width=300)


######################################################################################################

Adminpage=Frame(app,bg='blue')
#Adminpage.place(x=35,y=15,height=750,width=1450)
head6=Label(Adminpage,bg='blue',fg='white',text="Welcome To Admin Dash Board Page",font=("Arial",30))
head6.place(x=20,y=20)
Aassetbutton=Button(Adminpage,bg='green',fg='white',text='Assets Requested',font=("Arial",12),command=AssetReq)
Aassetbutton.place(x=40,y=150,height=50,width=210)
statusbutton=Button(Adminpage,bg='green',fg='white',text='Status',font=("Arial",12),command=Adm_Status)
statusbutton.place(x=40,y=250,height=50,width=210)
compbutton=Button(Adminpage,bg='green',fg='white',text='Complaints',font=("Arial",12),command=Complaints)
compbutton.place(x=40,y=350,height=50,width=210)
logoutbutton=Button(Adminpage,bg='green',fg='white',text='Logout',font=("Arial",12),command=LogoutA1)
logoutbutton.place(x=40,y=650,height=50,width=210)
##################################################################################################


Adminchild1=Frame(Adminpage,bg='orange')
#Adminchild1.place(x=350,y=150,height=500,width=1000)

Adminchild2=Frame(Adminpage,bg='gray')
#Adminchild1.place(x=350,y=150,height=500,width=1000)
ids1label=Label(Adminchild2,bg='gray',fg='white',text="Kindly select one Request/Complain ID for change the status",font=("Arial",15))
ids1label.place(x=250,y=60)

url = "http://127.0.0.1:5000/assetid"
response = requests.get(url)
data = json.loads(response.text)
request_ids = [row[0] for row in data]
request_id_list = request_ids
reqid=StringVar()
reqid_dropdown = ttk.Combobox(Adminchild2, values=request_id_list, font=("Arial", 12), state="readonly", textvariable=reqid)
reqid_dropdown.set("Select Request ID")
reqid_dropdown.place(x=100, y=120, width=200, height=30)

url = "http://127.0.0.1:5000/complainid"
response = requests.get(url)
data = json.loads(response.text)
complain_ids = [row[0] for row in data]
complain_id_list = complain_ids
compid=StringVar()
compid_dropdown = ttk.Combobox(Adminchild2, values=complain_id_list, font=("Arial", 12), state="readonly", textvariable=compid)
compid_dropdown.set("Select Complain ID")
compid_dropdown.place(x=600, y=120, width=200, height=30)

status_options = ["Pending", "Duplicate","Closed","Resolved","In-progress"]
status_label = Label(Adminchild2, bg='gray', fg='white', text="Select New Status", font=("Arial", 15))
status_label.place(x=350, y=150)
status1=StringVar()
status_dropdown = ttk.Combobox(Adminchild2, values=status_options, font=("Arial", 12), state="readonly", textvariable=status1)
status_dropdown.set("Select Status")
status_dropdown.place(x=350, y=200, width=200, height=30)

assetstatusAD=Button(Adminchild2,bg='green',fg='white',text="Update Asset",font=("Arial",12),command=update_asset)
assetstatusAD.place(x=250,y=400,height=50,width=200)
comstatusAD=Button(Adminchild2,bg='green',fg='white',text="Update Complain",font=("Arial",12),command=update_complain)
comstatusAD.place(x=480,y=400,height=50,width=200)

Adminchild3=Frame(Adminpage,bg='orange')
#Adminchild1.place(x=350,y=150,height=500,width=1000)



#Step3: Make the screen visible
app.mainloop()