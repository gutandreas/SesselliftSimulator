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
CAPACITY = 4

# Bilder
BACKGROUND = pygame.image.load(os.path.join("bilder", "background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))
SKIER1_PICTURE = pygame.image.load(os.path.join("bilder", "skifahrer1.png"))
SKIER1_PICTURE = pygame.transform.scale(SKIER1_PICTURE, (20, 30))
STATION_PICTURE = pygame.image.load(os.path.join("bilder", "station.png"))
STATION_PICTURE = pygame.transform.scale(STATION_PICTURE, (100, 70))
CHAIR_PICTURE = pygame.image.load(os.path.join("bilder", "sessel.png"))
CHAIR_PICTURE = pygame.transform.scale(CHAIR_PICTURE, (40, 40))
CHAIR_PICTURE_RIGHT = pygame.image.load(os.path.join("bilder", "sessel_seite.png"))
CHAIR_PICTURE_RIGHT = pygame.transform.scale(CHAIR_PICTURE_RIGHT, (40, 40))
CHAIR_PICTURE_LEFT = pygame.image.load(os.path.join("bilder", "sessel_seite_2.png"))
CHAIR_PICTURE_LEFT = pygame.transform.scale(CHAIR_PICTURE_LEFT, (40, 40))

SKIER_PICTURES = []
SKIER_PICTURES.append(SKIER1_PICTURE)


# Listen
SKIERS = []
CHAIRS = []
WAITING_SKIERS = pygame.sprite.Group()
DRIVING_SKIERS = pygame.sprite.Group()




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

    def __init__(self, direction, x, y, view):
        pygame.sprite.Sprite.__init__(self)
        self.distance = 0
        if view == "front":
            self.picture = CHAIR_PICTURE.copy()
        else:
            self.picture = CHAIR_PICTURE_RIGHT.copy()

        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.at_station = False
        CHAIRS.append(self)
        self.skiers = []

    def move(self, speed):

        if self.direction == 0:
            if self.rect.y < station_up.rect.midleft[1]+5:
                self.picture = CHAIR_PICTURE
                if len(self.skiers) > 0:
                    for s in self.skiers:
                        DRIVING_SKIERS.add(s)
                        s.rect.y = self.rect.y
                        self.skiers = []
                if self.rect.x < station_up.rect.midright[0]-22:
                    self.rect.x += speed
                    self.picture = CHAIR_PICTURE_RIGHT
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
                    self.picture = CHAIR_PICTURE_LEFT
                else:
                    self.rect.x = station_down.rect.midleft[0] - 15
                    self.direction = 0
                    self.rect.y -= speed
                    self.picture = CHAIR_PICTURE
                    for i in range(CAPACITY):
                        if WAITING_SKIERS.sprites()[0].rect.x < station_down.rect.x+70:
                            self.skiers.append(WAITING_SKIERS.sprites()[0])
                            WAITING_SKIERS.remove(WAITING_SKIERS.sprites()[0])
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
        self.rotated = False
        SKIERS.append(self)
        WAITING_SKIERS.add(self)


    def move(self, speed):
        point_to_check = self.rect.midleft
        collision_with = pygame.sprite.spritecollide(self, WAITING_SKIERS, False)
        collision_with.remove(self)
        way_free = True

        for c in collision_with:
            if c.rect.collidepoint(point_to_check):
                way_free = False

        if not self.rect.collidepoint(station_down.rect.x, station_down.rect.y+50) and way_free:
            self.rect.x -= speed

    def drive(self, speed):
        point_to_check = self.rect.midleft
        collision_with = pygame.sprite.spritecollide(self, DRIVING_SKIERS, False)
        collision_with.remove(self)
        way_free = True

        for c in collision_with:
            if c.rect.collidepoint(point_to_check):
                way_free = False

        if way_free:
            if self.rect.x > 850:
                self.rect.x -= speed
            else:
                self.rect.x -= speed*2
                self.rect.y += speed*2
                if not self.rotated:
                    self.picture = pygame.transform.rotate(self.picture, 45)
                    self.rect.x -= 5
                    self.rotated = True
            if self.rect.y > 335:
                self.remove(DRIVING_SKIERS)

def set_chairs_on_lift(number_of_chairs):

    distance = 1484 / number_of_chairs
    x_direction_1 = station_down.rect.x + 77
    x_direction_0 = station_down.rect.x - 16
    y_limit_up = station_up.rect.midleft[1]+5
    y_limit_down = station_down.rect.bottomright[1]-30
    x_current = x_direction_0
    y_current = station_down.rect.y
    direction = "a"

    for i in range(number_of_chairs):

        if direction == "a" and y_current < y_limit_up:
            direction = "b"
            rest = y_limit_up - y_current
            y_current = y_limit_up
            x_current += rest
        if direction == "b" and x_current > x_direction_1:
            direction = "c"
            rest = x_current -x_direction_1
            x_current = x_direction_1
            y_current += rest
        if direction == "c" and y_current > y_limit_down:
            direction = "d"
            rest = y_current - y_limit_down
            y_current = y_limit_down
            x_current -= rest

        if direction == "a":
            Chair(0, x_current, y_current, "front")
            y_current -= (distance)
        if direction == "b":
            Chair(0, x_current, y_current, "right")
            x_current += (distance)
        if direction == "c":
            Chair(1, x_current, y_current, "front")
            y_current += (distance)
        if direction == "d":
            Chair(1, x_current, y_current, "left")
            x_current -= (distance)



def main():
    global screen, running

    clock = pygame.time.Clock()
    counter = 0

    set_chairs_on_lift(20)




    print(station_down.rect.midleft[0] + 5, station_down.rect.midleft[1])
    print(station_up.rect.midleft[0] + 5, station_up.rect.midleft[1])
    print(station_down.rect.midright[0] - 3, station_down.rect.midright[1])





    while running:

        if counter % FREQUENCY == 0:
            print("Skier")
            Skier()

        counter += 1

        clock.tick(FPS)
        screen.fill(WHITE)
        screen.blit(BACKGROUND, (0,0))



        for s in DRIVING_SKIERS:
            screen.blit(s.picture, (s.rect.x, s.rect.y))
            s.drive(5)

        for c in CHAIRS:
            screen.blit(c.picture, (c.rect.x, c.rect.y))
            c.move(2)

        for s in WAITING_SKIERS:
            screen.blit(s.picture, (s.rect.x, s.rect.y))
            s.move(3)



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
