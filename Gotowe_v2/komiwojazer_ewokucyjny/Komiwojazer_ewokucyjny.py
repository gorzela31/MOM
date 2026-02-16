# ------------------------------------------------------------
# Ten plik jest częścią zestawu z zajęć z optymalizacji.
# Wersja Python: dodatkowe komentarze krok-po-kroku.
# ------------------------------------------------------------

# Plik: Komiwojazer_ewokucyjny.py
# Odpowiednik Java: Komiwojazer_ewokucyjny.java (projekt komiwojazer_ewokucyjny)


import os
import sys
import random

sys.path.append(os.path.dirname(__file__))

import Globals
from Genotype import Genotype

generation = 0  # numer pokolenia

# populacja ma rozmiar POPSIZE+1, a ostatni element (index POPSIZE) trzyma elita (best so far)
populacja = [Genotype() for _ in range(Globals.POPSIZE + 1)]
nowa_populacja = [Genotype() for _ in range(Globals.POPSIZE)]


# Inicjalizacja: przygotowanie rozwiązania startowego (osobnik lub populacja).
# W tym miejscu losujemy wartości początkowe.
def initialize():
    # inicjalizacja populacji losowymi genami w kodowaniu koszowym
    for j in range(Globals.POPSIZE):
        for i in range(Globals.IL_MIAST):
            populacja[j].gene[i] = int(random.random() * 1000) % (Globals.IL_MIAST - i)
            populacja[j].kosz[i] = i
        populacja[j].ustal_trase()


# Ocena populacji: przeliczamy fitness (dopasowanie) dla każdego osobnika.
def evaluate():
    # wyznacz trasy na podstawie genow i oblicz fitness
    for j in range(Globals.POPSIZE):
        for i in range(Globals.IL_MIAST):
            populacja[j].kosz[i] = i
        populacja[j].ustal_trase()

    # UWAGA: tutaj fitness jest przeksztalceniem minimalizacji w maksymalizacje:
    # fitness = MAXDROGA - dlugosc_trasy
    for mem in range(Globals.POPSIZE):
        populacja[mem].fitness = Globals.MAXDROGA - populacja[mem].oblicz_dopasowanie()


def keep_the_best():
    # kopiuje najlepszego dotychczasowego osobnika do populacja[POPSIZE]
    cur_best = 0
    for mem in range(Globals.POPSIZE):
        if populacja[mem].fitness > populacja[Globals.POPSIZE].fitness:
            cur_best = mem
            populacja[Globals.POPSIZE].fitness = populacja[mem].fitness

    populacja[Globals.POPSIZE].copy_genes_from(populacja[cur_best])


# Selekcja / akceptacja: decyzja czy przechodzimy na nowe rozwiązanie.
# - Hill climbing: przyjmuj tylko lepsze.
# - SA: czasem przyjmuj gorsze (zależnie od temperatury).
def select():
    # selekcja ruletkowa (proporcjonalnie do fitness), model elitarny jest realizowany przez keep_the_best/elitist
    fitness = [0.0] * Globals.POPSIZE
    rfitness = [0.0] * Globals.POPSIZE
    cfitness = [0.0] * Globals.POPSIZE

    suma = 0.0
    for mem in range(Globals.POPSIZE):
        suma += populacja[mem].fitness
        fitness[mem] = populacja[mem].fitness

    for mem in range(Globals.POPSIZE):
        rfitness[mem] = fitness[mem] / suma

    cfitness[0] = rfitness[0]
    for mem in range(1, Globals.POPSIZE):
        cfitness[mem] = cfitness[mem - 1] + rfitness[mem]

    # wybor osobnikow
    for i in range(Globals.POPSIZE):
        p = random.random()
        if p < cfitness[0]:
            nowa_populacja[i].copy_genes_from(populacja[0])
        else:
            for j in range(Globals.POPSIZE - 1):
                if p >= cfitness[j] and p < cfitness[j + 1]:
                    nowa_populacja[i].copy_genes_from(populacja[j + 1])
                    break

    # kopiowanie populacji po jej utworzeniu (kopiujemy geny, nie referencje)
    for i in range(Globals.POPSIZE):
        populacja[i].copy_genes_from(nowa_populacja[i])


# Krzyżowanie: tworzenie dzieci na bazie rodziców (operator rekombinacji).
def crossover():
    # wybor do krzyzowania (krzyzowanie jednopunktowe)
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
    # wykonanie krzyzowania dwojga rodzicow
    if Globals.IL_MIAST > 1:
        if Globals.IL_MIAST == 2:
            point = 1
        else:
            point = int(random.random() * 1000) % (Globals.IL_MIAST - 1) + 1

        for i in range(point):
            tmp = populacja[one].gene[i]
            populacja[one].gene[i] = populacja[two].gene[i]
            populacja[two].gene[i] = tmp


# Mutacja: losowa zmiana w osobniku (dywersyfikacja).
def mutate():
    # mutacja jednorodna: podmiana genu na losowa wartosc w jego dopuszczalnym zakresie
    for i in range(Globals.POPSIZE):
        for j in range(Globals.IL_MIAST):
            x = random.random()
            if x < Globals.PMUTATION:
                populacja[i].gene[j] = int(random.random() * 1000) % (Globals.IL_MIAST - j)


def elitist():
    # zachowanie elity (najlepszy osobnik "best so far" jest w populacja[POPSIZE])
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
        populacja[Globals.POPSIZE].copy_genes_from(populacja[best_mem])
        populacja[Globals.POPSIZE].fitness = populacja[best_mem].fitness
    else:
        populacja[worst_mem].copy_genes_from(populacja[Globals.POPSIZE])
        populacja[worst_mem].fitness = populacja[Globals.POPSIZE].fitness


def main():
    global generation

    Globals.czytaj_miasta()
    generation = 0
    initialize()
    evaluate()
    keep_the_best()

    while generation < 2000:
        generation += 1
        select()
        crossover()
        mutate()
        evaluate()
        elitist()

        if generation % 100 == 0:
            # raportujemy prawdziwa dlugosc trasy (odwracamy transformacje fitness)
            print(f"generation {generation} fitness {Globals.MAXDROGA - populacja[Globals.POPSIZE].fitness}")

    print("The best - geny")
    for i in range(Globals.IL_MIAST):
        print(f"{populacja[Globals.POPSIZE].gene[i]}, ", end="")
    print()

    print("The best - trasa")
    for i in range(Globals.IL_MIAST):
        populacja[Globals.POPSIZE].kosz[i] = i
    populacja[Globals.POPSIZE].ustal_trase()
    for i in range(Globals.IL_MIAST):
        print(f"{populacja[Globals.POPSIZE].trasa[i]}, ", end="")
    print()

    print(f"fitness {Globals.MAXDROGA - populacja[Globals.POPSIZE].fitness}")


# Uruchomienie pliku jako program (odpowiednik Java: public static void main).
if __name__ == "__main__":
    main()
