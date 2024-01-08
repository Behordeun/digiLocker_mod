import binascii
import datetime
import hashlib
import random
import string
from functools import wraps

import dropbox
import jwt
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.PublicKey import RSA
from dotenv import load_dotenv
from dropbox.exceptions import AuthError
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_mail import Mail, Message

import settings
from utils import *

load_dotenv()

app = Flask(__name__)
app.config.from_object(settings)


ALLOWED_EXTENSIONS = set(
    ["txt", "pdf", "png", "jpg", "jpeg", "gif", "docx", ".py", ".csv", ".xlsx"]
)


mail = Mail(app)
dropbox_ = dropbox.Dropbox(app.config["DROPBOX_ACCESS_TOKEN"])
SERVER_BASE_ADDRESS = app.config["SERVER_BASE_ADDRESS"]


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "x-access-tokens" in session.keys():
            token = session.get("x-access-tokens")
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"])
                user_address = session.get("user_address")
                data_ = data
                return f(user_address, *args, **kwargs)
            except AttributeError as e:
                print("AttributeError occurred", e)
                return f(None, *args, **kwargs)

        return f(None, *args, **kwargs)

    return decorator


@app.route("/")
@token_required
def index(user_address):
    return render_template("index.html", user_address=user_address)


@app.route("/dashboard", methods=["GET"])
@token_required
def dashboard(user_address=None):
    if not user_address:
        flash("You are not authenticated. Please login again!")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))
    return render_template("dashboard.html", user_address=user_address)


@app.route("/registration")
@token_required
def registration(user_address):
    if not user_address:
        flash("You are not authenticated. Please login again!")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))
    return render_template("registration.html", user_address=user_address)


@app.route("/dashboard/upload/doc", methods=["GET"])
@token_required
def upload_file(user_address):
    if not user_address:
        flash("You are not authenticated. Please login again!")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))
    return render_template("upload_doc.html", user_address=user_address)


@app.route("/post/api/upload/doc", methods=["POST"])
@token_required
def upload_file_postapi(user_address):
    if not user_address:
        return jsonify({"success": False, "status_code": 401})
    try:
        if "total_doc" not in request.form:
            return jsonify({"success": False, "error": "No files uploaded", "status_code": 200})

        total_doc = request.form["total_doc"]
        file = request.files["file"]
        docHash = None
        docId = None
        fileContent = None
        try:
            fileContent = file.read().strip()

            if len(fileContent) // (10**6) > 7:
                return {
                    "success": False,
                    "error": "The upload size should be less than 5MB",
                }
            docHash = hashlib.sha256(fileContent).hexdigest()
            docId = hashlib.sha256()
            docId.update(user_address.encode())
            docId.update(docHash.encode())
            docId = docId.hexdigest()
        except AttributeError as e:
            print(e, "dochash")
            return {"success": False, "error": str(e)}

        if file.filename == "":
            return jsonify({"success": False, "error": "No selected file", "status_code": 200})
        elif file.filename.split(".")[-1] not in ALLOWED_EXTENSIONS:
            return jsonify(
                {
                    "success": False,
                    "error": f"Not a valid file type. Valid file are f{str(ALLOWED_EXTENSIONS)}",
                    "status_code": 200,
                }
            )
        else:
            try:
                savepath = docId + "." + file.filename.split(".")[-1]
                savepath = f"/test_dropbox/{user_address}/{savepath}"
                res = dropbox_.files_upload(fileContent, savepath)
            except AttributeError as e:
                print(e, "error")
                return {"success": False, "error": str(e)}

            return jsonify(
                {
                    "success": True,
                    "redirect_url": "/dashboard",
                    "docHash": "0x" + docHash,
                    "docId": "0x" + docId,
                    "status_code": 200,
                }
            )
    except AttributeError as e:
        return jsonify({"success": False, "status_code": 400, "error": str(e)})


@app.route("/api/user/accesskey", methods=["POST"])
@token_required
def comparehash_digest_nd_senddockey(user_address):
    if not user_address:
        return jsonify({"success": False, "status_code": 401})
    try:
        master_key = request.form["master_key"]
        mkeydigest = request.form["mkeydigest"]
        is_upload = int(request.form["upload"])

        mkey_digest_new = hashlib.sha256()
        mkey_digest_new.update(master_key.strip().encode())
        mkey_digest_new.update(app.config["SECRET_KEY"].encode("utf-8"))
        mkey_digest_new = mkey_digest_new.hexdigest()

        if "0x" + mkey_digest_new == mkeydigest:
            result = {"valid": True, "success": True, "status_code": 200}
        else:
            result = {"valid": False, "success": True, "status_code": 200}

        if is_upload:
            total_doc = request.form["total_doc"]
            ekey = getKey(int(total_doc), master_key, user_address)
            result["ekey"] = ekey
            return jsonify(result)
        else:
            return jsonify(result)

    except AttributeError as e:
        print(e, "AttributeError in comparehash")
        return jsonify({"success": False, "status_code": 400})


@app.route("/api/user/registration/", methods=["POST"])
@token_required
def registration_postapi(user_address):
    try:
        user_address__ = request.form.get("user_address")
        if not user_address:
            return jsonify({"success": False, "status_code": 401})

        email = request.form.get("email")
        first_name = request.form.get("first_name")
        utype = request.form.get("utype")
        MAIL_SENDER = app.config["MAIL_SENDER"]

        if utype == "1":
            master_key = request.form.get("master_key")
            last_name = request.form.get("last_name")
            # TODO: ADD MORE PARAMS IN HASH
            mkey_digest = hashlib.sha256()
            mkey_digest.update(master_key.strip().encode())
            mkey_digest.update(app.config["SECRET_KEY"])
            mkey_digest = mkey_digest.hexdigest()

            msg = Message(
                recipients=[
                    email,
                ],
                subject="Account Successfully Created",
                sender=MAIL_SENDER,
            )
            msg.body = f"""
                    Hello, {first_name} {last_name},

                    Welcome to digiLocker. You are now authorized to use digiLocker to store your documents.

                    Your master key is '{master_key}', please keep this email safe as we do not record this information, and are unable to recover it for you.

                    Now, you are in full control of how your documents are shared with users.

                    Regards,
                    Muhammad A.
                    For the digiLocker Team
                """
            mail.send(msg)

            return {
                "success": True,
                "redirect_url": "/dashboard",
                "master_key_hash": mkey_digest,
                "error": "Address verification done",
                "status_code": 200,
            }

        elif utype == "2":
            pu, pr = generateRSAKeypair()
            pu = binascii.hexlify(pu.encode()).decode()
            org_name = request.form.get("org_name")
            msg = Message(
                recipients=[
                    email,
                ],
                subject=f"Hello {org_name}",
                sender=MAIL_SENDER,
            )
            msg.body = f"""
            welcome to digiLocker. Now, your organization can access and verify documents shared by residents. We hope that you'll keep their data protected in line with the appropriate global DPRs.

            Below are your credentials:
            public_key: * '{pu}'

            private_key: * '{pr}'

            Please keep this email safe as we are unable to retrieve these credentials for you.

            Regards,
            Muhammad A.
            For the digiLocker Team
            """
            mail.send(msg)
            return jsonify(
                {
                    "success": True,
                    "redirect_url": "/dashboard",
                    "pu": pu,
                    "status_code": 200,
                }
            )
    except AttributeError as e:
        print("register", e)
        return {
            "success": False,
            "redirect_url": "/",
            "error": "Address verification failed",
            "status_code": 400,
        }


@app.route("/api/login/metamask", methods=["GET"])
def login_api():
    urandomToken = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(32)
    )
    token = jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            "token": urandomToken,
        },
        app.config["SECRET_KEY"],
    ).decode("utf-8")
    session["x-access-tokens"] = token
    return jsonify(
        {
            "data": token,
        }
    )


@app.route("/api/login/metamask", methods=["POST"])
def login_postapi():
    token = session.get("x-access-tokens")
    if not token:
        return {
            "error": "No login token in session, please request token again by sending GET request to this url",
            "success": False,
        }
    else:
        # session.pop("x-access-tokens", None)
        signature = request.form.get("signature")
        address = request.form.get("address")
        is_registered = request.form.get("newuser")
        session["user_address"] = address
        recovered_addr = recover_to_addr(token, signature)
        if address != recovered_addr:
            return {
                "success": False,
                "redirect_url": "/",
                "error": "Address verification failed",
            }
        else:
            if is_registered == "false":
                return {"success": True, "redirect_url": "/registration"}
            else:
                return {"success": True, "redirect_url": "/dashboard"}


@app.route("/api/get/verify/master/code", methods=["GET"])
@token_required
def verifyMasterCode(user_address):
    try:
        if request.args.get("master_code", None) in app.config["VERIFICATION_CODES"]:
            return {"success": True, "valid": True, "status_code": 200}
        else:
            return {"success": True, "valid": False, "status_code": 200}
    except AttributeError as e:
        print(e, "xxx")
        return {"success": False, "error": str(e), "status_code": 400}


@app.route("/api/logout/metamask", methods=["GET"])
@token_required
def logout(user_address):
    print("logout")
    session.pop("x-access-tokens", None)
    session.pop("user_address", None)
    return {"success": True, "redirect_url": "/"}


@app.route("/dashboard", methods=["POST"])
@token_required
def dashboardPost(user_address):
    if not user_address:
        return redirect(url_for("index", next=request.path))

    uid = request.form.get("uid", None)
    docid = request.form.get("docid", None)
    print(uid, docid)
    if uid:
        return redirect(url_for("searchUser", uid=uid))
    elif docid:
        return redirect(url_for("searchDoc", docid=docid))


@app.route("/search/uid", methods=["GET"])
@token_required
def searchUser(user_address):
    if not user_address:
        flash("You are not authenticated. Please login again!")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))
        # return redirect(url_for('index',  next= request.path))

    if not request.args.get("uid", None):
        return redirect("/dashboard", code=400)

    return render_template("searchUser.html", user_address=user_address, uid=request.args["uid"])


@app.route("/search/doc", methods=["GET"])
@token_required
def searchDoc(user_address):
    if not user_address:
        flash("You are not authenticated. Please login again!")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))
        # return redirect(url_for('index',  next= request.path))

    if not request.args.get("docid", None):
        return redirect("/dashboard", code=400)

    return render_template(
        "searchDoc.html", user_address=user_address, docid=request.args["docid"]
    )


@app.route("/post/api/send/request/mail", methods=["POST"])
@token_required
def sendRequestMailToResident(user_address):
    if not user_address:
        return jsonify({"success": False, "status_code": 401})
    try:
        MAIL_SENDER = app.config["MAIL_SENDER"]
        doc_id = request.form.get("doc_id")
        requester_email = request.form.get("requester_email")
        doc_name = request.form.get("doc_name")
        requester_address = request.form.get("requester_address")
        owner_address = request.form.get("owner_address")
        owner_email = request.form.get("owner_email")
        owner_name = request.form.get("owner_name")

        approval_url = f"{SERVER_BASE_ADDRESS}/resident/approve/doc/?requester={requester_address}&owner={owner_address}&doc_id={doc_id}"
        msg = Message(
            recipients=[
                owner_email,
            ],
            subject="Document Request\033[0m",
            sender=MAIL_SENDER,
        )
        msg.body = f"""
            Hello {owner_name}, {requester_email} is requesting access to {doc_name} please review the request and accept/decline the request via {approval_url}"""
        mail.send(msg)
        return jsonify({"success": True, "redirect_url": "/dashboard", "status_code": 200})
    except AttributeError as e:
        return jsonify({"success": False, "error": str(e), "status_code": 400})


@app.route("/post/api/send/approve/mail", methods=["POST"])
@token_required
def sendapprovedMailToRequestor(user_address):
    if not user_address:
        return jsonify({"success": False, "status_code": 401})
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
        req_pub_key = request.form.get("req_pub_key", None)
        docIndex = request.form.get("docIndex")

        docKey = getKey(int(docIndex), master_key, owner_address)
        req_pub_key = binascii.unhexlify(req_pub_key).decode()
        pubKeyObj = RSA.import_key(req_pub_key)

        cipher = Cipher_PKCS1_v1_5.new(pubKeyObj)
        encrypted_mkey = cipher.encrypt(docKey.encode())
        encrypted_mkey = binascii.hexlify(encrypted_mkey).decode()

        access_url = f"{SERVER_BASE_ADDRESS}/requestor/doc/access"
        access_url += f"?requester={requester_address}&owner={owner_address}"
        access_url += f"&doc_id={doc_id}&ekey={encrypted_mkey}"

        msg = Message(
            recipients=[
                requester_email,
            ],
            subject="Request Approved\033[0m",
            sender=MAIL_SENDER,
        )
        msg.body = f"""
            Hello, {owner_name} has approved your request to access {doc_name}, you can now view the document via {access_url}.

            Regards,
            Muhammad A.
            For the digiLocker Team
        """
        mail.send(msg)
        return jsonify({"success": True, "status_code": 200})
    except AttributeError as e:
        print(e, "in mail send")
        return jsonify({"success": False, "error": str(e), "status_code": 400})


@app.route("/resident/approve/doc/", methods=["GET"])
@token_required
def approoveDoc(user_address):
    if not user_address:
        flash("You are not authenticated. Please login again!")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))

    requester_address = request.args.get("requester", None)
    owner_address = request.args.get("owner", None)
    doc_id = request.args.get("doc_id", None)

    if not requester_address or not owner_address or not doc_id:
        return redirect(url_for("index"))

    if owner_address != user_address:
        session.pop("x-access-tokens", None)
        session.pop("user_address", None)
        flash("Not a correct account address, you are logged in with. Try with different account.")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))

    return render_template(
        "doc_aprooval.html",
        user_address=user_address,
        requester_address=requester_address,
        owner_address=owner_address,
        doc_id=doc_id,
    )


@app.route("/requestor/doc/access", methods=["GET"])
@token_required
def access_doc(user_address):
    if not user_address:
        flash("You are not authenticated. Please login again!")
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))

    requester_address = request.args.get("requester", None)
    owner_address = request.args.get("owner", None)
    doc_id = request.args.get("doc_id", None)
    ekey = request.args.get("ekey", None)

    if not requester_address or not owner_address or not doc_id or not ekey:
        flash("Invalid URL")
        return redirect(url_for("index"))

    if requester_address != user_address:
        session.pop("x-access-tokens", None)
        session.pop("user_address", None)
        flash(
            "Not a correct account address, you are logging in with. Try with different account."
        )
        return redirect(url_for("index", next="/".join(request.url.split("/")[3:])))

    return render_template(
        "requester_decrypt.html",
        user_address=user_address,
        requester_address=requester_address,
        owner_address=owner_address,
        doc_id=doc_id,
        ekey=ekey,
    )


@app.route("/api/post/file/comparehash", methods=["POST"])
@token_required
def downloadEncryptedFileNcompareHash(user_address):
    """
    1. Download encrypted file
    2. Compare Hash
    3. Decrypt doc key
    4. Send file back, and key
    """

    if not user_address:
        return jsonify({"success": False, "status_code": 401})
    try:
        doc_id = request.form.get("doc_id")
        dochash = request.form.get("dochash")
        ekey = request.form.get("ekey")
        owner_add = request.form.get("owner_add")
        privKey = request.form.get("privKey")
        doc_name = request.form.get("doc_name")

        # 1. Download encrypted file
        fileData = None
        try:
            # remove 0x from docid
            savepath = doc_id[2:] + "." + doc_name.split(".")[-1]
            savepath = f"/test_dropbox/{owner_add}/{savepath}"
            metadata, fileData = dropbox_.files_download(savepath)
        except AttributeError as e:
            print(e, "error")
            return {"success": False, "error": str(e)}

        # 2. Compare hash
        docHashObtained = "0x" + hashlib.sha256(fileData.content).hexdigest()
        if docHashObtained != dochash:
            return {"success": False, "error": "Corrupted file, dochash not matched"}

        try:
            keyPriv = RSA.importKey(privKey)  # import the private key
            cipher = Cipher_PKCS1_v1_5.new(keyPriv)
        except AttributeError as e:
            print("Key error", str(e))
            return {
                "success": False,
                "error": "Private key is not valid. Please re enter the private key.",
            }

        # 3. Decrypt doc key
        try:
            ekey = binascii.unhexlify(ekey)
            decrypt_text = cipher.decrypt(ekey, None).decode()
        except AttributeError as e:
            print("Key error", str(e))
            return {"success": False, "error": "Private key is not valid"}

        return {
            "success": True,
            "fileData": fileData.content.decode(),
            "decrypt_key": decrypt_text,
            "owner_address": owner_add,
            "doc_name": doc_name,
        }
    except AttributeError as e:
        return {"success": False, "error": str(e)}
