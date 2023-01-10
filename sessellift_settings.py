
# TODO: Einstellungen anpassen

settings_dict = {
  "SITZE PRO SESSEL": 5,
  "PROZENT AUSLASTUNG SESSEL": 80,
  "ANZAHL SESSEL PRO KM": 20,
  "FAHRGESCHWINDIGKEIT": 15,
  "HIMMELSRICHTUNG": "NO",
  "GRUNDMENGE SKIFAHRER": 1000,
  "PROZENT TOLERANTE SKIFAHRER": 20
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


def get_dict():
    return settings_dict
