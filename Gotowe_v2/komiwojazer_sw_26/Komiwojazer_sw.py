# ------------------------------------------------------------
# Ten plik jest częścią zestawu z zajęć z optymalizacji.
# Wersja Python: dodatkowe komentarze krok-po-kroku.
# ------------------------------------------------------------

# Plik: Komiwojazer_sw.py
# Odpowiednik Java: Komiwojazer_sw.java (projekt komiwojazer_sw_26)


import os
import sys
import math
import random

sys.path.append(os.path.dirname(__file__))

import Globals
from Genotype import Genotype

generation = 0  # numer pokolenia
osobnik = Genotype()
nowy = Genotype()


# Inicjalizacja: przygotowanie rozwiązania startowego (osobnik lub populacja).
# W tym miejscu losujemy wartości początkowe.
def initialize():
    global osobnik

    for i in range(Globals.IL_MIAST - 1, 0, -1):
        osobnik.gene[Globals.IL_MIAST - 1 - i] = int(random.random() * 1000) % i
        osobnik.kosz[Globals.IL_MIAST - 1 - i] = i

    osobnik.gene[Globals.IL_MIAST - 1] = 0
    osobnik.kosz[Globals.IL_MIAST - 1] = 0
    osobnik.ustal_trase()

    print("osobnik")
    for i in range(Globals.IL_MIAST):
        print(f"{osobnik.gene[i]}, ", end="")
    print()
    print("trasa")
    for i in range(Globals.IL_MIAST):
        print(f"{osobnik.trasa[i]}, ", end="")
    print()


# Generowanie nowego kandydata (sąsiada) na bazie aktualnego rozwiązania.
# To tutaj definiujesz 'ruch' w przestrzeni rozwiązań.
def generuj_nowego():
    global nowy, osobnik

    gen_rand = int(random.random() * 1000) % Globals.IL_MIAST

    for i in range(Globals.IL_MIAST):
        nowy.gene[i] = osobnik.gene[i]

    for i in range(Globals.IL_MIAST - 1, 0, -1):
        nowy.kosz[Globals.IL_MIAST - 1 - i] = i

    nowy.gene[gen_rand] = int(random.random() * 1000) % (Globals.IL_MIAST - gen_rand)

    nowy.ustal_trase()
    nowy.fitness = nowy.oblicz_dopasowanie()


def temperatura(n):
    # Procedura obliczania temperatury
    wynik = Globals.temp_p - n * (Globals.temp_p - Globals.temp_k) / (Globals.liczba_zmian)
    return wynik


# Selekcja / akceptacja: decyzja czy przechodzimy na nowe rozwiązanie.
# - Hill climbing: przyjmuj tylko lepsze.
# - SA: czasem przyjmuj gorsze (zależnie od temperatury).
def select():
    global osobnik, nowy, generation

    if nowy.fitness < osobnik.fitness:
        for i in range(Globals.IL_MIAST):
            osobnik.gene[i] = nowy.gene[i]
        osobnik.fitness = nowy.fitness
    else:
        # Akceptacja gorszego rozwiazania z prawdopodobienstwem zaleznym od temperatury
        # Dla minimizacji: exp((stare - nowe) / T)
        if random.random() < math.exp((osobnik.fitness - nowy.fitness) / temperatura(generation)):
            print("zamieniam na gorszy")
            for i in range(Globals.IL_MIAST):
                osobnik.gene[i] = nowy.gene[i]
            osobnik.fitness = nowy.fitness


def main():
    global generation

    Globals.czytaj_miasta()
    generation = 0
    initialize()

    osobnik.fitness = osobnik.oblicz_dopasowanie()
    print(f"dopasowanie: {osobnik.fitness}")

    while generation < 800:
        generuj_nowego()
        select()
        generation += 1
        print(f"generation {generation} fitness {osobnik.fitness}")

    print("The best - geny, trasa")
    for i in range(Globals.IL_MIAST):
        print(f"{osobnik.gene[i]}, ", end="")
    print()
    for i in range(Globals.IL_MIAST):
        print(f"{osobnik.trasa[i]}, ", end="")
    print()
    print(f"fitness {osobnik.fitness}")

    print("Koniec - Algorytm sw dla optymalizacji komiwojazera")


# Uruchomienie pliku jako program (odpowiednik Java: public static void main).
if __name__ == "__main__":
    main()
