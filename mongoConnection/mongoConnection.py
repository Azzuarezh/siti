import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.chatbox

# Get the intent database
def getIntentCollection(collectionName):
    db = client.chatbox
    collection = getCollection(collectionName)
    document = collection.find({'intentId': {'$exists': True}})
    return document

def getCollection(collectionName):
    db = client.chatbox
    assert isinstance(db[collectionName],object)
    return db[collectionName]

def getIntent(intentName, collectionName):
    db = client.chatbox
    collection = getCollection(collectionName)
    document = collection.find({'intentId': intentName})
    return document;

def findOne(collectionName, criteria):
    db = client.chatbox
    collection = getCollection(collectionName)
    document = collection.find_one(criteria)
    return document
