import pygame
from pygame import Vector2

from Boid import Boid


class Simulation:



    def __init__(self, screen: pygame.Surface, boids: list[Boid] = []):
        self.boids = boids
        self.screen = screen
        self.dimension = Vector2(screen.get_size())

    def dessinerTousBoids(self):
        for boid in self.boids:
            boid.dessiner(self.screen)

    def actualiser(self):
        for boid in self.boids:
            boid.actualiser()
            boid.pos.x %= self.dimension.x
            boid.pos.y %= self.dimension.y