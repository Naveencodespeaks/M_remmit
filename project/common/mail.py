from fastapi.responses import JSONResponse
import uuid
import random
import smtplib, ssl
from csv import DictWriter

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
import os
from jinja2 import Environment, FileSystemLoader
#from ..email_templates
from ..constant.status_constant import API_URL 

class Email():

    
    @staticmethod
    def render_html_template(template_path, data):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath(os.path.join(script_dir, '..'))
            template_dir = os.path.join(base_dir, 'email_templates')
            template_name = os.path.basename(template_path)
            env = Environment(loader=FileSystemLoader(template_dir))
            header = env.get_template("header.html")
            body_content = env.get_template(template_name)
            footer_content = env.get_template("footer.html")

            # Render the template with the provided data
            return header.render(data)+body_content.render(data)+footer_content.render(data)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Template file not found: {template_path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while rendering the template: {str(e)}") from e
        
   

    @staticmethod
    def send_mail(recipient_email=[], subject='',body="", template='',data={}):
        
        data["api_base_url"] = f"""{API_URL}media/"""
        sender_email = "alerts@machint.com"
        sender_password = 'Mac&Vel#9904*'
        try:
            # Create the root message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipient_email)

            # Create the body of the message (a plain-text and an HTML version)
            body = data.get("body","")
            if template =="":
                html = f"""
                <html>
                <head>
                    <style>
                        .email-container {{
                            max-width: 600px;
                            margin: auto;
                            padding: 20px;
                            border: 1px solid #ddd;
                            font-family: Arial, sans-serif;
                            background-color: #f9f9f9;
                        }}
                        .header {{
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px;
                            text-align: center;
                        }}
                        .content {{
                            padding: 20px;
                        }}
                        .footer {{
                            text-align: center;
                            font-size: 12px;
                            color: #777;
                            padding: 10px;
                        }}
                        .logo {{
                            display: block;
                            margin-left: auto;
                            margin-right: auto;
                            width: 100px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                        <h1>M-Remmitance</h1>
                            
                            <h1>{subject}</h1>
                        </div>
                        <div class="content">
                            <h3>{str(body)}</h3>
                        </div>
                        <div class="footer">
                            <p>&copy; 2024 Your Company. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
                """
            else:
                html = Email.render_html_template(template_path=template, data=data)

            html = html # render_html_template(template_path=template, data=data)
            # Record the MIME types of both parts - text/plain and text/html
            #part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container
            #msg.attach(part1)
            msg.attach(part2)

            # Send the message via the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            
            print(f"Email sent to {recipient_email}")
            response = "Success"
        except Exception as err:
            print("Error while sending email:", err)
            response = "Failed"
        
        return response
    
    def process_template(template="",data={}):
        pass
        #if(template):

    

