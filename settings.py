#try:
#  from config import *
#except:
#  print("Please include the config.py in the project")

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', None)
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB

DROPBOX_KEY = os.getenv('DROPBOX_KEY', None)
DROPBOX_SECRET = os.getenv('DROPBOX_SECRET', None)
DROPBOX_ACCESS_TYPE = os.getenv('DROPBOX_ACCESS_TYPE', None)
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

SERVER_BASE_ADDRESS = os.getenv('SERVER_BASE_ADDRESS', None)
VERIFICATION_CODES = os.getenv("VERIFICATION_CODES", None)

APPLICATION_HOST = os.getenv("APPLICATION_HOST", None)
APPLICATION_PORT = os.getenv("APPLICATION_PORT", None)

SEPOLIA_URL = os.getenv('SEPOLIA_URL', None)
PRIVATE_KEY = os.getenv('PRIVATE_KEY', None)
