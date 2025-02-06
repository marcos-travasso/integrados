import requests
import numpy as np
import random
import time

def send_signal():
    user = f"user_{random.randint(1, 100)}"
    model = {'rows': 60, 'cols': 60}  
    
    H = np.random.rand(3600, 3600).tolist()  
    g = np.random.rand(3600, 1).tolist()

    data = {
        'user': user,
        'model': model,
        'H': H,
        'g': g
    }

    response = requests.post('http://localhost:8080/rebuild', json=data)
    print(response)
    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print("Error processing image.")

def monitor_performance():
    response = requests.get('http://localhost:8080/status')
    print(response)
    if response.status_code == 200:
        status = response.json()
        print(f"CPU use: {status['cpu_percent']}%")
        print(f"Memory usage: {status['memory_used']} bytes")
        print(f"Total memory: {status['memory_total']} bytes")
    else:
        print("Error getting server status.")

for _ in range(5):  
    send_signal()
    monitor_performance()
    time.sleep(random.randint(1, 5))  

