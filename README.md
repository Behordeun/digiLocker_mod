# Digital Locker using Ethereum Blockchain

[![Docker Image CI](https://github.com/Behordeun/digiLocker_mod/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Behordeun/digiLocker_mod/actions/workflows/docker-image.yml)

[![wakatime](https://wakatime.com/badge/user/e47dea41-8692-44e5-bd23-27b3544ed664/project/018b9bf5-3291-411c-9653-865e61cc89cb.svg)](https://wakatime.com/badge/user/e47dea41-8692-44e5-bd23-27b3544ed664/project/018b9bf5-3291-411c-9653-865e61cc89cb)

## Disclaimer

The original project belong to [Jai Singhal](https://www.linkedin.com/in/jai-singhal/) and the link to the original project is referenced [here](https://github.com/jai-singhal/digiLocker). I have only improved on the original project by making the following changes:

1. Change the Test Network to Sepolia.
2. Deployed the smart contract on **HardHat** wallet instead of the default **Truffle Wallet**.
3. Introduced a new logic to auto-regenerate the __DropBox__ token if the supplied token had expired. This ensures a continous availability of the project and prevents breakage in the application functionality.
4. Created a Dockerfile for building a docker image off the project for easy setup on different operating systems as well as integrating the application into other projects.
5. Setup CI/CD for continuous deployment of the image upon every update made to the main branch.

## How to setup

### Install the Metamask

Download the metamask extension from: https://metamask.io/

### Ethereum account and network

We have used Sepolia Test network, and deployed the contract on the same network. So to run the application, you may required to get some free ethers from [here](https://sepoliafaucet.com/).

### Clone repository

```powershell
git clone https://github.com/Behordeun/digiLocker_mod.git

# cd to digilocker_mod
cd digiLocker_mod
```

### create virtualenv

The application works better on Python3.9. Hence, it's recommended that you have Python3.9 installed on your machine or you set it up using Docker

```powershell
pip install virtualenv

# create virtualenv in digilocker dir
python3.9 -m virtualenv venv

# activate the virtualenv
## For Linux or MacOS
source venv/bin/activate

## For Windows OS
source venv/Scripts/activate
```

### Install required packages

```powershell
pip install -r requirements.txt
```

### Run the server

```powershell
python main.py
```

## System Design

### Resident Perspective

![Resident](https://i.imgur.com/2Lrcsux.png)

### Requestor Perspective

![Requestor](https://i.imgur.com/QAuXW5V.png)

### Auth Activity digram

![auth](https://i.imgur.com/SjtrkUV.png)

### Document upload and permission Grant Activity digram

![doc](https://i.imgur.com/LeaB6zf.png)

## Configuration

### config.py

Please add the `config.py` to your main directory with your credentials
**Sample config.py**

```python
# config.py
APPCONFIG = {
    "APP_SECRETKEY":"",
    "DROPBOX_KEY":"",
    "DROPBOX_SECRET":"",
    "DROPBOX_ACCESS_TYPE":"scopes",
    "DROPBOX_ACCESS_TOKEN":"",
    "MAIL_USERNAME":"",
    "MAIL_PASSWORD":"",
    "MAIL_DEFAULT_SENDER":"",
    "MAIL_SENDER":"",
    "SECRET_KEY": b"",
    "SERVER_BASE_ADDRESS": "",
    "VERIFICATION_CODES":[
	"12345",
	"other verification codes here"
    ],
    "APPLICATION_HOST":"0.0.0.0",
    "APPLICATION_PORT":"",
    "SEPOLIA_URL":"https://eth-sepolia.g.alchemy.com/v2/{your-sepolia-faucet-accound-id}",
    "PRIVATE_KEY":"your-metamask-wallet-private-key"
}
```
