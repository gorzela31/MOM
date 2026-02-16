# Plik: Genotype.py
# Odpowiednik Java: Genotype.java (projekt komiwojazer_sw_26)


import Globals


class Genotype:
    # lancuch genow
    gene: list[int]
    # zbior miast do wyboru
    kosz: list[int]
    # lista kolejno odwiedzanych miast
    trasa: list[int]
    # dopasowanie genotypu (dla TSP: dlugosc trasy, minimalizujemy)
    fitness: float

    def __init__(self):
        self.gene = [0] * Globals.IL_MIAST
        self.kosz = [0] * Globals.IL_MIAST
        self.trasa = [0] * Globals.IL_MIAST
        self.fitness = 0.0

    def usun_z_kosza(self, poz):
        # usuwa z kosza miasto dolaczone do trasy
        for i in range(poz, Globals.IL_MIAST - 1):
            self.kosz[i] = self.kosz[i + 1]

    def ustal_trase(self):
        # na podstawie genow i kosza ustala porzadek miast w trasie
        for i in range(Globals.IL_MIAST):
            self.trasa[i] = self.kosz[self.gene[i]]
            self.usun_z_kosza(self.gene[i])

    def oblicz_dopasowanie(self):
        dopasowanie = 0.0

        dopasowanie = Globals.miasta[self.trasa[0]][self.trasa[15]]
        for i in range(Globals.IL_MIAST - 1):
            dopasowanie += Globals.miasta[self.trasa[i]][self.trasa[i + 1]]
        return dopasowanie
