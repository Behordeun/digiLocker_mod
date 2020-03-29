from flask import Flask, escape, request, session, redirect, url_for, jsonify, flash
from flask import render_template
from utils import recover_to_addr
import jwt
import random, os, string
import datetime
from functools import wraps
import settings
# from werkzeug import secure_filename
import dropbox

app = Flask(__name__)
app.config['SECRET_KEY'] = b'OCML3BRawWEUeaxcuKHLpw'
app.config.from_object(settings)

API_KEY = 'your_api_key'
dbx_client = dropbox.Dropbox(API_KEY)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-tokens' in session.keys():
            token = session.get('x-access-tokens')
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"])
                user_address = session.get("user_address")
                return f(user_address, *args, **kwargs)
            except Exception as e:
                print(e)
                return redirect("/")

        return redirect("/")
    return decorator

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
@token_required
def dashboard(user_address = None):
    return render_template("dashboard.html", user_address = user_address)

@app.route("/registration")
@token_required
def registration(user_address):
    return render_template("registration.html", user_address = user_address)

@app.route("/api/register/metamask", methods = ['POST'])
@token_required
def registration_postapi(user_address):
    email = request.form.get("email")
    print(email)
    # send email
    if True:
        return {
            'success': True, 
            'redirect_url': "/dashboard",
            'error': "Address verification done"
        }
    else:
        return {
            'success': False, 
            'redirect_url': "/",
            'error': "Address verification failed"
        }


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route("/api/Upload/Doc", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file_obj = request.files['file']

    if file_obj:
        client = dropbox.client
        filename = file.filename

        # Actual uploading process
        result = client.put_file('/' + filename, file_obj.read())

        path = result['path'].lstrip('/')
        return redirect(url_for('success', filename=path))



@app.route("/api/login/metamask", methods = ['GET'])
def login_api():
    urandomToken = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(32))
    token = jwt.encode({
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'token': urandomToken
        }, 
        app.config['SECRET_KEY']
    ).decode("utf-8")
    session['x-access-tokens'] = token
    return jsonify({"data": token, })

@app.route("/api/login/metamask", methods = ['POST'])
def login_postapi():
    token = session.get('x-access-tokens')
    if not token:
        return {'error': "No login token in session, please request token again by sending GET request to this url",
                'success': False}
    else:
        # session.pop("x-access-tokens", None)
        signature = request.form.get("signature")
        address = request.form.get("address")
        is_registered = request.form.get("newuser")
        session["user_address"] = address
        recovered_addr = recover_to_addr(token, signature)
        if address != recovered_addr:
            return {
                'success': False, 
                'redirect_url': "/",
                'error': "Address verification failed"
            }
        else:
            if is_registered == "false":
                return {'success': True, 'redirect_url': "/registration"}
            else:
                return {'success': True, 'redirect_url': "/dashboard"}


            

@app.route("/api/logout/metamask", methods = ['GET'])
@token_required
def logout(user_address3):
    print("logout")
    session.pop("x-access-tokens", None)
    session.pop("user_address", None)
    return {'success': True, 'redirect_url': "/"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    # app.run(host="172.18.16.108", debug=True)