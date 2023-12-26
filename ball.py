import pygame


class Ball:
    def __init__(self):
        self.radius = 7
        self.speed = 0.25
        self.direction = [1, -1]  # Direção inicial (horizontal, vertical)
        self.position = [300, 650]
        self.lives = 3
        self.score = 0

    def move(self):
        self.position[0] += self.speed * self.direction[0]
        self.position[1] += self.speed * self.direction[1]

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.position[0]), int(self.position[1])), self.radius)

    def bounce(self):
        if self.position[0] >= 593:
            self.direction[0] *= -1
            self.speed += 0.001
        if self.position[0] <= 0:
            self.direction[0] *= -1
            self.speed += 0.001
        if self.position[1] <= 0:
            self.direction[1] *= -1
            self.speed += 0.001

    def game_over(self):
        if self.position[1] >= 793:
            self.direction[1] *= -1
            self.lives -= 1
            self.speed = 0.25
            self.position = self.position = [300, 650]

        elif self.lives == 0:
            return True

        else:
            return False






        # if colision:
        #     pass



