# Zanadrze metod i strategii - funkcja_sw

Ten plik to czytelna lista metod z prezentacji (mog1 do mog7), które NIE są zaimplementowane w tym projekcie, ale mogą zostać dołożone bez przebudowy całej struktury.
Służy jako ściąga: co jeszcze było na slajdach i w które miejsce w kodzie to wpiąć.

## Co jest zaimplementowane w tym projekcie
- Symulowane wyżarzanie (simulated annealing) + Metropolis dla funkcji ciągłej (5 zmiennych w 0..PI)
- Chłodzenie liniowe i większy krok modyfikacji niż w hill climbing

## Gdzie wpiąć alternatywy w obecnym kodzie
- generuj_nowego(): generator sąsiada. Tu dopiszesz inne kroki/perturbacje
- select(): reguła Metropolisa. Tu możesz stroić próg akceptacji i logikę
- pętla temperatury w main: tu wpinają się: limit_prob i inne schematy chłodzenia

## Zakres z prezentacji 1 do 7 - lista kontrolna
### mog1.pptx - Wprowadzenie do metaheurystyk optymalizacji globalnej
- pojęcia: heurystyki, metaheurystyki, optymalizacja globalna, krajobraz funkcji celu
- podstawowy schemat: generuj i testuj (iteracyjne ulepszanie rozwiązań)
- przegląd rodzin metod: przeszukiwanie lokalne, symulowane wyżarzanie, tabu search, algorytmy ewolucyjne, strategie ewolucyjne, systemy mrówkowe, rój cząsteczek

### mog2.pptx - Przeszukiwanie lokalne (local search)
- proste przeszukiwanie lokalne (local search)
- wspinaczkowy (hill climbing)
- wybór sąsiedztwa: wersja randomizowana vs systematyczna
- strategia wielostartu (multi-start)
- strategia wielostartu ze zmodyfikowanego punktu startowego
- iteracyjne przeszukiwanie lokalne (iterated local search) + perturbacja
- przeszukiwanie ze zmiennym sąsiedztwem (VNS)
- skrzywione przeszukiwanie ze zmiennym sąsiedztwem (skewed VNS)

### mog3.pptx - Symulowane wyżarzanie (simulated annealing) i Metropolis
- algorytm Metropolisa (akceptacja rozwiązań gorszych z pewnym prawdopodobieństwem)
- prosty algorytm symulowanego wyżarzania (pseudokod)
- schematy chłodzenia: parametry strojenia (T_pocz, T_konc, formuła T(t), liczba iteracji przy stałej temperaturze - limit_prob)
- interpretacja temperatury jako progu akceptacji i wpływ różnicy jakości na prawdopodobieństwo

### mog4.pptx - Przeszukiwanie z tabu (tabu search)
- pamięć i reguły tabu (tabu jako zakaz ruchu / przejścia)
- okres tabu (kadencja) i struktury pamięci (tablice statusów tabu-aktywny / tabu-nieaktywny)
- ogólny schemat algorytmu tabu (pseudokod)
- realizacja dla problemu komiwojażera - reguły tabu
- kryteria dążenia do przekraczania tabu: kryterium przymusowego przekraczania tabu, kryterium kierunku poprawy, kryterium wpływu

### mog5.pptx - Algorytmy ewolucyjne / genetyczne (GA)
- reprodukcja i selekcja: selekcja proporcjonalna (ruletki), selekcja rangowa, selekcja progowa, selekcja turniejowa, selekcja turniejowa Boltzmanna
- sukcesja: sukcesja z całkowitym zastępowaniem, sukcesja z częściowym zastępowaniem, sukcesja elitarna
- operatory genetyczne: krzyżowanie jednopunktowe, dwupunktowe, wielopunktowe
- krzyżowanie dla permutacji: PMX, OX
- mutacja: drobne losowe zmiany osobnika (w zależności od reprezentacji)

### mog6.pptx - Strategie ewolucyjne (ES)
- (1+1)-ES
- (μ+λ)-ES
- (μ,λ)-ES
- reguła 1/5 sukcesu (dostosowanie kroku mutacji)
- samoadaptacja parametrów

### mog7.pptx - Systemy mrówkowe i rojowe (ACO, particle swarm)
- systemy mrówkowe (ant systems) dla zadań kombinatorycznych (np. TSP): feromon, parowanie, pamięć mrówki, budowa ścieżki na grafie
- aktualizacja poziomu feromonu + metoda z poziomem cyklicznym (odkładanie feromonu zależnie od jakości ścieżki)
- modyfikacje systemów mrówkowych: globalna i lokalna aktualizacja feromonu, MAX-MIN, system mrówkowy z rangami
- rój cząsteczek (particle swarm): położenie i prędkość, aktualizacja, gbest i lbest, zarządzanie minimalnymi odległościami między osobnikami

## Metody z prezentacji niewykorzystane w tym projekcie - co można dołożyć

Poniżej masz podpowiedzi dopasowane do aktualnego projektu. Nazwy są zgodne z prezentacjami, a opisy mówią co trzeba zmienić w kodzie.

### Symulowane wyżarzanie - elementy strojenia (mog3)
- schematy chłodzenia jako parametry: T_pocz, T_konc, formuła zmiany temperatury, liczba iteracji przy stałej temperaturze (limit_prob)
- w prezentacji podkreślone jest, że liczba iteracji na temperaturę zależy od złożoności problemu i wpływa na czas oraz jakość
- możesz zrobić wersję, gdzie w każdej temperaturze robisz limit_prob prób ruchu, zamiast 1 próby na temperaturę
- możesz też rozdzielić generator sąsiada od mechanizmu akceptacji (Metropolis), żeby łatwo testować inne sąsiedztwa

Jak to wpiąć praktycznie:
- w pliku main: wprowadź pętlę po temperaturze, a wewnątrz pętlę po limit_prob
- w select() trzymaj dokładnie logikę Metropolis: jeśli gorsze, losuj i porównuj z progiem z temperatury

### Tabu search (mog4) - alternatywa dla local search/SA
- możesz dodać osobny tryb rozwiązania: zamiast select() i temperatury, utrzymujesz pamięć tabu dla wykonanych ruchów
- kluczowe elementy z prezentacji: reguły tabu, okres tabu (kadencja), tablice statusów tabu-aktywny/tabu-nieaktywny, analiza sąsiadów z uwzględnieniem tabu
- kryteria przekraczania tabu z prezentacji: kryterium przymusowego przekraczania tabu, kryterium kierunku poprawy, kryterium wpływu

Jak to wpiąć praktycznie:
- dopisz nowy plik main lub tryb w istniejącym main: tabu_search()
- potrzebujesz struktury pamięci tabu powiązanej z ruchem (np. w TSP: atrybuty przejścia, w funkcji: zmiany zmiennych)

### Strategie ewolucyjne (mog6) - dodatkowa rodzina metod
- (1+1)-ES
- (μ+λ)-ES
- (μ,λ)-ES
- reguła 1/5 sukcesu
- samoadaptacja parametrów

Jak to wpiąć praktycznie:
- najłatwiej jako osobny tryb w main: es_optimize() z własną strukturą osobnika (geny + parametry kroku)

### Systemy mrówkowe i rojowe (mog7) - dodatkowa rodzina metod
Systemy mrówkowe (ant systems) - głównie dla TSP i innych zadań kombinatorycznych:
- parowanie feromonu na wszystkich krawędziach
- budowanie ścieżek przez mrówki z użyciem feromonu
- odkładanie feromonu zależnie od jakości ścieżki (w slajdach jest metoda z poziomem cyklicznym)
- modyfikacje: globalna i lokalna aktualizacja, MAX-MIN, system mrówkowy z rangami

Rój cząsteczek (particle swarm) - głównie dla funkcji ciągłych:
- położenie i prędkość cząsteczek oraz ich aktualizacja
- gbest i lbest
- zarządzanie minimalnymi odległościami między osobnikami (utrzymanie różnorodności)

Jak to wpiąć praktycznie:
- najczyściej jako osobne pliki trybów: aco.py / pso.py w danym folderze projektu, korzystające z tej samej funkcji fitness

