# Komiwojazer_bf.py
# 1:1 odpowiednik Komiwojazer_bf.java z projektu komiwojazer_bf
#
# Uwaga: brute force dla 16 miast jest obliczeniowo niewykonalny w praktyce (16! przypadkow).
# Ten plik jest wiernym przepisaniem logiki z Javy, lacznie z wydrukami postepu.

import Globals
from genotype import genotype

osobnik = genotype()
best = genotype()


def wyswietl_osobnika():
    print("geny")
    for i in range(Globals.IL_MIAST):
        print(f"{osobnik.gene[i]} ", end="")
    print()


def wyswietl_trase():
    print("trasa")
    for i in range(Globals.IL_MIAST):
        print(f"{osobnik.trasa[i]} ", end="")
    print()


def oblicz_osobnika():
    # dokładnie jak w Javie
    for j in range(Globals.IL_MIAST):
        osobnik.kosz[j] = j

    for j in range(Globals.IL_MIAST):
        osobnik.trasa[j] = osobnik.kosz[osobnik.gene[j]]
        osobnik.usun_z_kosza(osobnik.gene[j])

    osobnik.fitness = osobnik.oblicz_dopasowanie()

    if (osobnik.fitness > 0) and (osobnik.fitness < best.fitness):
        best.fitness = osobnik.fitness
        for j in range(Globals.IL_MIAST):
            best.trasa[j] = osobnik.trasa[j]


def buduj_trase():
    # Odpowiednik kaskady petli i0..i14 z Javy (gene[15] zawsze 0)
    lk = 0.0
    liczba_kombinacji = 1307674368  # dokładnie jak w Javie

    osobnik.gene[15] = 0  # ostatni musi byc 0

    # Rekurencja odtwarza dokladnie petle:
    # gene[0] 0..15, gene[1] 0..14, ..., gene[14] 0..1
    def rec(pos: int):
        nonlocal lk

        if pos == 14:
            for val in range(2):  # i14 < 2
                osobnik.gene[14] = val
                lk = lk + 0.001
                oblicz_osobnika()
            return

        # zakres jak w Javie: i0<16, i1<15, ..., i13<3
        upper = Globals.IL_MIAST - pos
        for val in range(upper):
            osobnik.gene[pos] = val
            rec(pos + 1)

            # druk postepu jest wewnatrz petli i4 (dokladnie po zakonczeniu i5..i14)
            if pos == 4:
                print(f"liczba kombinacji {lk} procent {lk / liczba_kombinacji}")
                print(f"dopasowanie {best.fitness}")

    rec(0)


def main():
    Globals.czytaj_miasta()
    best.fitness = 1000000
    buduj_trase()

    print(f"dopasowanie najlepszego {best.fitness}")
    for i in range(Globals.IL_MIAST):
        print(f"{best.trasa[i]} ", end="")

if __name__ == "__main__":
    main()
