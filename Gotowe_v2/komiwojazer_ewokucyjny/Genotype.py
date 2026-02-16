# Plik: Genotype.py
# Odpowiednik Java: Genotype.java (projekt komiwojazer_ewokucyjny)


import Globals


class Genotype:
    # lancuch genow (kodowanie "koszowe": gen i ma zakres 0..IL_MIAST-i-1)
    gene: list[int]
    # zbior miast do wyboru
    kosz: list[int]
    # lista kolejno odwiedzanych miast (wyznaczana na podstawie gene+kosz)
    trasa: list[int]
    # dopasowanie genotypu (w tej implementacji: wartosc po transformacji MAXDROGA - dlugosc_trasy)
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
        # rzeczywista dlugosc trasy (minimalizujemy)
        dopasowanie = 0.0

        dopasowanie = Globals.miasta[self.trasa[0]][self.trasa[15]]
        for i in range(Globals.IL_MIAST - 1):
            dopasowanie += Globals.miasta[self.trasa[i]][self.trasa[i + 1]]

        return dopasowanie

    def copy_genes_from(self, other):
        # Pomocnicza metoda: kopiuje same geny (jak w Javie w keep_the_best/elitist)
        for i in range(Globals.IL_MIAST):
            self.gene[i] = other.gene[i]
