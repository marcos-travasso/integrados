import requests
import numpy as np
import random
import time
from PIL import Image
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import os

def send_signal(h, g, row, column):
    user = f"user_{random.randint(1, 100)}"
    model = {'rows': row, 'cols': column}  
    
    H = np.random.rand(3600, 3600).tolist()  
    g = np.random.rand(3600, 1).tolist()

    data = {
        'user': user,
        'model': model,
        'H': h,
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
    data_path = os.path.join(os.path.dirname(__file__), "../worker/Data")

    files = {
        "H_1": "H-1.csv",
        "G_1": "G-1.csv",
        "G_2": "G-2.csv",
        "G_3": "A-60x60-1.csv",
        "H_2": "H-2.csv",
        "g_1": "g-30x30-1.csv",
        "g_2": "g-30x30-2.csv",
        "g_3": "A-30x30-1.csv",
    }

    data = {
        key: pd.read_csv(os.path.join(data_path, file), header=None, delimiter=',').values.tolist()
        for key, file in files.items()
    }

    mapping = {
        1: ("H_1", "G_1", 60, 60),
        2: ("H_1", "G_2", 60, 60),
        3: ("H_1", "G_3", 60, 60),
        4: ("H_2", "g_1", 30, 30),
        5: ("H_2", "g_2", 30, 30),
        6: ("H_2", "g_3", 30, 30),
    }

    random_number = random.randint(1, 6) 

    if random_number in mapping:
        h, g, row, column = mapping[random_number]
        send_signal(data[h], data[g], row, column)
