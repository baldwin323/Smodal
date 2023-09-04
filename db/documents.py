
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# mongo setup
client = MongoClient('your-connection-string')
db = client['database-name']

col_documents = db['documents']

def validate_data(doc_data):
    if not isinstance(doc_data, dict):
        raise ValueError("The document data should be a dictionary.")
    # Add more validation rules here as necessary

def save_document(user_api_name, doc_data):
    validate_data(doc_data)

    doc_item = {
        'user_api_name': user_api_name,
        'data': doc_data
    }
    
    try:
        col_documents.insert_one(doc_item)
    except PyMongoError as pe:
        # Handle DB-related error here, possibly re-raise as a custom exception
        print(f"An error occurred while saving the document: {str(pe)}")

def get_documents_by_user(user_api_name):
    try:
        docs = col_documents.find({'user_api_name': user_api_name})
        return [doc for doc in docs]
    except PyMongoError as pe:
        print(f"An error occurred while fetching the document: {str(pe)}")

def get_all_documents():
    try:
        docs = col_documents.find()
        return [doc for doc in docs]
    except PyMongoError as pe:
        print(f"An error occurred while fetching the document: {str(pe)}")

def remove_document(doc_id):
    try:
        col_documents.delete_one({'_id': doc_id})
    except PyMongoError as pe:
        print(f"An error occurred while deleting the document: {str(pe)}")

def update_document(doc_id, doc_data):
    validate_data(doc_data)
    
    try:
        col_documents.update_one({'_id': doc_id}, {"$set": doc_data})
    except PyMongoError as pe:
        print(f"An error occurred while updating the document: {str(pe)}")