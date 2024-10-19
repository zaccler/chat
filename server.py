import socket
import threading

# Настройки сервера
HOST = '127.0.0.1'  # Локальный хост
PORT = 65432        # Порт для прослушивания

# Хранение подключений
clients = []

def handle_client(conn, sms):
    print(f"Подключен клиент: {sms}")
    while True:
        try:
            # Принимаем сообщение от клиента
            data = conn.recv(1024)
            if not data:
                break

            # Пересылаем сообщение другим клиентам
            for client in clients:
                if client != conn:
                    client.sendall(data)
        except ConnectionResetError:
            break

    print(f"Отключен клиент: {sms}")
    clients.remove(conn)
    conn.close()

# Создаем сокет TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Сервер запущен и слушает {HOST}:{PORT}")
    
    while True:
        conn, sms = s.accept()
        clients.append(conn)
        # Запускаем поток для обработки клиента
        thread = threading.Thread(target=handle_client, args=(conn, sms))
        thread.start()
