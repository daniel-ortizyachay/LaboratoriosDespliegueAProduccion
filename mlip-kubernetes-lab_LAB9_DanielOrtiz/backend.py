# backend.py
from flask import Flask, request
import os

app = Flask(__name__)

# Obtener el identificador único de la instancia desde una variable de entorno
INSTANCE_ID = os.getenv("INSTANCE_ID", "unknown")

@app.route('/')
def home():
    user_id = request.args.get("user_id", "Guest")
    return f"Hello, {user_id}! This response is from instance: {INSTANCE_ID}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
