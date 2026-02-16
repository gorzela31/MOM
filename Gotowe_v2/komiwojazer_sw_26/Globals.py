# Plik: Globals.py
# Odpowiednik Java: Globals.java (projekt komiwojazer_sw_26)


from pathlib import Path

IL_MIAST = 16  # liczba miast

# tablica odleglosci miedzy miastami
miasta = [[0 for _ in range(IL_MIAST)] for _ in range(IL_MIAST)]

temp_p = 801
temp_k = 1
liczba_zmian = 800


def czytaj_miasta():
    # czyta macierz 16x16 z pliku miasta.txt
    # Zachowujemy porzadek wczytywania taki jak w Javie: miasta[i][j]
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
