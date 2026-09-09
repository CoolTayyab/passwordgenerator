import socket
from pathlib import Path
from googleapiclient.discovery import build

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

CLIENT_SECRET_FILE = "assets/client_secret.json"
TOKEN_FILE = "data/token.json"


def google_login():
    creds = None

    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds


def google_logout():

    if Path(TOKEN_FILE).exists():
        Path(TOKEN_FILE).unlink()


def current_user():

    if Path(TOKEN_FILE).exists():
        return Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    return None
def get_user_info():

    creds = google_login()

    service = build(
        "oauth2",
        "v2",
        credentials=creds
    )

    user = service.userinfo().get().execute()

    return user

def is_logged_in():

    if not Path(TOKEN_FILE).exists():
        return False

    try:

        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

        if creds and creds.valid:
            return True

        return False

    except Exception:
        return False

def is_connected():

    try:

        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        return True

    except OSError:

        return False