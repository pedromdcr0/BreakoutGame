import pygame


class Bricks:
    def __init__(self, x, y):
        self.width = 40
        self.height = 13
        self.position = [x, y]
        self.color = (0, 0, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.width, self.height))

    def score_up(self, color):
        if color == (238, 210, 2):
            self.score += 1
        elif color == (0, 200, 0):
            self.score += 3
        elif color == (255, 140, 0):
            self.score += 5
        elif color == (220, 0, 0):
            self.score += 7

