from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

# Configuration for registration
UDP_PORT = 53533

def register_with_as(hostname, ip, as_ip, as_port):
    """Register the hostname with the Authoritative Server (AS) via UDP."""
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    response_data = ""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5) 
        sock.sendto(message.encode('utf-8'), (as_ip, int(as_port)))
        data, _ = sock.recvfrom(1024)
        response_data = data.decode('utf-8')
        print(f"Sent registration message to AS: {message}")
    except Exception as e:
        print(f"Error during registration: {e}")
        response_data = f"Error during registration: {e}"
    finally:
        sock.close()
        return response_data

@app.route('/register', methods=['PUT'])
def register():
    """Handles registration of the FS with the Authoritative Server."""
    data = request.json
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    # Check for missing fields
    if not hostname or not ip or not as_ip or not as_port:
        return jsonify({'error': 'Missing parameters'}), 400

    # Register with AS
    message = register_with_as(hostname, ip, as_ip, as_port)
    return jsonify({'message': message}), 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    """Returns the Fibonacci number for a given sequence number X."""
    number = request.args.get('number')
    
    # Validate if number is an integer
    try:
        number = int(number)
        result = compute_fibonacci(number)
        return jsonify({'result': result}), 200
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number, must be an integer'}), 400

def compute_fibonacci(n):
    """Compute the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)