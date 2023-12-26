class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.speed = 0.25
        self.position = [300, 700]

    def move(self, direction):
        if direction == "right" and self.position[0] < 600 - self.width:
            self.position[0] += self.speed
        if direction == "left" and self.position[0] > 0:
            self.position[0] -= self.speed

    def red_tresspassed(self):
        self.width /= 2
