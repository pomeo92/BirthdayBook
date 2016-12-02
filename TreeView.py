import datetime
import Tkinter as tk
from Tkinter import *
import tkMessageBox

import ttk

import BirthdayBook
from BirthdayBook import Contact
import notifier


class CustomWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.connection = None
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        """When you click to exit, this function is called"""
        self.connection.commit()
        self.connection.close()
        self.destroy()


class App(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.create_ui()
        self.name = StringVar()
        self.phone = StringVar()
        self.birthday = StringVar()
        self.book = BirthdayBook.ContactBook()

        self.load_table()
        self.grid(sticky=(tk.N, tk.S, tk.W, tk.E), columnspan=8)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        Label(parent, text="Name").grid(row=1, column=0, sticky=W)
        Entry(parent, textvariable=self.book.name, width=20).grid(row=1,
                                                                  column=1)

        Label(parent, text="Phone").grid(row=1, column=2, sticky=W)
        Entry(parent, textvariable=self.book.phone, width=20).grid(row=1,
                                                                   column=3)

        Label(parent, text="Birthday").grid(row=1, column=4, sticky=W)
        Entry(parent, textvariable=self.book.birthday, width=20).grid(
            row=1, column=5)
        Button(parent, text="Add",
               command=self.process_add).grid(row=1, column=6)

        Button(parent, text="Delete",
               command=self.process_delete).grid(row=1, column=7)

        notifier_obj = notifier.Notifier(self.book.contacts)
        notifier_obj.notifier_thread.start()

    def validate(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            return False
        return True

    def process_add(self):
        if not self.validate(self.book.birthday.get()):
            tkMessageBox.showinfo("Contact not saved",
                                  "Incorrect data format, it should be YYYY-MM-DD")
            return
        contact = Contact(name=self.book.name.get(), phone=self.book.phone.get(),
                          birthday=self.book.birthday.get())
        self.book.contacts.append(contact)
        self.book.save_contact(contact)
        self.update_tabel()

    def process_delete(self):
        current_name = str(self.treeview.item(self.treeview.focus())["text"])
        current_phone = str(self.treeview.item(
            self.treeview.focus())["values"][0])
        current_birthday = str(self.treeview.item(
            self.treeview.focus())["values"][1])
        for i in self.book.contacts:
            if (i.name == current_name and i.phone == current_phone and
                        i.birthday == current_birthday):
                self.book.contacts.remove(i)
        self.book.save_contacts()
        self.update_tabel()

    def create_ui(self):
        tv = ttk.Treeview(self)
        tv['columns'] = ('phone', 'birthday')
        tv.heading("#0", text='name', anchor='center')
        tv.column("#0", anchor="center", width=70)
        tv.heading('phone', text='phone')
        tv.column('phone', anchor='center', width=70)
        tv.heading('birthday', text='birthday')
        tv.column('birthday', anchor='center', width=70)

        tv.grid(sticky = (tk.N,tk.S,tk.W,tk.E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def update_tabel(self):
        self.book.load_contacts()
        for i in self.treeview.get_children():
            self.treeview.detach(i)
        for i, contact in enumerate(self.book.contacts):
            self.treeview.insert('', 'end', text=contact.name, values=(
                contact.phone, contact.birthday))

    def load_table(self):
        self.update_tabel()


def main():
    root = CustomWindow()
    root.resizable(0, 0)
    app = App(root)
    root.connection = app.book._conn
    root.mainloop()

if __name__ == '__main__':
    main()