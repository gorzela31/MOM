# Plik: Globals.py
# Dodatkowy plik (dla modulowosci). W Javie stale byly w klasie glownej.


import math

IL_ZMIENNYCH = 5  # liczba zmiennych x1..x5
PI = math.pi


def round_java(x):
    # Odpowiednik Math.round dla dodatnich liczb: floor(x + 0.5)
    return int(math.floor(x + 0.5))
