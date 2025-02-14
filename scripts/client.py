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

# def create_pdf(image_path, user):
#     """Cria um PDF com a imagem e as informações de desempenho."""
#     pdf_path = f"{user}_report.pdf"
#     c = canvas.Canvas(pdf_path, pagesize=letter)
#     width, height = letter

#     # Adiciona imagem
#     c.drawImage(image_path, 100, height - 300, width=300, height=300)

#     # Adiciona texto
#     text_y = height - 320
#     c.setFont("Helvetica", 12)
#     c.drawString(100, text_y, f"User: {user}")
#     c.drawString(100, text_y - 20, f"CPU Usage: 100%")
#     c.drawString(100, text_y - 40, f"Memory Used: 100 bytes")
#     c.drawString(100, text_y - 60, f"Total Memory: 100 bytes")

#     c.save()
#     print(f"PDF salvo como {pdf_path}")

for _ in range(5):  # Enviar 5 sinais
    data_path = os.path.join(os.path.dirname(__file__), "../worker/Data")

    # Dicionário para armazenar os caminhos dos arquivos
    arquivos = {
        "H_1": "A-60x60-1.csv",
        "G_1": "G-1.csv",
        "G_2": "G-2.csv",
        "G_3": "A-60x60-1.csv",
        "H_2": "A-60x60-1.csv",
        "g_1": "g-30x30-1.csv",
        "g_2": "g-30x30-2.csv",
        "g_3": "A-30x30-1.csv",
    }

    # Carregar todos os arquivos usando os caminhos corretos
    dados = {
        chave: pd.read_csv(os.path.join(data_path, arquivo), header=None, delimiter=',').values.tolist()
        for chave, arquivo in arquivos.items()
    }

    # Mapeamento das combinações possíveis
    mapeamento = {
        1: ("H_1", "G_1", 60, 60),
        2: ("H_1", "G_2", 60, 60),
        3: ("H_1", "G_3", 60, 60),
        4: ("H_2", "g_1", 30, 30),
        5: ("H_2", "g_2", 30, 30),
        6: ("H_2", "g_3", 30, 30),
    }

    random_number = random.randint(1, 6)  # Exemplo: número aleatório entre 1 e 6

    # Verificar se a chave existe antes de chamar a função
    if random_number in mapeamento:
        h, g, largura, altura = mapeamento[random_number]
        print(h,g,largura,altura)
        # send_signal(dados[h], dados[g], largura, altura)
