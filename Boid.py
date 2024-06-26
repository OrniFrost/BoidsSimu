import pygame
from pygame import Color
from pygame.math import Vector2
from random import  randint as ri

vitesse_max = 12

class Boid:

    def __init__(self, pos=Vector2(0, 0), vitesse=Vector2(0, 0), acceleration=Vector2(0,0)):
        self.pos = pos
        self.vitesse = vitesse
        self.acceleration = acceleration
        self.color = Color([ri(100,255) for _ in range(3)])


    def dessiner(self, screen):
        pygame.draw.circle(screen, "black", self.pos, 11)
        if self.vitesse != Vector2(0, 0):
            pygame.draw.line(
                screen,
                "red",
                self.pos,
                self.vitesse.normalize()* self.vitesse.magnitude()*3 + self.pos,
                4
            )

        pygame.draw.circle(screen, self.color, self.pos, 10)


    def actualiser(self):
        self.vitesse += self.acceleration
        self.acceleration = Vector2(0,0)
        if self.vitesse.magnitude() >= vitesse_max:
            self.vitesse = self.vitesse.normalize() * vitesse_max

        self.pos += self.vitesse