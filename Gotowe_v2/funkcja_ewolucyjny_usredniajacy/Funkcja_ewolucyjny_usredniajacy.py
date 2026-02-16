# ------------------------------------------------------------
# Ten plik jest częścią zestawu z zajęć z optymalizacji.
# Wersja Python: dodatkowe komentarze krok-po-kroku.
# ------------------------------------------------------------

# Plik: Funkcja_ewolucyjny_usredniajacy.py
# Odpowiednik Java: Funkcja_ewolucyjny_usredniajacy.java


import os
import sys
import math
import random

sys.path.append(os.path.dirname(__file__))

import Globals
from Genotype import Genotype

generation = 0

populacja = [Genotype() for _ in range(Globals.POPSIZE + 1)]
nowa_populacja = [Genotype() for _ in range(Globals.POPSIZE)]


def losowa(dol, gora):
    wynik = dol + random.random() * (gora - dol)
    return wynik


# Inicjalizacja: przygotowanie rozwiązania startowego (osobnik lub populacja).
# W tym miejscu losujemy wartości początkowe.
def initialize():
    for j in range(Globals.POPSIZE):
        for i in range(Globals.IL_ZMIENNYCH):
            populacja[j].gene[i] = losowa(0.0, math.pi)


# Ocena populacji: przeliczamy fitness (dopasowanie) dla każdego osobnika.
def evaluate():
    for mem in range(Globals.POPSIZE):
        populacja[mem].fitness = populacja[mem].oblicz_dopasowanie()


def keep_the_best():
    cur_best = 0
    for mem in range(Globals.POPSIZE):
        if populacja[mem].fitness > populacja[Globals.POPSIZE].fitness:
            cur_best = mem
            populacja[Globals.POPSIZE].fitness = populacja[mem].fitness

    for i in range(Globals.IL_ZMIENNYCH):
        populacja[Globals.POPSIZE].gene[i] = populacja[cur_best].gene[i]


# Selekcja / akceptacja: decyzja czy przechodzimy na nowe rozwiązanie.
# - Hill climbing: przyjmuj tylko lepsze.
# - SA: czasem przyjmuj gorsze (zależnie od temperatury).
def select():
    suma = 0.0
    for mem in range(Globals.POPSIZE):
        suma += populacja[mem].fitness

    for mem in range(Globals.POPSIZE):
        populacja[mem].rfitness = populacja[mem].fitness / suma

    populacja[0].cfitness = populacja[0].rfitness
    for mem in range(1, Globals.POPSIZE):
        populacja[mem].cfitness = populacja[mem - 1].cfitness + populacja[mem].rfitness

    for i in range(Globals.POPSIZE):
        p = random.random()
        if p < populacja[0].cfitness:
            nowa_populacja[i].copy_from(populacja[0])
        else:
            for j in range(Globals.POPSIZE - 1):
                if p >= populacja[j].cfitness and p < populacja[j + 1].cfitness:
                    nowa_populacja[i].copy_from(populacja[j + 1])
                    break

    for i in range(Globals.POPSIZE):
        populacja[i].copy_from(nowa_populacja[i])


# Krzyżowanie: tworzenie dzieci na bazie rodziców (operator rekombinacji).
def crossover():
    one = 0
    first = 0
    for mem in range(Globals.POPSIZE):
        x = random.random()
        if x < Globals.PXOVER:
            first += 1
            if first % 2 == 0:
                Xover(one, mem)
            else:
                one = mem


def Xover(one, two):
    # Krzyzowanie usredniajace (arytmetyczne) z losowym alfa:
    # dziecko1 = alfa*rodzic1 + (1-alfa)*rodzic2
    # dziecko2 = (1-alfa)*rodzic1 + alfa*rodzic2
    alfa = random.random()

    tmp1 = [0.0] * Globals.IL_ZMIENNYCH
    tmp2 = [0.0] * Globals.IL_ZMIENNYCH

    for i in range(Globals.IL_ZMIENNYCH):
        tmp1[i] = alfa * populacja[one].gene[i] + (1 - alfa) * populacja[two].gene[i]
        tmp2[i] = (1 - alfa) * populacja[one].gene[i] + alfa * populacja[two].gene[i]

    for i in range(Globals.IL_ZMIENNYCH):
        populacja[one].gene[i] = tmp1[i]
        populacja[two].gene[i] = tmp2[i]


# Mutacja: losowa zmiana w osobniku (dywersyfikacja).
def mutate():
    for i in range(Globals.POPSIZE):
        for j in range(Globals.IL_ZMIENNYCH):
            x = random.random()
            if x < Globals.PMUTATION:
                populacja[i].gene[j] = populacja[i].gene[j] + losowa(-0.1, 0.1)
                if populacja[i].gene[j] < 0:
                    populacja[i].gene[j] = 0.0
                if populacja[i].gene[j] > math.pi:
                    populacja[i].gene[j] = math.pi


def elitist():
    best = populacja[0].fitness
    worst = populacja[0].fitness
    best_mem = 0
    worst_mem = 0

    for i in range(1, Globals.POPSIZE):
        if populacja[i].fitness >= best:
            best = populacja[i].fitness
            best_mem = i
        if populacja[i].fitness <= worst:
            worst = populacja[i].fitness
            worst_mem = i

    if best >= populacja[Globals.POPSIZE].fitness:
        for i in range(Globals.IL_ZMIENNYCH):
            populacja[Globals.POPSIZE].gene[i] = populacja[best_mem].gene[i]
        populacja[Globals.POPSIZE].fitness = populacja[best_mem].fitness
    else:
        for i in range(Globals.IL_ZMIENNYCH):
            populacja[worst_mem].gene[i] = populacja[Globals.POPSIZE].gene[i]
        populacja[worst_mem].fitness = populacja[Globals.POPSIZE].fitness


def main():
    global generation

    generation = 0
    initialize()
    evaluate()
    keep_the_best()

    while generation < 1000:
        generation += 1
        select()
        crossover()
        mutate()
        evaluate()
        elitist()

        if generation % 1 == 0:
            print(f"generation {generation} fitness {populacja[Globals.POPSIZE].fitness}")

    print("The best - geny")
    for i in range(Globals.IL_ZMIENNYCH):
        print(f"{populacja[Globals.POPSIZE].gene[i]}, ", end="")
    print()
    print(f"fitness {populacja[Globals.POPSIZE].fitness}")


# Uruchomienie pliku jako program (odpowiednik Java: public static void main).
if __name__ == "__main__":
    main()
