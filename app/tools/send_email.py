import smtplib, ssl, os
from genshi.template import TemplateLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tools import redis_conection
import os

def formarter(token, data):
    reset_password = os.getenv('RESET_PASSWORD', '')
    loader = TemplateLoader('./tools/', auto_reload=True)
    template = loader.load('email_reset_password.html')
    data.update({'token': token, 'reset_password': reset_password})
    rendered_html = template.generate(**data).render('html', doctype='html')
    return rendered_html

async def send_email(receiver_email, data):
    token = await redis_conection.create_email_token(data['samaccountname'])
    if token:
        try:

            message = MIMEMultipart("alternative")
            sender_email = os.getenv('EMAIL_SENDER', '')
            message["Subject"] = "Restablecimiento de contraseña"
            message["From"] = sender_email
            message["To"] = receiver_email
            html_content = formarter(token, data)
            part = MIMEText(html_content, "html")
            message.attach(part)

            port = int(os.getenv('EMAIL_PORT', 465))
            smtp_server = os.getenv('EMAIL_SMTP', 'mail.hospitalposadas.gob.ar')
            password = os.getenv('EMAIL_PASSWORD', '')

            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

        except Exception as e:
            print(f"Error enviando el correo: {e}")
            return False
        return True
