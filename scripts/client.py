import random
import time

import numpy as np
import requests


for _ in range(5):
    user = f"user_{random.randint(1, 1000)}"
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
    time.sleep(random.randint(1, 5))
