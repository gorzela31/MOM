# ------------------------------------------------------------
# Ten plik jest częścią zestawu z zajęć z optymalizacji.
# Wersja Python: dodatkowe komentarze krok-po-kroku.
# ------------------------------------------------------------

# Plik: Funkcja_wspinaczkowy.py
# Odpowiednik Java: Funkcja_wspinaczkowy.java (projekt funkcja_wspinaczkowy)


import os
import sys
import random

sys.path.append(os.path.dirname(__file__))

import Globals
from genotype import genotype

osobnik = genotype()
nowy = genotype()


# Inicjalizacja: przygotowanie rozwiązania startowego (osobnik lub populacja).
# W tym miejscu losujemy wartości początkowe.
def initialize():
    # funkcja inicjujaca (x1..x5) wartosciami z zakresu od 0 do PI
    for i in range(Globals.IL_ZMIENNYCH):
        osobnik.gene[i] = random.random() * Globals.PI

    osobnik.fitness = osobnik.oblicz_dopasowanie()

    print("osobnik")
    for i in range(Globals.IL_ZMIENNYCH):
        print(f"{osobnik.gene[i]}, ", end="")
    print("\ndopasowanie")
    print(osobnik.oblicz_dopasowanie())


# Generowanie nowego kandydata (sąsiada) na bazie aktualnego rozwiązania.
# To tutaj definiujesz 'ruch' w przestrzeni rozwiązań.
def generuj_nowego():
    # modyfikuje losowo wybrana zmienna
    # do starej wartosci dodaje losowo wybrana z zakresu 0 0.5 z dokladnoscia 0.001
    gen_rand = Globals.round_java(random.random() * 4)

    print()
    print(f"gen_rand {gen_rand}")

    for i in range(Globals.IL_ZMIENNYCH):
        nowy.gene[i] = osobnik.gene[i]

    nowy.gene[gen_rand] = nowy.gene[gen_rand] + (random.random() - 0.5) / 100.0

    # ograniczenia [0, PI]
    if nowy.gene[gen_rand] < 0:
        nowy.gene[gen_rand] = 0.0
    if nowy.gene[gen_rand] > Globals.PI:
        nowy.gene[gen_rand] = Globals.PI

    nowy.fitness = nowy.oblicz_dopasowanie()


# Selekcja / akceptacja: decyzja czy przechodzimy na nowe rozwiązanie.
# - Hill climbing: przyjmuj tylko lepsze.
# - SA: czasem przyjmuj gorsze (zależnie od temperatury).
def select():
    # wybiera lepszego (tu: wieksze dopasowanie)
    if nowy.fitness > osobnik.fitness:
        print("zamieniam ")
        for i in range(Globals.IL_ZMIENNYCH):
            osobnik.gene[i] = nowy.gene[i]
        osobnik.fitness = nowy.fitness


def main():
    generation = 0

    initialize()

    while generation < 100000:
        generuj_nowego()
        select()
        generation += 1
        print(f"generation {generation} fitness {osobnik.fitness}", end="")

    print("The best - geny")
    for i in range(Globals.IL_ZMIENNYCH):
        print(f"{osobnik.gene[i]}, ", end="")
    print()
    print(f"fitness {osobnik.fitness}")


# Uruchomienie pliku jako program (odpowiednik Java: public static void main).
if __name__ == "__main__":
    main()
