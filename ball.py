import pygame


class Ball:
    def __init__(self):
        self.radius = 7
        self.speed = 3
        self.direction = [1, -1]  # Direção inicial (horizontal, vertical)
        self.position = [300, 650]
        self.lives = 3
        self.score = 0
        self.bounced = 0
        self.red_trespassed = 0
        self.game_on = None

    def move(self):
        self.position[0] += self.speed * self.direction[0]
        self.position[1] += self.speed * self.direction[1]

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.position[0]), int(self.position[1])), self.radius)

    def bounce(self):
        if self.position[0] >= 593:
            self.direction[0] *= -1
            self.bounced += 1
        if self.position[0] <= 0:
            self.direction[0] *= -1
            self.bounced += 1
        if self.position[1] <= 65:
            self.direction[1] *= -1
            self.bounced += 1

    def game_over(self):
        if self.position[1] >= 793:
            self.direction[1] *= -1
            self.lives -= 1
            self.position = self.position = [300, 650]

        elif self.lives == 0:
            self.game_on = False

        else:
            self.game_on = True

    def increase_speed(self, event):
        if event == "red":
            self.speed += 1
        elif event == "orange":
            self.speed += 1
        elif event == "four":
            self.speed += 1
        elif event == "twelve":
            self.speed += 1

    def reset(self):
        self.radius = 7
        self.speed = 3
        self.direction = [1, -1]  # Direção inicial (horizontal, vertical)
        self.position = [300, 650]
        self.lives = 3
        self.score = 0
        self.bounced = 0
        self.red_trespassed = 0

