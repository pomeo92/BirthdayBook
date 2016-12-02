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
        # Cache variable for fast access to contacts avoid qeury to db
        self.contacts = self.load_contacts()

    def save_contact(self, contact):
        show_msg = False
        try:
            self._cursor.execute(
                '''INSERT INTO Person (name, birthday) VALUES ('%s', '%s');''' % (
                    contact.name, contact.birthday))
            self._conn.commit()
            show_msg = True
        except sqlite3.IntegrityError as e:
            # Logging. Its normal situation
            pass
        row = self._cursor.execute(
            '''SELECT person_id from Person WHERE name=?''',
            (contact.name, )).fetchone()
        try:
            self._cursor.execute(
                '''INSERT INTO Phone_book (phone, person_id) VALUES (?, ?)''',
                (contact.phone, row[0], ))
            show_msg = True
        except sqlite3.IntegrityError as e:
            tkMessageBox.showinfo("Contact exists",
                                  "This contact already exists in your book.")
        self._conn.commit()
        self.contacts = self.load_contacts()
        if show_msg :
            tkMessageBox.showinfo("Contact saved", "A new contact is saved")

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
                FOREIGN KEY(person_id) REFERENCES Person(person_id),
                UNIQUE (person_id, phone))''')
        conn.commit()
        return conn

    def load_contacts(self):
        res = []
        contacts = self._cursor.execute(
            '''SELECT Person.name, Phone_book.phone, Person.birthday
            from Person JOIN Phone_book ON Person.person_id=
            Phone_book.person_id''')
        for i in contacts:
            res.append(Contact(i[0], i[1], i[2]))
        return res

    def delete_contact(self, contact):
        row = self._cursor.execute(
            '''SELECT person_id from Person WHERE name=?''',
            (contact.name,)).fetchone()

        self._cursor.execute(
            '''DELETE FROM Phone_book WHERE person_id=? and phone=?''', (
                row[0], contact.phone,))
        self._conn.commit()
        row = self._cursor.execute(
            '''SELECT * from Phone_book WHERE person_id=?''', (
                row[0],)).fetchall()
        if not len(row):
            self._cursor.execute(
                '''DELETE FROM Person WHERE name=?''', (contact.name,))
        self.contacts = self.load_contacts()