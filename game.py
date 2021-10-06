import random
from card import Card

class Game():
    def __init__(self):
        """The class that holds all of the information for a specific game.
        Setup all the players and cards, and mark the game as not over.
        """
        self.won = -1
        self.matches = [0,0]
        self.card_picked = []
        self.turn_to_go = 0
        self.ties = 0
        self.players = 0
        self.game_over = False
        self.cards = self.create_cards()

    def create_cards(self):
        # Creates 36 cards in a 6x6 2d list (It could have been done without nested for loops and in a single list, but
        # I wanted to get used to using 2d lists.) Then add a random value from 0-17 to that card. Every value will be 
        # shared by two cards.

        values = [n for n in range(18)]
        values += values
        cards = []
        starting_x = 100
        width_of_cards = 50
        height_of_cards = 70
        x = starting_x
        y = 10
        width_of_grid = 6
        column = 0
        for i in range(width_of_grid):
            new_row = []
            for j in range(width_of_grid):
                if column == width_of_grid:
                    x = starting_x
                    column = 0
                    y += height_of_cards + 10
                hidden_value = random.choice(values)
                values.remove(hidden_value)
                new_row.append(Card(x, y, width_of_cards, height_of_cards, hidden_value))
                column += 1
                x += width_of_cards + 10
            cards.append(new_row)
        return cards
    
    def get_move(self, pos1, pos2):
        self.pos = [pos1, pos2]

    def pick_card(self, row, column):
        if len(self.card_picked) != 2:
            self.card_picked.append((row, column))
            self.cards[row][column].checking = True
        else:
            pass

    def check_move(self, p):
        # Takes the positions for the cards that need to be checked which are held in self.card_picked
        # Check to see if the value matches on the two cards.
        # If it does, mark them as matched, otherwise unmark them from being in the state of "checking"
        # If all of the cards have been matched find which player won and end the game
        card1 = self.cards[self.card_picked[0][0]][self.card_picked[0][1]]
        card2 = self.cards[self.card_picked[1][0]][self.card_picked[1][1]]

        if card1.hidden_num == card2.hidden_num:
            self.matches[p] += 1
            card1.matched = True
            card2.matched = True
            card1.checking = False
            card2.checking = False
        else:
            card1.checking = False
            card2.checking = False
        
            if p == 0:
                self.turn_to_go = 1
            else:
                self.turn_to_go = 0
        
        if sum(self.matches) == 18:
            self.game_over = True

            if p == 0:
                other_player = 1
            else:
                other_player = 0
            
            if self.matches[p] > self.matches[other_player]:
                self.won = p
            else:
                self.won = other_player
        
        self.card_picked.clear()
                    
