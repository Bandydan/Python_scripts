textfile = open('mo2.txt', 'r')
domfile = open('mo1.txt', 'r')

import re
c = re.compile(r'\w+@\w+.\w+')

tx = (''.join(list(textfile))).rstrip()
df = (', '.join(list(domfile))).rstrip()


lMails = c.findall(tx)
send_to = []

for l in lMails:
    for d in df:
        if d in l:
            send_to.append(l)
            break


print('Email program says "Hello!" :)')
print()

from_addr = input('Enter your own e-address: ')
cc_addr_list = from_addr
print()

subject = input('Enter the subject: ')
message = input('Enter your message: ')
print()

login = input('Ok! Now enter your email login: ')
password = input('...and password: ')

print()
print('...sending your mail...')

import smtplib
def sendemail(from_addr, send_to, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ', '.join(send_to)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, send_to, message)
    server.quit()  


sendemail(from_addr, send_to, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587')



