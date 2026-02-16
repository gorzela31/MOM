# Plik: genotype.py
# Odpowiednik Java: genotype.java (projekt komiwojazer_wspinaczkowy_23)

class genotype:
    # lancuch genow
    gene: list[int]
    # zbior miast do wyboru
    kosz: list[int]
    # lista kolejno odwiedzanych miast
    trasa: list[int]
    # dopasowanie genotypu (dla TSP: dlugosc trasy, minimalizujemy)
    fitness: float

    def __init__(self):
        self.gene = [0] * 16
        self.kosz = [0] * 16
        self.trasa = [0] * 16
        self.fitness = 0.0

    def usun_z_kosza(self, poz):
        # usuwa z kosza miasto dolaczone do trasy
        for i in range(poz, 15):
            self.kosz[i] = self.kosz[i + 1]

    def ustal_trase(self):
        # na podstawie genow i kosza ustala porzadek miast w trasie
        for i in range(16):
            self.trasa[i] = self.kosz[self.gene[i]]
            self.usun_z_kosza(self.gene[i])
