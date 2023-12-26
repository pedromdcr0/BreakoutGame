import math

import pygame
import sys
from paddle import Paddle
from bricks import Bricks
from ball import Ball


paddle = Paddle()
ball = Ball()
pygame.init()
width = 600
height = 800
background_color = (0, 0, 0)

brick_rows = 8
brick_columns = 14
brick_width = 40
brick_height = 13
brick_margin = 3.1
brick_margin_top = 20
brick_start_y = 75

bricks = []
for row in range(brick_rows):
    for col in range(brick_columns):
        x = col * (brick_width + brick_margin)
        y = row * (brick_height + brick_margin_top) + brick_start_y
        print(x, y)
        bricks.append(Bricks(x, y))

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("breakout")
score = 0

while True:
    if not ball.game_over():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            paddle.move("right")
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        ball.move()
        ball.bounce()

        window.fill(background_color)

        paddle_rect = pygame.Rect(paddle.position[0], paddle.position[1], paddle.width, 10)
        ball_rect = pygame.Rect(ball.position[0] - ball.radius, ball.position[1] - ball.radius, 2 * ball.radius, 2 * ball.radius)

        if paddle_rect.colliderect(ball_rect):
            relative_position = ball_rect.x + ball.radius - paddle_rect.x
            normalized_position = relative_position / paddle.width

            # Calcular o ângulo baseado na posição relativa
            angle = (normalized_position - 0.5) * math.pi

            # Atualizar a direção da bola com base no ângulo
            ball.direction = [math.sin(angle), -math.cos(angle)]

        for block in bricks:
            rect_ball = pygame.Rect(ball.position[0] - ball.radius, ball.position[1] - ball.radius, 2 * ball.radius,
                                    2 * ball.radius)
            rect_block = pygame.Rect(block.position[0], block.position[1], block.width, block.height)

            if rect_ball.colliderect(rect_block):
                ball.direction[1] *= -1
                if block.color == (238, 210, 2):
                    score += 1
                elif block.color == (0, 200, 0):
                    score += 3
                elif block.color == (255, 140, 0):
                    score += 5
                elif block.color == (220, 0, 0):
                    score += 7
                bricks.remove(block)
                print(score)

            elif rect_ball.colliderect(rect_block.move(ball.direction[0] * ball.speed, 0)):
                ball.direction[0] *= -1
                if block.color == (238, 210, 2):
                    score += 1
                elif block.color == (0, 200, 0):
                    score += 3
                elif block.color == (255, 140, 0):
                    score += 5
                elif block.color == (220, 0, 0):
                    score += 7
                bricks.remove(block)
                print(score)

        for brick in bricks:
            if brick.position[1] == 75 or brick.position[1] == 108:
                brick.color = (220, 0, 0)
                brick.draw(window)
            if brick.position[1] == 141 or brick.position[1] == 174:
                brick.color = (255, 140, 0)
                brick.draw(window)
            if brick.position[1] == 207 or brick.position[1] == 240:
                brick.color = (0, 200, 0)
                brick.draw(window)
            if brick.position[1] == 273 or brick.position[1] == 306:
                brick.color = (238, 210, 2)
                brick.draw(window)

        ball.draw(window)

        pygame.draw.rect(window, (255, 255, 255), (paddle.position[0], paddle.position[1], paddle.width, 10))

        pygame.display.flip()
    else:
        break
