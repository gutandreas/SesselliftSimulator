import os
import random

import pygame

pygame.init()

# Fenster
(width, height) = (1536, 864)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption("Sessellift Simulator")

# Farben
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)

# Steuerungsvariablen
running = True
FPS = 25
FREQUENCY = 30
MAX_FRAME = 301
CAPACITY = 2

# Bilder
BACKGROUND = pygame.image.load(os.path.join("bilder", "background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))
SKIER1_PICTURE = pygame.image.load(os.path.join("bilder", "skifahrer1.png"))
SKIER1_PICTURE = pygame.transform.scale(SKIER1_PICTURE, (20, 30))
STATION_PICTURE = pygame.image.load(os.path.join("bilder", "station.png"))
STATION_PICTURE = pygame.transform.scale(STATION_PICTURE, (100, 70))
CHAIR_PICTURE = pygame.image.load(os.path.join("bilder", "sessel.png"))
CHAIR_PICTURE = pygame.transform.scale(CHAIR_PICTURE, (CAPACITY*20, 40))

SKIER_PICTURES = []
SKIER_PICTURES.append(SKIER1_PICTURE)


# Listen
SKIERS = []
CHAIRS = []


class Station(pygame.sprite.Sprite):

    def __init__(self, x, y, capacity):
        pygame.sprite.Sprite.__init__(self)
        self.distance = 0
        self.picture = pygame.transform.rotate(STATION_PICTURE.copy(), 0)
        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.capacity = capacity

# Stationen
station_down = Station(950, 750, CAPACITY)
station_up = Station(950, 100, CAPACITY)


class Chair(pygame.sprite.Sprite):

    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)
        self.distance = 0
        self.picture = CHAIR_PICTURE.copy()
        self.rect = self.picture.get_rect()
        self.rect.x = station_down.rect.x
        self.rect.y = 500
        self.direction = direction
        self.at_station = False
        CHAIRS.append(self)

    def move(self, speed):

        if self.direction == 0:
            if self.rect.y < station_up.rect.midleft[1]+5:
                if self.rect.x < station_up.rect.midright[0]-22:
                    self.rect.x += speed
                else:
                    self.rect.x = station_up.rect.midright[0]-22
                    self.direction = 1
                    self.rect.y += speed
            else:
                self.rect.y -= speed
        else:
            if self.rect.y >= station_down.rect.bottomright[1]-30:
                self.rect.y = station_down.rect.bottomright[1] - 30
                if self.rect.x > station_down.rect.midleft[0]-15:
                    self.rect.x -= speed
                else:
                    self.rect.x = station_down.rect.midleft[0] - 15
                    self.direction = 0
                    self.rect.y -= speed
            else:
                self.rect.y += speed


class Skier(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.distance = 0
        self.picture = pygame.transform.rotate(SKIER_PICTURES[random.randrange(len(SKIER_PICTURES))].copy(), 0)
        self.rect = self.picture.get_rect()
        self.rect.x = 1600
        self.rect.y = 800
        SKIERS.append(self)

    def move(self, speed):
        point_to_check = self.rect.midleft

        collision_with = pygame.sprite.spritecollide(self, SKIERS, False)
        collision_with.remove(self)
        way_free = True

        for c in collision_with:
            if c.rect.collidepoint(point_to_check):
                way_free = False

        if not self.rect.collidepoint(station_down.rect.x, station_down.rect.y+50) and way_free:
            self.rect.x -= speed




def main():
    global screen, running

    clock = pygame.time.Clock()
    counter = 0

    Chair(0)



    while running:

        if counter % FREQUENCY == 0:
            print("Skier")
            Skier()

        counter += 1

        clock.tick(FPS)
        screen.fill(WHITE)
        screen.blit(BACKGROUND, (0,0))

        for s in SKIERS:
            screen.blit(s.picture, (s.rect.x, s.rect.y))
            s.move(2)

        for c in CHAIRS:
            screen.blit(c.picture, (c.rect.x, c.rect.y))
            c.move(10)

        screen.blit(station_down.picture, (station_down.rect.x, station_down.rect.y))
        screen.blit(station_up.picture, (station_up.rect.x, station_up.rect.y))
        pygame.draw.line(screen, (0, 0, 0),
                                     (station_down.rect.midleft[0] + 5, station_down.rect.midleft[1]),
                                     (station_up.rect.midleft[0] + 5, station_up.rect.midleft[1]))
        pygame.draw.line(screen, (0, 0, 0),
                                      (station_down.rect.midright[0] - 3, station_down.rect.midright[1]),
                                      (station_up.rect.midright[0] - 3, station_up.rect.midright[1]))

        pygame.display.update()

        if counter == MAX_FRAME:
            counter = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
