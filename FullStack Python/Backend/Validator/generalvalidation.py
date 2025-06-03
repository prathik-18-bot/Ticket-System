#This file contains custom verification


def check_is_digit(value):
    if(value.isdigit()):
        return True
    return False

def check_is_alpha(value):
    if(value.isalpha()):
        return True
    return False

def check_is_validcontact(value):
    if(value.isdigit() and len(value)==10):
        return True
    return False

def check_is_validdob(value):
    if(len(value)==10 and value[2]=="-" and value[5]=="-"):
        data=value.split('-')
        dd=data[0]
        mm=data[1]
        yyyy=data[2]
        if(dd.isdigit() and int(dd)>0 and  int(dd)<32):
            if(mm.isdigit() and int(mm)>0 and int(mm)<13):
                if(yyyy.isdigit()):
                    return True
    return False

def check_is_valid_email(value):
   value=value.lower()
   data=list(value)
   a=0
   b=0
   c=0
   d=0
   j=-1
   for i in data:
       j=j+1
       for index in range (len(data)-11):
           s=value[index]
           if('a' <= s <= 'z'):
             c=c+1  
       if i.isdigit():
           d=d+1
       if(i =='@'):
          index_at=j
          a=a+1
       if(i=='.'):
           index_dot=j
           b=b+1
   if(a==1 and b==1 and c>0 and d>0 and index_dot==len(data)-4 and index_at== len(data)-10 and value[len(data)-9:len(data)-0]=="gmail.com"):
       return True
   return False


def check_is_valid_userid(value):
    data=list(value)
    a=0
    b=0
    c=0
    for i in data:
        if i.isdigit():
            a=a+1
        if i.isalpha():
            if i.islower():
                 b=b+1
            else:
                 c=c+1
    if(a>0 and b>0 and c>0 and len(data)>5):
        return True
    return False

def check_is_valid_password(value):
    data=list(value)
    a=0
    b=0
    c=0
    d=0
    for i in data:
        if i.isdigit():
            a=a+1
        if i.isalpha():
            if i.islower():
                b=b+1
            else:
                d=d+1
        if(i=="!" or i=="@"or i=="#"or i=="$"or i=="%"or i=="^"or i=="&"or i=="*" ):
            c=c+1
    if(a>0 and b>0 and c>0 and d>0 and len(data)>7):
        return True
    return False
    
def check_is_captcha(value,systemvalue):
    if(value == systemvalue):
        return True
    return False

def check_valid_pincode(value):
    if(value.isdigit() and len(value)==6):
        return True
    return False

