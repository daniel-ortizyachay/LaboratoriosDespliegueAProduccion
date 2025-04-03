# load_balancer.py
from flask import Flask, request
import itertools
import requests
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.logger.info("Load balancer is starting...")

# Backend server URL for round-robin distribution
BACKEND_SERVERS = [
    "http://flask-backend-service:5001" 
]

# Round-robin iterator for distributing requests
server_pool = itertools.cycle(BACKEND_SERVERS)

@app.route('/')
def load_balance():
    backend_url = next(server_pool)
    user_id = request.args.get("user_id", "Guest")
    try:
        response = requests.get(f"{backend_url}/", params={"user_id": user_id})
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {e}", 500

if __name__ == '__main__':
    # Running the load balancer on port 5000
    app.run(host='0.0.0.0', port=5000)
