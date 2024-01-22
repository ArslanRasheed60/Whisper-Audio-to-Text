import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from peewee import FieldFilter

cred = credentials.Certificate('./whisper.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Assuming you have the user_documentid you want to query
user_documentid = 'SinW664QZySxqc2X5XXRuwwhuUp2'

# Reference to the user's AudioData subcollection
audio_data_ref = db.collection('users').document(user_documentid).collection('AudioData')

# Query documents sorted by createdDateTime in descending order
query = audio_data_ref.where(filter=FieldFilter("text", "==", "Pending...")).order_by('createdDateTime', direction=firestore.Query.ASCENDING).get()

# # Loop through the query results and print the document IDs
# for doc in query:
#     print(f'Document ID: {doc.id}')
#     doc_data = doc.to_dict()
#     created_date_time = doc_data.get("createdDateTime")
#     audio_url = doc_data.get("audio")
#     model_type = doc_data.get("modelType")
#     text = doc_data.get("text")
#     print(f"Details:{model_type}, {text}, ")

