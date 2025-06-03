#validate the pincode and return the details
import pandas as pd
def validate_pincode(value,value2):   
    data=pd.read_excel('C:\\Users\\prath\\OneDrive\\Desktop\\FullStack Python\\Backend\\Validator\\AddressPincode.xlsx') 
    country=list(data.Country)
    state=list(data.State)
    dist=list(data.District)
    region=list(data.Region)
    pin=list(data.Pincode)
    #fetch the data of pincode
    for i in range(0,len(pin)):
        if(value==str(pin[i])):
            print(value,str(pin[i]))
            Data=value2.split(',')
            if(len(Data)==7):
                data1=Data[-1]
                data2=Data[-2]
                data3=Data[-3]
                data4=Data[-5]
                data5=Data[3]
                if(data1==country[i] and data2==state[i] and data3==dist[i] and data4==region[i] and data5==str(pin[i])):
                    #result=country[i]+","+state[i]+","+dist[i]+","+region[i]+","+str(pin[i])
                    return "VAlID"
            return "INVALID FORMAT"
    return "INVALID PIN"

    
print(validate_pincode("560036","45,Bank,K.R.Puram,560036,Bangalore,Karnataka,India"))


                              #HouseNo21,NearBank,Kalyan Nagar,560043,Bangalore,Karnataka,India