from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

def query_as_for_ip(hostname, as_ip, as_port):
    """Query the Authoritative Server (AS) to get the IP address of the given hostname."""
    query_message = f"TYPE=A\nNAME={hostname}\n"
    print(f"as_ip: {as_ip}, as_port: {as_port}, query_message: {query_message}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)  # 5-second timeout for the UDP response
        sock.sendto(query_message.encode('utf-8'), (as_ip, int(as_port)))
        data, _ = sock.recvfrom(1024)
        sock.close()
        print(f"data: {data.decode('utf-8')}")
        return data.decode('utf-8')
    except Exception as e:
        print(f"Error querying AS: {e}")
        return None

def parse_as_response(response):
    """Parse the response from the AS to extract the IP address."""
    lines = response.split('\n')
    for line in lines:
        if line.startswith("VALUE="):
            return line.split('=')[1]
    return None

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    """Handles GET requests to retrieve Fibonacci numbers via FS."""
    # Retrieve query parameters
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Check for missing parameters
    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return jsonify({'error': 'Missing parameters'}), 400

    # Query the Authoritative Server (AS) for the IP of the FS
    as_response = query_as_for_ip(hostname, as_ip, as_port)
    if not as_response:
        return jsonify({'error': 'Failed to get response from AS'}), 500

    # Parse the IP address from the AS response
    fs_ip = parse_as_response(as_response)
    if not fs_ip:
        return jsonify({'error': 'Failed to retrieve IP from AS response'}), 500

    # Forward the request to the Fibonacci Server (FS)
    try:
        fs_response = requests.get(f'http://{fs_ip}:{fs_port}/fibonacci', params={'number': number})
        return fs_response.content, fs_response.status_code
    except Exception as e:
        return jsonify({'error': f'Error contacting FS: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)