from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://pbprdcfapi.apimanagement.br10.hana.ondemand.com:443/v1"

USERS = {
    "Paula": "09823125",
    "Felipe": "0223698",
    "Josimar": "09852606",
    "Ricardo": "02452466",
    "Volnem": "09825630",
    "Sofia": "02485196",
    "Rafael": "02505937",
    "Tiara": "02562563",
    "Rafael Silva": "02564937",
    "Elvira": "40000610"
}


BODY = {
  "client_id": os.getenv("client_id"),
  "client_secret": os.getenv("client_secret"),
  "grant_type": os.getenv("grant_type"),
}

DBNAME=os.getenv("dbname")
USER=os.getenv("user")
PASSWORD=os.getenv("password")
HOST=os.getenv("host")

print(DBNAME, USER, PASSWORD, HOST)