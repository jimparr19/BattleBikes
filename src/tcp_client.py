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


# ***This is where the sensor sampling code needs to go!***
def sample_sensor():
    print("Sampling sensor")
    return bytes([1])


class PeriodicEvent:
    def __init__(self, function):
        self.last_exec = 0.0
        self.period = 1.0
        self.func = function

    def poll(self, now):
        diff = (now - self.last_exec)

        if diff >= self.period:
            self.last_exec = now
            return self

        return None

    def exec(self):
        return self.func()


def main_loop():
    # TODO: this requires that the tcp serer is already running otherwise the
    # connection will fail and the program will exit. We should attempt to 
    # reconnect at regular intervals.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 1500))

    # PeriodicEvent is really just a way of handling a function that you want
    # call periodically without cluttering the mainloop. Defaults to 1 second.
    # You should 'poll' it every loop iteration and it will tell you if its
    # time to execute the function.
    sample = PeriodicEvent(sample_sensor)

    while True:
        data = None
        if sample.poll(time.time()):
            data = sample.exec()

        if data:
            client_socket.send(data)
            pass

        if TERMINATE:
            break

        # You can slow down the mainloop by introducing a sleep.
        # time.sleep(0.5)

    print("***Terminated TCP Client***")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main_loop()