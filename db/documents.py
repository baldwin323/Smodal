
from pymongo import MongoClient

# mongo setup
client = MongoClient('your-connection-string')
db = client['database-name']

col_documents = db['documents']

def save_document(user_api_name, doc_data):
    doc_item = {
        'user_api_name': user_api_name,
        'data': doc_data
    }
    col_documents.insert_one(doc_item)

def get_documents_by_user(user_api_name):
    docs = col_documents.find({'user_api_name': user_api_name})
    return [doc for doc in docs]

def get_all_documents():
    docs = col_documents.find()
    return [doc for doc in docs]

def remove_document(doc_id):
    col_documents.delete_one({'_id': doc_id})
    
def update_document(doc_id, doc_data):
    col_documents.update_one({'_id': doc_id}, {"$set": doc_data})