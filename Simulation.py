import pygame
from pygame import Vector2

from Boid import Boid

vitesse_max = 10

facteur_cohesion = 1
facteur_alignement = 1
facteur_separation = 1.4

rayon_cohesion = 75
rayon_alignement = 75
rayon_separation = 25

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
            boid.pos.x %= self.dimension.x
            boid.pos.y %= self.dimension.y

            nouvelle_vitesse = Vector2(0, 0)
            # cohesion
            nouvelle_vitesse += self.calculerVitesseCohesion(boid) * facteur_cohesion

            # alignement
            nouvelle_vitesse += self.calulerVitesseAlignement(boid) * facteur_alignement

            # Separation
            nouvelle_vitesse += self.calculerVitesseSeparation(boid) * facteur_separation

            boid.vitesse += nouvelle_vitesse

            if boid.vitesse.magnitude() >= vitesse_max:
                boid.vitesse = boid.vitesse.normalize() * vitesse_max

            boid.actualiser()

    def trouverVoisin(self, centre: Vector2, rayon: float) -> list[Boid]:
        liste_boids_voisins = []
        for boid in self.boids:
            if centre == boid.pos: continue
            if centre.distance_squared_to(boid.pos) < rayon ** 2:  # Utilisation de squared pour optimiser
                liste_boids_voisins.append(boid)
        return liste_boids_voisins

    def mettreEnEvidenceBoids(self, pos: Vector2, rayon):
        liste_boids = self.trouverVoisin(pos, rayon)
        for boid in liste_boids:
            boid.color = "black"

    def calculerVitesseCohesion(self, boid_central: Boid) -> Vector2:

        liste_voisins = self.trouverVoisin(boid_central.pos, rayon_cohesion)
        somme_points = Vector2(0, 0)
        if not len(liste_voisins): return somme_points
        for boid_voisin in liste_voisins:
            somme_points += boid_voisin.pos
        point_central = somme_points / len(liste_voisins)

        return (point_central - boid_central.pos).normalize()

    def calulerVitesseAlignement(self, boid_central) -> Vector2:
        liste_voisins = self.trouverVoisin(boid_central.pos, rayon_alignement)
        somme_vitesse = Vector2(0, 0)
        if not len(liste_voisins): return somme_vitesse
        for boid_voisin in liste_voisins:
            somme_vitesse += boid_voisin.vitesse

        vitesse_moyenne = somme_vitesse / len(liste_voisins)
        return vitesse_moyenne.normalize()

    def calculerVitesseSeparation(self, boid_central) -> Vector2:
        liste_voisins = self.trouverVoisin(boid_central.pos, rayon_separation)
        vecteur_final = Vector2(0, 0)
        if not len(liste_voisins): return vecteur_final
        for boid_voisin in liste_voisins:
            vecteur_final += boid_central.pos - boid_voisin.pos

        return vecteur_final.normalize()