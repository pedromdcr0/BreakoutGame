import math
import pygame
import sys
from paddle import Paddle
from bricks import Bricks
from ball import Ball


paddle = Paddle()
ball = Ball()
pygame.init()
clock = pygame.time.Clock()
width = 600
height = 800
background_color = (0, 0, 0)

flash_timer = 0
flash_interval = 25
show_name = True
show_pause = True

bricks = []


def populate_bricks():
    bricks.clear()
    brick_rows = 8
    brick_columns = 14
    brick_width = 40
    brick_height = 13
    brick_margin = 3.1
    brick_margin_top = 20
    brick_start_y = 75

    for row in range(brick_rows):
        for col in range(brick_columns):
            x = col * (brick_width + brick_margin)
            y = row * (brick_height + brick_margin_top) + brick_start_y
            bricks.append(Bricks(x, y))


window = pygame.display.set_mode((width, height))
pygame.display.set_caption("breakout")
score = 0

with open("data/highscore.txt", "r") as highscore_file:
    highscore = highscore_file.read()

fonte = pygame.font.Font("data/font.ttf", 30)
fonte_final = pygame.font.Font("data/font.ttf", 20)

is_paused = False

while True:
    if ball.game_on is True:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    is_paused = not is_paused

        while is_paused:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        is_paused = not is_paused

            pause_game = fonte_final.render('Pause', True, (200, 205, 200))
            pause_game_x = (width - pause_game.get_width()) / 2
            pause_game_y = (height - pause_game.get_height()) / 2
            print(show_pause)

            flash_timer += clock.get_rawtime()
            print(flash_timer)

            flash_timer += clock.get_rawtime()
            if flash_timer >= flash_interval:
                show_pause = not show_pause
                flash_timer = 0

            if show_pause:
                window.blit(pause_game, (pause_game_x, pause_game_y))
            else:
                window.fill(background_color)

            pygame.time.delay(100)

            pygame.display.flip()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            paddle.move("right")
        if keys[pygame.K_LEFT]:
            paddle.move("left")

        ball.move()
        ball.bounce()
        ball.game_over()

        window.fill(background_color)

        paddle_rect = pygame.Rect(paddle.position[0], paddle.position[1], paddle.width, 10)
        ball_rect = pygame.Rect(ball.position[0] - ball.radius, ball.position[1] - ball.radius, 2 * ball.radius, 2 * ball.radius)

        if paddle_rect.colliderect(ball_rect):
            relative_position = ball_rect.x + ball.radius - paddle_rect.x
            normalized_position = relative_position / paddle.width

            angle = (normalized_position - 0.5) * math.pi

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
                    ball.red_trespassed += 1

                bricks.remove(block)

            elif rect_ball.colliderect(rect_block.move(ball.direction[0] * ball.speed, 0)):
                ball.direction[0] *= -1
                if block.color == (238, 210, 2):
                    score += 1
                elif block.color == (0, 200, 0):
                    score += 3
                elif block.color == (255, 140, 0):
                    score += 5
                    ball.increase_speed("orange")
                elif block.color == (220, 0, 0):
                    score += 7
                    ball.increase_speed("red")

                bricks.remove(block)

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

        if ball.red_trespassed == 1:
            ball.red_trespassed += 1
            paddle.red_tresspassed()

        if ball.bounced == 4:
            ball.increase_speed("four")
            ball.bounced += 1
        if ball.bounced == 13:
            ball.increase_speed("twelve")
            ball.bounced += 1

        ball.draw(window)

        if score > int(highscore):
            highscore = score

        pygame.draw.rect(window, (255, 255, 255), (paddle.position[0], paddle.position[1], paddle.width, 10))
        pygame.draw.rect(window, (200, 205, 200), (0, 50, 600, 10))
        pygame.draw.rect(window, (200, 205, 200), (295, 0, 10, 50))

        texto_score = fonte.render(f'{score}', True, (200, 205, 200))

        score_x = (295 - texto_score.get_width()) / 2
        score_y = (50 - texto_score.get_height()) / 2

        texto_highscore = fonte.render(f"{highscore}", True, (200, 200, 200))

        highscore_x = ((295 - texto_highscore.get_width()) / 2) + 300
        highscore_y = (50 - texto_highscore.get_height()) / 2

        window.blit(texto_highscore, (highscore_x, highscore_y))
        window.blit(texto_score, (score_x, score_y))

        pygame.display.flip()
        print(pygame.time.Clock().get_fps())

    elif ball.game_on is False:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            populate_bricks()
            ball.reset()
            paddle.reset()
            ball.game_on = True

        window.fill((0, 0, 0))
        final_score = fonte.render(f'Your Score: {score}', True, (200, 205, 200))

        final_score_x = (width - final_score.get_width()) / 2
        final_score_y = (height - final_score.get_height()) / 2

        final_highscore = fonte_final.render(f'Highscore: {highscore}', True, (200, 205, 200))

        final_highscore_x = (width - final_highscore.get_width()) / 2
        final_highscore_y = final_score_y + final_highscore.get_height() + 20

        play_again_text = fonte_final.render('Press SPACE to play again', True, (200, 205, 200))

        play_again_text_x = (width - play_again_text.get_width()) / 2
        play_again_text_y = final_highscore_y + final_highscore.get_height() + 20

        if score > int(highscore):
            with open("data/highscore.txt", "w") as highscore_file:
                highscore_file.write(f"{score}")
        else:
            with open("data/highscore.txt", "w") as highscore_file:
                highscore_file.write(f"{highscore}")

        window.blit(final_score, (final_score_x, final_score_y))
        window.blit(final_highscore, (final_highscore_x, final_highscore_y))
        window.blit(play_again_text, (play_again_text_x, play_again_text_y))

        pygame.display.flip()

    elif ball.game_on is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            ball.game_on = True
            populate_bricks()

        start_game = fonte_final.render('Press space to start', True, (200, 205, 200))
        start_game_x = (width - start_game.get_width()) / 2
        start_game_y = (height - start_game.get_height()) / 2

        flash_timer += clock.get_rawtime()

        if flash_timer >= flash_interval:
            show_name = not show_name
            flash_timer = 0

        if show_name:
            window.blit(start_game, (start_game_x, start_game_y))
        else:
            window.fill(background_color)

        pygame.display.flip()
        clock.tick(60)
