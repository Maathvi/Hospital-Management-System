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
    indexing=patientTable.get_children()
    newlist=[]
    for index in indexing:
        content=patientTable.item(index)
        datalist=content['values']
        newlist.append(datalist)


    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','bloodgroup','Address','appointment','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved succesfully')


def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,NameEntry,bloodgroupEntry,addressEntry,appointmentEntry,dobEntry,screen
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

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    bloodgroupLabel = Label(screen, text='Bloodgroup', font=('times new roman', 20, 'bold'))
    bloodgroupLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    bloodgroupEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    bloodgroupEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    appointmentLabel = Label(screen, text='Type of Appointment', font=('times new roman', 20, 'bold'))
    appointmentLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    appointmentEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    appointmentEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    patient_button = ttk.Button(screen, text=button_text, command=command)
    patient_button.grid(row=7, columnspan=2, pady=15)
    if title=='Update patient':
        indexing = patientTable.focus()

        content = patientTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        NameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        bloodgroupEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        appointmentEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

def update_data():
    query='update patient set Name=%s,mobile=%s,bloodgroup=%s,address=%s,appointment=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(NameEntry.get(),phoneEntry.get(),bloodgroupEntry.get(),addressEntry.get(),
                            appointmentEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_patient()



def show_patient():
    query = 'select * from patient'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    patientTable.delete(*patientTable.get_children())
    for data in fetched_data:
        patientTable.insert('', END, values=data)

def search_data():
    query='select * from patient where id=%s or Name=%s or bloodgroup=%s or mobile=%s or address=%s or appointment=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),bloodgroupEntry.get(),addressEntry.get(),appointmentEntry.get(),dobEntry.get()))
    patientTable.delete(*patientTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        patientTable.insert('',END,values=data)

def add_data():
    if idEntry.get()=='' or NameEntry.get()=='' or phoneEntry.get()=='' or bloodgroupEntry.get()=='' or addressEntry.get()=='' or appointmentEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('Error','All Feilds are required',parent=screen)
        
    else:
        try:
            query='insert into patient values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),bloodgroupEntry.get(),addressEntry.get(),
                                    appointmentEntry.get(),dobEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=screen)
            if result:
                idEntry.delete(0,END)
                NameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                bloodgroupEntry.delete(0,END)
                addressEntry.delete(0,END)
                appointmentEntry.delete(0,END)
                dobEntry.delete(0,END)
                screen.destroy()
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=screen)
            return
        query='select *from patient'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        patientTable.delete(*patientTable.get_children())
        for data in fetched_data:
            patientTable.insert('',END,values=data)
        

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
            query='create table patient(id int not null primary key, Name varchar(30),mobile varchar(10),bloodgroup varchar(30),' \
                  'address varchar(100),appointment varchar(20),dob varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query='use hms'
            mycursor.execute(query)
        connectWindow.destroy()
        addpatientButton.config(state=NORMAL)
        searchpatientButton.config(state=NORMAL)
        updatepatientButton.config(state=NORMAL)
        showpatientButton.config(state=NORMAL)
        exportpatientButton.config(state=NORMAL)
        deletepatientButton.config(state=NORMAL)
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

count=0
text=''
def slider():
    global text,count

    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)




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
root.title('patient Management System')
datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=10000)
clock()
s='ADD PATIENT DETAILS' #s[count]=t when count is 1
sliderLabel=Label(root,font=('times new roman',28,'bold'),width=30)
sliderLabel.place(x=250,y=100000)
slider()

connectButton=ttk.Button(root,text='Connect database',command=connect_database)
connectButton.place(x=80,y=40)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)


addpatientButton=ttk.Button(leftFrame,text='Add patient',width=25,state=DISABLED,command=lambda :toplevel_data('Add patient','Add',add_data))
addpatientButton.grid(row=1,column=0,pady=20)

searchpatientButton=ttk.Button(leftFrame,text='Search patient',width=25,state=DISABLED,command=lambda :toplevel_data('Search patient','Search',search_data))
searchpatientButton.grid(row=2,column=0,pady=20)


updatepatientButton=ttk.Button(leftFrame,text='Update patient',width=25,state=DISABLED,command=lambda :toplevel_data('Update patient','Update',update_data))
updatepatientButton.grid(row=4,column=0,pady=20)

showpatientButton=ttk.Button(leftFrame,text='Show patient',width=25,state=DISABLED,command=show_patient)
showpatientButton.grid(row=5,column=0,pady=20)

exportpatientButton=ttk.Button(leftFrame,text='Export data',width=25,state=DISABLED,command=export_data)
exportpatientButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=0,width=940,height=680)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

patientTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','bloodgroup','Address','appointment',
                                 'D.O.B','Added Date','Added Time'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=patientTable.xview)
scrollBarY.config(command=patientTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

patientTable.pack(expand=1,fill=BOTH)

patientTable.heading('Id',text='Id')
patientTable.heading('Name',text='Name')
patientTable.heading('Mobile',text='Mobile No')
patientTable.heading('bloodgroup',text='BG')
patientTable.heading('Address',text='Address')
patientTable.heading('appointment',text='appointment')
patientTable.heading('D.O.B',text='D.O.B')
patientTable.heading('Added Date',text='Added Date')
patientTable.heading('Added Time',text='Added Time')

patientTable.column('Id',width=50,anchor=CENTER)
patientTable.column('Name',width=200,anchor=CENTER)
patientTable.column('bloodgroup',width=50,anchor=CENTER)
patientTable.column('Mobile',width=200,anchor=CENTER)
patientTable.column('Address',width=300,anchor=CENTER)
patientTable.column('appointment',width=200,anchor=CENTER)
patientTable.column('D.O.B',width=200,anchor=CENTER)
patientTable.column('Added Date',width=200,anchor=CENTER)
patientTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40,font=('arial', 12, 'bold'), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='blue')

patientTable.config(show='headings')

root.mainloop()

