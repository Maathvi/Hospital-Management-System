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
    indexing=billTable.get_children()
    newlist=[]
    for index in indexing:
        content=billTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Doc_charges','Room_charges','Medicine','Total','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved succesfully')


def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,NameEntry,Doc_chargesEntry,Room_chargesEntry,MedicineEntry,TotalEntry,screen
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

    Doc_chargesLabel = Label(screen, text='Doctor Charges', font=('times new roman', 20, 'bold'))
    Doc_chargesLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    Doc_chargesEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    Doc_chargesEntry.grid(row=3, column=1, pady=15, padx=10)

    Room_chargesLabel = Label(screen, text='Room Charges', font=('times new roman', 20, 'bold'))
    Room_chargesLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    Room_chargesEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    Room_chargesEntry.grid(row=4, column=1, pady=15, padx=10)

    MedicineLabel = Label(screen, text='Medicine Cost', font=('times new roman', 20, 'bold'))
    MedicineLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    MedicineEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    MedicineEntry.grid(row=5, column=1, pady=15, padx=10)

    TotalLabel = Label(screen, text='Total', font=('times new roman', 20, 'bold'))
    TotalLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    TotalEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    TotalEntry.grid(row=6, column=1, pady=15, padx=10)

    total_button = ttk.Button(screen, text=button_text, command=command)
    total_button.grid(row=7,columnspan=2)

    if title=='Update bill':
        indexing = billTable.focus()

        content = billTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        NameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        Doc_chargesEntry.insert(0, listdata[3])
        Room_chargesEntry.insert(0, listdata[4])
        MedicineEntry.insert(0, listdata[5])
        TotalEntry.insert(0, listdata[6])

def update_data():
    query='update bill set Name=%s,mobile=%s,Doc_charges=%s,Room_charges=%s,Medicine=%s,Total=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(NameEntry.get(),phoneEntry.get(),Doc_chargesEntry.get(),Room_chargesEntry.get(),
                            MedicineEntry.get(),TotalEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_bill()



def show_bill():
    query = 'select * from bill'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    billTable.delete(*billTable.get_children())
    for data in fetched_data:
        billTable.insert('', END, values=data)

def search_data():
    query='select * from bill where id=%s or Name=%s or Doc_charges=%s or mobile=%s or Room_charges=%s or Medicine=%s or Total=%s'
    mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),Doc_chargesEntry.get(),Room_chargesEntry.get(),MedicineEntry.get(),TotalEntry.get()))
    billTable.delete(*billTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        billTable.insert('',END,values=data)

def add_data():
    if idEntry.get()=='' or NameEntry.get()=='' or phoneEntry.get()=='' or Doc_chargesEntry.get()=='' or Room_chargesEntry.get()=='' or MedicineEntry.get()=='' or TotalEntry.get()=='':
        messagebox.showerror('Error','All Feilds are required',parent=screen)

    else:
        try:
            query='insert into bill values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),NameEntry.get(),phoneEntry.get(),Doc_chargesEntry.get(),Room_chargesEntry.get(),
                                    MedicineEntry.get(),TotalEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=screen)
            if result:
                idEntry.delete(0,END)
                NameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                Doc_chargesEntry.delete(0,END)
                Room_chargesEntry.delete(0,END)
                MedicineEntry.delete(0,END)
                TotalEntry.delete(0,END)
                screen.destroy()
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=screen)
            return
        query='select *from bill'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        billTable.delete(*billTable.get_children())
        for data in fetched_data:
            billTable.insert('',END,values=data)


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
            query='create table bill(id int not null primary key, Name varchar(30),mobile varchar(10),Doc_charges varchar(30),' \
                  'Room_charges varchar(100),Medicine varchar(20),Total varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query='use hms'
            mycursor.execute(query)
        connectWindow.destroy()
        addbillButton.config(state=NORMAL)
        searchbillButton.config(state=NORMAL)
        updatebillButton.config(state=NORMAL)
        showbillButton.config(state=NORMAL)
        exportbillButton.config(state=NORMAL)
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
root.title('Bill Management System')
datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=10000)
clock()

connectButton=ttk.Button(root,text='Connect database',command=connect_database)
connectButton.place(x=80,y=40)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)


addbillButton=ttk.Button(leftFrame,text='New bill',width=25,state=DISABLED,command=lambda :toplevel_data('Add bill','Add',add_data))
addbillButton.grid(row=1,column=0,pady=20)

searchbillButton=ttk.Button(leftFrame,text='Search bill',width=25,state=DISABLED,command=lambda :toplevel_data('Search bill','Search',search_data))
searchbillButton.grid(row=2,column=0,pady=20)


updatebillButton=ttk.Button(leftFrame,text='Update bill',width=25,state=DISABLED,command=lambda :toplevel_data('Update bill','Update',update_data))
updatebillButton.grid(row=4,column=0,pady=20)

showbillButton=ttk.Button(leftFrame,text='Show Billing Details',width=25,state=DISABLED,command=show_bill)
showbillButton.grid(row=5,column=0,pady=20)

exportbillButton=ttk.Button(leftFrame,text='Export data',width=25,state=DISABLED,command=export_data)
exportbillButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=0,width=940,height=680)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

billTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','Doc_charges','Room_charges','Medicine',
                                 'D.O.B','Added Date','Added Time'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=billTable.xview)
scrollBarY.config(command=billTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

billTable.pack(expand=1,fill=BOTH)

billTable.heading('Id',text='Id')
billTable.heading('Name',text='Name')
billTable.heading('Mobile',text='Mobile No')
billTable.heading('Doc_charges',text='Doctor Charges')
billTable.heading('Room_charges',text='Room Charges')
billTable.heading('Medicine',text='Medicine Cost')
billTable.heading('D.O.B',text='Total')
billTable.heading('Added Date',text='Added Date')
billTable.heading('Added Time',text='Added Time')

billTable.column('Id',width=50,anchor=CENTER)
billTable.column('Name',width=200,anchor=CENTER)
billTable.column('Doc_charges',width=200,anchor=CENTER)
billTable.column('Mobile',width=200,anchor=CENTER)
billTable.column('Room_charges',width=200,anchor=CENTER)
billTable.column('Medicine',width=200,anchor=CENTER)
billTable.column('D.O.B',width=200,anchor=CENTER)
billTable.column('Added Date',width=200,anchor=CENTER)
billTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview', rowheight=40,font=('arial', 12, 'bold'), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='blue')

billTable.config(show='headings')

root.mainloop()