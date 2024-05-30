# Example file showing a circle moving on screen
import random

import pygame
from pygame import Vector2

from Boid import Boid
from Simulation import Simulation

import random as rd

# pygame setup

x_max = 1280
y_max = 720

vitesse_max = 10

pygame.init()
screen = pygame.display.set_mode((x_max, y_max))
clock = pygame.time.Clock()
running = True
dt = 0

nb_boids = 30
boids = []

for _ in range(nb_boids):
    boids.append(
        Boid(
            Vector2(rd.randint(0, x_max), rd.randint(0,y_max)),
            Vector2(rd.randint(- vitesse_max, vitesse_max), rd.randint(- vitesse_max,vitesse_max)),
        )
    )


simulation = Simulation(screen=screen, boids=boids)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_click = Vector2(pygame.mouse.get_pos())
            simulation.mettreEnEvidenceBoids(pos_click, 100)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # pygame.draw.circle(screen, "red", player_pos, 40)
    #
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt


    simulation.actualiser()

    simulation.dessinerTousBoids()



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()