#try:
#    from config import *
#except:
#    print("Please include the config.py in the project")

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = b"Admin__1234" #os.getenv('SECRET_KEY', None)
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB

DROPBOX_KEY = os.getenv('DROPBOX_KEY', None)
DROPBOX_SECRET = os.getenv('DROPBOX_SECRET', None) 
DROPBOX_ACCESS_TYPE = os.getenv('DROPBOX_ACCESS_TYPE', "files.content.write")
SCOPE = os.getenv("SCOPE")
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN', None)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = os.getenv('MAIL_USERNAME', None)
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', None)
MAIL_USE_TLS = False
MAIL_USE_SSL = True 
MAIL_ASCII_ATTACHMENTS = True
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', None)
MAIL_SENDER = os.getenv('MAIL_SENDER', None)
VERIFICATION_CODES = os.getenv("VERIFICATION_CODES", None)
APPLICATION_HOST = os.getenv("APPLICATION_HOST", None)
APPLICATION_PORT = os.getenv("APPLICATION_PORT", None)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", None)
MAILTRAP_API_KEY = os.getenv("MAILTRAP_API_KEY", None)

SERVER_BASE_ADDRESS = f"{APPLICATION_HOST}:{APPLICATION_PORT}"
