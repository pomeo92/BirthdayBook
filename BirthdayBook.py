import pickle
import os
from Tkinter import *
import tkMessageBox
import sqlite3


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
        self._conn = ContactBook.create_db()
        self._cursor = self._conn.cursor()
        self.contacts = self.load_contacts()

    def save_contacts(self):
        with open("contacts.json", "wb") as f:
            pickle.dump(self.contacts, f)
            tkMessageBox.showinfo("Contact saved", "A new contact is saved")

    def save_contact(self, contact):
        try:
            self._cursor.execute(
                '''INSERT INTO Person (name, birthday) VALUES ('%s', '%s');''' % (
                    contact.name, contact.birthday))
            self._conn.commit()
        except sqlite3.IntegrityError as e:
            # Logging. Its normal situation
            print e
        row = self._cursor.execute(
            '''SELECT person_id from Person WHERE name=?''',
            (contact.name, )).fetchone()
        self._cursor.execute(
            '''INSERT INTO Phone_book (phone, person_id) VALUES (?, ?)''', (
            contact.phone, row[0], ))
        self._conn.commit()

    @staticmethod
    def create_db(name="contacts.db"):
        conn = sqlite3.connect(name)
        c = conn.cursor()
        c.execute('''PRAGMA foreign_keys = ON;''')
        c.execute('''
           CREATE TABLE IF NOT EXISTS Person (
               name TEXT NOT NULL UNIQUE,
               birthday TEXT,
               person_id INTEGER PRIMARY KEY AUTOINCREMENT)''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS Phone_book (
                phone TEXT,
                person_id INTEGER,
                phone_id INTEGER PRIMARY KEY AUTOINCREMENT,
                FOREIGN KEY(person_id) REFERENCES Person(person_id))''')
        conn.commit()
        return conn

    def load_contacts(self):
        res = []
        contacts = self._cursor.execute(
            '''SELECT Person.name, Phone_book.phone, Person.birthday from Person, Phone_book''')
        for i in contacts:
            res.append(Contact(i[0], i[1], i[2]))
        return res

    # @staticmethod
    # def load_contact():
    #     if not os.path.isfile("contacts.json"):
    #         return []  # Return an empty list
    #
    #     try:
    #         with open("contacts.json", "rb") as f:
    #             contacts = pickle.load(f)
    #     except Exception as e:
    #         print e
    #         contacts = []
    #
    #     return contacts