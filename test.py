from service_functions import makeLists, getAllData
import json

data=getAllData()
with open('response.json', 'w') as f:
    json.dump(data,f)
makeLists('response.json',1)
