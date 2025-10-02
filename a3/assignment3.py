
import socket
import threading
import argparse
import time

max = 50
n = 100

listlock = threading.Lock()
listnofull = threading.Condition(listlock)
listnoempty = threading.Condition(listlock)

frequencylock = threading.Lock()

inindex = 0
outindex = 0
listupdated = False

class Listnode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.booktitle = None
        self.processed = False

class Linkedlist:
    def __init__(self):
        self.head = None

sharedLinkedlist = Linkedlist()

class Bookfrequency:
    def __init__(self):
        self.title = None
        self.frequency = 0

bookfrequencies = [Bookfrequency() for i in range(max)]

def countpattern(text, pattern):
    return text.count(pattern)

def handleClient(clientSocket, clientid):
    try:
        booktitle = None
        clientdata = b""  
        clientbooklines = []

        while True:
            data = clientSocket.recv(1024)
            if not data:
                break
            clientdata += data  

            while b"\n" in clientdata:
                line, clientdata = clientdata.split(b"\n", 1)
                lineStr = line.decode("utf-8").strip()

                if booktitle is None:
                    booktitle = lineStr  
                    print(f"client {clientid} sent book title: {booktitle}")
                clientbooklines.append(lineStr)

                node = Listnode(lineStr)
                node.booktitle = booktitle

                with listlock:
                    global inindex
                    while (inindex + 1) % n == outindex:
                        listnofull.wait()

                    if sharedLinkedlist.head is None:
                        sharedLinkedlist.head = node
                    else:
                        current = sharedLinkedlist.head
                        while current.next is not None:
                            current = current.next
                        current.next = node

                    inindex = (inindex + 1) % n
                    listnoempty.notify()

        bookFilename = f"book_{clientid:02d}.txt"
        with open(bookFilename, "w", encoding="utf-8") as bookFile:
            for line in clientbooklines:
                bookFile.write(line + "\n")
        print(f"book saved for client {clientid} to {bookFilename}")

    except Exception as e:
        print(f"error handling client {clientid}: {e}")
    finally:
        clientSocket.close()

def analysisThread(pattern):
    lastProcessed = None
    while True:
        with listlock:
            global outindex
            while inindex == outindex:
                listnoempty.wait()

            currentNode = sharedLinkedlist.head if lastProcessed is None else lastProcessed

            while currentNode is not None:
                if not currentNode.processed:
                    matchCount = countpattern(currentNode.data, pattern)
                    if matchCount > 0:
                        with frequencylock:
                            for book in bookfrequencies:
                                if book.title == currentNode.booktitle:
                                    book.frequency += matchCount
                                    break
                            else:
                                for book in bookfrequencies:
                                    if not book.title:
                                        book.title = currentNode.booktitle
                                        book.frequency += matchCount
                                        break

                            global listupdated
                            listupdated = True
                    currentNode.processed = True

                outindex = (outindex + 1) % n
                listnofull.notify()

                lastProcessed = currentNode
                currentNode = currentNode.next

def printFrequencies(pattern):
    global listupdated  
    while True:
        time.sleep(5)
        with frequencylock:
            if listupdated:
                sortedBooks = sorted(bookfrequencies, key=lambda x: -x.frequency)
                for book in sortedBooks:
                    if book.frequency > 0:
                        print(f"Book: {book.title}, Pattern: {pattern}, Frequency: {book.frequency}")
                listupdated = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--port", type=int, required=True)
    parser.add_argument("-p", "--pattern", type=str, required=True)
    args = parser.parse_args()

    host = "localhost"
    port = args.port
    pattern = args.pattern

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(5)

    print(f"server is listening on {host}:{port}")

    for i in range(2):
        threading.Thread(target=analysisThread, args=(pattern,)).start()

    threading.Thread(target=printFrequencies, args=(pattern,)).start()

    clientid = 1
    try:
        while True:
            clientSocket, clientAddress = serverSocket.accept()
            print(f"accepted connection from {clientAddress}")
            threading.Thread(target=handleClient, args=(clientSocket, clientid)).start()
            clientid += 1
    except KeyboardInterrupt:
        print("server interrupted. close server.")
    finally:
        serverSocket.close()

if __name__ == "__main__":
    main()