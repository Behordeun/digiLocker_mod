try:
  from config import *
except:
  print("Please include the config.py in the project")

SECRET_KEY = APPCONFIG.get('SECRET_KEY', None)
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB

DROPBOX_KEY = APPCONFIG.get('DROPBOX_KEY', None)
DROPBOX_SECRET = APPCONFIG.get('DROPBOX_SECRET', None)
DROPBOX_ACCESS_TYPE = APPCONFIG.get('DROPBOX_ACCESS_TYPE', None)
DROPBOX_ACCESS_TOKEN = APPCONFIG.get('DROPBOX_ACCESS_TOKEN', None)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = APPCONFIG.get('MAIL_USERNAME', None)
MAIL_PASSWORD = APPCONFIG.get('MAIL_PASSWORD', None)
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_ASCII_ATTACHMENTS = True
MAIL_DEFAULT_SENDER = APPCONFIG.get('MAIL_DEFAULT_SENDER', None)
MAIL_SENDER = APPCONFIG.get('MAIL_SENDER', None)

SERVER_BASE_ADDRESS = APPCONFIG.get('SERVER_BASE_ADDRESS', None)
VERIFICATION_CODES = APPCONFIG.get("VERIFICATION_CODES", None)

APPLICATION_HOST = APPCONFIG.get("APPLICATION_HOST", None)
APPLICATION_PORT = APPCONFIG.get("APPLICATION_PORT", None)

MONGODB_CONNECTION_STRING = APPCONFIG.get("MONGODB_CONNECTION_STRING", None)
MONGODB_DATABASE_NAME = APPCONFIG.get("MONGODB_DATABASE_NAME", None)