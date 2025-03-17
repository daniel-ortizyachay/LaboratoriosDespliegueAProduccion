import requests

url = "http://localhost:3000/api/v1/analysis/"
files = {'image': open('D:\\Proyectos IA\\mlip-api-lab-main_LAB1_DanielOrtiz\\Texto.jpg', 'rb')}

response = requests.post(url, files=files)
print(response.json())