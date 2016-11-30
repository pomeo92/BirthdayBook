import pickle
import os
from Tkinter import *
import tkMessageBox


class Contact():

    def __init__(self, name, phone, birthday):
        self.name = name
        self.phone = phone
        self.birthday = birthday


class ContactBook():

    def __init__(self):

        self.name = StringVar()
        self.phone = StringVar()
        self.birthday = StringVar()

        self.addressList = self.loadContact()

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