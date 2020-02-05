from service_functions import sendData 
import datetime
import random
now = datetime.datetime.now()


for i in range(0,24):
    for j in range(0,5):
        date=str(now.strftime("%Y-%m-%d %H:%M:%S"))
        interval=random.randint(40,60)
        si=random.randint(90,110)
        fi=random.randint(40,60)
        sendData(j,interval,date,si,fi)


