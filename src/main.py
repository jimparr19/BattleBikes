import argparse

# ----------------------------------------------------------------------------





# ----------------------------------------------------------------------------


def parse_mode(value):
    if value != 'client' and value != 'server':
        raise argparse.ArgumentTypeError('mode must be "client" or "server"')


def parse_port(value):
    number = int(value)
    if number < 1024 or number >= 65535:
        raise argparse.ArgumentTypeError('port number must be greater than 1024 and less than 65535')


# ----------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--http_port',
                        type=parse_port,
                        help='Http port number',
                        default=1499)

    parser.add_argument('--tcp_port',
                        type=parse_port,
                        help='Tcp port number',
                        default=1500)

    args = parser.parse_args()

