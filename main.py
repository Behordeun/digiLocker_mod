from app import app

if __name__ == "__main__":
    app.run(
        host=app.config["APPLICATION_HOST", "0.0.0.0"],
        debug=True,
        port=app.config["APPLICATION_PORT", 8083],
    )
