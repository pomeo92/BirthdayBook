import pickle
import os
from Tkinter import *
import tkMessageBox
import notifier


class Contact(object):

    def __init__(self, name, phone, birthday):
        self.name = name
        self.phone = phone
        self.birthday = birthday


class ContactBook(object):

    def __init__(self):

        self.name = StringVar()
        self.phone = StringVar()
        self.birthday = StringVar()
        print 222
        self.contacts = self.load_contact()
        print 222
        notifier_obj = notifier.Notifier(self.contacts)
        print 222
        notifier_obj.notifier_thread.start()

    def save_contact(self):
        with open("contacts.json", "wb") as f:
            pickle.dump(self.contacts, f)
            tkMessageBox.showinfo("Contact saved", "A new contact is saved")

    def load_contact(self):
        if not os.path.isfile("contacts.json"):
            return []  # Return an empty list

        try:
            with open("contacts.json", "rb") as f:
                contacts = pickle.load(f)
        except Exception as e:
            print e
            raise e
            contacts = []

        return contacts