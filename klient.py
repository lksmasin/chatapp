import socket
import threading
from colorama import init, Fore
from datetime import datetime

# Inicializace modulu colorama pro nastavení barev
init(autoreset=True)

# IP adresa a port serveru
HOST = '192.168.0.100'  # IP adresa serveru, na kterém je spuštěn serverový kód
PORT = 45945

# Vytvoření socketu pro klienta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(Fore.GREEN + message)  # Zelená barva pro přijaté zprávy
        except:
            break

# Spuštění vlákna pro příjem zpráv od serveru
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Zadání uživatelského jména
username = input("Zadejte své uživatelské jméno: ")
client_socket.sendall(username.encode())

print("Připojen do chatu. Pro odhlášení napište /quit.")

while True:
    message = input()

    if message == "/quit":
        break
    elif message == "/help":
        print("Dostupné příkazy:")
        print("/quit - Odhlásit se z chatu")
        print("/help - Zobrazit dostupné příkazy")
        print("/time - Zobrazit aktuální čas")
        print("/info - Zobrazit informace o projektu")
    elif message == "/time":
        current_time = datetime.now().strftime("%H:%M:%S")
        message_with_time = f"Aktuální čas: {current_time}"
        print(Fore.YELLOW + message_with_time)
        client_socket.sendall(message_with_time.encode())
    elif message == "/info":
        info_message = """
        Projekt: Jednoduchý chat 
        Tvůrce: LUKYMAS
        Verze: 0.2
        """
        print(Fore.CYAN + info_message)
    else:
        client_socket.sendall(message.encode())

client_socket.close()
