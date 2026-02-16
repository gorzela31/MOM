# ------------------------------------------------------------
# Ten plik jest częścią zestawu z zajęć z optymalizacji.
# Wersja Python: dodatkowe komentarze krok-po-kroku.
# ------------------------------------------------------------

# Plik: Komiwojazer_wspinaczkowy.py
# Odpowiednik Java: Komiwojazer_wspinaczkowy.java (projekt komiwojazer_wspinaczkowy_23)


import os
import sys
import math
import random

# Pozwala uruchamiac plik z dowolnego katalogu: python sciezka/do/Komiwojazer_wspinaczkowy.py
sys.path.append(os.path.dirname(__file__))

from genotype import genotype
from odleglosci import odleglosci

# numer biezacego pokolenia
generation = 0

# tablica odleglosci miedzy miastami
tsp = odleglosci()

osobnik = genotype()
nowy = genotype()


# Inicjalizacja: przygotowanie rozwiązania startowego (osobnik lub populacja).
# W tym miejscu losujemy wartości początkowe.
def initialize():
    # inicjalizacja losowa genow i kosza, potem wyznaczenie trasy
    global osobnik
    for i in range(15, -1, -1):
        osobnik.gene[15 - i] = int(random.random() * 1000) % (i + 1)
        osobnik.kosz[15 - i] = i

    osobnik.ustal_trase()

    print("osobnik")
    for i in range(16):
        print(f"{osobnik.gene[i]}, ", end="")
    print()
    print("trasa")
    for i in range(16):
        print(f"{osobnik.trasa[i]}, ", end="")
    print()


def oblicz_dopasowanie(osob):
    # dla TSP: dopasowanie = dlugosc trasy (minimalizujemy)
    dopasowanie = 0.0

    # domkniecie cyklu: od pierwszego do ostatniego
    dopasowanie = tsp.miasta[osob.trasa[0]][osob.trasa[15]]

    # suma odleglosci kolejnych odcinkow
    for i in range(15):
        dopasowanie += tsp.miasta[osob.trasa[i]][osob.trasa[i + 1]]

    return dopasowanie


# Generowanie nowego kandydata (sąsiada) na bazie aktualnego rozwiązania.
# To tutaj definiujesz 'ruch' w przestrzeni rozwiązań.
def generuj_nowego():
    # modyfikuje losowo wybrany gen, pozostale kopiuje
    global nowy, osobnik

    gen_rand = int(random.random() * 1000) % 16

    # kopiowanie genow
    for i in range(16):
        nowy.gene[i] = osobnik.gene[i]

    # odtworzenie kosza (15..1, a ostatnia wartosc domyslnie zostaje 0)
    for i in range(15, 0, -1):
        nowy.kosz[15 - i] = i

    # modyfikacja jednego genu
    nowy.gene[gen_rand] = int(random.random() * 1000) % (16 - gen_rand)

    # wyznacz trase i policz fitness
    nowy.ustal_trase()
    nowy.fitness = oblicz_dopasowanie(nowy)


# Selekcja / akceptacja: decyzja czy przechodzimy na nowe rozwiązanie.
# - Hill climbing: przyjmuj tylko lepsze.
# - SA: czasem przyjmuj gorsze (zależnie od temperatury).
def select():
    # wybiera lepszego (mniejsza dlugosc trasy)
    global osobnik, nowy
    if nowy.fitness < osobnik.fitness:
        print("zamieniam ")
        for i in range(16):
            osobnik.gene[i] = nowy.gene[i]
        osobnik.fitness = nowy.fitness


def main():
    global generation

    tsp.czytaj_miasta()
    generation = 0
    initialize()

    osobnik.fitness = oblicz_dopasowanie(osobnik)
    print(osobnik.fitness)

    while generation < 10000:
        generuj_nowego()
        select()
        generation += 1
        print(f"generation {generation} fitness {osobnik.fitness}")

    print("The best - geny, trasa")
    for i in range(16):
        print(f"{osobnik.gene[i]}, ", end="")
    print()
    for i in range(16):
        print(f"{osobnik.trasa[i]}, ", end="")
    print()
    print(f"fitness {osobnik.fitness}")

    print("Koniec - Algorytm wspinaczkowy dla optymalizacji komiwojazera")


# Uruchomienie pliku jako program (odpowiednik Java: public static void main).
if __name__ == "__main__":
    main()
