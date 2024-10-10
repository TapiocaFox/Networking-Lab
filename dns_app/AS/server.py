import socket
import json

# Configuration
HOST = '0.0.0.0'
UDP_PORT = 53533
RECORD_FILE = 'dns_records.txt'

def store_record(name, value, record_type, ttl):
    """Store DNS record in a file."""
    record = {
        'name': name,
        'value': value,
        'type': record_type,
        'ttl': ttl
    }
    with open(RECORD_FILE, 'a') as f:
        f.write(json.dumps(record) + '\n')

def lookup_record(name):
    """Lookup DNS record by name."""
    try:
        with open(RECORD_FILE, 'r') as f:
            for line in f:
                record = json.loads(line.strip())
                if record['name'] == name:
                    return record
    except FileNotFoundError:
        pass
    return None

def handle_request(data, address):
    """Handle UDP request for registration or query."""
    lines = data.decode('utf-8').split('\n')
    if len(lines) >= 2 and lines[0].startswith("TYPE=") and lines[1].startswith("NAME="):
        record_type = lines[0].split('=')[1]
        name = lines[1].split('=')[1]

        if len(lines) == 4 and lines[2].startswith("VALUE=") and lines[3].startswith("TTL="):
            # Registration request
            value = lines[2].split('=')[1]
            ttl = int(lines[3].split('=')[1])
            store_record(name, value, record_type, ttl)
            response = "Registration successful"
            print(f"Registered: {name} with IP {value}")
        else:
            # DNS Query request
            record = lookup_record(name)
            if record:
                response = (
                    f"TYPE={record['type']}\n"
                    f"NAME={record['name']}\n"
                    f"VALUE={record['value']}\n"
                    f"TTL={record['ttl']}\n"
                )
                print(f"Query response: {response}")
            else:
                response = "Record not found"
                print(f"No record found for: {name}")
    else:
        response = "Invalid request format"
    
    # Send the response back to the client
    sock.sendto(response.encode('utf-8'), address)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, UDP_PORT))
print(f"Authoritative Server running on {HOST}:{UDP_PORT}")

# Listen for incoming UDP packets
while True:
    data, address = sock.recvfrom(1024)  # Buffer size of 1024 bytes
    print(f"Received data from {address}")
    handle_request(data, address)