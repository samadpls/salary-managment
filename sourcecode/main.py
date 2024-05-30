from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from time import sleep
import tkinter
import re
from docxtpl import DocxTemplate #to make a word file
from docx2pdf import convert #to converr into pdf (pip install docx2pdf)
from pdf2image import convert_from_path #to convert into image from pdf (pip install pdf2image, downlode Poppler for Windows)
import os #to remove unwanted file
import pywhatkit
import datetime
import random
from PIL import Image, ImageTk



class Salaryslip:
    '''
    generating salary slip
    '''
    def __init__(self,name,num,cnic,service,salary):
        self.name=name
        self.number=str(num)
        self.cnic=cnic
        self.service=service
        self.salary=int(salary)
        
        
        self.calculation()
        

    def mainscreen(self):
        self.window4=Toplevel() 
        self.window4.title('Salary Slip')
        #925x500 is size , 300+200 is postion on screen 
        self.window4.geometry('925x500+300+200')
        self.window4.configure(bg='#FDF0D5')
        self.window4.resizable(0,0)
        
        whatsapp=Button(self.window4,text='send  to whatsapp',bg='#780000',fg='white',font=('verdena',12,'bold'),border=0,command=self.whatsapp)
        whatsapp.place(x=480,y=400)
        
    def calculation(self):
        self.basic=self.salary//2
        self.home_rent=round(self.basic*0.45)
        self.utility=round(self.basic*0.15)
        self.convence=round(self.basic*0.20)
        self.special_al=round(self.basic*0.10)
        self.amount=round(self.home_rent+self.utility+self.convence+self.special_al)
        self.tax=round(self.salary-(self.amount+self.basic))
        self.total=round(self.basic+self.amount)
        
        
        self.creating()
        
    #creating  file
    def creating(self):
        
        #making word file
        now =datetime.datetime.now()
        date=f'{now.day}/{now.month}/{now.year}'
        filename=f'salaryslip#{random.randint(100,999)}.docx'

        doc=DocxTemplate('salarysliptemp.docx')
        context={'Emp_name':self.name,
        'Emp_service':self.service,
        'slip_date':date,
        'basic':self.basic,
        'house_rent':self.home_rent,
        'utility':self.utility,
        'conv':self.convence,
        'special':self.special_al,
        'tax':self.tax,
        'total':self.total
        }
        doc.render(context)
        doc.save(filename) 
        #converting into pdf
        pdf_file=filename.replace('.docx',".pdf")
        convert(filename)
        #converting into image form
        self.imageslip=filename.replace('.docx','.png')
        
        pages= convert_from_path(pdf_file,poppler_path=r"poppler-0.68.0\\bin")
        #it take argumnet in list
        pages[0].save(self.imageslip, 'PNG')

        
        os.remove(filename)
        self.mainscreen()
        
        os.remove(pdf_file)
        
        #adding images
        logo=PhotoImage(file='images/logo.png')
        Label(self.window4,image=logo,bg='#FDF0D5').place(x=0,y=0)

        img1=PhotoImage(file='images/last.png')
        Label(self.window4,image=img1,bg='#FDF0D5').place(x=60,y=100)
        preview=Label(self.window4,text='Preview',fg='#780000',bg='#FDF0D5',font=('Helvetica',24,'bold'))
        preview.place(x=470,y=5)
        #image resizing
        image = Image.open(self.imageslip) 
        resize_image = image.resize((300, 300))
        img2 = ImageTk.PhotoImage(resize_image)
        Label(self.window4,image=img2,bg='#FDF0D5').place(x=450,y=100) 

        
        
        self.window4.mainloop()
        #self.whatsapp()
    def whatsapp(self):    
        number='+92'+self.number[1:]
        captin=f'{self.name} we have sent you the salary slip of this month. Reply as soon as you receive'
        pywhatkit.sendwhats_image(number,self.imageslip,caption=captin)
#p=Salaryslip("appi",'033311766',87777,7777877,88787)
class Employeeinfo:
    def __init__(self):
        '''set the employee data and saving it in sqlite3 
        '''
        self.Emp_name=''
        self.number=0
        self.service=''
        self.salary=0
        self.cnic=''
        self.gender=''

        self.window=Tk()
        # self.window.iconbitmap('icon.ico') // commit it this cause error
        self.mainscreen()
    def mainscreen(self):
        self.window.title('Employee info')
        self.window.geometry('925x500+300+200')
        self.window.configure(bg='#FDF0D5')
        self.window.resizable(0,0)
        img1=PhotoImage(file=r'images/addmember.png')
        Label(self.window,image=img1,bg='#FDF0D5').place(x=60,y=100)
        logo=PhotoImage(file='images/logo.png')
        Label(self.window,image=logo,bg='#FDF0D5').place(x=0,y=0)
        self.sub_section()

    def sub_section(self):
        self.frame=Frame(self.window, width=450, height=480,bg='#FDF0D5')
        self.frame.place(x=480,y=70)
        self.heading=self.heading=Label(self.frame,text='Employee Data',fg='#540B0E',bg='#FDF0D5',font=('verdena',24,'bold'))
        self.heading.place(x=25,y=-5)

        #employee name
        self.Emp_name=Entry(self.frame,width=25,fg='black',border=0,bg='#FDF0D5',font=('verdena',12))
        self.Emp_name.place(x=30,y=55)
        self.Emp_name.insert(0,'Employee Name')
        self.Emp_name.bind('<FocusIn>',(lambda x:self.Emp_name.delete(0,END) ))
        name=self.Emp_name.get()
        #self.Emp_name.insert(0,"Employee Name")
        self.Emp_name.bind('<FocusOut>', self.name_leave)
        Frame(self.frame,width=175,height=1,bg='#C1121F').place(x=30,y=80)

        #employee phonenumber
        self.number=Entry(self.frame,width=25,fg='black',border=0,bg='#FDF0D5',font=('verdena',12))
        self.number.place(x=30,y=95)
        self.number.insert(0,'Employee  Phone Number')
        self.number.bind('<FocusIn>',lambda x:self.number.delete(0,END) )
        
        self.number.bind('<FocusOut>',self.num_leave)
        Frame(self.frame,width=175,height=1,bg='#C1121F').place(x=30,y=122)
        #employee gender
        i = IntVar() #Basically Links Any Radiobutton With The Variable=i.
        self.r1 = Radiobutton(self.frame, text="Male", value='male', variable=i,border=0,bg='#FDF0D5',font=('verdena',12)).place(x=30,y=255)
        self.r2 = Radiobutton(self.frame, text="Female", value='female', variable=i,border=0,bg='#FDF0D5',font=('verdena',12)).place(x=30,y=280)
        if self.r1=='male':
            self.gender='male'
        else:
            self.gender='female'
        #Employee service in Software house
        
        services=['WEB DEVELOPER','MOBILE APP DEVELOPER','DIGITAL MARKETING',
               'WEB & GRAPHIC DESIGN','FRONT-END DEVELOPER','BACK-END DEVELOPER','FULL STACK DEVELOPER']  
        self.click=StringVar()
        self.click.set('Employee Service')
        self.drop=OptionMenu(self.frame,self.click,*services,command=self.selected)
        
        self.drop.config(bg="#FDF0D5", fg="black",border=0,font=('verdena',10))
        self.drop['menu'].config(bg="#FDF0D5", fg="black",border=0,font=('verdena',10))
        self.drop.place(x=30,y=130)
        Frame(self.frame,width=175,height=1,bg='#C1121F').place(x=30,y=165)
        #Employee Cnic number
        self.cnic=Entry(self.frame,width=25,fg='black',border=0,bg='#FDF0D5',font=('verdena',12))
        self.cnic.place(x=30,y=180)
        self.cnic.insert(0,'Employee CNIC')
        self.cnic.bind('<FocusIn>',lambda x:self.cnic.delete(0,END) )
        self.cnic.bind('<FocusOut>',self.cnic_leave)

        Frame(self.frame,width=175,height=1,bg='#C1121F').place(x=30,y=205)

        #Employee salary
        self.salary=Entry(self.frame,width=25,fg='black',border=0,bg='#FDF0D5',font=('verdena',12))
        self.salary.place(x=30,y=225)
        self.salary.insert(0,'Employee Salary')
        self.salary.bind('<FocusIn>',lambda x:self.salary.delete(0,END) )
        self.salary.bind('<FocusOut>',self.salary_leave)
        Frame(self.frame,width=175,height=1,bg='#C1121F').place(x=30,y=250)
        
    #savig all data in sqlite3
    #button
        
        Button(self.window,width=10,text="<Back",bg='#FDF0D5',command=self.back,fg='#C1121F',font=('verdena',10,'bold'),border=0).place(x=30,y=420)
        Button(self.frame,width=20,pady=6,text="Save & Next",bg='#780000',command=self.saving,fg='white',font=('verdena',12,'bold'),border=0).place(x=30,y=320)
        self.update()
    def back(self):
        self.window.destroy()
        pp=SearchEngine()   
    def selected(self,event):
        self.service=self.click.get()    
    def saving(self):
        
        #connectig with sqlite3
        with sqlite3.connect('data.db') as db:
            cursor=db.cursor()
        #***************************
        name=self.Emp_name.get().strip()
        number=self.number.get().strip()
        cnic=self.cnic.get().strip()
        salary=self.salary.get().strip()
        service=self.service
        gender=self.gender
        num=re.match('[03][0-9]{10}',number)
        sal=re.match('[0-9]{4}',salary)
        nam=re.match('[A-Za-z]', name) 
        nic= re.match('[0-9]{12}',cnic)
        
           
        #**************************
        #checking validity of entry
        if num and sal and nam and nic or service!="":

            #cursor is used for sql command  
            sql=f"insert into 'Employee info'(name,'phone num',Cnic,service,salary,gender) values('{name}','{number}','{cnic}','{service}','{salary}','{gender}')"  
            cursor.execute(sql)
            db.commit()
            self.window.destroy()
            p3=SearchEngine()
        else:
            messagebox.showwarning("Oops!", "Please don't enter invalid values")   
    #binding function just for little animation
    #for employe name
    def name_leave(self,e):
        name=self.Emp_name.get()
        if name=='':
            self.Emp_name.insert(0,'Employee Name')
    def num_leave(self,e):   
        name=self.number.get()
        if name=='':
            self.number.insert(0,'Employee Phone Number') 
    def cnic_leave(self,e): 
        name=self.cnic.get()
        if name=='':
            self.cnic.insert(0,'Employee CNIC')   
    def salary_leave(self,e):
        name=self.salary.get()
        if name=='':
            self.salary.insert(0,'Employee Salary') 


    def update(self):
        self.window.mainloop()   

# if __name__=="__main__":
#     p2=Employeeinfo()
class SearchEngine:
  def __init__(self):
    '''set the data screen 
    '''
    self.window3=Tk()
    # self.window3.iconbitmap('icon.ico') // commit it this cause error
    self.mainscreen()
  def mainscreen(self):
    self.window3.title('Employee Data')
    #925x500 is size , 300+200 is postion on screen 
    self.window3.geometry('925x500+300+200')
    self.window3.configure(bg='#FDF0D5')
    self.window3.resizable(0,0)
  
    logo=PhotoImage(file='images/logo.png')
    Label(self.window3,image=logo,bg='#FDF0D5').place(x=-10,y=-20)
    

    #menu bar
    menu_bar=Menu(self.window3,background='#FDF0D5', foreground='black', activebackground='#FDF0D5', activeforeground='black')
    self.window3.config(menu=menu_bar)
    #SEARCH MENU
    search_menu=Menu(menu_bar,tearoff=0,background='#FDF0D5', foreground='black')#it minus -- this line tearoff=0
    menu_bar.add_cascade(label="Search",menu=search_menu) #menu side place this option
    #drop down menu
    search_menu.add_command(label='Search',command=self.lookup)
    search_menu.add_separator() #for an space
    #Reset to previous data
    reset_menu=Menu(menu_bar,tearoff=0,background='#FDF0D5', foreground='black')
    menu_bar.add_cascade(label="Reset",menu=reset_menu)
    reset_menu.add_command(label="Reset",command=self.Data)
    #creating data showing
    self.style=ttk.Style()
    # self.style.theme_use('vista') // commit it this cause error
    self.style.configure("Treeview",
    background='#FDF0D5',
    foreground='black',
    rowheight=30)
  #change selected color
    self.style.map("Treeview",
    background=[('selected','#C1121F')])
  #   self.subsection()
  #   #creating sub section
  # def subsection(self):
    #create Employee Frame
    self.frame=Frame(self.window3, width=450, height=250)
    self.frame.place(x=90,y=80)
    #creating scroll bar
    scrollbar=Scrollbar( self.frame)
    scrollbar.pack(side=RIGHT,fill=Y)
    #creating the DATAview              #set is used to configure later
    self.emp_data=ttk.Treeview(self.frame,yscrollcommand=scrollbar.set,selectmode='extended')
    self.emp_data.pack()


  #configure the scrollbar
    scrollbar.config(command=self.emp_data.yview)

    #define our columns
    self.emp_data['columns']=('EMPID','Name',"Number","CNIC","Service","Salary","Gender")
    #format our columns
    #hiding the default zero row
    self.emp_data.column('#0',width=0,stretch=NO)
    self.emp_data.column("EMPID",anchor=W,width=40)
    self.emp_data.column('Name',anchor=CENTER,width=110)
    self.emp_data.column("Number",anchor=CENTER,width=110)
    self.emp_data.column("CNIC",anchor=CENTER,width=120)
    self.emp_data.column("Service",anchor=CENTER,width=180)
    self.emp_data.column("Salary",anchor=CENTER,width=100)
    self.emp_data.column("Gender",anchor=CENTER,width=80)

    #create Headings
    self.emp_data.heading('#0',text='',anchor=W)
    self.emp_data.heading("EMPID",text="EMPID",anchor=CENTER)
    self.emp_data.heading('Name',text='Name',anchor=CENTER)
    self.emp_data.heading('Number',text='Number',anchor=CENTER)
    self.emp_data.heading('CNIC',text='CNIC',anchor=CENTER)
    self.emp_data.heading('Service',text='Service',anchor=CENTER)
    self.emp_data.heading('Salary',text='Salary',anchor=CENTER)
    self.emp_data.heading('Gender',text='Gender',anchor=CENTER)
    self.data_frame()
  def Data(self,loop=0):
    for record in self.emp_data.get_children():
      self.emp_data.delete(record) #delete preveious run record
    self.sqlite()
    #create stripped Row tags
    self.emp_data.tag_configure('oddrow',background="#FDF0D5")
    self.emp_data.tag_configure('evenrow',background="#669BBC")
    
    #Add our Data to screen
    column=0
    loop=self.searchdata if loop else self.data
    for record in loop:
        if column%2==0:
          self.emp_data.insert(parent='', index=END,values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]),tags=('evenrow',))
        else:
          self.emp_data.insert(parent='', index=END,values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]),tags=('oddrow',))
        column+=1
  def data_frame(self):
    self.Data()
    self.frame2=LabelFrame(self.window3,text='Record',border=0,fg='#540B0E',bg='#FDF0D5',font=('Helvetica',16,'bold'))
    self.frame2.place(x=20,y=310,height=150,width=850)
    #H=heading E=Entry box
    nameH=Label(self.frame2,text="Name",bg='#FDF0D5',font=('verdena',10,'bold')).place(x=3,y=10)
    self.nameE=Entry(self.frame2,fg='black',border=0.5,bg='#ECE5C7',font=('verdena',10))
    self.nameE.place(x=75,y=10)
    numberH=Label(self.frame2,text="Number",bg='#FDF0D5',font=('verdena',10,'bold')).place(x=230,y=10)
    self.numberE=Entry(self.frame2,fg='black',border=0.5,bg='#ECE5C7',font=('verdena',10))
    self.numberE.place(x=310,y=10)
    cnicH=Label(self.frame2,text="Cnic",bg='#FDF0D5',font=('verdena',10,'bold')).place(x=510,y=15)
    self.cnicE=Entry(self.frame2,fg='black',border=0.5,bg='#ECE5C7',font=('verdena',10))
    self.cnicE.place(x=595,y=15)
    serviceH=Label(self.frame2,text="Service",bg='#FDF0D5',font=('verdena',10,'bold')).place(x=3,y=45)



    services=['WEB DEVELOPER','MOBILE APP DEVELOPER','DIGITAL MARKETING',
              'WEB & GRAPHIC DESIGN','FRONT-END DEVELOPER','BACK-END DEVELOPER','FULL STACK DEVELOPER']  
    self.serviceE=StringVar()
    self.serviceE.set('                  ')
    self.drop=OptionMenu(self.frame2,self.serviceE,*services,command=self.selected)
        
    self.drop.config(bg="#ECE5C7", fg="black",border=0,font=('verdena',8))
    self.drop['menu'].config(bg="#FDF0D5", fg="black",border=0,font=('verdena',10))
    self.drop.place(x=72,y=45)
    # self.serviceE=Entry(self.frame2,fg='black',width=23,border=0.5,bg='#ECE5C7',font=('verdena',10))
    # self.serviceE.place(x=75,y=45)

    salaryH=Label(self.frame2,text="Salary",bg='#FDF0D5',font=('verdena',10,'bold')).place(x=280,y=45)
    self.salaryE=Entry(self.frame2,fg='black',border=0.5,bg='#ECE5C7',font=('verdena',10))
    self.salaryE.place(x=345,y=45)
    genderH=Label(self.frame2,text="Gender",bg='#FDF0D5',font=('verdena',10,'bold')).place(x=510,y=45)
    self.genderE=Entry(self.frame2,fg='black',border=0.5,width=20,bg='#ECE5C7',font=('verdena',10))
    self.genderE.place(x=595,y=45)
    
    
    #BUTTONS FRAME
    btn_frame=LabelFrame(self.window3,text="",border=0,fg='#540B0E',bg='#FDF0D5',font=('verdena',8,'bold'))
    btn_frame.place(x=40,y=420,width=900,height=100)
    update_button=Button(btn_frame,text='Update',bg='#FDF0D5',fg='#780000',font=('verdena',12,'bold'),border=0,command=self.update).grid(row=0,column=0,padx=20,pady=10)
    delete_button=Button(btn_frame,text='Delete',bg='#FDF0D5',fg='#780000',font=('verdena',12,'bold'),border=0,command=self.remove).grid(row=0,column=2,padx=20,pady=10)
    next_button=Button(btn_frame,text='Next',bg='#780000',fg='white',font=('Helvetica',14,'bold'),border=0,command=self.nextpage).grid(row=0,column=5,padx=350,pady=10)
    add_button=Button(btn_frame,text='Add',bg='#FDF0D5',fg='#780000',font=('verdena',12,'bold'),border=0,command=self.add).grid(row=0,column=1,padx=20,pady=10)
    clear_button=Button(btn_frame,text='Clear',bg='#FDF0D5',fg='#780000',font=('verdena',12,'bold'),border=0,command=self.clear).grid(row=0,column=4,padx=20,pady=10)


    #binding wohooo
    self.emp_data.bind("<ButtonRelease-1>",self.select)
    self.window3.mainloop()

  def lookup(self):
    self.search=Toplevel(self.window3) 
    self.search.title('SEARCH RECORD')
    self.search.geometry('400x200+400+300')
    self.search.resizable(0,0)
    self.search.config(background='#FDF0D5')
    #search  label Frame
    search_frame=LabelFrame(self.search,text="Employee Name",border=0,fg='#540B0E',bg='#FDF0D5',font=('Helvetica',16,'bold'))
    search_frame.pack(padx=10,pady=10)
    #Adding Entery BOX
    self.searchE=Entry(search_frame,fg='black',border=0.5,bg='#FDF0D5',font=('verdena',10))
    self.searchE.pack(padx=10,pady=20)

    #search button
    Button(self.search,text='Search',bg='#780000',fg='#FDF0D5',font=('Helvetica',12,'bold'),border=0,command=self.search_Id).place(x=130,y=100)
 
  #this function is call from lookup function which the search bar menu
  def search_Id(self):
    lookup=self.searchE.get()
      
    conn=sqlite3.connect('data.db')
    #cursor do what we ask it
    cursor=conn.cursor()
    cursor.execute(''' select rowid,* from 'Employee info' where "name" like ?''',(lookup,)) #so case is not dependent
    self.searchdata=cursor.fetchall()
    if self.searchdata:
      conn.commit() 
      conn.close()
      self.Data(self.searchdata)
      self.search.destroy()
    else:
      messagebox.showwarning("Warning",'Employee Record Has No Such Name')  
  
    #after searching
    
  #add go to 2nd page
  def add(self):
      self.window3.destroy()
      p2=Employeeinfo()
    #when select
  def select(self,e):
    self.clear()
  #grab record  .focus allow us to grab values
    selected=self.emp_data.focus()
    #saving all values which were selected
    values= self.emp_data.item(selected,'values')
  
    self.rowid=values[0]
     #output to entery boxes values wil come in list 
    self.nameE.insert(0,values[1])
    self.numberE.insert(0,values[2])
    self.cnicE.insert(0,values[3])
    self.serviceE.set(values[4])
    self.salaryE.insert(0,values[5])
    self.genderE.insert(0,values[6])

  #service 
  def selected(self,event):
        self.service=self.serviceE.get()
  def clear(self):
    self.nameE.delete(0,END)
    self.numberE.delete(0,END)
    self.cnicE.delete(0,END)
    self.salaryE.delete(0,END)
    self.genderE.delete(0,END)
    self.serviceE.set('\t\t')
  def remove(self):
    char=self.emp_data.selection()[0]
    self.emp_data.delete(char)
    conn=sqlite3.connect('data.db')
    #cursor do what we ask it
    cursor=conn.cursor()
    cursor.execute(''' delete from  'Employee info' where oid='''+self.rowid)
    conn.commit() 
    conn.close()

    #giving message
    messagebox.showwarning("DELETED!",'EMPLOYEE RECORD HAS BEEN DELETED')
    #clear entry boxes
    self.clear()

  def update(self):
    #Grab the record
    selected=self.emp_data.focus()

    #for service only 
    if type(self.serviceE) is not str:
      self.service=self.serviceE.get()
    #update #SELECTED will give list and we asscoiate each index value with tuple value example rowid=empid self.name=name
    self.emp_data.item(selected,text='',
    values=(self.rowid,self.nameE.get(),self.numberE.get(),self.cnicE.get(),self.service,
    self.salaryE.get(),self.genderE.get(),))


    conn=sqlite3.connect('data.db')
    #cursor do what we ask it
    cursor=conn.cursor()
    cursor.execute('''update 'Employee info' set
    rowid=:oid,
    name=:name,
    'phone num'=:number,
    Cnic=:cnic,
    service=:service,
    salary=:salary,
    gender=:gender
    where oid=:oid''', #oid is the primary key in sqlite
    { 'oid':self.rowid,
      'name':self.nameE.get(),
      'number':self.numberE.get(),
      'cnic':self.cnicE.get(),
      'service':self.service,
      'salary':self.salaryE.get(),
      'gender':self.genderE.get()
    })
    self.data=cursor.fetchall()
    conn.commit() 
    conn.close()

    #clearinf after updating
    self.nameE.delete(0,END)
    self.numberE.delete(0,END)
    self.cnicE.delete(0,END)

    self.salaryE.delete(0,END)
    self.genderE.delete(0,END)


 
    #next== opning new window
  def nextpage(self): 
    try: 
      Salaryslip(self.nameE.get(),self.numberE.get(),self.cnicE.get(),self.serviceE.get(),self.salaryE.get())
    except Exception as e:
      messagebox.showerror('Erro!',"No Field is selected")


  #database connection and controlling 
  def sqlite(self):
    conn=sqlite3.connect('data.db')
    #cursor do what we ask it
    cursor=conn.cursor()
    cursor.execute(''' select rowid,* from 'Employee info' ''')
    self.data=cursor.fetchall()
    
    conn.commit() 
    conn.close() 

# p3=SearchEngine() 
class login:
    def __init__(self):
        '''set the first screen 
        '''
        self.window1=Tk()
        # self.window1.iconbitmap('icon.ico')  // commit it this couse error
        self.mainscreen()
    def mainscreen(self):
        self.window1.title('Login')
        #925x500 is size , 300+200 is postion on screen 
        self.window1.geometry('925x500+300+200')
        self.window1.configure(bg='#FDF0D5')
        self.window1.resizable(0,0)
        img1=PhotoImage(file='images/logo.png')
        Label(self.window1,image=img1,bg='#FDF0D5').place(x=480,y=70)
        logo=PhotoImage(file='images/logo.png')
        Label(self.window1,image=logo,bg='#FDF0D5').place(x=0,y=0)
       
        
        self.sub_section()       
    def sub_section(self):
        
        self.frame=Frame(self.window1, width=350, height=350,bg='#FDF0D5')
        self.frame.place(x=40,y=110)
        self.heading=Label(self.frame,text='Sign In',fg='#540B0E',bg='#FDF0D5',font=('Helvetica',24,'bold'))
        self.heading.place(x=55,y=5)

        #username
        self.user=Entry(self.frame,width=25,fg='black',border=0,bg='#FDF0D5',font=('verdena',14))
        self.user.place(x=50,y=90)
        #0 defines if nothing is type thn enter 'username'
        self.user.insert(0,'Username')
        #to remove strinf 'username' on clicking 
        self.user.bind('<FocusIn>',self.on_enter)
        self.user.bind('<FocusOut>',self.on_leave)
          #adding line underneath username
        Frame(self.frame,width=175,height=2,bg='#C1121F').place(x=50,y=120)
        #password
        self.code=Entry(self.frame,width=25,fg='black',border=0,bg='#FDF0D5',font=('verdena',14),show="*")
        self.code.place(x=50,y=140)
        self.code.insert(0,'Password')

        self.code.bind('<FocusIn>',self.on_entery)
        self.code.bind('<FocusOut>',self.on_leavy)
        #adding line underneath password
        Frame(self.frame,width=175,height=2,bg='#C1121F').place(x=50,y=170)
     
        Button(self.frame,width=20,pady=6,text="Sign in",bg='#780000',command=self.signin,fg='white',font=('verdena',12,'bold'),border=0).place(x=50,y=200)
        self.update()
    def update(self):
            self.window1.mainloop()  
    #button logic
    def signin(self):
        username=self.user.get()
        password=self.code.get()
        with open('HRdata.txt') as file:
            content=eval(file.read())
            if username==content['username'] and password==content['password']:
                self.window1.destroy()
                p2=SearchEngine()
            else:
                messagebox.showwarning("Wrong",'Username or password is incorrect')
                


    #it will just delete the string as this function is calleds      
    def on_enter(self,e):
        self.user.delete(0,END) 
    def on_leave(self,e):
        name=self.user.get()
        if name=='':
            self.user.insert(0,'Username')
    #it will just delete the string as this function is called   
    def on_entery(self,e):
        self.code.delete(0,END)
    def on_leavy(self,e):
        name=self.code.get()
        if name=='':
            self.code.insert(0,'Password')    
if __name__=="__main__":
    p1=login()
