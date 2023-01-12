
# TODO: Einstellungen anpassen

settings_dict = {
    "SITZE PRO SESSEL": 4,
    "PROZENT AUSLASTUNG SESSEL": 75,
    "ANZAHL SESSEL PRO KM": 20,
    "FAHRGESCHWINDIGKEIT": 15,
    "HIMMELSRICHTUNG": "S",
    "GRUNDMENGE SKIFAHRER": 1000,
    "PROZENT TOLERANTE SKIFAHRER": 20,
    "STARTZEIT STUNDEN": 8,
    "STARTZEIT MINUTEN": 0,
    "STARTZEIT SEKUNDEN": 0
}

noten_skipiste = [[1,	1,	2,	2],
                  [2,	2,	2,	2],
                  [3,	2,	2,	2],
                  [3,	3,	1,	1],
                  [2,	3,	3,	1],
                  [2,	2,	3,	3],
                  [2,	2,	2,	3],
                  [2,	2,	2,	2]]

noten_sonneneinstrahlung = [[1,	1,	1,	1],
                            [2,	1,	1,	1],
                            [3,	2,	1,	1],
                            [3,	3,	2,	1],
                            [2,	3,	3,	2],
                            [1,	2,	3,	3],
                            [1,	1,	2,	3],
                            [1,	1,	1,	2]]

# NICHT VERÄNDERN!!!
def check_settings():

  if not 2 <= settings_dict["SITZE PRO SESSEL"] <= 6:
    exit("Ungültige Sesselgrösse")
  if not 0 <= settings_dict["PROZENT AUSLASTUNG SESSEL"] <= 100:
    exit("Ungültige Sesselauslastung")
  if not 0 <= settings_dict["ANZAHL SESSEL PRO KM"] <= 20:
    exit("Ungültige Anzahl Sessel pro km")
  if not settings_dict["HIMMELSRICHTUNG"] in ["N", "NO", "O", "SO", "S", "SW", "W", "NW", "N"]:
    exit("Ungültige Himmelsrichtung")
  if not 0 <= settings_dict["GRUNDMENGE SKIFAHRER"] <= 2000:
    exit("Ungültige Grundmegne Skifahrer")
  if not 0 <= settings_dict["PROZENT TOLERANTE SKIFAHRER"] <= 100:
    exit("Ungültige Prozentangabe zu toleranten Skifahrern")
  if not 8 <= settings_dict["STARTZEIT STUNDEN"] <= 16:
    exit("Ungültige Startzeit")
  if not 0 <= settings_dict["STARTZEIT MINUTEN"] <= 59:
    exit("Ungültige Startzeit")
  if not 0 <= settings_dict["STARTZEIT STUNDEN"] <= 59:
    exit("Ungültige Startzeit")


def get_dict():
    return settings_dict
