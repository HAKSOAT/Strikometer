from flask_mail import Mail, Message

mail = Mail()

class Mailer(object):

    def __init__(self, first_name, last_name, email, message):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.message = message


    def send_messages(self):
        msg = Message("Strikometer Reach Out",
                      recipients=["shopejuh@gmail.com"])
        msg.body = "First Name:{} \nLast Name:{} \nEmail:{} \nMessage:{}".format(
            self.first_name, self.last_name, self.email, self.message)
        mail.send(msg)
