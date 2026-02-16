# Plik: Genotype.py
# Odpowiednik Java: Genotype.java (projekt funkcja_ewolucyjny)


import math
import Globals


class Genotype:
    gene: list[float]        # lancuch genow
    fitness: float           # dopasowanie genotypu (maksymalizacja)
    rfitness: float          # dopasowanie wzgledne
    cfitness: float          # dopasowanie laczne

    def __init__(self):
        self.gene = [0.0] * Globals.IL_ZMIENNYCH
        self.fitness = 0.0
        self.rfitness = 0.0
        self.cfitness = 0.0

    def oblicz_dopasowanie(self):
        # dopasowanie = 1000 + 1000*cos(x1)*...*cos(x5)
        dopasowanie = (
            1000.0
            + 1000.0
            * math.cos(self.gene[0])
            * math.cos(self.gene[1])
            * math.cos(self.gene[2])
            * math.cos(self.gene[3])
            * math.cos(self.gene[4])
        )
        return dopasowanie

    def copy_from(self, other):
        # kopiuje geny i pola fitness (dla czytelnosci, w Javie czesto kopiowano tylko geny)
        for i in range(Globals.IL_ZMIENNYCH):
            self.gene[i] = other.gene[i]
        self.fitness = other.fitness
        self.rfitness = other.rfitness
        self.cfitness = other.cfitness
