from app import app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    app.run(
        host=os.getenv("APPLICATION_HOST"),
        debug=True,
        port=os.getenv("APPLICATION_PORT"),
    )
