import requests
import json

test=""

def sendData(light_id, interval, date, success_counter, fail_counter):

    url = 'http://127.0.0.1:5000/add/record'
    headers = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}
    data =  {
        'light_id':light_id,
        'interval':interval,
        'date' : date,
        'success_counter' :success_counter,
        'fail_counter': fail_counter
        }
    answer = requests.post(url, data=json.dumps(data),headers=headers)
    return answer

#Get all data from database
def getAllData():
    url = 'http://127.0.0.1:5000/get/all/'
    answer=requests.get(url)
    response = answer.json()
    return response

#Get all data from database by intervals
def getByIntervals(data_from,data_to):
    #data_from=data_from.replace(" ","%")
    #data_to=data_to.replace(" ","%")
    url="http://127.0.0.1:5000/get/bytime?from={}&to={}".format(str(data_from),str(data_to))
    answer = requests.get(url)
    responce = answer.json()
    return responce

def jsonToDict(fname):
    with open(fname, 'r') as f:
        parsed = json.load(f)
    return parsed

def makeLists(fname,light_id):
    responce=jsonToDict(fname)
    data=responce['records']
    date=[]
    success=[]
    fail=[]
    interval=[]
    for i in range(0,len(data)):
        if(data[i]['light_id']==light_id):
            date.append(data[i]['date'])
            success.append(data[i]['success_counter'])
            fail.append(data[i]['fail_counter'])
            interval.append(data[i]['interval'])
    return date,success,fail,interval
