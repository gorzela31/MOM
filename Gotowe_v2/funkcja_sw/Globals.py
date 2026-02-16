# Plik: Globals.py
# Dodatkowy plik (dla modulowosci). W Javie stale byly w klasie glownej.


import math

IL_ZMIENNYCH = 5
PI = math.pi

temp_p = 801
temp_k = 1
liczba_zmian = 800


def round_java(x):
    # Math.round dla dodatnich liczb: floor(x + 0.5)
    return int(math.floor(x + 0.5))
