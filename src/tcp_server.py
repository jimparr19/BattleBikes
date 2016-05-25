import socket
import signal
import time
import select

# tcp_server.py - A blocking TcpServer.
# It is important that when performing blocking operations such as "accept" and
# "recv" that you don't wait for too long for the operation to complete
# otherwise you'll starve the application of processing cycles.
# With this in mind, the minimal time you can wait is 0.001 seconds. Anything
# less get's ignored because the cost of the operating system performing a
# context switch out-weights this time i.e. it is impossible to context switch
# faster than 1/0.001 times a second.
# ----------------------------------------------------------------------------
class TcpServer:
    def __init__(self, port, max_connections=1):
        self.port = port
        self.max_connections = max_connections
        self.active_connections = []

        # create an INET, STREAMing socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(1)
        self.server_socket.settimeout(0.001)

        # TODO: Remove - Just listen on localhost for now.
        ipv4 = '127.0.0.1'

        # bind the socket to a port
        self.server_socket.bind((ipv4, self.port))

        # become a server socket which up to max_connections
        self.server_socket.listen(self.max_connections)

        print('Listening on %s:%d' % (ipv4, self.port))

    def handle_new_connection(self, connection):
        # remember connection is a tuple of (socket, address)
        self.active_connections += [connection]

    def poll_new_connections(self):
        try:
            print('poll_new_connections')
            # accept connections from outside, if there are no connections this
            # statement will terminate after 0.001 seconds because of the
            # settimeout statement in the constructor.
            client_connection = self.server_socket.accept()
            print('got new connection')

            self.handle_new_connection(client_connection)

        except socket.timeout:
            print('.')

    def handle_active_connection(self, connection):
        # this looks a bit weird because select can take a list of sockets to
        # check if they are ready to read and write from but we only have one
        # at the moment.
        # But this is the most efficient way to check if the socket is ready.
        client_socket = connection[0]
        readables, writables, exceptionals = select.select([client_socket], [], [], 0.001)

        for r in readables:
            data = r.recv(1024)
            print(data)

    def poll_active_connections(self):
        print('poll_active_connections')
        for connection in self.active_connections:
            self.handle_active_connection(connection)


TERMINATE = False


def terminate():
    print("Terminating TCP Server")
    global TERMINATE
    TERMINATE = True


def signal_handler(signal, frame):
    terminate()


def main_loop(port=1500, max_connections=1):
    tcp_server = TcpServer(port, max_connections)
    while True:
        tcp_server.poll_new_connections()
        tcp_server.poll_active_connections()

        # it is important to allocate some time to the checking of termination
        # signals i.e. when the user presses Control-C for example.
        if TERMINATE:
            break

        # TODO: Remove - Throttles the main loop for now - makes things easier to debug.
        time.sleep(1)

    print("***Terminated TCP Server***")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main_loop()