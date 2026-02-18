# genotype.py
# 1:1 odpowiednik genotype.java z projektu komiwojazer_bf

import Globals


class genotype:
    # lancuch genow
    gene: list[int]
    # zbior miast do wyboru
    kosz: list[int]
    # lista kolejno odwiedzanych miast
    trasa: list[int]
    # dopasowanie (dla TSP: dlugosc trasy, minimalizujemy)
    fitness: float

    def __init__(self):
        self.gene = [0] * Globals.IL_MIAST
        self.kosz = [0] * Globals.IL_MIAST
        self.trasa = [0] * Globals.IL_MIAST
        self.fitness = 0.0

    def usun_z_kosza(self, poz: int) -> None:
        for i in range(poz, Globals.IL_MIAST - 1):
            self.kosz[i] = self.kosz[i + 1]

    def ustal_trase(self) -> None:
        for i in range(Globals.IL_MIAST):
            self.trasa[i] = self.kosz[self.gene[i]]
            self.usun_z_kosza(self.gene[i])

    def oblicz_dopasowanie(self) -> float:
        dopasowanie = Globals.miasta[self.trasa[0]][self.trasa[Globals.IL_MIAST - 1]]
        for i in range(Globals.IL_MIAST - 1):
            dopasowanie += Globals.miasta[self.trasa[i]][self.trasa[i + 1]]
        return float(dopasowanie)
