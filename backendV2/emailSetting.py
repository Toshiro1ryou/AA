import smtplib
from email.mime.text import MIMEText



def send_email(subject, body, to_email):
    sender_email = "alikaouia469@gmail.com"
    password = "iugvwosmlngjbqup"  
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls() 
        server.login(sender_email, password)
        server.send_message(msg)
