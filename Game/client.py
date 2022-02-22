import pygame
from network import Network

def write(display, font, font_size, position, message, color):
    # Take in some qualities of a message and prints it.
    text_font = pygame.font.SysFont(font, font_size)
    text = text_font.render(message, 1, color)
    display.blit(text, position)

def game_ended(game, player):
    # Runs when every card in game.cards is matched and the game is finished.
    # Compare the number of matches from each player to determine who won, and then print it.
    run = True
    while run:
        display.fill((0, 0, 0))
        if game.won == player:
            write(display, "Arial", 30, (150, 250), "You Won! Congratulations!!!!!!", (255, 255, 255))
        else:
            write(display, "Arial", 30, (150, 250), "You Lost, better luck next time!", (255, 255, 255))
        write(display, "Arial", 30, (50, 450), "The game has finished! Press 'a' to play again!", (255, 255, 255))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            replay()
            break

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cl.send("CLOSE")
                run = False
                pygame.quit()
        


def take_turn(client, game, mouse_pos):
    # Sends the positions for the card (Nested loops because it is a 2d list) that the player selected to the server
    # returns the new game object
    for i in range(len(game.cards)):
        for j in range(len(game.cards[i])):
            if game.cards[i][j].rect.collidepoint(mouse_pos) and not game.cards[i][j].checking and not game.cards[i][j].matched:
                try:
                    game = client.send(f"{i},{j}")
                    return game
                except:
                    pass
    return game

def replay():
    # Disconnects the client from the first game, and starts a new one.
    global cl
    cl.send("CLOSE")
    cl = Network()
    main_menu()

pygame.init()
display = pygame.display.set_mode((800, 810))
pygame.display.set_caption("Memory Game")

cl = Network()

def main_menu():
    # Displays a menu screen until another player joins the game, then runs main().
    dots = 0
    dot_count = 0
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        try:
            game = cl.send('GET')
        except: 
            pass
        if game.players != 2:
            if dot_count == 30:
                dots += 1
                dot_count = 0
            if dots > 3:
                dots = 0
            display.fill((0, 0, 0))
            write(display, "Arial", 40, (200, 250), "Waiting for players", (255, 255, 255))
            waiting_dots = [pygame.image.load('dot.png'), pygame.image.load('dot1.png'), pygame.image.load('dot2.png'), pygame.image.load('dot3.png')]
            display.blit(waiting_dots[dots], (530, 265))
            dot_count += 1
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # The new connection when quitting is to stop the server from crashing when it cannot
                    # find the proper game in the dictionary of games.
                    quitting_conn = Network()
                    quitting_conn.send("CLOSE")
                    cl.send("CLOSE")
                    pygame.quit()
                    run = False
        else:
            main()
            break

def main():
    # Lets the player play through a round with someone else.
    # Displays the game graphics.
    # When it is the players turn the game will look for his move, otherwise, wait for the opponent to make a move.
    clock = pygame.time.Clock()
    run = True
    player = int(cl.get_player())
    while run:
        clock.tick(60)
        display.fill((0, 102, 0))

        try:
            game = cl.send('GET')
        except:
            pass
        
        if game.players < 2:
            write(display, "Arial", 12, (10, 600), "Opponent has left the match. Press 'a' to return to the main menu", (255, 255, 255))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                replay()

        if game.game_over:
            game_ended(game, player)
            break

        if player == game.turn_to_go:
            write(display, "Arial", 12, (10, 10), "Your turn", (255, 255, 255))
            instructions = "Hover over a card and press SPACE to select it. Choose two cards then check to see if they match!"
            write(display, "Arial", 18, (5, 700), instructions, (0, 0, 0))

            keys = pygame.key.get_pressed()
            if len(game.card_picked) == 2:
                write(display, "Arial", 12, (600, 60), "Press ENTER to check", (255, 255, 255))
                if keys[pygame.K_RETURN]:
                    cl.send("CHECK")
            else:
                if keys[pygame.K_SPACE]:
                    mouse_pos = pygame.mouse.get_pos()
                    game = take_turn(cl, game, mouse_pos)
        else:
            write(display, "Arial", 12, (10, 10), "Opponent's turn", (255, 255, 255))
            
        write(display, "Arial", 12, (600, 10), f"Your matches: {game.matches[player]}", (255, 255, 255))
        write(display, "Arial", 12, (600, 30), f"Opponent's matches: {sum(game.matches) - game.matches[player]}", (255, 255, 255))

        for i in game.cards:
            for j in i:
                j.draw_card(display)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                cl.send("CLOSE")
                pygame.quit()

main_menu()