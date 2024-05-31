from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import pygame
from pygame import Vector2

from Boid import Boid



facteur_cohesion = 0.2
facteur_alignement = 0.25
facteur_separation = 1.25

rayon_cohesion = 75
rayon_alignement = 75
rayon_separation = 20




class Simulation:

    def __init__(self, screen: pygame.Surface, boids: list[Boid] = []):
        self.boids = boids
        self.screen = screen
        self.dimension = Vector2(screen.get_size())

    def dessinerTousBoids(self):
        for boid in self.boids:
            boid.dessiner(self.screen)

    def actualiser(self):
        with ThreadPoolExecutor(max_workers=8) as executor:

            executor.map(self.calculerForce, self.boids)

    def calculerForce(self, boid: Boid):
        boid.pos.x %= self.dimension.x
        boid.pos.y %= self.dimension.y

        nouvelle_acceleration = Vector2(0, 0)
        # cohesion
        nouvelle_acceleration += self.calculerVitesseCohesion(boid) * facteur_cohesion

        # alignement
        nouvelle_acceleration += self.calulerVitesseAlignement(boid) * facteur_alignement

        # Separation
        nouvelle_acceleration += self.calculerVitesseSeparation(boid) * facteur_separation

        # Force bordure
        nouvelle_acceleration += self.calculerForceBordures(boid)

        boid.acceleration += nouvelle_acceleration

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

    def calculerVitesseSeparation(self, boid_central: Boid) -> Vector2:
        liste_voisins = self.trouverVoisin(boid_central.pos, rayon_separation)
        vecteur_final = Vector2(0, 0)
        if not len(liste_voisins): return vecteur_final
        for boid_voisin in liste_voisins:
            vecteur_final += boid_central.pos - boid_voisin.pos

        return vecteur_final.normalize()

    def calculerForceBordures(self, boid: Boid) -> Vector2:

        dim = Vector2(self.screen.get_size())
        # milieu = dim/2
        # force_x = milieu.x - boid.pos.x
        # force_y = milieu.y - boid.pos.y
        #
        # force = Vector2(force_x,force_y)
        #
        # return force.normalize() * force.magnitude()/500

        force_bordure_gauche = Vector2(0, boid.pos.y) - boid.pos

        force_bordure_droite = Vector2(dim.x, boid.pos.y) - boid.pos

        force_bordure_haute = Vector2(boid.pos.x, 0) - boid.pos

        force_bordure_basse = Vector2(boid.pos.x, dim.y) - boid.pos

        # if force_bordure_gauche.magnitude() != 0: force_bordure_gauche *= 1 / force_bordure_gauche.magnitude()
        # if force_bordure_droite.magnitude() != 0: force_bordure_droite *= 1 / force_bordure_droite.magnitude()
        # if force_bordure_haute.magnitude() != 0: force_bordure_haute *= 1 / force_bordure_haute.magnitude()
        # if force_bordure_basse.magnitude() != 0: force_bordure_basse *= 1 / force_bordure_basse.magnitude()


        force_horizontal = force_bordure_gauche + force_bordure_droite
        force_horizontal *= 1/force_horizontal.magnitude()*0.4

        force_vertical = force_bordure_basse + force_bordure_haute
        force_vertical *= 1/force_vertical.magnitude()*.5

        return force_horizontal + force_vertical
