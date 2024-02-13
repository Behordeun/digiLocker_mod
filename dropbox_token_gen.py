#!/usr/bin/env python3

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
from dotenv import load_dotenv

'''
Populate your app key in order to run this locally
'''
load_dotenv()

# Replace these with your app's key and secret
APP_KEY = os.getenv("DROPBOX_KEY")
APP_SECRET = os.getenv("DROPBOX_SECRET")

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')

authorize_url = auth_flow.start()
print(f"1. Go to: {authorize_url}")
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print(f'Error: {e}')
    exit(1)

with dropbox.Dropbox(oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY) as dbx:
    dbx.users_get_current_account()
    print("Successfully set up client!")
    # View the details of the oauth result
    print(f'Access Token  = {oauth_result.access_token}')
    print(f'Account ID    = {oauth_result.account_id}')
    print(f'Refresh Token = {oauth_result.refresh_token}')
    #print(f'Expiration    = {oauth_result.expiration}')
    print(f'Scope         = {oauth_result.scope}')