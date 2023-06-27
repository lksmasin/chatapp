import socket
import threading

# IP adresa a port, na kterém bude server naslouchat
HOST = '0.0.0.0'  # Naslouchá na všech dostupných síťových rozhraních
PORT = 8080

# Získání veřejné IP adresy serveru
def get_public_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]
    finally:
        sock.close()
    return ip_address

# Vytvoření socketu pro server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []  # Seznam připojených klientů

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            client.sendall(message.encode())

def handle_client(client_socket, client_address):
    client_name = client_socket.recv(1024).decode()
    welcome_message = f"Vítejte v chatu, {client_name}!"
    client_socket.sendall(welcome_message.encode())
    broadcast(f"{client_name} se připojil do chatu.", sender=client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            broadcast(f"{client_name}: {message}", sender=client_socket)
        except:
            break

    clients.remove(client_socket)
    broadcast(f"{client_name} opustil chat.", sender=client_socket)
    client_socket.close()

# Výpis IP adresy serveru
public_ip = get_public_ip()
print('Server naslouchá na {}:{}'.format(public_ip, PORT))

# Přijetí připojení od klientů
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print('Připojen klient: ', client_address)

    # Spuštění vlákna pro obsluhu klienta
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
