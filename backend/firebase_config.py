import firebase_admin
from firebase_admin import credentials, firestore

# get credentials
cred = credentials.Certificate("dev-paste-firebase-adminsdk.json")

# initialize firebase admin once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# create firestore client
db_firestore = firestore.client()