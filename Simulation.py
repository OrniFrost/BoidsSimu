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

    def trouverVoisin(self, centre: Vector2, rayon: float) -> list[Boid] :
        liste_boids_voisins = []
        for boid in self.boids:
            if centre.distance_squared_to(boid.pos) < rayon**2:  # Utilisation de squared pour optimiser
                liste_boids_voisins.append(boid)
        return liste_boids_voisins

    def mettreEnEvidenceBoids(self, pos: Vector2, rayon):
        liste_boids = self.trouverVoisin(pos, rayon)
        for boid in liste_boids:
            boid.color = "black"