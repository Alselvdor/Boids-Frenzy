import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("Creds/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Replace 'your_collection' with the actual collection name
collection_ref = db.collection(u'player1')

# Query the collection, order by a timestamp field, and limit to one document

coderunning = 1
Timestampx_temp = 0
while coderunning:
    doc_ref = collection_ref.document("movements")
    docs_ref = collection_ref.document("movements")
    doc = doc_ref.get()
    docs = docs_ref.get()
    datas = docs.to_dict()
    Timestampx = datas['Timestamp']

    # Check if any documents were retrieved
    if Timestampx != Timestampx_temp:
        if doc.exists:
            # Get the first (and only) document from the result
            
            # Get the data from the document
            data = doc.to_dict()

            # Check if the 'pop' key exists in the document
            if 'Direction' in data:
                direction = data['Direction']
                print(f"Value of 'pop': {direction}")
            else:
                print("No 'pop' key in the document!")
        else:
            print("No documents found in the collection!")
        Timestampx_temp = Timestampx 
