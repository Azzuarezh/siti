import pymongo
from pymongo import MongoClient

dbuser ="mongobitch"
dbpassword="YouShouldBeAwareofThisShit!1!1!"
dbhost ="ds035613.mlab.com"
dbport=35613
dbname="heroku_w4pfm1mj"
client = MongoClient(host=dbhost,port=dbport,username=dbuser, password=dbpassword,authSource=dbname)
db = client.heroku_w4pfm1mj

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
