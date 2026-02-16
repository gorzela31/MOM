# Plik: genotype.py
# Odpowiednik Java: genotype.java (projekt funkcja_wspinaczkowy)


import math
import Globals


class genotype:
    # lancuch genow: x1..x5
    gene: list[float]
    # dopasowanie genotypu (maksymalizacja)
    fitness: float

    def __init__(self):
        self.gene = [0.0] * Globals.IL_ZMIENNYCH
        self.fitness = 0.0

    def oblicz_dopasowanie(self):
        # metoda obliczajaca dopasowanie
        # dopasowanie = 1000 * sin(x1)*sin(x2)*sin(x3)*sin(x4)*sin(x5)
        dopasowanie = (
            1000.0
            * math.sin(self.gene[0])
            * math.sin(self.gene[1])
            * math.sin(self.gene[2])
            * math.sin(self.gene[3])
            * math.sin(self.gene[4])
        )
        return dopasowanie
