import Tkinter as tk
from Tkinter import *

import ttk

import BirthdayBook
from BirthdayBook import Contact

class App(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.CreateUI()
        self.name = StringVar()
        self.phone = StringVar()
        self.birthday = StringVar()
        self.book = BirthdayBook.ContactBook()

        self.LoadTable()
        self.grid(sticky = (tk.N,tk.S,tk.W,tk.E), columnspan=8)
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)

        Label(parent, text="Name").grid(row=1, column=0, sticky=W)
        Entry(parent, textvariable=self.book.name,
              width=20).grid(row=1, column=1)

        Label(parent, text="Phone").grid(row=1, column=2, sticky=W)
        Entry(parent, textvariable=self.book.phone, width=20).grid(row=1, column=3)

        Label(parent, text="Birthday").grid(row=1, column=4, sticky=W)
        Entry(parent, textvariable=self.book.birthday, width=20).grid(row=1,
                                                                 column=5)
        Button(parent, text="Add",
               command=self.book.processAdd).grid(row=1, column=6)

        Button(parent, text="Delete",
               command=self.processDelete).grid(row=1, column=7)

    def processDelete(self):
        current_name = self.treeview.item(self.treeview.focus())["text"]
        current_phone = self.treeview.item(self.treeview.focus())["values"][0]
        current_birthday = self.treeview.item(self.treeview.focus())["text"][1]
        for i in self.book.addressList:
            if (i.name == current_name and i.name == current_phone and
                        i.name == current_birthday):
                self.book.addressList.remove(i)
        self.book.saveContact()
        self.update_tabel()

    def CreateUI(self):
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
        addressList = BirthdayBook.ContactBook.loadContact()
        for i in self.treeview.get_children():
            self.treeview.detach(i)
        for i, contact in enumerate(addressList):
            self.treeview.insert('', 'end', text=contact.name, values=(
                contact.phone, contact.birthday))

    def LoadTable(self):
        self.update_tabel()

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == '__main__':
    main()