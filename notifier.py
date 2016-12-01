import datetime
import threading
import tkMessageBox


class Notifier(object):

    def __init__(self, contacts):
        self.contacts = contacts
        self.birthday_men = []
        self.notifier_thread = threading.Thread(target=self.check_events())

    def check_events(self):
        self.birthday_men = []
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        for i in self.contacts:
            if i.birthday == current_date:
                self.birthday_men.append(i)
        if self.birthday_men:
            self.notify()

    def notify(self):
        msg = ", ".join(self.birthday_men)
        tkMessageBox.showinfo("Today birthdays", msg)