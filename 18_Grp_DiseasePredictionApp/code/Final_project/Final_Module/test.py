import urllib

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
def sendemailtouser(filetosend):   
    fromaddr = "pranalibscproject@gmail.com"
    toaddr = "pranalibscproject@gmail.com"
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "Drowsiness alert"
  
    # string to store the body of the mail 
    body = "Click on this link to verify yourself 'http://localhost:5000/login'"

  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # # open the file to be sent  
    # filename = filetosend
    # attachment = open(filetosend, "rb") 
  
    # # instance of MIMEBase and named as p 
    # p = MIMEBase('application', 'octet-stream') 
  
    # # To change the payload into encoded form 
    # p.set_payload((attachment).read()) 
  
    # # encode into base64 
    # encoders.encode_base64(p) 
   
    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
    # # attach the instance 'p' to instance 'msg' 
    # msg.attach(p) 
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login(fromaddr, "pranalibscproject@123") 
  
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
  
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
    # terminating the session 
    s.quit()    


if __name__=="__main__":

    filetosend = "static/images/1.jpg"
    sendemailtouser(filetosend)
