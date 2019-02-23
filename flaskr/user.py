from flask_login import UserMixin
from emailer import send_email
import basic as db


class User(UserMixin):
    def __init__(self, k_number):
        self.k_number = k_number
        self.id = k_number
        self.password = None
        self.email_confirmed = False
        self.role = "ADMIN"

        try:
            self.password = db.get_user_hashed_password(k_number)
            self.email_confirmed = bool(db.get_user_data(k_number)["email_confirmed"])

        except Exception as e:
            print("Exeception occured:{}".format(e))
    
    @property
    def is_active(self):
        # user only able to login if email is confirmed
        return self.email_confirmed

    
    def activate(self):
        # activates user account in database
        db.update_students(k_number=str(self.k_number), email_confirmed=True)
