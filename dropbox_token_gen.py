#!/usr/bin/env python3

# import os
# from dotenv import load_dotenv
# import dropbox
# import sys
#
# load_dotenv()
#
#
# def get_dropbox_credentials():
#    """
#    Initiates the Dropbox OAuth2 flow to obtain access token.
#    """
#    app_key = os.getenv("DROPBOX_KEY")
#    app_secret = os.getenv("DROPBOX_SECRET")
#
#    auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
#
#    authorize_url = auth_flow.start()
#    print("1. Go to: " + authorize_url)
#    print('2. Click "Allow" (you might have to log in first).')
#    print("3. Copy the authorization code.")
#    auth_code = input("Enter the authorization code here: ").strip()
#
#    try:
#        oauth_result = auth_flow.finish(auth_code)
#        return oauth_result.access_token
#    except AttributeError as e:
#        print(f"Error: {e}")
#        sys.exit(1)
#
#
# def setup_dropbox_client(access_token):
#    """
#    Sets up the Dropbox client using the obtained access token.
#    """
#    dbx = dropbox.Dropbox(access_token)
#
#    try:
#        dbx.users_get_current_account()
#        print("Successfully set up client!")
#    except dropbox.exceptions.AuthError as e:
#        print(f"Authentication error: {e}")
#        sys.exit(1)
#
#
# def main():
#    """_summary_
#    """
#    access_token = get_dropbox_credentials()
#    setup_dropbox_client(access_token)
#    print(f"Access token: {access_token}")
#
#
# if __name__ == "__main__":
#    main()
#

# import dropbox
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
## Replace these with your app's key and secret
# APP_KEY = os.getenv("DROPBOX_KEY")
# APP_SECRET = os.getenv("DROPBOX_SECRET")
#
# flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
# authorize_url = flow.start()
# print("1. Go to: " + authorize_url)
# print('2. Click "Allow" (you might have to log in first).')
# print("3. Copy the authorization code.")
#
# auth_code = input("Enter the authorization code here: ").strip()
# oauth_result = flow.finish(auth_code)
#
# print("Access Token:", oauth_result.access_token)
# print("Refresh Token:", oauth_result)
#

import dropbox

import os
from dotenv import load_dotenv

load_dotenv()

# Your app key and secret from the Dropbox App Console
APP_KEY = os.getenv("DROPBOX_KEY")
APP_SECRET = os.getenv("DROPBOX_SECRET")

# Create a Dropbox OAuth2 flow
auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

# Replace 'your_access_token' and 'your_refresh_token' with the actual tokens
access_token = "your_access_token"
refresh_token = "your_refresh_token"

# Refresh the access token using the refresh token
new_tokens = auth_flow.refresh_access_token(refresh_token)

# Updated access token
updated_access_token = new_tokens.access_token

print(f"Updated Access Token: {updated_access_token}")
