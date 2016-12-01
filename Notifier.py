import threading
import tkMessageBox


class Notifier(object):

    def __init__(self):
        self.notifier_thread = threading.Thread(target=self.check_events())

    def check_events(self):
        pass

    def notify(self):
        msg = "A new contact is saved"
        tkMessageBox.showinfo("Today birthdays", msg)