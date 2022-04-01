import random
import socket

#Connects the client side, using tcp/ip protcol
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connects the client using the socket, to the IP and Port
client.connect(('localhost', 4444))

# Listing of the different verbs the user can use
verbs = ["read", "work", "play", "train", "code", "run", "walk", "jump", "see", "glare", "talk"]

#  Listing of the four Bots i have Allowed
bots = ['Ole', 'Dole', 'Doffen', 'Donald']


#Bot nr 1 Simple
def ole(a):
    return "I think {}ing, could be dangerous for me".format(a)

#bot nr2 Simple
def dole(a):
    return "-Yes! {}ing is lovely".format(a)

#BOt nr3 sligtly advanced, sentenced are build with two shifting verbs
def doffen(a):
    alternatives = ["coding", "singing", "sleeping", "fighting"]
    b = random.choice(alternatives)
    res = "UH, {}ing, do i have to? I would rather do {}".format(a, b)
    return res

# Bot nr 4 the most advanced. The sentence is formed based on the verb, and what category it falls under.
# on top of that it has, a sentence with two random verbs.
def donald(a):
    action = f'{a}ing'
    bad_things = ["boxing", "spying", "jumping", "complaining"]
    good_things = ["running", "talking", "playing", "working"]

    if action in bad_things:
        return "Yay!! its {} time,but remember i would never do {}".format(action, random.choice(good_things))
    elif action in good_things:
        return "What? {} sucks. Not doing that.".format(action)
    return "I don't care!"


# Randomizing sentences and sending them
def sendMessage(msg):
    message = msg.encode()
    client.send(message)

#connects bots with the client, runs a while loop, keep updating for messages
while True:
    # receives the coded message from server, and decodes it
    msg = client.recv(1024).decode('utf-8')
    #Looks for the msg in bot-list, if yes, it shows the connected bot
    if msg in bots:
        connectedBot = msg
        print(f'Connected BOT {connectedBot} to client')
    elif msg.startswith("\n", 1, 2): # prints the amount of rounds
        print(msg)
    elif msg in verbs:
        print(f'Suggested action from server: {msg}')
        # if the individual bots are connected. Prints the following bots messages, corresponding the verb
        if connectedBot == 'Ole':
            sendMessage(f'BOT {connectedBot}: {ole(msg)}')
        elif connectedBot == 'Dole':
            sendMessage(f'BOT {connectedBot}: {dole(msg)}')
        elif connectedBot == 'Doffen':
            sendMessage(f'BOT {connectedBot}: {doffen(msg)}')
        elif connectedBot == 'Donald':
            sendMessage(f'BOT {connectedBot}: {donald(msg)}')
    elif msg == 'wait':
        print(f'BOT {connectedBot} is waiting for server')
    elif msg == 'remove':
        print(f'\nBOT {connectedBot} has disconnected from the server')
        exit()
    else:
        #if the conditions above are not met, the following message will be printed
        print(f'{msg}')


