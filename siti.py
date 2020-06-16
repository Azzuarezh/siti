import functools
from intentparser import intentparser as ip
import readjson as rj
import random
import sys
import json
import datetime
import requests
from flask import send_file, send_from_directory
from flask_cors import CORS

from flask import (
    request, Response,Flask
)
app = Flask(__name__,
static_url_path='',
static_folder='resources')
CORS(app)


@app.route('/image', methods=['GET'])
def getImage():    
    return send_from_directory(app.static_folder+'\\image','cepe.jpg', mimetype='image/jpeg')

@app.route('/Api', methods=['POST'])
def getresponsefromsiti():
    URL_TELEGRAM_BOT='https://api.telegram.org/bot'
    API_TELEGRAM_TOKEN='1193301158:AAHkO-hxofjlEBj5W-3ZnSMRDZEXXDgEcsQ'
    text = request.json['message']['text']
    chatId = request.json['message']['chat']['id']
    print("text : " + text)
    if '/' in text:
        print("this is a command request")        
        responsetext = {'response':"ini command"}
        if '/showmemoney' in text: 

            """r = requests.post(
                URL_TELEGRAM_BOT + API_TELEGRAM_TOKEN + "/sendPhoto", 
                data={
                    'chat_id':chatId, 
                    'caption':'here is your money dude!',
                    'photo':"AgACAgQAAxkDAAOZXtzKulhuIBLWfQftNRgY_uB01MsAAjirMRtXKOxSZ2MG3TEIR5_zPn8jXQADAQADAgADbQADH14CAAEaBA"
                    }
                )"""
            
        responsedata = json.dumps(responsetext)
        response = Response(responsedata, status=200, mimetype='application/json')
    else:
        allIntent = []
        dbObject = rj.getIntentFromDb('basicConversation')
        for obj in dbObject:
            intentproperties = rj.createDictionary(obj)  # masukan property untuk si intentparser
            intent = ip.intentParser(intentproperties)
            intent.teachWords(obj['teachWords'])  # ajarin kata-katanya
            allIntent.append(intent)

        
        print(text)
        responsetext={}
        temp = []
        for i in allIntent:
            _temp = i.getResult(text)
            print('temp : ' , _temp)
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
                        print('type of time', typeOfTime)
                        print('typeof time is jam', typeOfTime == ['jam'])
                        print('typeof time is hari', typeOfTime == ['hari'])
                        now = datetime.datetime.now()
                        strDate = obj['response'][0]
                        dtPlaceholder = ['hari', 'jam']
                        if typeOfTime == ['hari'] or typeOfTime == ['tanggal']:
                            responsetext = {'response': strDate.format(dtPlaceholder[0], now.strftime("%A") +                                                                    " {}".format(now.isoformat()))}
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
            print(e)
            responsetext = {'response':"maaf gak ngerti"}

        if '<user>' in responsetext['response']:
            print('there is <user> placehoder in response. replace it with current name')
            print('firstname ' + request.json['message']['from']['first_name'])
            responsetext['response'] = responsetext['response'].replace("<user>",request.json['message']['from']['last_name'])
        responsedata = json.dumps(responsetext)
        print('responsedata:' +responsedata)
        response = Response(responsedata, status=200, mimetype='application/json')
        
        #testing send to telegram bot
        """r = requests.post(
            URL_TELEGRAM_BOT + API_TELEGRAM_TOKEN + "/sendMessage", 
            data={'chat_id':chatId, 'text':responsetext['response']}
            )"""

    return response

if __name__ == "__main__":
    app.run()