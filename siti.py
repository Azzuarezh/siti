import functools
from intentparser import intentparser as ip
import readjson as rj
import random
import sys
import json
import datetime
from flask_cors import CORS

from flask import (
    request, Response,Flask
)
app = Flask(__name__)

CORS(app)


@app.route('/Api', methods=['POST'])
def getresponsefromsiti():
    allIntent = []
    dbObject = rj.getIntentFromDb('basicConversation')
    for obj in dbObject:
        intentproperties = rj.createDictionary(obj)  # masukan property untuk si intentparser
        intent = ip.intentParser(intentproperties)
        intent.teachWords(obj['teachWords'])  # ajarin kata-katanya
        allIntent.append(intent)

    text = request.json['input'].lower()
    responsetext={}
    temp = []
    for i in allIntent:
        _temp = i.getResult(text)
        try:
            temp.append((_temp['confidence'], _temp['type'], _temp['args']))
        except Exception as e:
            pass
    try:
        candidate = max(temp)
        dbObject = rj.getIntentFromDb('basicConversation')
        for obj in dbObject:
            if candidate[1] == obj['intentId']:
                if candidate[1] == 'TimeFn':
                    typeOfTime = candidate[2]
                    typeOfTime = [item for item in typeOfTime if item[0] == 'scopes'][0][1]
                    now = datetime.datetime.now()
                    strDate = obj['response'][0]
                    dtPlaceholder = ['hari', 'jam']
                    if typeOfTime == ['hari']:
                        responsetext = {'response': strDate.format(dtPlaceholder[0], now.strftime("%A") +
                                                                   " {}".format(now.isoformat()))}
                    else:
                        responsetext = {'response': strDate.format(dtPlaceholder[1],
                                                                 "{}:{}".format(now.hour, now.minute))}
                    del typeOfTime, now
                elif candidate[1] == 'TerminateFn':
                    responsetext = {'response':random.choice(obj['response'])}
                    pass
                    #ini nanti di redirect ke index.html seharusnya, utk sementara di pass aja
                else:
                    responsetext ={'response': random.choice(obj['response'])}
    except Exception as e:
        print("error")
        responsetext = {'response':"error"}

    responsedata = json.dumps(responsetext)
    response = Response(responsedata, status=200, mimetype='application/json')
    return response

if __name__ == "__main__":
    app.run()