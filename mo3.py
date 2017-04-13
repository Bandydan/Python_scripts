textfile = open('mo2.txt', 'r')
domfile = open('mo1.txt', 'r')

import re
c = re.compile(r'\w+@\w+.\w+')

tx = (''.join(list(textfile))).rstrip()
df = (', '.join(list(domfile))).rstrip()


lMails = c.findall(tx)
sendTo = []

for l in lMails:
    for d in df:
        if d in l:
            sendTo.append(l)
            break

#print(l)
        
sendTo = (', '.join(sendTo))



import smtplib
         
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()  






