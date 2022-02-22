import pygame

class Card():
    def __init__(self, x, y, width, height, hidden_num):
        """Holds all of the information for a specific card."""
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.hidden_num = hidden_num
        self.checking = False
        self.matched = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_card(self, display):
        # If the card is marked as matched the number iwll be revealed, and if it is marked as checking then it will also light up.
        if self.checking:
            color = (210, 225, 255)
        else:
            color = (199, 115, 255)
        pygame.draw.rect(display, color, self.rect)
        if self.checking:
            self.reveal_num(display)

        if self.matched:
            self.reveal_num(display)

    def reveal_num(self, display):
        fonts = pygame.font.SysFont("Arial", 12)
        text = fonts.render(f"{self.hidden_num}", 1, (0, 0, 0))
        display.blit(text, (self.x + int(self.width/2.5), self.y + int(self.height/2.5)))