import firebase_admin
from firebase_admin import credentials, db
import json

# Path to your Firebase service account JSON file
service_account_file = 'boidsfrenzy.json'

# Initialize Firebase with your service account
cred = credentials.Certificate(service_account_file)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://player2-controller.firebaseio.com/'
})

# Reference to the root of your Firebase Realtime Database
ref = db.reference('/')

def callback(event):
    # This callback will be triggered when data changes in the database
    data = event.data
    print("\nData from Firebase Realtime Database:")
    print(json.dumps(data, indent=2))

# Set up the callback for data changes
ref.listen(callback)

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nTerminating the script.")
    firebase_admin.delete_app(firebase_admin.get_app())
