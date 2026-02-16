# Plik: Globals.py
# Odpowiednik Java: Globals.java (projekt komiwojazer_ewokucyjny)


from pathlib import Path

IL_MIAST = 16                 # ilosc zmiennych (miast)
POPSIZE = 25                  # liczebnosc populacji
MAXGENS = 100                 # maksymalna liczba pokolen (w kodzie glowne petle maja wlasny limit)
PXOVER = 0.8                # prawdopodobienstwo krzyzowania
PMUTATION = 0.1             # prawdopodobienstwo mutacji
MAXDROGA = 8000             # maksymalna droga (do transformacji fitness dla ruletki)

# tablica odleglosci miedzy miastami
miasta = [[0 for _ in range(IL_MIAST)] for _ in range(IL_MIAST)]


def czytaj_miasta():
    file_path = Path(__file__).resolve().parent / "miasta.txt"
    tokens = file_path.read_text(encoding="utf-8").split()
    if len(tokens) < IL_MIAST * IL_MIAST:
        raise ValueError(f"Za malo danych w {file_path}. Oczekiwano 256 liczb, jest {len(tokens)}.")

    idx = 0
    for j in range(IL_MIAST):
        for i in range(IL_MIAST):
            miasta[i][j] = int(tokens[idx])
            idx += 1

    for i in range(IL_MIAST):
        for j in range(IL_MIAST):
            print(f"{miasta[i][j]}, ", end="")
        print()
