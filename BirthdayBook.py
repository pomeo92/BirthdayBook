import pickle
import os
from Tkinter import *
import tkMessageBox

import Grid


class Contact():

    def __init__(self, name, phone, birthday):
        self.name = name
        self.phone = phone
        self.birthday = birthday


class ContactBook():

    def __init__(self):      
        window = Tk() # Create a window
        window.title("ContactBook") # Set title

        self.name = StringVar()
        self.phone = StringVar()
        self.birthday = StringVar()
                
        frame1 = Frame(window)
        frame1.pack()
        Label(frame1, text = "Name").grid(row = 1, 
            column = 1, sticky = W)
        Entry(frame1, textvariable = self.name,
              width = 40).grid(row = 1, column = 2)
        
        frame2 = Frame(window)
        frame2.pack()
        Label(frame2, text = "Phone").grid(row=1, column=1, sticky=W)
        Entry(frame2, textvariable=self.phone, width=40).grid(row=1, column=2)
            
        frame3 = Frame(window)
        frame3.pack()
        Label(frame3, text = "Birthday").grid(row=1, column=1, sticky=W)
        Entry(frame3, textvariable=self.birthday, width=40).grid(row=1, column=2)
        
        frame4 = Frame(window)
        frame4.pack()
        Button(frame4, text = "Add", 
            command = self.processAdd).grid(row = 1, column = 1)
        btFirst = Button(frame4, text = "First", 
            command = self.processFirst).grid(row = 1, column = 2)
        btNext = Button(frame4, text = "Next", 
            command = self.processNext).grid(row = 1, column = 3)
        btPrevious = Button(frame4, text = "Previous", command = 
            self.processPrevious).grid(row = 1, column = 4)  
        btLast = Button(frame4, text = "Last", 
            command = self.processLast).grid(row = 1, column = 5)

        frame5 = Frame(window)
        frame5.pack()
        Grid.GridTable(parent=frame5, rows=10, columns=3)
          
        self.addressList = self.loadContact()
        self.current = 0
      
        if len(self.addressList) > 0:
            self.setContact()

        window.mainloop() # Create an event loop
        
    def saveContact(self):
        with open("contacts.json", "wb") as f:
            pickle.dump(self.addressList, f)
            tkMessageBox.showinfo("Address saved", "A new contact is saved")
    
    @staticmethod
    def loadContact():
        if not os.path.isfile("contacts.json"):
            return []  # Return an empty list

        try:
            with open("contacts.json", "rb") as f:
                addressList = pickle.load(f)
        except Exception as e:
            print e
            addressList = []

        return addressList
            
    def processAdd(self):
        address = Contact(name=self.name.get(), phone=self.phone.get(),
                          birthday=self.birthday.get())
        self.addressList.append(address)
        self.saveContact()
        
    def processFirst(self):
        self.current = 0
        self.setContact()
    
    def processNext(self):
        if self.current < len(self.addressList) - 1:
            self.current += 1
            self.setContact()
    
    def processPrevious(self):
        pass # Left as exercise
    
    def processLast(self):
        pass # Left as exercise

    def setContact(self):
        self.name.set(self.addressList[self.current].name)
        self.phone.set(self.addressList[self.current].phone)
        self.birthday.set(self.addressList[self.current].birthday)

if __name__ == "__main__":
    ContactBook() # Create GUI