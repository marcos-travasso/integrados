import os
import random
from time import sleep

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import pandas as pd
import requests

data_user = []

def send_signal(h, g, dimension):
    rand_number = random.randint(1, 100)
    user = f"user_{rand_number}"

    data = {
        'user': user,
        'model': "cgnr" if random.random() < 0.5 else "cgne",
        'H': h,
        'g': g,
        'dimensions': dimension,
    }

    response = requests.post('http://localhost:8080/rebuild', json=data)
    if response.status_code != 200:
        print("Error processing image.")

    monitor_performance(response, data)
    while get_rebuild(response.json()['id'])['status'] != "finished":
        print('=============')
        sleep(1)
        monitor_performance(response, data)
    print('=============')
    print(get_rebuild(response.json()['id']))

def monitor_performance( response_rebuild, data_full):
    response = requests.get('http://localhost:8080/status')
    if response.status_code == 200:
        rebuild = response_rebuild.json()
        status = response.json()
        print(f"CPU use: {status['cpu_percent']}%")
        print(f"Memory usage: {status['memory_used']} MB")
        print(f"Total memory: {status['memory_total']} MB")
        data = {
            "id": rebuild['id'],
            "cpu_percent": status['cpu_percent'],
            "memory_used": status['memory_used'],
            "memory_total": status['memory_total'],
            "model": data_full['model'],
            "dimensions": data_full['dimensions']
        }
        data_user.append(data)
    else:
        print("Error getting server status.")

def get_rebuild(image_id):
    response = requests.get(f'http://localhost:8080/rebuild/{image_id}')
    return response.json()

# def generate_pdf(image_paths, output_pdf):
#     """Gera um PDF com várias imagens e seus dados correspondentes"""
    
#     c = canvas.Canvas(output_pdf, pagesize=letter)
#     width, height = letter  # Tamanho da página

#     for image_path in image_paths:
#         # Gerando um número aleatório e criando o ID do usuário
#         numero_aleatorio = random.randint(1, 100)
#         user = f"user_{numero_aleatorio}"

#         # Obtendo os dados do servidor
#         status = monitor_performance()
#         if status:
#             user_data = {
#                 "id": user,
#                 "cpu_percent": status['cpu_percent'],
#                 "memory_used": status['memory_used'],
#                 "memory_total": status['memory_total']
#             }
#         else:
#             user_data = {
#                 "id": user,
#                 "cpu_percent": "N/A",
#                 "memory_used": "N/A",
#                 "memory_total": "N/A"
#             }

#         # Adicionando imagem ao PDF
#         img = ImageReader(image_path)
#         img_width, img_height = img.getSize()
#         aspect = img_height / img_width  # Mantendo proporção
        
#         max_width = width - 100
#         max_height = height - 200  # Reservando espaço para texto
        
#         if img_width > max_width or img_height > max_height:
#             img_width = max_width
#             img_height = max_width * aspect
        
#         c.drawImage(img, 50, height - img_height - 50, width=img_width, height=img_height)

#         # Adicionando texto abaixo da imagem
#         text_y_position = height - img_height - 70
#         c.setFont("Helvetica", 12)
#         c.drawString(50, text_y_position, f"ID: {user_data['id']}")
#         c.drawString(50, text_y_position - 20, f"CPU Uso: {user_data['cpu_percent']}%")
#         c.drawString(50, text_y_position - 40, f"Memória Usada: {user_data['memory_used']} MB")
#         c.drawString(50, text_y_position - 60, f"Memória Total: {user_data['memory_total']} MB")

#         # Adicionando uma nova página se houver mais imagens
#         c.showPage()

#     # Salvando o PDF
#     c.save()
#     print(f"PDF '{output_pdf}' criado com sucesso!")

def generate_pdf(data_user, output_pdf):
    """Gera um PDF com imagens e seus dados correspondentes"""

    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter  # Tamanho da página

    for user in data_user:
        image_path = f"gatinho.jpg"  # Supondo que as imagens estejam nesse formato

        try:
            img = ImageReader(image_path)
            img_width, img_height = img.getSize()
            aspect = img_height / img_width  # Mantendo proporção
            
            max_width = width - 100
            max_height = height - 200  # Reservando espaço para texto
            
            if img_width > max_width or img_height > max_height:
                img_width = max_width
                img_height = max_width * aspect
            
            c.drawImage(img, 50, height - img_height - 50, width=img_width, height=img_height)
        except Exception as e:
            print(f"Erro ao carregar imagem {image_path}: {e}")
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 100, f"Imagem não encontrada: {image_path}")

        # Adicionando os dados abaixo da imagem
        text_y_position = height - img_height - 70
        c.setFont("Helvetica", 12)
        c.drawString(50, text_y_position, f"ID: {user['id']}")
        c.drawString(50, text_y_position - 20, f"CPU Uso: {user['cpu_percent']}%")
        c.drawString(50, text_y_position - 40, f"Memória Usada: {user['memory_used']} MB")
        c.drawString(50, text_y_position - 60, f"Memória Total: {user['memory_total']} MB")
        c.drawString(50, text_y_position - 80, f"Modelo: {user['model']}")
        c.drawString(50, text_y_position - 100, f"Dimensões: {user['dimensions']}")

        # Nova página se houver mais imagens
        c.showPage()

    c.save()
    print(f"PDF '{output_pdf}' criado com sucesso!")


output_pdf = "relatorio.pdf"


for i in range(1):
    # generate_pdf(data_user, output_pdf)
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


