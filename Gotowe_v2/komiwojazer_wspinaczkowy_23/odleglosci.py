# Plik: odleglosci.py
# Odpowiednik Java: odleglosci.java (projekt komiwojazer_wspinaczkowy_23)


from pathlib import Path


class odleglosci:
    def __init__(self):
        # tablica odleglosci miedzy miastami
        self.miasta = [[0 for _ in range(16)] for _ in range(16)]

    def czytaj_miasta(self):
        # czyta macierz 16x16 z pliku miasta.txt
        # UWAGA: zachowujemy dokladnie taki sam porzadek wczytywania jak w Javie:
        # petla zewnetrzna po j, wewnetrzna po i i zapis do miasta[i][j].
        file_path = Path(__file__).resolve().parent / "miasta.txt"
        tokens = file_path.read_text(encoding="utf-8").split()
        if len(tokens) < 16 * 16:
            raise ValueError(f"Za malo danych w {file_path}. Oczekiwano 256 liczb, jest {len(tokens)}.")

        idx = 0
        for j in range(16):
            for i in range(16):
                self.miasta[i][j] = int(tokens[idx])
                idx += 1

        # wyswietlenie wczytanej macierzy (jak w Javie)
        for i in range(16):
            for j in range(16):
                print(f"{self.miasta[i][j]}, ", end="")
            print()
