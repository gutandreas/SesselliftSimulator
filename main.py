import math
import os
import random
from datetime import datetime

import pygame
from pygame.rect import Rect

pygame.init()

# Fenster
(width, height) = (1536, 864)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption("Sessellift Simulator")

# Farben
WHITE = (255, 255, 255)
GREEN = (78, 173, 91)
BLUE = (100, 100, 255)
DARK_BLUE = (47, 110, 186)
BLACK = (0, 0, 0)
RED = (234, 51, 35)
GREY = (82, 82, 82)
DARK_YELLOW = (170, 170, 0)

# Steuerungsvariablen

FACTORS = [[0.222,	0.222,	1.112,	1.112],
[0.890,	0.444,	0.890,	0.890],
[2.000,	0.666,	0.666,	0.666],
[1.778,	1.778,	0.890,	0.444],
[1.112,	3.333,	0.666,	0.222],
[0.890,	1.778,	0.890,	0.890],
[0.666,	0.666,	0.666,	2.000],
[0.444,	0.444,	0.890,	1.778]]

column_dict = {
  "N": 0,
  "NO": 1,
  "O": 2,
  "SO": 3,
  "S": 4,
  "SW": 5,
  "W": 6,
  "NW": 7
}

running = True
FPS = 80
CAPACITY = 3
UTILISATION = 0.80
TOLERANCE = 20
LIFT_SPEED_KMH = 15
LIFT_SPEED_PIXEL = math.ceil(LIFT_SPEED_KMH / 3.6)
LIFT_LENGTH = 1.484
NUMBER_OF_CHAIRS_PER_KM = 20
NUMBER_OF_CHAIRS = math.ceil(NUMBER_OF_CHAIRS_PER_KM * LIFT_LENGTH)
EXPECTED_SKIERS_PER_HOUR = 1000
DIRECTION = "SW"
SKIERS_PER_HOUR = EXPECTED_SKIERS_PER_HOUR*FACTORS[column_dict[DIRECTION]][0]
FREQUENCY = math.ceil(3600 / SKIERS_PER_HOUR)

current_utilisation = 0


# Zeiteinstellung
hours_start = 8
minutes_start = 0
seconds_start = 0

hours_time = 0
minutes_time = 0
seconds_time = 0

report_interval_hours = 0
report_interval_minutes = 0
report_interval_seconds = 55
report_interval = report_interval_hours * 3600 + report_interval_minutes * 60 + report_interval_seconds

duration_as_string = ""
time_as_string = ""




SKIER_DIMENSIONS = (25, 30)
# Bilder
BACKGROUND = pygame.image.load(os.path.join("bilder", "background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))
SKIER_GREEN_PICTURE = pygame.image.load(os.path.join("bilder", "skifahrer_gruen.png"))
SKIER_GREEN_PICTURE = pygame.transform.scale(SKIER_GREEN_PICTURE, SKIER_DIMENSIONS)
SKIER_RED_PICTURE = pygame.image.load(os.path.join("bilder", "skifahrer_rot.png"))
SKIER_RED_PICTURE = pygame.transform.scale(SKIER_RED_PICTURE, SKIER_DIMENSIONS)
SKIER_BLUE_PICTURE = pygame.image.load(os.path.join("bilder", "skifahrer_blau.png"))
SKIER_BLUE_PICTURE = pygame.transform.scale(SKIER_BLUE_PICTURE, SKIER_DIMENSIONS)
SKIER_GREY_PICTURE = pygame.image.load(os.path.join("bilder", "skifahrer_grau.png"))
SKIER_GREY_PICTURE = pygame.transform.scale(SKIER_GREY_PICTURE, SKIER_DIMENSIONS)
SKIER_YELLOW_PICTURE = pygame.image.load(os.path.join("bilder", "skifahrer_gelb.png"))
SKIER_YELLOW_PICTURE = pygame.transform.scale(SKIER_YELLOW_PICTURE, SKIER_DIMENSIONS)
STATION_PICTURE = pygame.image.load(os.path.join("bilder", "station.png"))
STATION_PICTURE = pygame.transform.scale(STATION_PICTURE, (100, 70))
CHAIR_PICTURE = pygame.image.load(os.path.join("bilder", "sessel.png"))
CHAIR_PICTURE = pygame.transform.scale(CHAIR_PICTURE, (40, 40))
CHAIR_PICTURE_RIGHT = pygame.image.load(os.path.join("bilder", "sessel_seite.png"))
CHAIR_PICTURE_RIGHT = pygame.transform.scale(CHAIR_PICTURE_RIGHT, (40, 40))
CHAIR_PICTURE_LEFT = pygame.image.load(os.path.join("bilder", "sessel_seite_2.png"))
CHAIR_PICTURE_LEFT = pygame.transform.scale(CHAIR_PICTURE_LEFT, (40, 40))
POLE = pygame.image.load(os.path.join("bilder", "masten.png"))
POLE = pygame.transform.scale(POLE, (100, 120))
FENCE = pygame.image.load(os.path.join("bilder", "zaun.png"))
FENCE = pygame.transform.scale(FENCE, (250, 20))

SKIER_PICTURES = []
SKIER_PICTURES.append(SKIER_GREY_PICTURE)
SKIER_PICTURES.append(SKIER_YELLOW_PICTURE)
SKIER_PICTURES.append(SKIER_BLUE_PICTURE)
SKIER_PICTURES.append(SKIER_RED_PICTURE)
SKIER_PICTURES.append(SKIER_GREEN_PICTURE)

# Werte
skiers_in_queue = 0
skiers_transported = 0
skiers_on_lift = 0
percent_of_lift_in_use = 0
waiting_time_min = 0
skier_counter_to_adjust_frequency = 0
expected_skiers = 0
lost_skiers = 0
counters_to_adjust_frequency = [0,0,0,0]
time_phase_to_adjust_frequency = 0
lost_skiers_to_adjust_frequency = 0
starting_point = 1600
counter = 0

# Listen
SKIERS = []
CHAIRS = []
TRANSPORTING_CHAIRS = []
WAITING_SKIERS = pygame.sprite.Group()
QUEUE_SKIERS = pygame.sprite.Group()
DRIVING_SKIERS = pygame.sprite.Group()
TEXT_MESSAGES_TITLE = []
TEXT_MESSAGES_VALUES = []



# Textanzeigen
FONTSIZE = 20
#font = pygame.font.Font(pygame.font.get_default_font(), FONTSIZE)
font = pygame.font.SysFont('arial black', FONTSIZE)

colors = [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, ]

titles = ["Skifahrer in Warteschlange:", "Skifahrer transportiert:", "Skifahrer auf Lift:",
          "Auslastung Lift:", "Aktuelle Wartezeit:", "Dauer der Simulation:", "Uhrzeit der Simlation:",
          "Anzahl Sessel pro km:",
          "Anzahl Sessel total:", "Liftgeschwindigkeit:", "Sessel pro Minute:", "Sitze pro Sessel:", "Kapazität pro Stunde:",
          "Neue Skifahrer pro Stunde:", "Soll neue Skifahrer: ", "Verlorene Skifahrer: ", "Himmelsrichtung Lift:"]
for i in range(len(titles)):
    text_message_title = font.render(titles[i], True, (0,0,0))
    TEXT_MESSAGES_TITLE.append(text_message_title)


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
        elif view == "right":
            self.picture = CHAIR_PICTURE_RIGHT.copy()
        else:
            self.picture = CHAIR_PICTURE_LEFT.copy()
        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.at_station = False
        CHAIRS.append(self)
        self.skiers = []

    def move(self, speed):

        global skiers_transported, skiers_on_lift

        if self.direction == 0:
            if self.rect.y < station_up.rect.midleft[1]+5:
                self.picture = CHAIR_PICTURE.copy()
                if self in TRANSPORTING_CHAIRS:
                    TRANSPORTING_CHAIRS.remove(self)
                if len(self.skiers) > 0:
                    for s in self.skiers:
                        DRIVING_SKIERS.add(s)
                        s.rect.y = self.rect.y
                        self.skiers = []
                        skiers_transported += 1
                        skiers_on_lift -= 1
                if self.rect.x < station_up.rect.midright[0]-22:
                    self.rect.x += speed
                    self.picture = CHAIR_PICTURE_RIGHT.copy()
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
                    self.picture = CHAIR_PICTURE_LEFT.copy()
                else:
                    self.rect.x = station_down.rect.midleft[0] - 15
                    self.direction = 0
                    self.rect.y -= speed
                    self.picture = CHAIR_PICTURE.copy()


                    if not self in TRANSPORTING_CHAIRS:
                        global current_utilisation
                        current_utilisation = skiers_on_lift / (len(TRANSPORTING_CHAIRS) * CAPACITY)
                        TRANSPORTING_CHAIRS.append(self)

                        if current_utilisation < UTILISATION:
                            persons_to_transport = math.ceil(CAPACITY*UTILISATION)
                        else:
                            persons_to_transport = math.floor(CAPACITY*UTILISATION)

                        position = 10
                        for i in range(persons_to_transport):
                            if len(WAITING_SKIERS.sprites()) > 0 and WAITING_SKIERS.sprites()[0].rect.x < station_down.rect.x+70:
                                skier = WAITING_SKIERS.sprites()[0]
                                self.skiers.append(skier)
                                WAITING_SKIERS.remove(skier)
                                pygame.draw.circle(self.picture, skier.get_color(), (position, self.picture.get_rect().center[1]+8), 3)
                                position += 30/CAPACITY
                                skiers_on_lift += 1
                                if skier in QUEUE_SKIERS:
                                    QUEUE_SKIERS.remove(skier)

            else:
                self.rect.y += speed



class Skier(pygame.sprite.Sprite):

    def __init__(self):
        global starting_point, skier_counter_to_adjust_frequency
        pygame.sprite.Sprite.__init__(self)
        self.distance = 0
        self.type_number = random.randrange(len(SKIER_PICTURES))
        self.picture = pygame.transform.rotate(SKIER_PICTURES[self.type_number].copy(), 0)
        self.rect = self.picture.get_rect()
        if len(WAITING_SKIERS.sprites()) > 0 and WAITING_SKIERS.sprites()[len(WAITING_SKIERS.sprites())-1].rect.x == starting_point:
            starting_point += 5
        self.rect.x = starting_point
        self.rect.y = 800
        self.rotated = False
        self.waiting_frames = 0
        SKIERS.append(self)
        WAITING_SKIERS.add(self)
        skier_counter_to_adjust_frequency += 1


    def get_color(self):
        if self.type_number == 0:
            return (100, 100, 100)
        elif self.type_number == 1:
            return (184, 191, 13)
        elif self.type_number == 2:
            return (0, 200, 255)
        elif self.type_number == 3:
            return (255, 20, 20)
        else:
            return (20, 220, 20)

    def move(self, speed):
        if not self.rect.collidepoint(station_down.rect.x, station_down.rect.y+50) and self.is_way_free():
            self.rect.x -= speed
        if self.is_in_queue():
            QUEUE_SKIERS.add(self)
        else:
            if self in QUEUE_SKIERS:
                QUEUE_SKIERS.remove(self)


    def is_way_free(self):
        point_to_check = self.rect.midleft
        collision_with = pygame.sprite.spritecollide(self, WAITING_SKIERS, False)
        collision_with.remove(self)
        way_free = True

        for c in collision_with:
            if c.rect.collidepoint(point_to_check):
                way_free = False
        return way_free

    def is_in_queue(self):
        if not self.rect.collidepoint(station_down.rect.x, station_down.rect.y+50) and not self.is_way_free():
            return True
        else:
            return False

    def drive(self, speed):
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
            c = Chair(0, x_current, y_current, "front")
            y_current -= (distance)
            TRANSPORTING_CHAIRS.append(c)
        if direction == "b":
            Chair(0, x_current, y_current, "right")
            x_current += (distance)
        if direction == "c":
            Chair(1, x_current, y_current, "front")
            y_current += (distance)
        if direction == "d":
            Chair(1, x_current, y_current, "left")
            x_current -= (distance)


def update_text(counter):

    global FREQUENCY, hours_time, minutes_time, seconds_time, duration_as_string, time_as_string, expected_skiers, lost_skiers

    TEXT_MESSAGES_VALUES = []
    TEXT_MESSAGES_VALUES.append(font.render(str(len(QUEUE_SKIERS.sprites())), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(font.render(str(skiers_transported), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(font.render(str(skiers_on_lift), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(
        font.render(str(current_utilisation * 100) + " %", True, RED))
    TEXT_MESSAGES_VALUES.append(font.render(str(waiting_time_min) + " min", True, (0, 0, 0)))

    minutes, seconds = divmod(counter, 60)
    hours, minutes = divmod(minutes, 60)
    duration_as_string = f'{hours:d}:{minutes:02d}:{seconds:02d}'
    TEXT_MESSAGES_VALUES.append(font.render(duration_as_string, True, (0, 0, 0)))
    minutes_time, seconds_time = divmod(counter + seconds_start, 60)
    hours_time, minutes_time = divmod(minutes_time + minutes_start, 60)
    days_time, hours_time = divmod(hours_time + hours_start, 24)
    time_as_string = f'{hours_time:d}:{minutes_time:02d}:{seconds_time:02d}'
    TEXT_MESSAGES_VALUES.append(font.render(time_as_string, True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(font.render(str(NUMBER_OF_CHAIRS_PER_KM), True, GREEN))
    TEXT_MESSAGES_VALUES.append(font.render(str(NUMBER_OF_CHAIRS), True, GREEN))
    TEXT_MESSAGES_VALUES.append(font.render(str(LIFT_SPEED_KMH) + " km/h", True, GREY))
    TEXT_MESSAGES_VALUES.append(
        font.render(str(math.ceil(LIFT_SPEED_PIXEL / (1484 / NUMBER_OF_CHAIRS) * 60)), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(font.render(str(CAPACITY), True, DARK_BLUE))
    TEXT_MESSAGES_VALUES.append(
        font.render(str(math.ceil(LIFT_SPEED_PIXEL / (1484 / NUMBER_OF_CHAIRS) * 3600 * CAPACITY*UTILISATION)), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(font.render(str(math.floor(expected_skiers/2)), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(
        font.render(str(math.ceil(SKIERS_PER_HOUR)), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(font.render(str(lost_skiers), True, (0, 0, 0)))
    TEXT_MESSAGES_VALUES.append(font.render(DIRECTION, True, DARK_YELLOW))



    position = 10
    for t in TEXT_MESSAGES_TITLE:
        screen.blit(t, pygame.Rect(20, position, 200, 30))
        position += FONTSIZE + 10

    position = 10
    for t in TEXT_MESSAGES_VALUES:
        screen.blit(t, pygame.Rect(350, position, 200, 30))
        position += FONTSIZE + 10

def get_current_phase():
    if 8 <= hours_time <= 9:
        return 0
    elif 10 <= hours_time <= 11:
        return 1
    elif 12 <= hours_time <= 13:
        return 2
    elif 14 <= hours_time <= 15:
        return 3
    else:
        return 4



def update_rate():


    global FREQUENCY, counters_to_adjust_frequency, counter, time_phase_to_adjust_frequency, skier_counter_to_adjust_frequency, SKIERS_PER_HOUR, lost_skiers_to_adjust_frequency

    if get_current_phase() == 0:
        SKIERS_PER_HOUR = EXPECTED_SKIERS_PER_HOUR * FACTORS[column_dict[DIRECTION]][0]
        counters_to_adjust_frequency[0] = counter
        time_phase_to_adjust_frequency = 0
    elif get_current_phase() == 1:
        SKIERS_PER_HOUR = EXPECTED_SKIERS_PER_HOUR * FACTORS[column_dict[DIRECTION]][1]
        counters_to_adjust_frequency[1] = counter
        if time_phase_to_adjust_frequency != 1:
            print("Phase 1")
            time_phase_to_adjust_frequency = 1
            skier_counter_to_adjust_frequency = 0
            lost_skiers_to_adjust_frequency = 0
    elif get_current_phase() == 2:
        SKIERS_PER_HOUR = EXPECTED_SKIERS_PER_HOUR * FACTORS[column_dict[DIRECTION]][2]
        counters_to_adjust_frequency[2] = counter
        if time_phase_to_adjust_frequency != 2:
            print("Phase 2")
            time_phase_to_adjust_frequency = 2
            skier_counter_to_adjust_frequency = 0
            lost_skiers_to_adjust_frequency = 0
    elif get_current_phase() == 3:
        SKIERS_PER_HOUR = EXPECTED_SKIERS_PER_HOUR * FACTORS[column_dict[DIRECTION]][3]
        counters_to_adjust_frequency[3] = counter
        if time_phase_to_adjust_frequency != 3:
            print("Phase 3")
            time_phase_to_adjust_frequency = 3
            skier_counter_to_adjust_frequency = 0
            lost_skiers_to_adjust_frequency = 0
    else:
        SKIERS_PER_HOUR = 0


    if SKIERS_PER_HOUR == 0:
        FREQUENCY = float("inf")


def draw_screen(counter):
    for s in DRIVING_SKIERS:
        screen.blit(s.picture, (s.rect.x, s.rect.y))
        s.drive(5)

    for c in CHAIRS:
        screen.blit(c.picture, (c.rect.x, c.rect.y))
        c.move(LIFT_SPEED_PIXEL)

    screen.blit(station_down.picture, (station_down.rect.x, station_down.rect.y))
    screen.blit(station_up.picture, (station_up.rect.x, station_up.rect.y))

    skiers_in_queue = 0
    waiting_sum = 0
    for s in WAITING_SKIERS:
        screen.blit(s.picture, (s.rect.x, s.rect.y))
        s.move(7)
        if s.is_in_queue():
            skiers_in_queue += 1
            s.waiting_frames += 1
            waiting_sum += s.waiting_frames

    screen.blit(FENCE, (station_down.rect.x - 15, station_down.rect.y + 63))

    global waiting_time_min, FREQUENCY

    if counter % FPS == 0:
        if skiers_in_queue > 0:
            waiting_time_min = math.floor(skiers_in_queue / (LIFT_SPEED_PIXEL / (1484 / NUMBER_OF_CHAIRS) * CAPACITY * 60))
        else:
            waiting_time_min = 0



    pygame.draw.line(screen, (0, 0, 0),
                     (station_down.rect.midleft[0] + 5, station_down.rect.midleft[1]),
                     (station_up.rect.midleft[0] + 5, station_up.rect.midleft[1]))
    pygame.draw.line(screen, (0, 0, 0),
                     (station_down.rect.midright[0] - 3, station_down.rect.midright[1]),
                     (station_up.rect.midright[0] - 3, station_up.rect.midright[1]))


    screen.blit(POLE, (station_down.rect.midleft[0], station_down.rect.midleft[1] - 200))
    screen.blit(POLE, (station_down.rect.midleft[0], station_down.rect.midleft[1] - 400))
    screen.blit(POLE, (station_down.rect.midleft[0], station_down.rect.midleft[1] - 600))

    update_text(counter)
    update_rate()


    pygame.display.update()

def save_report():

    try:
        file = open("report.txt", "a")
        file.write( "Dauer: " + duration_as_string + "\n"
                    + "Uhrzeit in Simulation: " + time_as_string + "\n"
                    + "Transportierte Skifahrer: " + str(skiers_transported) + "\n"
                    + "Skifahrer in Warteschlange: " + str(len(QUEUE_SKIERS)) + "\n"
                    + "Wartezeit in Minuten: " + str(waiting_time_min) + "\n"
                    + "Liftauslastung tatsaechlich: " + str(current_utilisation) + "\n"
                    + "Liftauslastung angenommen: " + str(UTILISATION) + "\n"
                    + "Ueber/unter Kapazität: " + str(math.ceil(SKIERS_PER_HOUR) - math.ceil(LIFT_SPEED_PIXEL / (1484 / NUMBER_OF_CHAIRS) * 3600 * CAPACITY*UTILISATION)) + "\n"
                    + "Skifahrer pro Stunde (real): " + str(expected_skiers/2) + "\n"
                    + "Skifahrer pro Stunde (soll): " + str(math.ceil(SKIERS_PER_HOUR)) + "\n"
                    + "Vertriebene Skifahrer: " + str(lost_skiers) +
                    "\n\n")
        file.close()
        print("Report wurde gespeichert.")
    except Exception as e:
        print("Report konnte nicht gespeichert werden.")



def main():
    global screen, running, FREQUENCY, counter, time_phase_to_adjust_frequency, expected_skiers, lost_skiers, lost_skiers_to_adjust_frequency

    clock = pygame.time.Clock()

    set_chairs_on_lift(NUMBER_OF_CHAIRS)
    time_phase_to_adjust_frequency = get_current_phase()

    file = open("report.txt", "w")
    file.write("Report zur Simulation von " + str(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
               + " des Users " + str(os.environ.get('USER')) + "\n"
               + "Anzahl Plätze pro Sessel " + str(CAPACITY) + ", Sesselauslastung: " + str(UTILISATION*100) + "%"
               + ", Anzahl Sessel pro km: " + str(NUMBER_OF_CHAIRS_PER_KM) + ", Fahrgeschwindigkeit: " + str(LIFT_SPEED_KMH) + " km/h"
            + ", Toleranz: " + str(TOLERANCE) + "%"
               + ", Himmelsrichtung: " + DIRECTION + "\n\n")
    file.close()


    while running:


        if counter % FREQUENCY == 0:
            if waiting_time_min < 10:
                Skier()
            else:
                if random.randrange(100) < TOLERANCE:
                    Skier()
                else:
                    lost_skiers += 1
                    lost_skiers_to_adjust_frequency += 1



        if counter > 0 and counter % 30 == 0:
            print(skier_counter_to_adjust_frequency)
            print("Aktuelle Phase: ", time_phase_to_adjust_frequency)
            print(EXPECTED_SKIERS_PER_HOUR * FACTORS[column_dict[DIRECTION]][2])
            print(SKIERS_PER_HOUR)
            if time_phase_to_adjust_frequency != 0:
                current_counter = counters_to_adjust_frequency[time_phase_to_adjust_frequency]\
                                  -counters_to_adjust_frequency[time_phase_to_adjust_frequency-1]
            else:
                current_counter = counter

            skiers_in_future = ((7200-current_counter)/FREQUENCY)
            expected_skiers = skier_counter_to_adjust_frequency + skiers_in_future + lost_skiers_to_adjust_frequency

            if expected_skiers < SKIERS_PER_HOUR*2:
                if FREQUENCY != 1:
                    FREQUENCY -= 1
                    print("Häufigkeit erhöht", FREQUENCY)
            else:
                FREQUENCY += 1
                print("Häufigkeit vertieft: ", FREQUENCY)
            print("Aktuelle Skier pro Stunde: ", expected_skiers)
            print("Soll Skier pro Stunde: ", SKIERS_PER_HOUR)
            print("Aktueller Counter: ", current_counter)
            print("Lost Skiers to adjust: ", lost_skiers_to_adjust_frequency)

        counter += 1

        clock.tick(FPS)
        screen.fill(WHITE)
        screen.blit(BACKGROUND, (0,0))


        draw_screen(counter)

        if counter % report_interval == 0:
            save_report()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
