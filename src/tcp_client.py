import socket
import time
import signal
import queue


TERMINATE = False


def terminate():
    print("Terminating TCP Client")
    global TERMINATE
    TERMINATE = True


def signal_handler(signal, frame):
    terminate()


def main_loop():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1500))

    while True:
        client_socket.send(b"hello")
        time.sleep(30)

        if TERMINATE:
            break

    print("***Terminated TCP Client***")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main_loop()