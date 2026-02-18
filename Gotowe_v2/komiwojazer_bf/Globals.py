# Globals.py
# 1:1 odpowiednik Globals.java z projektu komiwojazer_bf (wczytywanie macierzy 16x16)

from pathlib import Path

IL_MIAST = 16
miasta = [[0 for _ in range(IL_MIAST)] for _ in range(IL_MIAST)]


def czytaj_miasta() -> None:
    """Czyta macierz 16x16 z pliku miasta.txt (w tym samym katalogu).
    Zachowuje dokladnie taki sam porzadek jak w Javie:
    petla zewnetrzna po j, wewnetrzna po i i zapis do miasta[i][j].
    """
    file_path = Path(__file__).resolve().parent / "miasta.txt"
    tokens = file_path.read_text(encoding="utf-8").split()
    if len(tokens) < IL_MIAST * IL_MIAST:
        raise ValueError(f"Za malo danych w {file_path}. Oczekiwano 256 liczb, jest {len(tokens)}.")

    idx = 0
    for j in range(IL_MIAST):
        for i in range(IL_MIAST):
            miasta[i][j] = int(tokens[idx])
            idx += 1

    # wyswietlenie wczytanej macierzy (jak w Javie)
    for i in range(IL_MIAST):
        for j in range(IL_MIAST):
            print(f"{miasta[i][j]}, ", end="")
        print()
