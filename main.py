import time
import pygame
import random

WIDTH = 1280
HEIGHT = 620
SPEED = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

balloon_surf = pygame.image.load('img/balloon.png').convert_alpha()
balloons_rect = []

flowncontrol = 0
flownvalue = True
game_font = pygame.font.SysFont('arial', 60)

timer = 0
start_time = pygame.time.get_ticks()
time_left = 8
GAME_TIME = 8000
max_ballons = 10
for _ in range(max_ballons):
    balloon_rect = balloon_surf.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(150, HEIGHT - 50)))
    balloons_rect.append(balloon_rect)

background = pygame.image.load("img/sky.png").convert_alpha()
background = pygame.transform.scale(background, (1280, 620))
crosshair = pygame.image.load('img/crosshair.png').convert_alpha()
crosshair = pygame.transform.scale(crosshair, (50, 50))
score = 0
crosshair_x = WIDTH / 2
crosshair_y = HEIGHT / 2
crosshair_rect = crosshair.get_rect(center=(crosshair_x, crosshair_y))
startdisplay = game_font.render('', True, (255, 0, 0))
previous_score = game_font.render('', True, (255, 0, 0))
timer_surf = game_font.render('', True, (255, 0, 0))
score_surf = game_font.render('', True, (255, 0, 0))

running = True
inAction = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            crosshair_rect = crosshair.get_rect(center=event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if inAction == False:
                    inAction = True
                    balloons_rect = []
                    for _ in range(max_ballons):
                        balloon_rect = balloon_surf.get_rect(
                            center=(random.randint(50, WIDTH - 50), random.randint(150, HEIGHT - 50)))
                        balloons_rect.append(balloon_rect)
                    timer = 0
                    start_time = pygame.time.get_ticks()
                    time_left = 8
                    GAME_TIME = 8000
                    score = 0
                if inAction:
                    startdisplay = game_font.render('', True, (255, 0, 0))
                    previous_score = game_font.render('', True, (255, 0, 0))
    if not inAction:
        startdisplay = game_font.render('Press space to start', True, (255, 0, 0))
        previous_score = game_font.render('Your score was: ' + str(score), True, (255, 0, 0))
        timer_surf = game_font.render('', True, (255, 0, 0))
        score_surf = game_font.render('', True, (255, 0, 0))
    # delete
    for index, balloon_rect in enumerate(balloons_rect):
        if balloons_rect[index].right >= WIDTH:
            del balloons_rect[index]
        elif balloons_rect[index].left <= 0:
            del balloons_rect[index]
        elif balloons_rect[index].top <= 0:
            del balloons_rect[index]
        elif balloons_rect[index].bottom >= HEIGHT:
            del balloons_rect[index]
    screen.blit(background, (0, 0))

    # flowncontrol
    for index, balloon_rect in enumerate(balloons_rect):
        balloons_rect[index].top -= 1
        if flownvalue and flowncontrol <= 150:
            balloons_rect[index].left += 1
            flowncontrol += 1
        elif flownvalue and flowncontrol > 150:
            flownvalue = False
        elif not flownvalue and flowncontrol >= 0:
            balloons_rect[index].left -= 1
            flowncontrol -= 1
        elif not flownvalue and flowncontrol < 0:
            flownvalue = True

        # score
    if inAction:
        for index, balloon_rect in enumerate(balloons_rect):
            if balloon_rect.colliderect(crosshair_rect) and pygame.mouse.get_pressed()[0]:
                score += 1
                del balloons_rect[index]
            else:
                screen.blit(balloon_surf, balloon_rect)
            # timer
            time_left = int((start_time + GAME_TIME - pygame.time.get_ticks()) / 1000)
        timer_surf = game_font.render('Time: ' + str(time_left), True, (255, 0, 0))
        score_surf = game_font.render('Score: ' + str(score), True, (255, 0, 0))

    # ending
    winning_surf = game_font.render('', True, (255, 0, 0))
    if time_left == 0:
        winning_surf = game_font.render('Time ran out', True, (255, 0, 0))
        screen.blit(winning_surf, (320, 220))
        inAction = False
    elif balloons_rect == []:
        if score == max_ballons:
            winning_surf = game_font.render('You won', True, (255, 0, 0))
            screen.blit(winning_surf, (320, 220))
            inAction = False
        elif score != max_ballons:
            winning_surf = game_font.render('You didnt got all of them', True, (255, 0, 0))
            screen.blit(winning_surf, (320, 220))
            inAction = False
    screen.blit(score_surf, (0, 0))
    screen.blit(timer_surf, (0, 560))
    screen.blit(winning_surf, (320, 220))
    screen.blit(crosshair, crosshair_rect)
    screen.blit(startdisplay, (420, 320))
    screen.blit(previous_score, (420, 370))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
