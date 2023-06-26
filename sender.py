import queue
import threading

from network.net import net
from client.gui import gui

# GUI events queue (gui -> net)
eventQueue = queue.Queue()

# Connection state queue (net -> gui)
stateQueue = queue.Queue()
# Logs queue (net -> gui)
logQueue = queue.Queue()


guiThread = threading.Thread(
    target=gui, args=(stateQueue, eventQueue, logQueue,))
netThread = threading.Thread(
    target=net, args=(stateQueue, eventQueue, logQueue,))

guiThread.start()
netThread.start()

guiThread.join()
eventQueue.put('exit')
netThread.join()
