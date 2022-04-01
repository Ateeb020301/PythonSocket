import socket
import random
import time
from _thread import *

# Create a socket at server side with TCP or IP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects or binds the socket with port and IP address
server.bind(('localhost', 4444))

# yh
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# List of my bots, inspiered by Donald duck
bot = ['Ole', 'Dole', 'Doffen', 'Donald']

#List of my verbs
verbs = ["read", "work", "play", "train", "code", "run", "walk", "jump", "see", "glare", "talk"]

#Saves a random encoded verb in a variable
randomverb = random.choice(verbs).encode()
connecting = True  # Run the while loop as long as it is true
iterations = 1

# list of clients connected
clients = []

# list of connected bots
bots = []

print("")


def threadClient(client, iterations):  # client thread started in while loop below
    run = True
    while run:

        if iterations >= 2:
            print(f'Activities that can be chosen from: {verbs}')
            while True:
                sendActivity = input(f"Host: what do you guys think about ")
                if sendActivity in verbs:
                    for connection in clients:
                        connection.send(f'\nRound {iterations}'.encode())
                    for connection in clients:
                        connection.send(sendActivity.encode())
                    print("")
                    break
                else:
                    print(f'\nPlease chose a valid verb from the given list: {verbs}')
                    continue
            run = False
        else:
            client.send(f'\nRound {iterations}'.encode())
            client.send(randomverb)
            run = False

        if len(clients) == 4:# runs only if the four bots are registered
            time.sleep(random.randint(1, 3))#set a timer between the messages
            while True:
                try:
                    for connection in clients:
                        msg = connection.recv(1024).decode('utf-8')# receives message from client and decodes it
                        if msg: # if message is true or contains a message, then print and send to sendToCLient()
                            message = f'{msg}'
                            print(message)
                            sendToClient(message, connection)
                        else:
                            disconnect(connection)
                    iterations += 1
                    break
                except:
                    continue

            if startnewRound(iterations):
                run = True







def sendToClient(msg, connection):
    for conn in clients:# runs a for loop to check client
        if conn != connection:
            conn.send(msg.encode())#sends message to client


# Removes given client from client list
def disconnect(connection):
    if connection in clients:
        clients.remove(connection)


#Starts new rounds on both sides Server and client
#A while loop which runs as long as, the user keeps asking for it
def startnewRound(iterations):
    runRound = True
    while runRound:
        choice = input(f"\nStart round {iterations}: (yes/no)")
        if choice == 'yes': # yes, to continue with a new round
            return True
        elif choice == 'no':# no, to end the rounds and close server
            if len(clients) > 0:
                for connection in clients:
                    connection.send('remove'.encode())
                    disconnect(connection)
                server.close()
                exit()
            else:
                print('There are no connections, server is closing!')
                server.close()
                exit()
            return False
        runRound = False


if startnewRound(iterations):
    connecting = True
elif not startnewRound(iterations):
    connecting = False

space = 0  # Create a space after the 4th print of connection
while connecting:
    try:
        space += 1
        # listens for coonections, 4 is max and the requirement to run the rounds
        server.listen(4)
        client, addr = server.accept() # accepts the TCP connecions

        clients.append(client)
        while True:
            #chooses a random bot from my list of bots
            clientBot = random.choice(bot)
            if clientBot not in bots:
                #appends connection and the bot to the connected bot
                bots.append(clientBot)
                ##appends connection to the client, to know who is connected
                client.send(clientBot.encode())
                break

        if space == 4:
            print(f'Bot {clientBot} connected on {addr}\n')
        else:
            print(f'Bot {clientBot} connected on {addr}')
        start_new_thread(threadClient, (client, iterations))
    except:
        print('Server is closing')
        server.close()
        exit()
