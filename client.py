import socket
import threading

# Настройки подключения
HOST = '127.0.0.1'  # IP адрес сервера
PORT = 65432        # Порт, на котором работает сервер

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print("Сообщение от другого клиента:", data.decode())
        except ConnectionResetError:
            print("Соединение с сервером потеряно.")
            break

# Создаем сокет TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Подключено к серверу.")

    # Запускаем поток для приема сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    while True:
        message = input("Введите сообщение: ")
        s.sendall(message.encode())
