from pymongo import MongoClient
from bson import ObjectId
import datetime

class MongoConversationStore:
    def __init__(self, connection_string: str, db_name: str, collection_name: str):
        # Initialize the connection to MongoDB Atlas
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_conversation(self, conversation_id: str, conversation_data: dict) -> str:
        """
        Save a conversation to the collection. If a conversation with the given ID exists, update it.
        
        :param conversation_id: Unique identifier for the conversation.
        :param conversation_data: The conversation data, typically a dictionary with conversation details.
        :return: The ID of the saved or updated conversation.
        """
        conversation_data["_id"] = conversation_id  # Use conversation_id as the document ID
        conversation_data["updated_at"] = datetime.datetime.now()  # Set/update timestamp
        self.collection.update_one({"_id": conversation_id}, {"$set": conversation_data}, upsert=True)
        return conversation_id
    
    def get_all(self):
        return list(self.collection.find())

    def get_conversation(self, conversation_id: str) -> dict:
        """
        Retrieve a conversation by its ID.
        
        :param conversation_id: Unique identifier for the conversation.
        :return: The conversation data as a dictionary, or None if not found.
        """
        return self.collection.find_one({"_id": conversation_id})

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()
