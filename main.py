from app import app
import settings

if __name__ == "__main__":
    app.run(
        host=app.config["APPLICATION_HOST"],
        debug=True,
        #port=app.config["APPLICATION_PORT"],
    )
