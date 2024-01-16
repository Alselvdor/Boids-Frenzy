import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter,Or

cred = credentials.Certificate("path/to/your/credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_data_docs(collection_name):
    # Reference to the Firestore collection
    collection_ref = db.collection(collection_name)

    # Query to get documents where the "Direction" field exists
    query = collection_ref.where("Direction", ">", "")

    # Get documents based on the query
    documents = query.stream()

    # Process and print the data
    for document in documents:
        data = document.to_dict()
        print(f"Document ID: {document.id}, Data: {data}")

# Example: Get data from 'Player1' collection
get_data_docs('Player1')