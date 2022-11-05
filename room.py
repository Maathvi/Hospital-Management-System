from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import mysql.connector
import pandas
#functionality Part

def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=roomTable.get_children()
    newlist=[]
    for index in indexing:
        content=roomTable.item(index)
        datalist=content['values']
        newlist.append(datalist)


    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','roomno','RoomType','price','doctor','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved succesfully')

def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,NameEntry,roomnoEntry,RoomTypeEntry,priceEntry,doctorEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Patient Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    NameLabel = Label(screen, text='Patient Name', font=('times new roman', 20, 'bold'))
    NameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    NameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    NameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone No.', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    roomnoLabel = Label(screen, text='Room No.', font=('times new roman', 20, 'bold'))
    roomnoLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    roomnoEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    roomnoEntry.grid(row=3, column=1, pady=15, padx=10)

    RoomTypeLabel = Label(screen, text='Room Type', font=('times new roman', 20, 'bold'))
    RoomTypeLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    RoomTypeEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    RoomTypeEntry.grid(row=4, column=1, pady=15, padx=10)

    priceLabel = Label(screen, text='Price', font=('times new roman', 20, 'bold'))
    priceLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    priceEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    priceEntry.grid(row=5, column=1, pady=15, padx=10)

    doctorLabel = Label(screen, text='Consulting Doctor', font=('times new roman', 20, 'bold'))
    doctorLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    doctorEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    doctorEntry.grid(row=6, column=1, pady=15, padx=10)

    room_button = ttk.Button(screen, text=button_text, command=command)
    room_button.grid(row=7, columnspan=2)
    if title=='Update room':
        indexing = roomTable.focus()

        content = roomTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        NameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        roomnoEntry.insert(0, listdata[3])
        RoomTypeEntry.insert(0, listdata[4])
        priceEntry.insert(0, listdata[5])
        doctorEntry.insert(0, listdata[6])

def update_data():
    query='update room set Name=%s,mobile=%s,roomno=%s,RoomType=%s,price=%s,doctor=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(NameEntry.get(),phoneEntry.get(),roomnoEntry.get(),RoomTypeEntry.get(),
                            priceEntry.get(),doctorEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_room()



def show_room():
    query = 'select * from room'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    roomTable.delete(*roomTable.get_children())
    for data in fetched_data:
        roomTable.insert('', END, values=data)

def search_data():
    query='select * from room where id=%s or Name=%s or roomno=%s or mobile=%s or RoomType=%s or price=%s or doctor=%s'
    mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),roomnoEntry.get(),RoomTypeEntry.get(),priceEntry.get(),doctorEntry.get()))
    roomTable.delete(*roomTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        roomTable.insert('',END,values=data)

def add_data():
    if idEntry.get()=='' or NameEntry.get()=='' or phoneEntry.get()=='' or roomnoEntry.get()=='' or RoomTypeEntry.get()=='' or priceEntry.get()=='' or doctorEntry.get()=='':
        messagebox.showerror('Error','All Feilds are required',parent=screen)

    else:
        try:
            query='insert into room values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),roomnoEntry.get(),RoomTypeEntry.get(),
                                    priceEntry.get(),doctorEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=screen)
            if result:
                idEntry.delete(0,END)
                NameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                roomnoEntry.delete(0,END)
                RoomTypeEntry.delete(0,END)
                priceEntry.delete(0,END)
                doctorEntry.delete(0,END)
                screen.destroy()
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=screen)
            return
        query='select *from room'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        roomTable.delete(*roomTable.get_children())
        for data in fetched_data:
            roomTable.insert('',END,values=data)


def connect_database():
    def connect():
        global mycursor,con
        try:
            con=mysql.connector.connect(host='localhost',user='root',password='')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return

        try:
            query='use hms'
            mycursor.execute(query)
            query='create table room(id int not null primary key, Name varchar(30),mobile varchar(10),roomno varchar(30),' \
                  'RoomType varchar(100),price varchar(20),doctor varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query='use hms'
            mycursor.execute(query)
        connectWindow.destroy()
        addroomButton.config(state=NORMAL)
        searchroomButton.config(state=NORMAL)
        updateroomButton.config(state=NORMAL)
        showroomButton.config(state=NORMAL)
        exportroomButton.config(state=NORMAL)
    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='HostName',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='UserName', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)

def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)



#GUI Part
root=ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('breeze')

root.geometry('1310x680+230+95')
root.resizable(0,0)
root.title('room Management System')
datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=10000)
clock()

connectButton=ttk.Button(root,text='Connect database',command=connect_database)
connectButton.place(x=80,y=40)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)


addroomButton=ttk.Button(leftFrame,text='Allot room',width=25,state=DISABLED,command=lambda :toplevel_data('Add room','Add',add_data))
addroomButton.grid(row=1,column=0,pady=20)

searchroomButton=ttk.Button(leftFrame,text='Search room',width=25,state=DISABLED,command=lambda :toplevel_data('Search room','Search',search_data))
searchroomButton.grid(row=2,column=0,pady=20)


updateroomButton=ttk.Button(leftFrame,text='Update room',width=25,state=DISABLED,command=lambda :toplevel_data('Update room','Update',update_data))
updateroomButton.grid(row=4,column=0,pady=20)

showroomButton=ttk.Button(leftFrame,text='Show room',width=25,state=DISABLED,command=show_room)
showroomButton.grid(row=5,column=0,pady=20)

exportroomButton=ttk.Button(leftFrame,text='Export data',width=25,state=DISABLED,command=export_data)
exportroomButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=0,width=940,height=680)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

roomTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','roomno','RoomType','price',
                                 'D.O.B','Added Date','Added Time'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=roomTable.xview)
scrollBarY.config(command=roomTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

roomTable.pack(expand=1,fill=BOTH)

roomTable.heading('Id',text='Id')
roomTable.heading('Name',text='Name')
roomTable.heading('Mobile',text='Mobile No')
roomTable.heading('roomno',text='Room No.')
roomTable.heading('RoomType',text='RoomType')
roomTable.heading('price',text='Price')
roomTable.heading('D.O.B',text='Doctor')
roomTable.heading('Added Date',text='Added Date')
roomTable.heading('Added Time',text='Added Time')

roomTable.column('Id',width=50,anchor=CENTER)
roomTable.column('Name',width=200,anchor=CENTER)
roomTable.column('roomno',width=100,anchor=CENTER)
roomTable.column('Mobile',width=200,anchor=CENTER)
roomTable.column('RoomType',width=300,anchor=CENTER)
roomTable.column('price',width=100,anchor=CENTER)
roomTable.column('D.O.B',width=200,anchor=CENTER)
roomTable.column('Added Date',width=200,anchor=CENTER)
roomTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40,font=('arial', 12, 'bold'), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='blue')

roomTable.config(show='headings')

root.mainloop()