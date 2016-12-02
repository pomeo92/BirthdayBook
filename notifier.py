import datetime
import threading
import time
import tkMessageBox


class Notifier(object):

    def __init__(self, contacts):
        self.contacts = contacts
        self.birthday_men = []
        self.notifier_thread = threading.Thread(target=self.check_events)
        self.showed_at = None

    def check_events(self):
        while True:
            self.birthday_men = []
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            if current_date != self.showed_at:
                for i in self.contacts:
                    if i.birthday[5:] == current_date[5:]:
                        self.birthday_men.append(i.name)
                if self.birthday_men:
                    self.notify()
            time.sleep(0.01)

    def notify(self):
        msg = ", ".join(self.birthday_men)
        tkMessageBox.showinfo("Today birthdays", msg)
        self.showed_at = datetime.datetime.now().strftime("%Y-%m-%d")