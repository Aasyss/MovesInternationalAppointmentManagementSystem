# Moves international sample application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Aasyss/MovesInternationalAppointmentManagementSystem.git
$ cd MovesInternationalAppointmentManagementSystem
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ py venv -m venv
```
Staying on MovesInternationalAppointmentSystem
```sh
$ venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv` using python.

Once `pip` has finished downloading the dependencies:
Copy your .env file from the which containd following keys:
SECRET_KEY=

STRIPE_PUBLIC_KEY=

STRIPE_SECRET_KEY=

HOST_EMAIL=

HOST_EMAIL_PASSWORD=

GOOGLE_CLIENT_ID=

GOOGLE_CLIENT_SECRET=


*Note: For my lecturer, I have provided you another file called 'Environment variables.docx' . This file contains the logins and credentials with secret keys for APIs. follow the following steps please:

1. Create `.env` file inside MIAMS folder.
2. Please Input all the credentials like above inside `.env` file

After that, follow the following steps below:
```sh
(venv)$ cd MIAMS
(venv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
