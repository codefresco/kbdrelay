import time
from network.connection import *


def net(stateQueue, eventQueue, logQueue):
    connection = None
    while True:
        item = eventQueue.get()
        if item is None:
            break

        print('Consuming', item)
        if item['cmd'] == 'connect':
            logQueue.put(
                f"Connecting to <font color='#9fef00'>{item['data']}</font>...\n")
            connection, error = connect(item['data'])
            if not error:
                time.sleep(5)
                logQueue.put(f"Connected!\n")
                stateQueue.put(True)
            else:
                logQueue.put(f'{error}\n')
                stateQueue.put(False)

        elif item['cmd'] == 'disconnect':
            disconnect(connection)
            time.sleep(2)
            logQueue.put(f"Disconnected!\n")
            stateQueue.put(False)

        elif item['cmd'] == 'send':
            _, error = send(item['data'], connection)
            if error:
                disconnect(connection)
                logQueue.put(f"{error}\n")
                stateQueue.put(False)
