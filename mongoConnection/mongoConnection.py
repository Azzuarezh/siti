import pymongo
from pymongo import MongoClient


client = MongoClient()
db = client.chatbot

# Get the intent database
def getIntentCollection(collectionName):
    collection = getCollection(collectionName)
    document = collection.find({'intentId': {'$exists': True}})
    return document

def getCollection(collectionName):
    assert isinstance(db[collectionName],object)
    return db[collectionName]

def getIntent(intentName, collectionName):
    collection = getCollection(collectionName)
    document = collection.find({'intentId': intentName})
    return document

def findOne(collectionName, criteria):
    collection = getCollection(collectionName)
    document = collection.find_one(criteria)
    return document
