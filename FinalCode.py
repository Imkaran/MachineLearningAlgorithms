# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 00:37:11 2018

@author: karan
"""
#!/usr/bin/env python

import glob
import csv
from Tkinter import *
import Tkinter as tk
import tkMessageBox
import csv
from tkFileDialog import askopenfilename
import os,shutil
import sys
import math

global jvalue
global listData
global mylist
global frameList
global positionXList
global positionYList
global obsVelXList
global obsVelYList
global numberofObjects
global totalObjects
global mylen
global timeCounter_List
global ActVelList
global active
global frame

jvalue=[]
timeCounter_List=[]
numberofObjects=[]
obsVelXList=[]
obsVelYList=[]
positionXList=[]
positionYList=[]
frameList=[]
ActVelList=[]
listData=[]
mylist=[]
mylen=3
inputFile=''


'''
Closes the window while click on close button
'''
def on_closing():

    tmp = tkMessageBox.askokcancel(title='Permission Window',message='Do you Want To Quit ?',parent=master)
    if tmp is True:
        master.destroy()
        sys.exit()
        
#--------------------------------------------------------------------------------------------------------------------------------
'''
Close the current window
'''
def quit():
    master.destroy()
    
#--------------------------------------------------------------------------------------------------------------------------------
'''
Ask user for browsing a input file
'''
def callback():
    global video_name
    global inputFile
    inputFile = askopenfilename()             #Browse the file
    trim_path=os.path.basename(inputFile)#Trims the pathname and gives only the filename
    tname=trim_path[:-4]
    print (inputFile)
    entry_text.insert(0,tname)
errmsg = 'Error!'

#--------------------------------------------------------------------------------------------------------------------------------    
'''
fetching objNum column from csv into list(numberofObjects)
and then finding out max from that list(numberofObjects)

'''
def objectCount():
    cnt=0
    temp=0
    with open(inputFile,'r') as f:
        rows = csv.reader(f)
        for row in rows:
            flag=1
            if(cnt!=0):
                temp=row[2]  # Only print the column in the row
                #if(cnt!=0):
                numberofObjects.append(int(temp))                  
            cnt=cnt+1
    totalObjects= max(numberofObjects)+1
    return totalObjects
    
#--------------------------------------------------------------------------------------------------------------------------------
'''
Write frame number into csv file where objectId appears along with its properties
'''
def writeDataToCsv(list_frame,filename,ActVelList1):
    absoluteVelocity=[]
    path="C:\CSV\Honda_"
    directory = os.path.dirname(path)
    result=0.0
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)       

    for i in range(0,len(ActVelList1)):
        result=float(ActVelList1[i])+(float(obsVelXList[i]))*3.6
        absoluteVelocity.append(result)
    

    print 'list_frame',len(list_frame)
    print 'positionXList',len(positionXList)
    print 'positionYList',len(positionYList)
    print 'obsVelXList',len(obsVelXList)
    print 'obsVelYList',len(obsVelYList)
    print 'absoluteVelocity',len(absoluteVelocity)

    with open(path+filename+'.csv','wb') as f:
        fieldnames = ['obsPosX_'+filename,'obsPosY_'+filename,'obsVelX_'+filename,'obsVelY_'+filename,'absoluteVelocity_'+filename]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(list_frame)):
            writer.writerow({fieldnames[0]:positionXList[i],fieldnames[1]:positionYList[i],fieldnames[2]:obsVelXList[i],fieldnames[3]:obsVelYList[i],fieldnames[4]:absoluteVelocity[i]})

#--------------------------------------------------------------------------------------------------------------------------------

def EgoWriteDataToCsv(timeCounter_List,totalObjects,objCount,frameEgoList):
    path="C:\CSV\Ego_"
    print 'writing...'
    column=0
    objCount=3
    cnt=0
    temp=0
    frame=0
    active=0
    #name=str(key)
    with open(inputFile) as f:
            rows1 = csv.reader(f)
            for row in rows1:
                if(cnt!=0 and objCount<totalObjects+3):
                    frame=frame+1
    
                    ActVelList.append(row[1])
                    
                                              
                cnt=cnt+1
    active= len(ActVelList)
    with open(path+'.csv','wb') as f:
        #fieldnames = ['#Time','FrameNumber',' ActVel[kph]']
        fieldnames = ['#Time','FrameNumber',' ActVel[kph]']
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,active):
            #writer.writerow({fieldnames[0]:timeCounter_List[i],fieldnames[1]:ActVelList[i]})
            writer.writerow({fieldnames[0]:timeCounter_List[i],fieldnames[1]:frameEgoList[i],fieldnames[2]:ActVelList[i]})
#--------------------------------------------------------------------------------------------------------------------------------
def getActualVelocity():
    ActVelList1=[]
    
    with open(inputFile) as f:
            rows1 = csv.reader(f)
            next(rows1)
            for row in rows1:   
                ActVelList1.append(row[1])
    return  ActVelList1      
#--------------------------------------------------------------------------------------------------------------------------------  
'''
Remove duplicate object id in a list(listData) and store
it in finalList
'''
def removeDupl(inputList):
    newList=[]
    for element in inputList:
        if int(element)>30000:
            if element not in newList:
                newList.append(element)
    return newList

#--------------------------------------------------------------------------------------------------------------------------------
def precedingVehicles(data,objCount):
    finalList_new=[]
    velocity=0.0
    with open(inputFile,'r') as f:
        rows = csv.reader(f)
        for row in rows:
            if(row[objCount]==data):
                velocity=row[objCount+totalObjects*4]
                if(float(velocity)>0.0):
                    jvalue.append(row[objCount+totalObjects*4])
                    return 1               
            
#--------------------------------------------------------------------------------------------------------------------------------
def csvToDat():
    srcdir='C:\CSV'
    dstdir='C:\Dat files'

    directory = os.path.dirname(dstdir)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)       
  

    csvFilenames=[]
    for basename in os.listdir(srcdir):
        if basename.endswith('.csv'):
            pathname = os.path.join(srcdir, basename)
            if os.path.isfile(pathname):
                shutil.copy2(pathname, dstdir)
                csvFilenames.append(dstdir+'\\'+basename)

    for thisFile in csvFilenames:
        print thisFile
        base = os.path.splitext(thisFile)[0]
        os.rename(thisFile, base + ".dat")

    print 'Dat File Generated.'    
            
#--------------------------------------------------------------------------------------------------------------------------------  
'''
Fetching unique data from each column of objId's and storing it
in a list(listData)
'''
def myFunction(n):
    cnt=0
    flagCount=0
    with open(inputFile,'r') as f:
        rows = csv.reader(f)
        for row in rows:
            flag=1
            if(cnt!=0 and n<totalObjects+3):
                temp=row[n]  # Only print the column in the row
                if(cnt==1):
                    listData.append(temp)
                for i in range(0,len(listData)):
                    if(temp==listData[i]):
                        flag=0
                if(flag==1):
                    listData.append(temp)
            cnt=cnt+1       

#--------------------------------------------------------------------------------------------------------------------------------
'''
fetch the frame number and properties of particular objectID 
'''
def frameCounting(objCount,key):
    frame=0
    cnt=0
    temp=0
    name=str(key)
    global xValue
    global yValue
    #print 'totalObjects+3:- ',totalObjects+3
    with open(inputFile) as f:
            rows1 = csv.reader(f)
            for row in rows1:
                if(cnt!=0 and objCount<totalObjects+3):
                    frame=frame+1 
                    #print 'totalObjects+3:- ',totalObjects+3
                    temp=row[objCount]
                    if(temp==key):
                     
                        frameList.append(frame)
                        positionXList.append(float("{0:.4f}".format(float(row[objCount+totalObjects*1]))))
                        xValue=float("{0:.4f}".format(float(row[objCount+totalObjects*1])))
                        
                        positionYList.append(float("{0:.4f}".format(float(row[objCount+totalObjects*2]))))
                        yValue=float("{0:.4f}".format(float(row[objCount+totalObjects*2])))
                        
                        obsVelXList.append(float("{0:.4f}".format(float(row[objCount+totalObjects*4]))))
                        obsVelYList.append(float("{0:.4f}".format(float(row[objCount+totalObjects*5]))))
                              
                cnt=cnt+1
    print frame
    return frame
#--------------------------------------------------------------------------------------------------------------------------------
def replaceZero():
    value=0
    
    for data in range(0,len(positionXList)):
        value=float(positionXList[data])
        if(value!=0.0):
            break
        else:
            for i in range(0,len(positionXList)):
                if(float(positionXList[i])!=0.0):
                    positionXList[data]=positionXList[i]
                    break
                 


    for data in range(0,len(positionYList)):
        value=float(positionYList[data])
        if(value!=0.0):
            break
        else:
            for i in range(1,len(positionYList)):
                if(float(positionYList[i])!=0.0):
                    positionYList[data]=positionYList[i]
                    break   

             
#--------------------------------------------------------------------------------------------------------------------------------
def sortData(frame):
    flag=0
    temp=0
    
    for i in range(1,frame+1):
        for j in range(0,len(frameList)):
            if(i==int(frameList[j])):
                flag=1
                break
            else:
                flag=0
            
        if(flag!=1):
            frameList.append(i)
            positionXList.append(0.0)
            positionYList.append(0.0)
            obsVelXList.append(0.0)
            obsVelYList.append(0.0)


    for passnum in range(len(frameList)-1,0,-1):
        for i in range(passnum):
            if frameList[i]>frameList[i+1]:
                temp = frameList[i]
                frameList[i] = frameList[i+1]
                frameList[i+1] = temp

                temp = positionXList[i]
                positionXList[i] = positionXList[i+1]
                positionXList[i+1] = temp

                temp = positionYList[i]
                positionYList[i] = positionYList[i+1]
                positionYList[i+1] = temp

                temp = obsVelXList[i]
                obsVelXList[i] = obsVelXList[i+1]
                obsVelXList[i+1] = temp

                temp = obsVelYList[i]
                obsVelYList[i] = obsVelYList[i+1]
                obsVelYList[i+1] = temp
                
    for mydata in range(0, len(positionXList)-1):
        if(int(positionXList[mydata+1])==0):
            positionXList[mydata+1]=positionXList[mydata]

    for mydata in range(0, len(positionYList)-1):
        if(int(positionYList[mydata+1])==0):
            positionYList[mydata+1]=positionYList[mydata]
#--------------------------------------------------------------------------------------------------------------------------------
#exceution of program starts from main        
if __name__=='__main__':
    
    
    #declartion of local variables
    frame=0
    cnt=0
    temp=0
    name=0
    totalObjects=0
    mylist1=[]
    frameEgoList=[]
    #Building GUI using Tkinter library
    master = Tk()                                               #initializing the Tkinter                                                                            
    master.title("Working With CSV")                            #setting up window title
    Label(master, text="Input Filename",width=12).grid(row=0)   #positioning a label widget in a window
    entry_text = Entry(master)                                  #input text box to display name of selected file
    entry_text.grid(row=0, column=1)
    Button(master,text='Select File', command=callback,width =10).grid(row=0,column=2,sticky=E, padx=5,pady=5)#creates a select file button
    Button(master, text = 'START', command=quit).grid(row=1,column=1,sticky=E, padx=5,pady=5)                 #creates a START button
    master.protocol("WM_DELETE_WINDOW", on_closing)             #closes the window when clicked on close button
    master.mainloop()                                           #GUI appearance till end the program/till program terminates
    totalObjects=objectCount()                                  #function call to objectCount and get total number of objects
    ActVelList1=getActualVelocity()
    
    timeCounter=0
    with open(inputFile,'r') as f:
        rows = csv.reader(f)
        for row in rows:
            timeCounter_List.append(timeCounter)
            timeCounter=round(timeCounter+0.2,3)
    
    #iterates till total number of objects
    for i in range(1,totalObjects):
        myFunction(mylen)                                       #calling myFunction
        mylen=mylen+1

    mylist=removeDupl(listData)
    #del mylist
    jvalue=[]
    for i in mylist:
        #print "----------------"
        #print "I:- ",i
        #jvalue.append(i)
        for j in range(3,33):
            #jvalue.append(j)
            
            data=precedingVehicles(i,j)
            if(data==1):
                mylist1.append(i)
                break
        #print ("J-",jvalue)
        #del jvalue
    del mylist
    #print "j-",jvalue
    #print "j length",len(jvalue)
    
    mylist=removeDupl(mylist1)#calling removeDupl function to remove duplicates from listData created earlier and create list(mylist) with unique data
    
    for i in mylist:
        Count=3
        name=str(i)
        print ("List Data:- ",i)
        print 'totalObjects+3',totalObjects+3
        for j in range(3,totalObjects+3):
            frame=frameCounting(Count,i)
            Count=Count+1
        sortData(frame)
        xValue=0
        yValue=0
        replaceZero()
        writeDataToCsv(frameList,name,ActVelList1)
        
        
        del frameList[:]
        del obsVelXList[:]
        del obsVelYList[:]
        del positionXList[:]
        del positionYList[:]
    #frameCounting(3,0)
    for k in range(1,152):
        frameEgoList.append(k)
    EgoWriteDataToCsv(timeCounter_List,totalObjects,3,frameEgoList)
    #csvToDat()
#--------------------------------------------------------------------------------------------------------------------------------      
    
    
                        
    

