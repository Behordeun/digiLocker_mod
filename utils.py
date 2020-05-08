from eth_utils import is_hex_address
from web3.auto import w3
from eth_account.messages import defunct_hash_message
from flask_mail import Mail, Message
import binascii
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes

def recover_to_addr(token, signature):
    msghash = defunct_hash_message(text=token)
    address = w3.eth.account.recoverHash(msghash, signature=signature)
    res = is_hex_address(address)
    return address

def generateRSAKeypair():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return public_key, private_key

def prepareMailMsg(name, from_mail, address, pub, pr, master_key, MAIL_SENDER):
    msgHtml = f"""
        <html>
        <head><title>Welcome To DigiLocker</title></head>
        <body>
        <p> Hello {name} <br />
        Congrats. Your account has been created in Digilocker. Here are the details: </p>
        <table>
        <tr><td>Account Address</td><td>{address}</td></tr>
        <tr><td>Master key</td><td>{master_key}</td></tr>
        </table>
        <p><br>PFA the Public key and private key
        Don't share these credentials with anyone, keep it with you<br></p>
        <p>Best<br>Digilocker Team</p>
        </body>
        </html>
    """
    msg = Message(
        recipients=[from_mail.strip(),],
        sender = MAIL_SENDER
    )
    msg.html = msgHtml
    msg.subject = "Account Created Successfully"
    msg.attach(
        "pub.key",
        'application/octect-stream',
        pub
    )
    msg.attach(
        "pr.key",
        'application/octect-stream',
        pr
    )
    return msg



def getKey(total_doc, masterKey, user_address):
    salt = user_address.encode()
    masterKey = masterKey.encode()
    keys = PBKDF2(masterKey, salt, 128*(total_doc+1), count=10000, prf= None)
    keys = binascii.hexlify(keys)
    key = keys[total_doc*128:(total_doc+1)*128]
    return key.decode()