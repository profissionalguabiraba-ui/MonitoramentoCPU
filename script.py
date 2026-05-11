from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import threading
import time

app = Flask(__name__)
CORS(app)

# Variáveis globais para armazenar dados
cpu_data = {
    "percent": 0,
    "cores": 0,
    "process_count": 0,
    "memory_percent": 0,
    "timestamp": 0
}

def update_cpu_data():
    """Atualiza dados de CPU continuamente"""
    while True:
        try:
            cpu_data["percent"] = psutil.cpu_percent(interval=1)
            cpu_data["cores"] = psutil.cpu_count(logical=False)
            cpu_data["process_count"] = len(psutil.pids())
            cpu_data["memory_percent"] = psutil.virtual_memory().percent
            cpu_data["timestamp"] = time.time()
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
        time.sleep(1)

@app.route('/api/cpu', methods=['GET'])
def get_cpu_data():
    """Retorna dados de CPU em JSON"""
    return jsonify(cpu_data)

@app.route('/health', methods=['GET'])
def health_check():
    """Verifica se o servidor está rodando"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Inicia thread para atualizar dados de CPU
    update_thread = threading.Thread(target=update_cpu_data, daemon=True)
    update_thread.start()
    
    print("Servidor rodando em http://localhost:5000")
    print("Dashboard disponível em http://localhost:5000")
    
    # Roda o servidor Flask
    app.run(debug=False, host='localhost', port=5000)
