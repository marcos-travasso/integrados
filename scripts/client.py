import os
import random

import pandas as pd
import requests


def send_signal(h, g, dimension):
    user = f"user_{random.randint(1, 100)}"

    data = {
        'user': user,
        'model': "cgnr" if random.random() < 0.5 else "cgne",
        'H': h,
        'g': g,
        'dimension': dimension,
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
        print(f"Memory usage: {status['memory_used']} MB")
        print(f"Total memory: {status['memory_total']} MB")
    else:
        print("Error getting server status.")


for i in range(50):
    data_path = os.path.join(os.path.dirname(__file__), "../worker/Data")

    files = {
        "G_1": "G-1.csv",
        "G_2": "G-2.csv",
        "g_1": "g-30x30-1.csv",
        "g_2": "g-30x30-2.csv",
    }

    data = {
        key: [l[0] for l in pd.read_csv(os.path.join(data_path, file), header=None, delimiter=',').values.tolist()]
        for key, file in files.items()
    }

    mapping = {
        1: ("H-1", "G_1", 60),
        2: ("H-1", "G_2", 60),
        3: ("H-2", "g_1", 30),
        4: ("H-2", "g_2", 30),
    }

    random_number = random.randint(1, 4)

    h, g, dimension = mapping[random_number]
    send_signal(h, data[g], dimension)
