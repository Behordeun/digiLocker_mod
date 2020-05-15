from flask import Flask, escape, request, session, redirect, url_for, jsonify, flash
from flask import render_template
from utils import *
import jwt
import random, os, string
import datetime
from functools import wraps
import settings
import hashlib
import binascii
from flask_mail import Mail
from werkzeug.utils import secure_filename
from base64 import b64decode,b64encode
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey import RSA
# from werkzeug import secure_filename
import dropbox


app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', "docx"])
app.config.from_object(settings)
mail = Mail(app)
dropbox_ = dropbox.Dropbox(app.config["DROPBOX_ACCESS_TOKEN"])
SERVER_BASE_ADDRESS = app.config["SERVER_BASE_ADDRESS"]


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
                print("Exception occured", e)
                return f(None, *args, **kwargs)

        return f(None, *args, **kwargs)
    return decorator

@app.route("/")
@token_required
def index(user_address):
    return render_template("index.html", user_address = user_address)

@app.route("/dashboard", methods=['GET'])
@token_required
def dashboard(user_address = None):
    if not user_address:
        print(request.path)
        return redirect(url_for('index',  next= request.path))
    return render_template("dashboard.html", user_address = user_address)

@app.route("/registration")
@token_required
def registration(user_address):
    if not user_address:
        return redirect(url_for('index',  next= request.path))
    return render_template("registration.html", user_address = user_address)

@app.route('/dashboard/upload/doc', methods=['GET'])
@token_required
def upload_file(user_address):
    if not user_address:
        return redirect(url_for('index',  next= request.path))
    return render_template("upload_doc.html", user_address=user_address)


@app.route('/post/api/upload/doc', methods=['POST'])
@token_required
def upload_file_postapi(user_address):
    if not user_address:
        return jsonify({
            'success': False, 
            "status_code": 401
        })

    if 'total_doc' not in request.form:
        return jsonify({"success": False, "error": "No files uploaded", "status_code": 400})
    
    total_doc = request.form["total_doc"]
    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file", "status_code": 200})
    else:
        try:
            savepath = secure_filename(file.filename)
            savepath = f"/test_dropbox/{user_address}/{savepath}"
            res = dropbox_.files_upload(file.read(), savepath)
        except Exception as e:
            print(e, "error")
            return {"success": False, "error": str(e)}
        return jsonify({"success": True, "redirect_url": "/dashboard", "status_code": 200})


@app.route("/api/user/accesskey", methods = ['POST'])
@token_required
def comparehash_digest(user_address):
    if not user_address:
        return jsonify({
            'success': False, 
            "status_code": 401
        })
    try:
        master_key = request.form['master_key']
        mkeydigest = request.form['mkeydigest']
        is_upload = int(request.form['upload'])

        mkey_digest_new = hashlib.sha256(master_key.strip().encode()).hexdigest()
        if "0x" + mkey_digest_new == mkeydigest:
            result={"valid": True, 'success': True, "status_code": 200}
        else:
            result={"valid": False, 'success': True, "status_code": 200} 

        if is_upload:
            total_doc = request.form['total_doc']
            ekey = getKey(int(total_doc), master_key, user_address)
            result["ekey"] = ekey
            return jsonify(result)
        else:
            return jsonify(result)

    except Exception as e:
        print(e, "Exception in comparehash")
        return jsonify({'success': False, "status_code": 400})   


@app.route("/api/user/registration/", methods = ['POST'])
@token_required
def registration_postapi(user_address):
    try:
        user_address__ = request.form.get("user_address")
        print(user_address, user_address__)
        if not user_address:
            return jsonify({
                'success': False, 
                "status_code": 401
            })

        email = request.form.get("email")
        first_name = request.form.get("first_name")
        utype = request.form.get("utype")
        MAIL_SENDER = app.config["MAIL_SENDER"]

        if utype == "1":
            master_key = request.form.get("master_key")
            last_name = request.form.get("last_name")
            # TODO: ADD MORE PARAMS IN HASH
            mkey_digest = hashlib.sha256((master_key.strip()).encode()).hexdigest()

            msg = prepareMailMsg(f"{first_name} {last_name}", email, user_address, None, None, master_key, MAIL_SENDER)
            mail.send(msg)  

            return {
                'success': True, 
                'redirect_url': "/dashboard",
                "master_key_hash": mkey_digest,
                'error': "Address verification done",
                "status_code": 200
            }

        elif utype == "2":
            mastercode = request.form.get("mastercode")
            if mastercode not in app.config["VERIFICATION_CODES"]:
                return {'success': False, 'error': "Verification code not valid.", "status_code": 400}

            pu, pr = generateRSAKeypair()
            msg = prepareMailMsg(f"{first_name}", email, user_address, pu, pr, None, MAIL_SENDER)
            mail.send(msg)  
            return {
                'success': True, 
                'redirect_url': "/dashboard",
                "pu": pu.decode(),
                "status_code": 200
            }
    except Exception as e:
        print("resgister", e)
        return {
            'success': False, 
            'redirect_url': "/",
            'error': "Address verification failed",
            "status_code": 400
        }


@app.route("/api/login/metamask", methods = ['GET'])
def login_api():
    urandomToken = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(32))
    token = jwt.encode({
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
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


@app.route("/api/get/verify/master/code", methods = ['GET'])
@token_required
def verifyMasterCode(user_address):
    try:
        if request.args.get("master_code", None) in app.config["VERIFICATION_CODES"]:
            return {'success': True, 'valid': True, "status_code": 200}
        else:
            return {'success': True, 'valid': False, "status_code": 200}
    except Exception as e:
        print(e, "xxx")
        return {'success': False, 'error': str(e), "status_code": 400}


@app.route("/api/logout/metamask", methods = ['GET'])
@token_required
def logout(user_address):
    print("logout")
    session.pop("x-access-tokens", None)
    session.pop("user_address", None)
    return {'success': True, 'redirect_url': "/"}


@app.route("/dashboard", methods = ['POST'])
@token_required
def dashboardPost(user_address):
    if not user_address:
        return redirect(url_for('index',  next= request.path))

    uid = request.form.get("uid", None)
    docid = request.form.get("docid", None)
    print(uid, docid)
    if uid:
        return redirect(url_for('searchUser', uid=uid))
    elif docid:
        return redirect(url_for('searchDoc', docid=docid))


@app.route("/search/uid", methods = ["GET"])
@token_required
def searchUser(user_address):
    if not user_address:
        return redirect(url_for('index',  next= request.path))

    if not request.args.get("uid", None):
        return redirect("/dashboard", code= 400)

    return render_template(
        "searchUser.html", 
        user_address = user_address,
        uid = request.args['uid']
    )


@app.route("/search/doc", methods = ["GET"])
@token_required
def searchDoc(user_address):
    if not user_address:
        return redirect(url_for('index',  next= request.path))

    if not request.args.get('docid', None):
        return redirect("/dashboard", code = 400)

    return render_template(
        "searchDoc.html", 
        user_address = user_address,
        docid = request.args['docid']
    )

@app.route("/post/api/send/request/mail", methods = ["POST"])
@token_required
def sendRequestMailToResident(user_address):
    if not user_address:
        return jsonify({
            'success': False, 
            "status_code": 401
        })
    try:
        MAIL_SENDER = app.config["MAIL_SENDER"]
        doc_id = request.form.get("doc_id")
        requester_email = request.form.get("requester_email")
        doc_name = request.form.get("doc_name")
        requester_address = request.form.get("requester_address")
        owner_address = request.form.get("owner_address")
        owner_email = request.form.get("owner_email")
        owner_name = request.form.get("owner_name")
        
        approval_url = f"{SERVER_BASE_ADDRESS}/resident/aproove/doc/?requester={requester_address}&owner={owner_address}&doc_id={doc_id}"
        msg = prepareRequestMail(
            owner_name, 
            owner_email, 
            requester_email, 
            doc_name, 
            approval_url,
            owner_address,
            requester_address,
            MAIL_SENDER
        )
        mail.send(msg)
        return jsonify({'success': True, 'redirect_url': "/dashboard", "status_code": 200})
    except Exception as e:
        return jsonify({'success': False, "error": str(e), "status_code": 400})


@app.route("/post/api/send/aproove/mail", methods = ["POST"])
@token_required
def sendAproovedMailToRequestor(user_address):
    if not user_address:
        return jsonify({
            'success': False, 
            "status_code": 401
        })
    try:
        MAIL_SENDER = app.config["MAIL_SENDER"]
        doc_id = request.form.get("doc_id")
        doc_name = request.form.get("doc_name")
        requester_email = request.form.get("requester_email")
        requester_address = request.form.get("requester_address")
        owner_address = request.form.get("owner_address")
        owner_email = request.form.get("owner_email")
        owner_name = request.form.get("owner_name")
        master_key = request.form.get("master_key")
        req_pub_key = request.form.get("req_pub_key")
        print(request.form)
        pubKeyObj =  RSA.importKey(req_pub_key)  
        cipher = Cipher_PKCS1_v1_5.new(pubKeyObj) 
        encrypted_mkey = cipher.encrypt(master_key.encode())
        encrypted_mkey = binascii.hexlify(encrypted_mkey).decode()

        access_url = f"{SERVER_BASE_ADDRESS}/requestor/doc/access"
        access_url +=  f"?requester={requester_address}&owner={owner_address}"
        access_url += f"&doc_id={doc_id}&ekey={encrypted_mkey}"

        msg = prepareAproovedMail(
            owner_name, 
            owner_email, 
            requester_email, 
            doc_name, 
            access_url,
            owner_address,
            requester_address,
            MAIL_SENDER
        )
        mail.send(msg)
        return jsonify({'success': True, "status_code": 200})
    except Exception as e:
        print(e, "in mail send")
        return jsonify({'success': False, "error": str(e), "status_code": 400})


@app.route("/resident/aproove/doc/", methods = ["GET"])
@token_required
def approoveDoc(user_address):
    if not user_address:
        flash("You must login into the system")
        return redirect(url_for('index', next= "/".join(request.url.split('/')[3:])))

    requester_address = request.args.get('requester', None)
    owner_address = request.args.get('owner', None)
    doc_id = request.args.get('doc_id', None)

    if not requester_address or not owner_address or not doc_id:
        return redirect("/dashboard", code = 400)

    if owner_address != user_address:
        session.pop("x-access-tokens", None)
        session.pop("user_address", None)
        flash("You was logined with different account. Login with current account")
        return redirect(url_for('index', next= "/".join(request.url.split('/')[3:])))

    return render_template(
        "doc_aprooval.html", 
        user_address = user_address,
        requester_address = requester_address,
        owner_address = owner_address,
        doc_id = doc_id,

    )


@app.route('/requestor/doc/access',methods=['GET'])
@token_required
def access_doc(user_address):
    if not user_address:
        flash("You must login into the system")
        return redirect(url_for('index', next= "/".join(request.url.split('/')[3:])))

    print(request.args)
    return render_template("requester_decrypt.html", user_address=user_address)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    # app.run(host="172.18.16.108", debug=True)

