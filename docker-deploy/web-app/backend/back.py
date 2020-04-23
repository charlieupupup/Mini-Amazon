# email set up
smtp_server = "smtp.gmail.com"
email_port = 587  # For starttls
sender_email = "568.hw1.yh218.yx139@gmail.com"
password = 'QWE123!@#'

# send email to user


def SendEmail(db, packageid):
    global smtp_server
    global email_port
    global sender_email
    global password
    message = 'Your package ' + str(packageid) + ' has been delivered!'
    message = 'Subject: Package Delivered\n\n' + message
    context = ssl.create_default_context()
    receiver_email = GetEmail(db, packageid)
    if receiver_email == -1:
        return
    with smtplib.SMTP(smtp_server, email_port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
