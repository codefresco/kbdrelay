import socket


def connect(url):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = tuple(url.strip().split(':'))
    try:
        connection.connect((host, int(port)))
    except Exception as e:
        return None, f'Unable to connect: {e}'
    return connection, None


def disconnect(connection):
    if connection:
        try:
            connection.close()
        except OSError:
            pass


def send(data, connection):
    try:
        connection.sendall(data)
    except (BrokenPipeError, ConnectionResetError) as e:
        return None, f'Connection lost!: {e}'
    return len(data), None


def recieve(connection):
    try:
        data = connection.recv(256)
        if data == b'':
            connection.close()
            return None, 'Connection closed by server.'
        return data, None
    except ConnectionResetError:
        connection.close()
        return None, 'Connection reset by server.'
    except Exception as e:
        connection.close()
        return None, f'An error occurred while receiving data: {e}'
