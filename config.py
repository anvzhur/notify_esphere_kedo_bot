import os

from dotenv import load_dotenv

load_dotenv()

KEDO_API_KEY_KDP = os.getenv("KEDO_API_KEY_KDP")
KEDO_API_KEY_ADM = os.getenv("KEDO_API_KEY_ADM")
URLPLATFORM = os.getenv("URLPLATFORM")
host = os.getenv("PGHOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_DATABASE = os.getenv("PG_DATABASE")
TOKEN = os.getenv("TOKEN")

admins = [
    os.getenv("ADMIN_ID"),
]

kdp_list = os.getenv("KDP_ID").split((','))


