import socket
import time

TERMINATE_TCP_CLIENT = False


def signal_handler(signal, frame):
    global TERMINATE_TCP_CLIENT
    TERMINATE_TCP_CLIENT= True


def main_loop():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1500))

    while True:
        client_socket.send(b"hello")
        time.sleep(30)

        if TERMINATE_TCP_CLIENT:
            break

if __name__ == '__main__':
    main_loop()