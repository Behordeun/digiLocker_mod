# Import the needed modules
from app2 import app
# from app import get_dropbox_credentials, setup_dropbox_client


#def main():
#    """_summary_"""
#    access_token = get_dropbox_credentials()
#    setup_dropbox_client(access_token)


if __name__ == "__main__":
    app.run(
        host=app.config["APPLICATION_HOST"],
        debug=True,
        port=app.config["APPLICATION_PORT"],
    )
