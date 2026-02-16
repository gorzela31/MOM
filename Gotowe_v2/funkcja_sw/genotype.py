# Plik: genotype.py
# Odpowiednik Java: genotype.java (projekt funkcja_sw)


import math
import Globals


class genotype:
    gene: list[float]   # lancuch genow
    fitness: float      # dopasowanie genotypu (maksymalizacja)

    def __init__(self):
        self.gene = [0.0] * Globals.IL_ZMIENNYCH
        self.fitness = 0.0

    def oblicz_dopasowanie(self):
        dopasowanie = (
            1000.0
            * math.sin(self.gene[0])
            * math.sin(self.gene[1])
            * math.sin(self.gene[2])
            * math.sin(self.gene[3])
            * math.sin(self.gene[4])
        )
        return dopasowanie
