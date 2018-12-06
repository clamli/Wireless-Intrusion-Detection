import requests
import numpy as np
from threading import Thread

class MyThread(Thread):
    def __init__(self, url, data):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.url = url
        self.data = data
 
    def run(self):
        response = requests.post(self.url, json=self.data)
        if response.ok:
            # print(response.json()) #--> {'temp_1': 100, 'temp_2': 150}
            print(self.getName())

cnt = 0
while True:
    data_from_pi = {'temp_1': [100.5, 100.2], 'temp_2': [23.22, 150.656]}
    thread = MyThread('http://192.168.1.144:5000/pi', data_from_pi)
    thread.setName(cnt)
    thread.start()
    thread.join()
    cnt += 1
    

