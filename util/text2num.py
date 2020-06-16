import re
import json

singleDigit = {
    'nol': 0,
    'satu': 1,
    'dua': 2,
    'tiga': 3,
    'empat': 4,
    'lima': 5,
    'enam': 6,
    'tujuh': 7,
    'delapan': 8,
    'sembilan': 9,
    'sepuluh': 10,
    'sebelas': 11,
    'seratus':1_00,
    'seribu':1_000,
    'sejuta':1_000
}

dualDigit = {
    "belas":1_0    
}

multiplier = {
    'puluh':       1_0,
    'ratus':       1_00,        
}

exponent = {
    'ribu':        1_000,
    'juta':        1_000_000,
    'milyar':      1_000_000_000,
    'triliun':     1_000_000_000_000,
    'quadriliun':  1_000_000_000_000_000,
    'quintiliun':  1_000_000_000_000_000_000,
    'sektiliun':   1_000_000_000_000_000_000_000,
    'septiliun':   1_000_000_000_000_000_000_000_000,
    'oktiliun':    1_000_000_000_000_000_000_000_000_000,
    'noniliun':    1_000_000_000_000_000_000_000_000_000_000,
    'desiliun':    1_000_000_000_000_000_000_000_000_000_000_000,
}

ListNumber =[]

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

#read the text words by words, from begining to end
def readword(listWords):
    #if there is no more words left
    if len(listWords) == 0:
       print('no words left')
    else:
        print(listWords , '>',len(listWords))
        word = listWords[0]       
        if len(ListNumber) == 0:
            word = listWords[0]
            if word in singleDigit:
                print(word ,' is single')
                val = (singleDigit[word])             
                objNumber = {
                    "val": val,
                    "previousWord":"",
                    "word":word,
                    "type":"single"
                }
                ListNumber.append(objNumber)
                listWords.pop(0)
                readword(listWords) 
        else:

            if word in singleDigit:
                print(word ,' word is single')
                val = singleDigit[word]
                objNumber ={
                    "val":val,
                    "previousWord": ListNumber[-1]['word'],
                    "word": word,
                    "type":"single"
                }
                listWords.pop(0)
                ListNumber.append(objNumber)
                readword(listWords)

            if word in dualDigit:
                print(word ,' word is dual')
                val = (ListNumber[-1]['val'] + 10 ) 
                objNumber = {
                    "val": val,
                    "previousWord":ListNumber[-1]['word'],
                    "word":word,
                    "type":"dual"
                }

                listWords.pop(0)
                del ListNumber[len(ListNumber)-1]
                ListNumber.append(objNumber)
                readword(listWords)

            if word in multiplier:
                print(word ,' word is multiplier')
                val = multiplier[word]
                objNumber ={
                    "val":val,
                    "previousWord": ListNumber[-1]['word'],
                    "word": word,
                    "type":"multiplier"
                }
                listWords.pop(0)
                ListNumber.append(objNumber)
                readword(listWords)

            if word in exponent:
                print(word ,' word is multiplier')
                val = exponent[word]
                objNumber ={
                    "val":val,
                    "previousWord": ListNumber[-1]['word'],
                    "word": word,
                    "type":"exponent"
                }
                listWords.pop(0)
                ListNumber.append(objNumber)
                readword(listWords)

    objListNumber = ListNumber.copy()           
    return objListNumber

def textToNum(text):
    result=0
    listWords = text.split(" ")
    print("text : ",text)
    print("listWords: ", listWords)
    listToCount = readword(listWords)    
    print(json.dumps(listToCount))
    single = 0
    listToCalculate=[]
    listMultiplier=[]
    listExponent =[]
    for idx,count in enumerate(listToCount):
        if count['type'] =="single" or count['type'] == "dual":
            single = count['val']
            listMultiplier.append(single)
            print('listMultiplier (single): ', listMultiplier)
            #if end of the line, the single value should be append to list exponent
            if idx == len(listToCount) -1:
                listExponent.append(sum(listToCalculate) + single)
        elif count['type'] == "multiplier":
            tempVal = listMultiplier[0] * count['val']
            listMultiplier.clear()
            listMultiplier.append(tempVal)
            print('listMultiplier (multi): ', listMultiplier)
            listToCalculate.append(listMultiplier[0])
            listMultiplier =[]
            print('listToCalculate : ', listToCalculate)
            #if the end of the line, it should be the multiplier value
            if idx == len(listToCount) -1:
                listExponent.append(sum(listToCalculate))
        elif count['type']=='exponent':           
            if idx == len(listToCount) -1:
                
                if len(listToCalculate) == 0:
                    print('listMultiplier (exponent): ', listMultiplier)
                    listExponent.append(sum(listMultiplier) * count['val']) 
                else:    
                    listExponent.append(sum(listToCalculate) * count['val'])
                print('listToCalculate (exponent): ', listToCalculate)                
            else:
                tempVal = listMultiplier[0] * 1
                listMultiplier.clear()
                listMultiplier.append(tempVal)
                listToCalculate.append(listMultiplier[0])
                listExponent.append(sum(listToCalculate * count['val']))
            print('listExponent : ', listExponent)
            listMultiplier.clear()
            listToCalculate.clear()

    result = sum(listExponent)
    listExponent.clear()
    listMultiplier.clear()
    listToCalculate.clear()
    single = 0
    return result
    
if __name__ == "__main__":
    while True:
        text = input('tulis angka dengan kata : ').lower()
        ListNumber.clear()
        print(textToNum(text))