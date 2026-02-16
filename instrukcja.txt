Pewnie. Poniżej masz instrukcję w dokładnie takiej strukturze, żebyś mógł robić punkt po punkcie i po każdym zestawie kliknąć Run.

Założenia wspólne (żebyś nie musiał zgadywać):

* **W każdym folderze** masz plik `opcje_z_prezentacji.py` (to jest “magazyn” opcji).
* W `funkcja_*` fitness liczy się w `Genotype.py` albo `genotype.py` w metodzie `oblicz_dopasowanie()`.
* W `komiwojazer_*` fitness liczy się z trasy w podobnym miejscu, ale część operatorów działa na `route`, więc czasem robisz `gene -> route -> gene`.

---

# A) Funkcje dla folderów `funkcja_*`

## 1) `f_sin(x)`

**Co to jest:** funkcja celu, dostaje `x = lista floatów` i zwraca fitness.

### Krok po kroku

1. Otwórz plik:
   `funkcja_ewolucyjny/Genotype.py`
   (albo `genotype.py` w innych `funkcja_*`)
2. Znajdź metodę liczącą fitness:
   `def oblicz_dopasowanie(self):`
3. Na górze pliku dopisz import:

   ```python
   from opcje_z_prezentacji import f_sin
   ```
4. Wewnątrz `oblicz_dopasowanie()` podmień całe liczenie fitness na:

   ```python
   return f_sin(self.gene)
   ```
5. Kliknij Run.

### Co jeszcze może wymagać zmiany

* Jeśli w Twoim kodzie po drodze robisz jakieś “+1000” albo odwracanie wyniku: usuń to w tym miejscu, bo `f_sin` ma być zwracane bez kombinowania.

---

## 2) `f_cos_shift(x)`

**Co to jest:** alternatywna funkcja celu (maksimum 2000).

### Krok po kroku

1. Otwórz: `funkcja_ewolucyjny/Genotype.py`
2. Dopisz import:

   ```python
   from opcje_z_prezentacji import f_cos_shift
   ```
3. W `oblicz_dopasowanie()` ustaw:

   ```python
   return f_cos_shift(self.gene)
   ```
4. Run.

### Co jeszcze może wymagać zmiany

* Nic poza miejscem liczenia fitness.

---

## 3) `clamp_pi(x)`

**Co to jest:** ograniczenie wektora do zakresu `[0, PI]`.

### Krok po kroku (kiedy używać)

Używasz tego wtedy, gdy Twoja mutacja / ruch może wyjść poza zakres.

1. Otwórz plik, gdzie modyfikujesz `gene`:

   * hill climb / SA: plik główny (`Funkcja_wspinaczkowy.py`, `Funkcja_sw.py`)
   * GA: tam gdzie jest mutacja dziecka
2. Dopisz import:

   ```python
   from opcje_z_prezentacji import clamp_pi
   ```
3. Po każdej zmianie genu dopisz:

   ```python
   osobnik.gene = clamp_pi(osobnik.gene)
   ```

   albo dla dziecka:

   ```python
   dziecko.gene = clamp_pi(dziecko.gene)
   ```
4. Run.

### Co jeszcze może wymagać zmiany

* Nic, to jest bezpieczne i zawsze działa.

---

## 4) `neigh_small_step(x, step=...)`

**Co to jest:** gotowy ruch (sąsiad) dla hill climbing i SA.

### Krok po kroku

1. Otwórz:

   * `funkcja_wspinaczkowy/Funkcja_wspinaczkowy.py` albo
   * `funkcja_sw/Funkcja_sw.py`
2. Dopisz import:

   ```python
   from opcje_z_prezentacji import neigh_small_step
   ```
3. Znajdź miejsce tworzenia kandydata (zwykle `generuj_nowego()` albo fragment gdzie ustawiasz `nowy.gene`)
4. Podmień generowanie kandydata na:

   ```python
   nowy.gene = neigh_small_step(osobnik.gene, step=0.05)
   ```
5. Run.

### Co jeszcze może wymagać zmiany

* Dla SA często dajesz większy krok, np. `step=0.1` lub `0.2`.
* `neigh_small_step` sam pilnuje zakresu `[0, PI]`.

---

## 5) `cooling_linear(...)`, `cooling_geometric(...)`, `cooling_logarithmic(...)`

**Co to jest:** harmonogram temperatury dla SA.

### Krok po kroku

1. Otwórz: `funkcja_sw/Funkcja_sw.py`
2. Dopisz import:

   ```python
   from opcje_z_prezentacji import cooling_linear, cooling_geometric, cooling_logarithmic
   ```
3. Znajdź miejsce, gdzie zmniejszasz temperaturę `temp` w pętli
4. Podmień na jeden wariant:

* liniowy:

  ```python
  temp = cooling_linear(t0, t_end, k, iters)
  ```

* geometryczny:

  ```python
  temp = cooling_geometric(temp, alpha=0.995)
  ```

* logarytmiczny:

  ```python
  temp = cooling_logarithmic(t0, k)
  if temp < t_end:
      temp = t_end
  ```

5. Run.

### Co jeszcze może wymagać zmiany

* Upewnij się, że masz:

  * `t0` (start temp), `t_end` (koniec), `iters` (max iteracji), `k` (numer iteracji).
* Jeśli nie masz, ustaw na początku:

  ```python
  t0 = 10.0
  t_end = 1e-3
  iters = 10000
  ```

---

## 6) Selekcje GA: `select_roulette`, `select_tournament`, `select_rank`, `select_sus`

**Co to jest:** różne sposoby wyboru rodziców.

### Krok po kroku

1. Otwórz:

   * `funkcja_ewolucyjny/Funkcja_ewolucyjny.py` lub
   * `funkcja_ewolucyjny_usredniajacy/Funkcja_ewolucyjny_usredniajacy.py`
2. Dopisz import:

   ```python
   from opcje_z_prezentacji import select_roulette, select_tournament, select_rank, select_sus
   ```
3. Znajdź fragment wyboru rodziców (rodzic1/rodzic2)
4. Podmień:

* ruletka:

  ```python
  rodzic1 = select_roulette(populacja, fitnessy)
  rodzic2 = select_roulette(populacja, fitnessy)
  ```

* turniej:

  ```python
  rodzic1 = select_tournament(populacja, fitnessy, k=3)
  rodzic2 = select_tournament(populacja, fitnessy, k=3)
  ```

* rangowa:

  ```python
  rodzic1 = select_rank(populacja, fitnessy)
  rodzic2 = select_rank(populacja, fitnessy)
  ```

* SUS:

  ```python
  rodzice = select_sus(populacja, fitnessy, n_select=2)
  rodzic1, rodzic2 = rodzice[0], rodzice[1]
  ```

5. Run.

### Co jeszcze może wymagać zmiany

* `fitnessy` musi być listą liczb, gdzie większe = lepsze (w funkcjach tak jest).

---

## 7) Krzyżowania GA: `crossover_uniform`, `crossover_arithmetic`, `crossover_blx_alpha`

### Krok po kroku

1. Otwórz plik GA (`Funkcja_ewolucyjny.py` / `Funkcja_ewolucyjny_usredniajacy.py`)
2. Import:

   ```python
   from opcje_z_prezentacji import crossover_uniform, crossover_arithmetic, crossover_blx_alpha
   ```
3. Znajdź miejsce tworzenia genów dziecka

* uniform:

  ```python
  dziecko.gene = crossover_uniform(rodzic1.gene, rodzic2.gene)
  ```

* BLX-alpha:

  ```python
  dziecko.gene = crossover_blx_alpha(rodzic1.gene, rodzic2.gene, alpha=0.5)
  ```

* arytmetyczne (daje 2 dzieci):

  ```python
  g1, g2 = crossover_arithmetic(rodzic1.gene, rodzic2.gene)
  dziecko1.gene = g1
  dziecko2.gene = g2
  ```

4. Run.

### Co jeszcze może wymagać zmiany

* Jeśli Twój kod tworzy tylko jedno dziecko naraz, wybierz uniform albo BLX-alpha.

---

## 8) Mutacje GA: `mutate_gaussian`, `mutate_non_uniform`

### Krok po kroku

1. Import w pliku GA:

   ```python
   from opcje_z_prezentacji import mutate_gaussian, mutate_non_uniform
   ```
2. W miejscu mutacji dziecka:

* gauss:

  ```python
  dziecko.gene = mutate_gaussian(dziecko.gene, sigma=0.05, p=0.1)
  ```

* non-uniform:

  ```python
  dziecko.gene = mutate_non_uniform(dziecko.gene, t=generation, t_max=IL_POKOLEN, b=2.0, p=0.1)
  ```

3. Run.

### Co jeszcze może wymagać zmiany

* Musisz mieć `generation` i `IL_POKOLEN` w tym miejscu (albo podaj swoje nazwy).

---

# B) Funkcje dla folderów `komiwojazer_*`

Tu pamiętaj o jednej rzeczy: wiele “ładnych” operatorów działa na `route` (permutacji), a Ty często masz `gene` w Lehmer code. Dlatego często robisz konwersję:

* `route = gene_to_route(osobnik.gene)`
* modyfikacja route
* `osobnik.gene = route_to_gene(route)`

---

## 1) Sąsiedztwa: `neigh_swap(route)`, `neigh_insert(route)`, `neigh_inversion(route)`

### Krok po kroku

1. Otwórz plik główny:

   * `komiwojazer_wspinaczkowy_23/Komiwojazer_wspinaczkowy.py` lub
   * `komiwojazer_sw_26/Komiwojazer_sw.py`
2. Import:

   ```python
   from opcje_z_prezentacji import gene_to_route, route_to_gene, neigh_swap, neigh_insert, neigh_inversion
   ```
3. W miejscu generowania `nowy` podmień na schemat:

* swap:

  ```python
  r = gene_to_route(osobnik.gene)
  r2 = neigh_swap(r)
  nowy.gene = route_to_gene(r2)
  ```

* insert:

  ```python
  r = gene_to_route(osobnik.gene)
  r2 = neigh_insert(r)
  nowy.gene = route_to_gene(r2)
  ```

* inversion:

  ```python
  r = gene_to_route(osobnik.gene)
  r2 = neigh_inversion(r)
  nowy.gene = route_to_gene(r2)
  ```

4. Run.

### Co jeszcze może wymagać zmiany

* Nic więcej, fitness liczysz jak dotychczas.

---

## 2) `two_opt_best_improvement(route, odleglosci, max_checks=...)`

### Krok po kroku

1. Otwórz `komiwojazer_sw_26/Komiwojazer_sw.py` (albo wspinaczkowy)
2. Import:

   ```python
   from opcje_z_prezentacji import gene_to_route, route_to_gene, two_opt_best_improvement
   ```
3. W generowaniu nowego:

   ```python
   r = gene_to_route(osobnik.gene)
   r2, _ = two_opt_best_improvement(r, odleglosci, max_checks=200)
   nowy.gene = route_to_gene(r2)
   ```
4. Run.

### Co jeszcze może wymagać zmiany

* `max_checks` kontroluje czas. Jak wolno, zmniejsz np. 50-100.

---

## 3) GA selekcje: `select_tournament`, `select_rank`, `select_sus`, `select_roulette`

### Krok po kroku

1. Otwórz: `komiwojazer_ewokucyjny/Komiwojazer_ewokucyjny.py`
2. Import:

   ```python
   from opcje_z_prezentacji import select_roulette, select_tournament, select_rank, select_sus
   ```
3. W miejscu wyboru rodziców podmień analogicznie jak w funkcjach:

   * turniej:

     ```python
     rodzic1 = select_tournament(populacja, fitnessy, k=3)
     rodzic2 = select_tournament(populacja, fitnessy, k=3)
     ```
   * rangowa:

     ```python
     rodzic1 = select_rank(populacja, fitnessy)
     rodzic2 = select_rank(populacja, fitnessy)
     ```
   * SUS:

     ```python
     rodzice = select_sus(populacja, fitnessy, n_select=2)
     rodzic1, rodzic2 = rodzice[0], rodzice[1]
     ```
4. Run.

### Co jeszcze może wymagać zmiany

* W TSP fitnessy w GA muszą być większe = lepsze. U Ciebie zwykle jest to już zrobione przez `MAXDROGA - długość`.

---

## 4) GA krzyżowania permutacji: `crossover_ox`, `crossover_pmx`, `crossover_cx`

### Krok po kroku

1. Otwórz: `komiwojazer_ewokucyjny/Komiwojazer_ewokucyjny.py`
2. Import:

   ```python
   from opcje_z_prezentacji import gene_to_route, route_to_gene, crossover_ox, crossover_pmx, crossover_cx
   ```
3. W miejscu krzyżowania zrób:

* OX:

  ```python
  p1 = gene_to_route(rodzic1.gene)
  p2 = gene_to_route(rodzic2.gene)
  dziecko_route = crossover_ox(p1, p2)
  dziecko.gene = route_to_gene(dziecko_route)
  ```

* PMX / CX analogicznie tylko zmieniasz nazwę funkcji.

4. Run.

### Co jeszcze może wymagać zmiany

* Nic, ale pamiętaj: krzyżowanie działa na `route`, więc konwersja jest obowiązkowa.

---

## 5) GA mutacje permutacji: `mutate_swap`, `mutate_inversion`, `mutate_scramble`

### Krok po kroku

1. Import:

   ```python
   from opcje_z_prezentacji import gene_to_route, route_to_gene, mutate_swap, mutate_inversion, mutate_scramble
   ```
2. W miejscu mutacji dziecka:

   ```python
   r = gene_to_route(dziecko.gene)
   r = mutate_inversion(r, p=0.05)  # swap lub scramble też ok
   dziecko.gene = route_to_gene(r)
   ```
3. Run.

---

## 6) Tabu Search: `tabu_search_tsp(odleglosci, ...)`

### Krok po kroku (najłatwiej jako osobny run)

1. Otwórz dowolny plik TSP (np. `Komiwojazer_sw.py`)
2. Import:

   ```python
   from opcje_z_prezentacji import tabu_search_tsp
   ```
3. W bloku:

   ```python
   if __name__ == "__main__":
       route, dist = tabu_search_tsp(odleglosci, iters=5000, tabu_size=50)
       print(route, dist)
   ```
4. Run.

### Co jeszcze może wymagać zmiany

* musisz mieć `odleglosci` wczytane (tak jak w Twoim projekcie).

---

## 7) ACO: `aco_tsp(odleglosci, ...)`

### Krok po kroku

1. Import:

   ```python
   from opcje_z_prezentacji import aco_tsp
   ```
2. W `__main__`:

   ```python
   route, dist = aco_tsp(odleglosci, ants=30, iters=200)
   print(route, dist)
   ```
3. Run.

---

Jeśli chcesz, mogę Ci to przerobić jeszcze bardziej “bezmyślnie”: powiesz mi jedną konkretną podmianę (np. w `funkcja_ewolucyjny`: f_sin + turniej + BLX + mutate_gaussian) i dostaniesz dokładnie listę:

* plik
* linia/sekcja do znalezienia
* gotowy blok do wklejenia
  tak żeby nie było żadnego “domyśl się”.
