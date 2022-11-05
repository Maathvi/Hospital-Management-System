from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import mysql.connector
import pandas



def add_patient():
    import h

def add_doctor():
    import m

def exit():
    if messagebox.askyesno('Exit','Do you really want to exit'):
        root.destroy()

def add_bill():
    import bill


def add_room():
    import room

count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

def clock():
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'    DATE: {date}\nTIME: {currenttime}')
    datetimeLabel.after(1000,clock)

root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1550x800+0+0')
root.resizable(0,0)
root.title('Hospital Management System')
root.configure(background='black')

datetimeLabel=Label(root,bg="black",fg="white",font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()

s='SATHYABAMA GENERAL HOSPITAL'
sliderLabel=Label(root,bg="black",fg="white",text=s,font=('times new roman',28,'bold'),width=30)
sliderLabel.place(x=420,y=10)
slider()

img1=Image.open(r"C:\project\hospital.jpg")
img1=img1.resize((1550,750),Image.ANTIALIAS)
photoimg1=ImageTk.PhotoImage(img1)

lbling=Label(root,image=photoimg1,bd=4,relief=RIDGE)
lbling.place(x=225,y=60,width=1310,height=750)

btn_frame=Frame(root,bd=4,relief=RIDGE)
btn_frame.place(x=0,y=60,width=229,height=890)

img2=Image.open(r"C:\project\sathyabama.jpg")
img2=img2.resize((215,100),Image.ANTIALIAS)
photoimg2=ImageTk.PhotoImage(img2)

lbling=Label(btn_frame,image=photoimg2,bd=4,relief=RIDGE)
lbling.grid(row=2,column=0)


patient_btn=Button(btn_frame,text=" ADD PATIENT",font=("times new roman",20,"bold"),bg="black",fg="white",bd=4,relief=RIDGE,command=add_patient)
patient_btn.grid(row=6,column=0)

doctor_btn=Button(btn_frame,text=" ADD DOCTOR",font=("times new roman",20,"bold"),bg="black",fg="white",bd=4,relief=RIDGE,command=add_doctor)
doctor_btn.grid(row=8,column=0)

billing_btn=Button(btn_frame,text="    BILLING       ",font=("times new roman",20,"bold"),bg="black",fg="white",bd=4,relief=RIDGE,command=add_bill)
billing_btn.grid(row=10,column=0)

room_btn=Button(btn_frame,text=" ALLOT ROOM",font=("times new roman",20,"bold"),bg="black",fg="white",bd=4,relief=RIDGE,command=add_room)
room_btn.grid(row=12,column=0)

exit_btn=Button(btn_frame,text="       EXIT           ",font=("times new roman",20,"bold"),bg="black",fg="white",bd=4,relief=RIDGE,command=exit)
exit_btn.grid(row=22,column=0)

img3=Image.open(r"C:\project\hospital1.jpg")
img3=img3.resize((215,160),Image.ANTIALIAS)
photoimg3=ImageTk.PhotoImage(img3)

lbling=Label(btn_frame,image=photoimg3,bd=4,relief=RIDGE)
lbling.grid(row=14,column=0)

img4=Image.open(r"C:\project\hospital0.png")
img4=img4.resize((215,160),Image.ANTIALIAS)
photoimg4=ImageTk.PhotoImage(img4)

lbling=Label(btn_frame,image=photoimg4,bd=4,relief=RIDGE)
lbling.grid(row=18,column=0)




















root.mainloop()

