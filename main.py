# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition
import pickle
import time
import os
import sqlite3
from datetime import datetime

cameraSel=0
pickleFileLoc="faceModel.pickle"
detectionModel="hog"

print("[INFO] program started...")
print("[INFO] loading encodings...")
data = pickle.loads(open(pickleFileLoc, "rb").read())

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("500x400")

#DataBase

#Create or Connect to a Database
conn = sqlite3.connect('students_book.db')

#Create cursor
c = conn.cursor()

# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=0, column=0)
cap=cv2.VideoCapture(cameraSel)

def Display(ID):
    rootI = Tk()
    rootI.title('IT')
    rootI.geometry("500x400")
    
    
    #Create or Connect to a Database
    conn = sqlite3.connect('students_book.db')

    #Create cursor
    c = conn.cursor()
    
    #Query the database
    c.execute("SELECT * FROM students WHERE oid =" + str(ID))
    records = c.fetchall()
    
    #Loop Thru Results
    fname_records= ''
    lname_records= ''
    email_records= ''
    departement_records= ''
    for record in records:
        fname_records += str(record[0]) #+ "\n"
        lname_records += str(record[1])
        email_records += str(record[2])
        departement_records += str(record[3])
        file = write_file(record[4],"image.jpg")
        #photo = cv2.imread("image.jpg")
        #print(photo)
        #plt.imshow(photo)
        #plt.show()
    
    #query_label = Label(root, text=print_records)
    #query_label.grid(row=8, column=0, columnspan=2)

    #Create Text Box Labels
    f_name_label = Label(rootI, text="Fist Name")
    f_name_label.grid(row=3, column=0)
    query_label = Label(rootI, text=fname_records)
    query_label.grid(row=3, column=1, columnspan=2)

    l_name_label = Label(rootI, text="Last Name")
    l_name_label.grid(row=5, column=0)
    query_label = Label(rootI, text=lname_records)
    query_label.grid(row=5, column=1, columnspan=2)

    email_label = Label(rootI, text="Email")
    email_label.grid(row=7, column=0)
    query_label = Label(rootI, text=email_records)
    query_label.grid(row=7, column=1, columnspan=2)

    departement_label = Label(rootI, text="Departement")
    departement_label.grid(row=9, column=0)
    query_label = Label(rootI, text=departement_records)
    query_label.grid(row=9, column=1, columnspan=2)
    
    
    global photo
    image = Image.open("image.jpg")
    image = image.resize((100,100))
    photo = ImageTk.PhotoImage(image,master=rootI)
    c = Label(rootI,image=photo)
    c.grid(row=1, column=1)

    # Convert image to PhotoImage

    #queryI.place(x=0, y=0)
    # Repeat after an interval to capture continiously
    #label.after(20, show_frames)
    #Commit changes
    conn.commit()

    #Close Connection
    conn.close()

    rootI.after(5000,lambda:rootI.destroy())
    #Automatically close the window after 5 seconds


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
def ADD():
    root = Tk()
    root.title('IT')
    root.geometry("400x200")


    #DataBase

    #Create or Connect to a Database
    conn = sqlite3.connect('students_book.db')

    #Create cursor
    c = conn.cursor()
    
    #Create Submit Fuction For Attendance list
    def submit():
        markAttendance(f_name.get())



        #Clear The Text Boxes
        f_name.delete(0, END)
        l_name.delete(0, END)
        email.delete(0, END)
        

    #Create Text Boxes
    f_name = Entry(root, width=30)
    f_name.grid(row=0, column=1, padx=20)

    l_name = Entry(root, width=30)
    l_name.grid(row=1, column=1)

    email = Entry(root, width=30)
    email.grid(row=2, column=1)

    #Create Text Box Labels
    f_name_label = Label(root, text="Fist Name")
    f_name_label.grid(row=0, column=0)

    l_name_label = Label(root, text="Last Name")
    l_name_label.grid(row=1, column=0)

    email_label = Label(root, text="Email")
    email_label.grid(row=2, column=0)

    #Create Submit Botton
    submit_btn = Button(root, text="Add to Attendence List", command=submit)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


    #Commit changes
    conn.commit()

    #Close Connection
    conn.close()
    

#this fonction will help keep track of attendence by marking the name and a date into an excel file
def markAttendance(name):
    with open('AttendaceLog.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            name=name.upper()
#REPLACE THE NAME AND ID :
            if(name =="NAME"):
                Display(ID)


# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   rgb= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   rgb = cv2.resize(rgb,(0,0),None,0.25,0.25)
   img = Image.fromarray(rgb)
   
   #sami print("[INFO] recognizing faces...")
   boxes = face_recognition.face_locations(rgb,
											model=detectionModel)
   encodings = face_recognition.face_encodings(rgb, boxes)
   names = []
   for encoding in encodings:
       matches = face_recognition.compare_faces(data["encodings"],
												encoding)
       
       faceDis = face_recognition.face_distance(data["encodings"],
												encoding)
       
       name = "Unknown"
       if True in matches:
           matchedIdxs = [i for (i, b) in enumerate(matches) if b]
           counts = {}
           for i in matchedIdxs:
               name = data["names"][i]
               counts[name] = counts.get(name, 0) + 1
           name = max(counts, key=counts.get)
           
       if(min(faceDis>0.5)):
           name = "Unknown"
       else:
           name = name
           names.append(name)
           markAttendance(name)
       print("The Person is : " + name)
       
       
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)
   

f_name_label = Label(win, text="IF YOU ARE NOT A PART OF THIS CLASS")
f_name_label.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

f_name_label = Label(win, text="------------------------------------")
f_name_label.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

Add_btn = Button(win, text="Register", command=ADD)
Add_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

show_frames()

#Commit changes
conn.commit()

#Close Connection
conn.close()

win.mainloop()
