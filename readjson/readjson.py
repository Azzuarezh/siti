import json
from typing import List, Any, Tuple
import mongoConnection as mongo

import intentparser as ip
import datetime
import random
import re


# buat chatbot, translate list jadi tupple untuk keyword di dalam description
# dan arguments
def createDictionary(jsonobject):
    # hapus _id intentId
    copyjsonobject = dict(jsonobject)
    print("------------")
    for key in copyjsonobject.keys():
        if type(copyjsonobject[key]) is dict:
            # in tree view such as description, keyword,or etc.
            for subkey in copyjsonobject[key]:
                print('\tsubkey : "', subkey, '" | type : ', type(copyjsonobject[key][subkey]))
                if type(copyjsonobject[key][subkey]) is list:
                    # in tree view such as description[args] or description[type]
                    jsonobject[key][subkey] = translateListToTuple(copyjsonobject[key][subkey])

    entriestoremove =('_id', 'intentId', 'response','teachWords')
    list(map(copyjsonobject.__delitem__, filter(copyjsonobject.__contains__, entriestoremove)))
    print("json object : " , copyjsonobject)
    return copyjsonobject



#buat chatbot, translate list jadi tuple
def translateListToTuple(list):
    tmplist: List[Tuple[Any, Any]] = []
    if len(list) > 0:
        for item in list:
            print("\t\t\titem : ",item)
            if item[0].lower() == "required":
                key: int = ip.REQUIRE
            elif item[0].lower() == "optional":
                key: int = ip.OPTIONAL
            else:
                key: int = ip.REGEX

            resulttuple = (key, item[1])
            tmplist.append(resulttuple)
    return tmplist

#buat chatbot
def getIntentFromDb(collectionName):
    listIntenses = mongo.getIntentCollection(collectionName)
    return listIntenses

def cariMakanan(namaMakanan):
    makanan = mongo.findOne('makanan', {'nama': namaMakanan})
    return makanan

def cariMinuman(namaMinuman):
    minuman = mongo.findOne('minuman', {'nama': namaMinuman})
    return minuman

def translateTextToNumber(numberText):
    try:
        number = mongo.findOne('textToNumber', {'keywords': {'$all': [numberText]}})
        return int(number['numberId'])
    except Exception as ex:
        return None

def translateTextToBoolean(text):
    word = mongo.findOne('textToBoolean', {'keywords': {'$all': [text]}})
    return word['value']


def getIntent(namaIntent, collectionName):
    return mongo.getIntent(namaIntent, collectionName)
