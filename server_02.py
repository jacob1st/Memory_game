import pickle
import socket
import threading
from game_01 import Game

# Can change PORT, but make sure to change it on the client side also.
PORT = 7777
# Add your local IPv4 address for the value of ADDR. (Example: ADDR = "127.0.0.1")
ADDR = ""
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
new_games = {0:Game()}

try:
    server.bind((ADDR, PORT))
except socket.error as error:
    print(str(error))

server.listen(2)
print("Server started. Waiting for player connections...")

def handle_client(conn, currentId, player_id):
    # A seperate thread to run for each client connection.
    # The connection starts with the server sending a player id.
    # Then it will constantly wait for the client to send information and respond with the new game object.
    conn.sendall(str(player_id).encode(FORMAT))

    while True:
        try:
            data = conn.recv(2048).decode(FORMAT)
            if currentId % 2 == 0:
                game_number = currentId
                new_game = new_games[currentId]
            else:
                game_number = currentId - 1
                new_game = new_games[currentId - 1]

            if not data:
                print("Error in connection, disconnecting from client...")
                new_games[game_number].players -= 1
                if new_games[game_number].players == 0:
                    del new_games[game_number]
                    print("Game Finished.")
                conn.close()
                break
            else:
                if data == "CLOSE":
                    print("Disconnecting from a client")
                    new_games[game_number].players -= 1
                    if new_games[game_number].players == 0:
                        del new_games[game_number]
                        print("Game Finished.")
                    conn.close()
                    break
                elif data == 'CHECK':
                    new_game.check_move(player_id)
                elif data != 'GET':
                    data = data.split(",")
                    new_game.pick_card(int(data[0]), int(data[1]))
                conn.sendall(pickle.dumps(new_game))
        except:
            break

playerId = 0
currentId = 0
while True:
    connection, address = server.accept()
    print("connection made at IP address:", address[0])

    new_thread = threading.Thread(target=handle_client, args=(connection, currentId, playerId))
    new_thread.start()

    # The game instances are all held in a dictionary. 
    # The first key corresponds to player 0 and iterates for every other subsequent connection.
    # Any player who has an odd ID is the second player to that game, and retrieves the game ID from the previous player ID.
    # I.E When player 0 connects it creates a new game for them with the game key of 0.
    #     When player 1 connects they will get the game made for player 0 and join it, then iterate the game key for the next 
    #     pair of players.

    if currentId % 2 == 0:
        new_games[currentId].players += 1
    else:
        new_games[currentId-1].players += 1
    
    if currentId % 2 != 0:
        new_games[currentId+1] = Game()

    currentId += 1
    playerId += 1
    if playerId > 1:
        playerId = 0
