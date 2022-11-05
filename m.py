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
    indexing=doctorTable.get_children()
    newlist=[]
    for index in indexing:
        content=doctorTable.item(index)
        datalist=content['values']
        newlist.append(datalist)


    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Qualification','Specialization','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved succesfully')


def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,NameEntry,QualificationEntry,SpecializationEntry,genderEntry,dobEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    NameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    NameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    NameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    NameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    QualificationLabel = Label(screen, text='Qualification', font=('times new roman', 20, 'bold'))
    QualificationLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    QualificationEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    QualificationEntry.grid(row=3, column=1, pady=15, padx=10)

    SpecializationLabel = Label(screen, text='Specialization', font=('times new roman', 20, 'bold'))
    SpecializationLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    SpecializationEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    SpecializationEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    doctor_button = ttk.Button(screen, text=button_text, command=command)
    doctor_button.grid(row=7, columnspan=2, pady=15)
    if title=='Update doctor':
        indexing = doctorTable.focus()

        content = doctorTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        NameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        QualificationEntry.insert(0, listdata[3])
        SpecializationEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])

def update_data():
    query='update doctor set Name=%s,mobile=%s,Qualification=%s,Specialization=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(NameEntry.get(),phoneEntry.get(),QualificationEntry.get(),SpecializationEntry.get(),
                            genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_doctor()



def show_doctor():
    query = 'select * from doctor'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    doctorTable.delete(*doctorTable.get_children())
    for data in fetched_data:
        doctorTable.insert('', END, values=data)

def delete_doctor():
    indexing=doctorTable.focus()
    print(indexing)
    content=doctorTable.item(indexing)
    content_id=content['values'][0]
    query='delete from doctor where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is deleted succesfully')
    query='select * from doctor'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    doctorTable.delete(*doctorTable.get_children())
    for data in fetched_data:
        doctorTable.insert('',END,values=data)


def search_data():
    query='select * from doctor where id=%s or Name=%s or Qualification=%s or mobile=%s or Specialization=%s or gender=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),QualificationEntry.get(),SpecializationEntry.get(),genderEntry.get(),dobEntry.get()))
    doctorTable.delete(*doctorTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        doctorTable.insert('',END,values=data)

def add_data():
    if idEntry.get()=='' or NameEntry.get()=='' or phoneEntry.get()=='' or QualificationEntry.get()=='' or SpecializationEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('Error','All Feilds are required',parent=screen)

    else:
        try:
            query='insert into doctor values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),QualificationEntry.get(),SpecializationEntry.get(),
                                    genderEntry.get(),dobEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=screen)
            if result:
                idEntry.delete(0,END)
                NameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                QualificationEntry.delete(0,END)
                SpecializationEntry.delete(0,END)
                genderEntry.delete(0,END)
                dobEntry.delete(0,END)
                screen.destroy()
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=screen)
            return
        query='select *from doctor'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        doctorTable.delete(*doctorTable.get_children())
        for data in fetched_data:
            doctorTable.insert('',END,values=data)


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
            query='create table doctor(id int not null primary key, Name varchar(30),mobile varchar(10),Qualification varchar(30),' \
                  'Specialization varchar(100),gender varchar(20),dob varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query='use hms'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
        connectWindow.destroy()
        adddoctorButton.config(state=NORMAL)
        searchdoctorButton.config(state=NORMAL)
        updatedoctorButton.config(state=NORMAL)
        showdoctorButton.config(state=NORMAL)
        exportdoctorButton.config(state=NORMAL)
        deletedoctorButton.config(state=NORMAL)
    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
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
root.title('Doctor Management System')
datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=10000)
clock()
s='ADD doctor DETAILS' #s[count]=t when count is 1
sliderLabel=Label(root,font=('times new roman',28,'bold'),width=30)
sliderLabel.place(x=250,y=100000)
slider()

connectButton=ttk.Button(root,text='Connect database',command=connect_database)
connectButton.place(x=80,y=40)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)


adddoctorButton=ttk.Button(leftFrame,text='Add doctor',width=25,state=DISABLED,command=lambda :toplevel_data('Add doctor','Add',add_data))
adddoctorButton.grid(row=1,column=0,pady=20)

searchdoctorButton=ttk.Button(leftFrame,text='Search doctor',width=25,state=DISABLED,command=lambda :toplevel_data('Search doctor','Search',search_data))
searchdoctorButton.grid(row=2,column=0,pady=20)

updatedoctorButton=ttk.Button(leftFrame,text='Update doctor',width=25,state=DISABLED,command=lambda :toplevel_data('Update doctor','Update',update_data))
updatedoctorButton.grid(row=4,column=0,pady=20)

showdoctorButton=ttk.Button(leftFrame,text='Show doctor',width=25,state=DISABLED,command=show_doctor)
showdoctorButton.grid(row=5,column=0,pady=20)

exportdoctorButton=ttk.Button(leftFrame,text='Export data',width=25,state=DISABLED,command=export_data)
exportdoctorButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=0,width=940,height=680)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

doctorTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','Qualification','Specialization','Gender',
                                 'D.O.B','Added Date','Added Time'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=doctorTable.xview)
scrollBarY.config(command=doctorTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

doctorTable.pack(expand=1,fill=BOTH)

doctorTable.heading('Id',text='Id')
doctorTable.heading('Name',text='Name')
doctorTable.heading('Mobile',text='Mobile No')
doctorTable.heading('Qualification',text='Qualification')
doctorTable.heading('Specialization',text='Specialization')
doctorTable.heading('Gender',text='Gender')
doctorTable.heading('D.O.B',text='D.O.B')
doctorTable.heading('Added Date',text='Added Date')
doctorTable.heading('Added Time',text='Added Time')

doctorTable.column('Id',width=50,anchor=CENTER)
doctorTable.column('Name',width=200,anchor=CENTER)
doctorTable.column('Qualification',width=300,anchor=CENTER)
doctorTable.column('Mobile',width=200,anchor=CENTER)
doctorTable.column('Specialization',width=300,anchor=CENTER)
doctorTable.column('Gender',width=100,anchor=CENTER)
doctorTable.column('D.O.B',width=200,anchor=CENTER)
doctorTable.column('Added Date',width=200,anchor=CENTER)
doctorTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40,font=('arial', 12, 'bold'), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='blue')

doctorTable.config(show='headings')

root.mainloop()

