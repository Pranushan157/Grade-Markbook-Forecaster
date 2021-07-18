#Grade Forecaster and Markbook 
#Developed on Pyhton 3.6 (64-bit) 
#Date: 26/12/2019 

from tkinter import * 
import tkinter as tk 
import sqlite3
from sqlite3 import Error 
import csv
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt  
import matplotlib.lines as mlines 
import math
from statistics import mean  

login=tk.Tk() 
login.geometry("500x500")
login.title("FCL login page")
login.configure(background="turquoise")
topframe=tk.Frame(master=login,width=500,height=150)
photo=PhotoImage(file="Logo.png")
label=Label(login,image=photo)
label.pack() 

conn=sqlite3.connect("Coursework.db") 
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Studentdetails(id INTEGER PRIMARY KEY, Forename TEXT, Surname TEXT,DateofBirth TEXT,address TEXT,contactNo TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS Behaviour(Comment TEXT PRIMARY KEY,id INTEGER,FOREIGN KEY(id) REFERENCES Studentdetails(id))")
c.execute("CREATE TABLE IF NOT EXISTS Mathsmarks(Mark INTEGER ,Percentage INTEGER,id INTEGER,FOREIGN KEY(id) REFERENCES Studentdetails(id))")
c.execute("CREATE TABLE IF NOT EXISTS Englishmarks(Mark INTEGER ,Percentage INTEGER,id INTEGER, FOREIGN KEY(id) REFERENCES Studentdetails(id))")
c.execute("CREATE TABLE IF NOT EXISTS Pastavg(Percentage INTEGER, Grade INTEGER,Subject Text)")
conn.commit() 
conn.close() 

class pageoverview(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container=tk.Frame(self)  
        
        container.pack(side="left",fill="both",expand="True") 
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        
        self.frames={} 

        for F in (ss,be,gme,gf):
            frame=F(container,self)
            self.frames[F]=frame 
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(ss)
    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()

class ss(tk.Frame):
     def __init__(self,parent,controller,):
        tk.Frame.__init__(self,parent,bg="firebrick2")
        label=Label(self,text="Student Details",font="calibri 30 bold italic underline",fg="lavender blush",bg="firebrick2")
        label.place(relx=0,rely=0.075,anchor="w")
        button=Button(self,text="Behaviour Entry",bg="grey97",command=lambda:controller.show_frame(be)) #BAND A
        button.place(relx=0,rely=0.0176,anchor="w")
        button2=Button(self,text="Mark Entry/Search",bg="grey97",command=lambda:controller.show_frame(gme))
        button2.place(relx=0.073,rely=0.0176,anchor="w")
        button3=Button(self,text="Grade Forecaster",bg="grey97",command=lambda:controller.show_frame(gf))
        button3.place(relx=0.152,rely=0.0176,anchor="w")
        add=Label(self,text="Add new student",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        add.place(relx=0,rely=0.18,anchor="w")
        ############################################################
        name=Label(self,text="First Name:",font="calibri 14",fg="old lace",bg="firebrick2") 
        name.place(relx=0,rely=0.255,anchor="w")
        self.entername=Entry(self)
        self.entername.place(relx=0.11,rely=0.255,anchor="w")
        name2=Label(self,text="Surname:",font="calibri 14",fg="old lace",bg="firebrick2")
        name2.place(relx=0,rely=0.355,anchor="w")
        self.entersurname=Entry(self)
        self.entersurname.place(relx=0.11,rely=0.355,anchor="w")
        dob=Label(self,text="Date of birth:",font="calibri 14",fg="old lace",bg="firebrick2")
        dob.place(relx=0,rely=0.455,anchor="w")
        self.enterdob=Entry(self) 
        self.enterdob.place(relx=0.11,rely=0.455,anchor="w")
        address=Label(self,text="Enter Address:",font="calibri 14",fg="old lace",bg="firebrick2")
        address.place(relx=0,rely=0.555,anchor="w")
        self.enteraddress=Entry(self)
        self.enteraddress.place(relx=0.11,rely=0.555,anchor="w")
        phone=Label(self,text="Enter Phone No:",font="calibri 14",fg="old lace",bg="firebrick2")
        phone.place(relx=0,rely=0.655,anchor="w")
        self.enterphone=Entry(self)
        self.enterphone.place(relx=0.11,rely=0.655,anchor="w") 
        updatebutton=Button(self,text="Add new student",command=self.insert) 
        updatebutton.place(relx=0.195,rely=0.75,anchor="w")
        #############################################################
        search=Label(self,text="Search for Student details",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        search.place(relx=0.615,rely=0.18,anchor="w")
        find1=Label(self,text="Enter Forename:",font="calibri 14",fg="old lace",bg="firebrick2")
        find1.place(relx=0.615,rely=0.235,anchor="w")
        self.e_find1=Entry(self)
        self.e_find1.place(relx=0.725,rely=0.236,anchor="w") 
        find=Label(self,text="Enter surname:",font="calibri 14",fg="old lace",bg="firebrick2")
        find.place(relx=0.615,rely=0.255)
        self.e_find=Entry(self)
        self.e_find.place(relx=0.725,rely=0.26) 
        find1=Button(self,text="Enter",command=self.dsearch)
        find1.place(relx=0.795,rely=0.32,anchor="w")
        display=Label(self,text="Here's what we found:",font="calibri 14",fg="old lace",bg="firebrick2")
        display.place(relx=0.615,rely=0.385,anchor="w")
        clear=Button(self,text="Clear result",command=self.clear)
        clear.place(relx=0.875,rely=0.57,anchor="w")
        #################################################################

       
        
     def insert(self):
        r_name=self.entername.get()
        r_name=r_name.strip() 
        r_name=r_name.capitalize()
        self.entername.delete(0,tk.END)
        r_surname=self.entersurname.get()
        r_surname=r_surname.strip() 
        r_surname=r_surname.capitalize() 
        self.entersurname.delete(0,tk.END)
        r_dob=self.enterdob.get() 
        self.enterdob.delete(0,tk.END)
        r_address=self.enteraddress.get() 
        self.enteraddress.delete(0,tk.END)
        r_phone=self.enterphone.get()
        self.enterphone.delete(0,tk.END) 
        if len(r_name) ==0 or len(r_surname)==0 or len(r_dob)==0 or len(r_address)==0 or len(r_phone)==0:
            self.failpopout() 
        else: 
            conn=sqlite3.connect("Coursework.db")
            c=conn.cursor() 
            c.execute("INSERT INTO Studentdetails(Forename,Surname,DateofBirth,address,contactNo) VALUES (?,?,?,?,?)",(r_name,r_surname,r_dob,r_address,r_phone)) 
            conn.commit() 
            conn.close()
                   

     def dsearch(self):
       forename=self.e_find1.get()
       forename=forename.strip()
       forename=forename.capitalize()
       self.e_find1.delete(0,tk.END)
       surname=self.e_find.get()
       surname=surname.strip()
       surname=surname.capitalize() 
       self.e_find.delete(0,tk.END)
       conn=sqlite3.connect("Coursework.db")
       c=conn.cursor()
       c.execute("SELECT * FROM Studentdetails WHERE Forename=? AND Surname=?",(forename,surname,))
       result=c.fetchone()
       if result==None:
           self.failpopout()
       else:
        rows=["ID:","First Name:","Surname:","D.O,B:","Address:","Contact Number:"]
        result1=pd.DataFrame(result,rows)
        results2=(result1.to_string(header=False)) 
        conn.commit()
        conn.close() 
        self.output=Label(self,text=results2,font=11,fg="old lace",bg="firebrick2")
        self.output.place(relx=0.757,rely=0.455,anchor="w")  
            

     def clear(self):
         try:
             self.output.destroy()
         except:
             notif=tk.Tk()
             notif.wm_title("Clear")
             label=Label(notif,text="Nothing to clear")
             label.pack(side="top",fill="x",pady=10,padx=45)
             notif.mainloop() 
     
     def  failpopout(self):
        failnotif=tk.Tk() 
        failnotif.wm_title("Failed insert")
        label=Label(failnotif,text="One or more fields were left blank or entered data is incorrect \n Please re-enter the details")
        label.pack(side="top",fill="x",pady=10)
        failnotif.mainloop() 


class be(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="firebrick2")
        label=Label(self,text="Behaviour Entry",font="calibri 30 bold italic underline",fg="lavender blush",bg="firebrick2") 
        label.place(relx=0,rely=0.075,anchor="w") 
        button=Button(self,text="Student Search",bg="grey97",command=lambda:controller.show_frame(ss))
        button.place(relx=0,rely=0.0176,anchor="w")
        button1=Button(self,text="Mark Entry/Search",bg="grey97",command=lambda:controller.show_frame(gme))
        button1.place(relx=0.0695,rely=0.0176,anchor="w")   
        button2=Button(self,text="Grade Forecaster",bg="grey97",command=lambda:controller.show_frame(gf))
        button2.place(relx=0.15,rely=0.0176,anchor="w") 
        ############################################################
        title_label=Label(self,text="Add new comment",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        title_label.place(relx=0,rely=0.18,anchor="w")
        forename=Label(self,text="Enter forename:",font="calibri 14",fg="old lace",bg="firebrick2")
        forename.place(relx=0,rely=0.255,anchor="w")
        self.forename=Entry(self)
        self.forename.place(relx=0.11,rely=0.255,anchor="w")
        surname=Label(self,text="Enter surname:",font="calibri 14",fg="old lace",bg="firebrick2")
        surname.place(relx=0,rely=0.355,anchor="w")
        self.surname=Entry(self)
        self.surname.place(relx=0.11,rely=0.355,anchor="w") 
        comment=Label(self,text="Enter comment:",font="calibri 14",fg="old lace",bg="firebrick2")
        comment.place(relx=0,rely=0.455,anchor="w")
        self.comment=Text(self)
        self.comment.place(relx=0.11,rely=0.535,anchor="w",height=110,width=200)
        enter=Button(self,text="Enter",command=self.add)
        enter.place(relx=0.255,rely=0.685,anchor="w")
        #############################################################
        title1_label=Label(self,text="Check previous comments",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        title1_label.place(relx=0.615,rely=0.18,anchor="w")
        forename1=Label(self,text="Enter Forename:",font="calibri 14",fg="old lace",bg="firebrick2")
        forename1.place(relx=0.615,rely=0.255,anchor="w")
        self.forename1=Entry(self)
        self.forename1.place(relx=0.725,rely=0.255,anchor="w")
        surname1=Label(self,text="Enter Surname:",font="calibri 14",fg="old lace",bg="firebrick2")
        surname1.place(relx=0.615,rely=0.355,anchor="w")
        self.surname1=Entry(self)
        self.surname1.place(relx=0.725,rely=0.355,anchor="w")
        d_label=Label(self,text="Previous comments found:",font="calibri 14",fg="old lace",bg="firebrick2")
        d_label.place(relx=0.615,rely=0.455)
        enter1=Button(self,text="Enter",command=self.search)
        enter1.place(relx=0.8,rely=0.44,anchor="w")
        clear=Button(self,text="Clear below commments",command=self.clear)
        clear.place(relx=0.86,rely=0.44,anchor="w")
        ############################################################
    
    def  failpopout(self):
        failnotif=tk.Tk() 
        failnotif.wm_title("Failed search")
        label=Label(failnotif,text="Student not found \n Please reenter all entries")
        label.pack(side="top",fill="x",pady=15,padx=30)
        failnotif.mainloop() 
    
    def add(self):
       search=self.forename.get() 
       search2=self.surname.get()
       search=search.strip()
       search=search.capitalize()
       search2=search2.strip()
       search2=search2.strip() 
       r_comment=self.comment.get("1.0",'end-1c')
       if len(r_comment)==0:
           notif=tk.Tk()
           notif.wm_title("Clear")
           label=Label(notif,text="Failed entry comments left blank")
           label.pack(side="top",fill="x",pady=10,padx=45)
           notif.mainloop() 
       else:
            self.forename.delete(0,tk.END)
            self.surname.delete(0,tk.END)
            self.comment.delete("1.0",END)  
            conn=sqlite3.connect("Coursework.db")
            c=conn.cursor()
            c.execute("SELECT id FROM Studentdetails WHERE Forename=? AND Surname=?",(search,search2,))
            try:
                result=c.fetchone()[0]
                c.execute("INSERT INTO Behaviour (Comment,id) VALUES (?,?)",(r_comment,result)) 
                conn.commit() 
            except:
                self.failpopout()  
       
    def search(self): 
        field=self.forename1.get() 
        field1=self.surname1.get()
        field=field.strip()
        field=field.capitalize()
        field1=field1.strip()
        field1=field1.capitalize() 
        self.forename1.delete(0,tk.END)
        self.surname1.delete(0,tk.END) 
        conn=sqlite3.connect("Coursework.db")
        c=conn.cursor() 
        c.execute("SELECT id From Studentdetails WHERE Forename=? AND Surname=?",(field,field1))
        try:
            result=c.fetchone()[0]  
            c.execute("SELECT Comment From Behaviour WHERE id=?",(result,)) 
            global comments 
            comments=c.fetchall() 
            df=pd.DataFrame(data=comments) 
            comments=(df.to_string(index=False,header=False))  
            self.clabel=Label(self,text=comments,font=11,fg="old lace",bg="firebrick2")
            self.clabel.place(relx=0.6125,rely=0.555,anchor="w") 
        except:
            self.failpopout() 
        
       
    def clear(self):
         try:
             self.clabel.destroy()
         except:
              notif=tk.Tk()
              notif.wm_title("Clear")
              label=Label(notif,text="Nothing to clear")
              label.pack(side="top",fill="x",pady=10,padx=45)
              notif.mainloop() 


       
          
class gme(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="firebrick2")
        label=Label(self,text="Mark Entry/Search",font="calibri 30 bold italic underline",fg="lavender blush",bg="firebrick2")
        label.place(relx=0,rely=0.075,anchor="w") 
        button=Button(self,text="Student Search",bg="grey97",command=lambda:controller.show_frame(ss))
        button.place(relx=0,rely=0.0176,anchor="w")
        button1=Button(self,text="Behaviour Entry",bg="grey97",command=lambda:controller.show_frame(be))
        button1.place(relx=0.0685,rely=0.0176,anchor="w")
        button2=Button(self,text="Grade Forecaster",bg="grey97",command=lambda:controller.show_frame(gf))
        button2.place(relx=0.1395,rely=0.0176,anchor="w") 
        #################################################
        title_label=Label(self,text="Enter new marks",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        title_label.place(relx=0,rely=0.18,anchor="w")
        title1_label=Label(self,text="Maths",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        title1_label.place(relx=0,rely=0.45,anchor="w")
        title2_label=Label(self,text="English",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        title2_label.place(relx=0.22,rely=0.45,anchor="w")
        forename=Label(self,text="Enter forename:",font="calibri 14",fg="old lace",bg="firebrick2")
        forename.place(relx=0,rely=0.255,anchor="w") 
        self.forenameentry=Entry(self)
        self.forenameentry.place(relx=0.11,rely=0.255,anchor="w")
        surname=Label(self,text="Enter surname:",font="calibri 14",fg="old lace",bg="firebrick2")
        surname.place(relx=0,rely=0.355,anchor="w")
        self.surnameentry=Entry(self)
        self.surnameentry.place(relx=0.11,rely=0.345)
        ###################################################
        mathslabel=Label(self,text="Enter mark:",font="calibri 14",fg="old lace",bg="firebrick2")
        mathslabel.place(relx=0,rely=0.5,anchor="w")
        self.mathsentry=Entry(self)
        self.mathsentry.place(relx=0.11,rely=0.5,anchor="w")
        mathslabel2=Label(self,text="Enter percentage:",font="calibri 14",fg="old lace",bg="firebrick2")
        mathslabel2.place(relx=0,rely=0.55,anchor="w")
        self.mathsentry2=Entry(self)
        self.mathsentry2.place(relx=0.11,rely=0.55,anchor="w")
        m_entry=Button(self,text="Enter",command=self.maths)
        m_entry.place(relx=0.18,rely=0.6,anchor="w")
        ##################################################
        englishlabel=Label(self,text="Enter mark:",font="calibri 14",fg="old lace",bg="firebrick2")
        englishlabel.place(relx=0.22,rely=0.5,anchor="w")
        self.englishentry=Entry(self)
        self.englishentry.place(relx=0.335,rely=0.5,anchor="w")
        englishlabel2=Label(self,text="Enter percentage:",font="calibri 14",fg="old lace",bg="firebrick2")
        englishlabel2.place(relx=0.22,rely=0.55,anchor="w")
        self.englishentry2=Entry(self)
        self.englishentry2.place(relx=0.335,rely=0.55,anchor="w")
        e_entry=Button(self,text="Enter",command=self.english)
        e_entry.place(relx=0.405,rely=0.6,anchor="w")
        ####################################################
        stitle=Label(self,text="Search for student marks",font="calibri 18 underline",fg="old lace",bg="firebrick2")
        stitle.place(relx=0.55,rely=0.18,anchor="w")
        s_forename=Label(self,text="Enter forename:",font="calibri 14",fg="old lace",bg="firebrick2")
        s_forename.place(relx=0.55,rely=0.255,anchor="w")
        s_surname=Label(self,text="Enter surname:",font="calibri 14",fg="old lace",bg="firebrick2")
        s_surname.place(relx=0.55,rely=0.355,anchor="w")
        self.s_forenameentry=Entry(self)
        self.s_forenameentry.place(relx=0.653,rely=0.255,anchor="w")
        self.s_surnameentry=Entry(self)
        self.s_surnameentry.place(relx=0.653,rely=0.355,anchor="w")
        enter=Button(self,text="Enter",command=self.search)
        enter.place(relx=0.72,rely=0.4,anchor="w")
        found=Label(self,text="Marks found:",font="calibri 14",fg="old lace",bg="firebrick2")
        found.place(relx=0.55,rely=0.5,anchor="w")
        found1=Label(self,text="Maths marks (mark,percentage)-",font="calibri 14",fg="old lace",bg="firebrick2")
        found1.place(relx=0.55,rely=0.55,anchor="w")
        found3=Label(self,text="Maths average:",font="calibri 14",fg="old lace",bg="firebrick2")
        found3.place(relx=0.55,rely=0.6,anchor="w")
        found2=Label(self,text="English marks(mark,percentage)-",font="calibri 14",fg="old lace",bg="firebrick2")
        found2.place(relx=0.55,rely=0.7,anchor="w")
        found4=Label(self,text="English averge:",font="calibri 14",fg="old lace",bg="firebrick2")
        found4.place(relx=0.55,rely=0.73)
        clear=Button(self,text="Clear",command=self.clear)
        clear.place(relx=0.65,rely=0.5,anchor="w")
        #####################################################

    
    def  failpopout(self):
        failnotif=tk.Tk() 
        failnotif.wm_title("Failed search")
        label=Label(failnotif,text="Student not found \n Please reenter all entries")
        label.pack(side="top",fill="x",pady=10)
        failnotif.mainloop()    
        
        
        
    def maths(self): 
        p1=self.forenameentry.get() 
        p1=p1.strip()
        p1=p1.capitalize()
        p2=self.surnameentry.get()
        p2=p2.strip()
        p2=p2.capitalize() 
        e1=self.mathsentry.get()
        e1=e1.strip()
        e2=self.mathsentry2.get()
        e2=e2.strip()
        self.forenameentry.delete(0,tk.END)
        self.surnameentry.delete(0,tk.END)
        self.mathsentry.delete(0,tk.END)
        self.mathsentry2.delete(0,tk.END)
        conn=sqlite3.connect("Coursework.db")
        c=conn.cursor()
        c.execute("SELECT id FROM Studentdetails WHERE Forename=? AND Surname=?",(p1,p2,))
        try:
            result=c.fetchone()[0]
            c.execute("INSERT INTO Mathsmarks (Mark,Percentage,id) VALUES (?,?,?)",(e1,e2,result)) 
            conn.commit() 
        except:
            self.failpopout() 
    
    def english(self):
        p1=self.forenameentry.get()
        p1=p1.strip()
        p1=p1.capitalize()
        p2=self.surnameentry.get()
        p2=p2.strip()
        p2=p2.capitalize()
        e1=self.englishentry.get()
        e1=e1.strip()
        e2=self.englishentry2.get()
        e2=e2.strip()
        self.forenameentry.delete(0,tk.END) 
        self.surnameentry.delete(0,tk.END)
        self.englishentry.delete(0,tk.END)
        self.englishentry2.delete(0,tk.END)
        conn=sqlite3.connect("Coursework.db")
        c=conn.cursor()
        c.execute("SELECT id FROM Studentdetails WHERE Forename=? AND Surname=?",(p1,p2,))
        try:
            result=c.fetchone()[0]
            c.execute("INSERT INTO Englishmarks (Mark,Percentage,id) VALUES (?,?,?)",(e1,e2,result))
            conn.commit()
        except:
            self.failpopout() 

    def search(self):
        global name1
        global name2
        name1=self.s_forenameentry.get()
        name2=self.s_surnameentry.get()
        name1=name1.strip()
        name2=name2.strip()
        name1=name1.capitalize()
        name2=name2.capitalize()
        self.s_forenameentry.delete(0,tk.END)
        self.s_surnameentry.delete(0,tk.END)
        conn=sqlite3.connect("Coursework.db")
        c=conn.cursor() 
        c1=conn.cursor()
        c.execute("SELECT id From Studentdetails WHERE Forename=? AND Surname=?",(name1,name2))
        try:
            result=c.fetchone()[0]
        except:
            self.failpopout()
        c.execute("SELECT Mark,Percentage From Mathsmarks WHERE id=?",(result,))
        c1.execute("SELECT Mark,Percentage From Englishmarks WHERE id=?",(result,))
        marks=c.fetchall()
        marks1=c1.fetchall() 
        df=pd.DataFrame(data=marks)
        df1=pd.DataFrame(data=marks1)
        marks=(df.to_string(index=False,header=False))
        marks1=(df1.to_string(index=False,header=False))
        self.clabel=Label(self,text=marks,font=11,fg="old lace",bg="firebrick2")
        self.clabel.place(relx=0.78,rely=0.55,anchor="w") 
        self.clabel2=Label(self,text=marks1,font=11,fg="old lace",bg="firebrick2")
        self.clabel2.place(relx=0.78,rely=0.7,anchor="w")
        self.avg() 
        
             
    def avg(self): 
        conn=sqlite3.connect("Coursework.db")
        c=conn.cursor() 
        c1=conn.cursor()
        c.execute("SELECT id From Studentdetails WHERE Forename=? AND Surname=?",(name1,name2))
        result=c.fetchone()[0]
        c.execute("SELECT Mark, AVG(Percentage) From Mathsmarks WHERE id=?",(result,)) #BAND A 
        c1.execute("SELECT Mark,AVG(Percentage) FROM Englishmarks WHERE id=?",(result,)) #BAND A 
        mavg=round(c.fetchone()[1])
        eavg=round(c1.fetchone()[1])
        self.mavglabel=Label(self,text=mavg,font="calibri 14",fg="old lace",bg="firebrick2")
        self.mavglabel.place(relx=0.65,rely=0.58)
        self.eavglabel=Label(self,text=eavg,font="calibri 14",fg="old lace",bg="firebrick2")
        self.eavglabel.place(relx=0.65,rely=0.73)

    def clear(self):
         try:
            self.clabel.destroy()
            self.clabel2.destroy() 
            self.mavglabel.destroy()
            self.eavglabel.destroy()
         except:
            notif=tk.Tk()
            notif.wm_title("Clear")
            label=Label(notif,text="Nothing to clear")
            label.pack(side="top",fill="x",pady=10,padx=45)
            notif.mainloop() 

        
class gf(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg="firebrick2")
        label=Label(self,text="Grade Forecaster",font="calibri 30 bold italic underline",fg="lavender blush",bg="firebrick2")
        label.place(relx=0,rely=0.075,anchor="w") 
        button=Button(self,text="Student Search",bg="grey97",command=lambda:controller.show_frame(ss))
        button.place(relx=0,rely=0.0176,anchor="w")
        button1=Button(self,text="Behaviour Entry",bg="grey97",command=lambda:controller.show_frame(be))
        button1.place(relx=0.0686,rely=0.0176,anchor="w")
        button2=Button(self,text="Mark Entry/Search",bg="grey97",command=lambda:controller.show_frame(gme))
        button2.place(relx=0.14,rely=0.0176,anchor="w")  
        label1=Label(self,text="Enter previous marks and percentage:",font="calibri 14 underline",fg="old lace",bg="firebrick2")
        label1.place(relx=0,rely=0.18,anchor="w")
        label2=Label(self,text="Enter average percentage:",font="calibri 14",fg="old lace",bg="firebrick2")
        label2.place(relx=0,rely=0.25,anchor="w")
        self.entry1=Entry(self)
        self.entry1.place(relx=0.17,rely=0.25,anchor="w")
        label3=Label(self,text="Enter final achieved grade:",font="calibri 14",fg="old lace",bg="firebrick2")
        label3.place(relx=0.28,rely=0.25,anchor="w")
        self.entry2=Entry(self)
        self.entry2.place(relx=0.45,rely=0.25,anchor="w")
        label3=Label(self,text="Enter M or E indicating subject :",font="calibri 14",fg="old lace",bg="firebrick2")
        label3.place(relx=0.55,rely=0.25,anchor="w")
        self.entry3=Entry(self)
        self.entry3.place(relx=0.7475,rely=0.25,anchor="w")
        enter=Button(self,text="Enter",command=self.insert)
        enter.place(relx=0.815,rely=0.3,anchor="w")
        field1=Label(self,text="Enter Student's average percentage to recieve predicition:",font="calibri 14",fg="old lace",bg="firebrick2")
        field1.place(relx=0,rely=0.4,anchor="w")
        self.efield1=Entry(self)
        self.efield1.place(relx=0.35,rely=0.4,anchor="w")
        field2=Label(self,text="Indicate subject to be predicted enter M or E:",font="calibri 14",fg="old lace",bg="firebrick2")
        field2.place(relx=0,rely=0.45,anchor="w")
        self.efield2=Entry(self)
        self.efield2.place(relx=0.35,rely=0.45,anchor="w")
        plot=Button(self,text="Create graph",command=self.plot)
        plot.place(relx=0.391,rely=0.5,anchor="w")
        regression=Label(self,text="Regression line:",font="calibri 14",fg="old lace",bg="firebrick2")
        regression.place(relx=0,rely=0.55,anchor="w")
        gradelabel=Label(self,text="Predicted grade based of model:",font="calibri 14",fg="old lace",bg="firebrick2")
        gradelabel.place(relx=0,rely=0.62,anchor="w") 
        undo=Button(self,text="Undo",command=self.undo)
        undo.place(relx=0.25,rely=0.65)
        self.save=[] #BAND A 
        self.end=10  #BAND A 
        self.top=0   #BAND A 


    def insert(self):
        percent=self.entry1.get()
        grade=self.entry2.get()
        subject=self.entry3.get()
        subject=subject.strip()
        subject=subject.capitalize()
        self.entry1.delete(0,tk.END)
        self.entry2.delete(0,tk.END)
        self.entry3.delete(0,tk.END)
        if len(percent)==0 or len(grade)==0 or len(subject)==0:
            self.failsafe()
        else:
            conn=sqlite3.connect("Coursework.db")
            c=conn.cursor()
            c.execute("INSERT INTO Pastavg (Percentage,Grade,Subject) VALUES (?,?,?)",(percent,grade,subject))
            conn.commit() 


#https://pythonprogramming.net/how-to-program-best-fit-line-machine-learning-tutorial/
    def plot(self): #BAND A 
        conn=sqlite3.connect("Coursework.db")
        c=conn.cursor()
        check=self.efield2.get()
        check=check.strip()
        check=check.capitalize()
        self.efield2.delete(0,tk.END) 
        try:
            predictx=int(self.efield1.get())
            self.efield1.delete(0,tk.END)
        except:
            self.failsafe() 
        try:
            c.execute("SELECT Percentage,Grade FROM Pastavg WHERE Subject=?",(check))
            percent=[]
            grade=[]
            for row in c.fetchall(): 
                percent.append(row[0]) #BAND A
                grade.append(row[1])   #BAND A 
                xcords=np.array(grade)
                ycords=np.array(percent)
            gradient=(((mean(xcords)*mean(ycords))-mean(xcords*ycords)) / ((mean(xcords)*mean(xcords))-mean(xcords*xcords))) #BAND A 
            ycut=(mean(ycords)-gradient*mean(xcords)) #BAND A 
            equation=("y=%sx+%s"%(gradient,ycut))  
            lineofregression=[(gradient*x)+ycut for x in xcords]
            self.predicted=(predictx-ycut)/gradient 
            self.predicted=math.ceil(self.predicted)
            if self.predicted<=0:
                self.predicted=1
            if self.predicted>9:
                self.predicted=9
            self.push() 
            elabel=Label(self,text=equation,fg="old lace",bg="firebrick2",font="calibri 14")
            elabel.place(relx=0.1,rely=0.55,anchor="w")
            self.glabel=Label(self,text=self.predicted,fg="old lace",bg="firebrick2",font="calibri 14")
            self.glabel.place(relx=0.22,rely=0.62,anchor="w")
            plt.scatter(xcords,ycords)
            plt.plot(xcords,lineofregression)
            plt.xlabel("Grade")
            plt.ylabel("Percentage")
            plt.title("Regression creator")
            plt.show() 
        except:
            self.failsafe()  #BAND A 
        

    def push(self): #BAND A 
        if self.top>=self.end:
            failnotif=tk.Tk() 
            failnotif.wm_title("No more records")
            label=Label(failnotif,text="No grades will be predicted now \n due to the fact undo button will no longer be able to undo latest actions")
            label.pack(side="top",fill="x",pady=15)
            failnotif.mainloop() 
        else:
            self.save.append(self.predicted) #BAND A 
            self.top+=1
    
    def undo(self):
        if self.top<=0:
            emptynotif=tk.Tk()
            emptynotif.wm_title("Undo unavaliable")
            label=Label(emptynotif,text="Undo unavaliable \n All previous values have been displayed")
            label.pack(side="top",fill="x",pady=15)
            emptynotif.mainloop() 
        else:
            item = self.save.pop() #BAND A 
            self.top -= 1
            self.glabel=Label(self,text=item,fg="old lace",bg="firebrick2",font="calibri 14")
            self.glabel.place(relx=0.22,rely=0.62,anchor="w") #BAND A 
    
    def failsafe(self):
        failnotif=tk.Tk() 
        failnotif.wm_title("Failed entry")
        label=Label(failnotif,text="Incorrect entry \n Please reenter all fields and try again")
        label.pack(side="top",fill="x",pady=15)
        failnotif.mainloop() 
            
         

class loginpage:
    def __init__(self,login):
        self.user_label=Label(login,text="Username",bg="turquoise") 
        self.pass_label=Label(login,text="Password",bg="turquoise")
        self.entry_var=tk.StringVar() 
        self.entry_var1=tk.StringVar()
        self.user_label.place(relx=.4,rely=.5,anchor="center")
        self.pass_label.place(relx=.4,rely=.6,anchor="center")
        self.user_entry=Entry(login,textvariable=self.entry_var)
        self.pass_entry=Entry(login,textvariable=self.entry_var1,show="*")
        self.ok=Button(login,text="Enter",command=self.logincheck) 
        self.ok.place(relx=.7,rely=.7,anchor="center")
        self.user_entry.bind("<Return>",self.logincheck)
        self.pass_entry.bind("<Return>",self.logincheck) 
        self.user_entry.place(relx=.6,rely=.5,anchor="center")
        self.pass_entry.place(relx=.6,rely=.6,anchor="center")
    
    def logincheck(self,*args):
        usercheck=self.user_entry.get() 
        passcheck=self.pass_entry.get()
        usercheck=usercheck.strip() 
        check=False
        check1=False
        with open("userdets.csv","r") as f:
            reader=csv.reader(f,delimiter=",")
            for line in reader:
                if usercheck==line[0]:
                    check=True
                    if passcheck==line[1]:
                        check1=True

        if check and check1==True:
            login.destroy() 
            app=pageoverview() 
            app.geometry("1600x2560")
            app.resizable(0,0)
            app.title("FCL Grade Forecaster and Markbook")
            app.mainloop()
        else:
            popup=tk.Tk()
            popup.wm_title("Error")
            label=Label(popup,text="Login failed \n Please reenter username and password")
            label.pack(side="top",fill="x",pady=10)
            popup.mainloop() 
        


loginpage(login)
tk.mainloop() 






