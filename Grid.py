import os
import pickle

import Tkinter as tk

import BirthdayBook
from BirthdayBook import Contact

class GridTable(tk.Tk):

    def __init__(self, parent=None, rows=1, columns=1):
        tk.Tk.__init__(self)
        self.table = SimpleTable(parent, rows=rows, columns=columns)
        self.table.pack(side="top", fill="x")

    def load_data(self, path):
        addressList = BirthdayBook.ContactBook.loadContact()
        for i, contact in enumerate(addressList):
            self.table.set(i, 0, contact.name)
            self.table.set(i, 1, contact.phone)
            self.table.set(i, 2, contact.birthday)


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in xrange(rows):
            current_row = []
            for column in xrange(columns):
                label = tk.Label(self, text="%s/%s" % (row, column),
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in xrange(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == "__main__":
    grid = GridTable(10, 3)
    grid.load_data(path="contacts.json")
    grid.mainloop()