# Biblioteka zapasowa metod z prezentacji (mog1–mog7).
# Metody są gotowe do podpięcia w main poprzez import.

# opcje_z_prezentacji.py
# ------------------------------------------------------------
# Zapasowe (niepodpięte) strategie i metody z prezentacji mog1–mog7
# dla problemu komiwojażera (TSP).
#
# Cel: mieć w zanadrzu alternatywy do selekcji/krzyżowania/mutacji,
# różne sąsiedztwa (swap/insert/inversion/2-opt), Tabu Search, ACO itd.
#
# Uwaga o reprezentacji:
# - W projektach TSP w głównym kodzie masz często "gene" w stylu Lehmer code
#   (wybór indeksu z "kosza"). Poniżej masz konwertery:
#     gene -> route (permutacja miast)
#     route -> gene (Lehmer code)
#   Dzięki temu możesz korzystać z operatorów permutacyjnych (PMX/OX/2-opt)
#   nawet jeśli w głównym kodzie trzymasz gene.
# ------------------------------------------------------------

import math
import random
from collections import deque

# ---------- Reprezentacja: gene <-> route (Lehmer code) ----------

def gene_to_route(gene):
    """Zamienia Lehmer code (gene) na permutację miast (route)."""
    kosz = list(range(len(gene)))
    route = []
    for i in range(len(gene)):
        idx = gene[i]
        route.append(kosz.pop(idx))
    return route

def route_to_gene(route):
    """Zamienia permutację miast (route) na Lehmer code (gene)."""
    n = len(route)
    kosz = list(range(n))
    gene = [0] * n
    for i in range(n):
        val = route[i]
        idx = kosz.index(val)
        gene[i] = idx
        kosz.pop(idx)
    return gene

# ---------- Ocena trasy ----------

def route_length(route, odleglosci):
    """Długość cyklu Hamiltona: suma odległości + domknięcie."""
    s = 0.0
    n = len(route)
    for i in range(n - 1):
        s += odleglosci[route[i]][route[i + 1]]
    s += odleglosci[route[-1]][route[0]]
    return s

# ---------- Sąsiedztwa (mog1 / local search) ----------

def neigh_swap(route):
    """Losowa zamiana dwóch pozycji (swap)."""
    n = len(route)
    i, j = random.sample(range(n), 2)
    r = route[:]
    r[i], r[j] = r[j], r[i]
    return r

def neigh_insert(route):
    """Wyjęcie elementu z i i wstawienie na j (insert)."""
    n = len(route)
    i, j = random.sample(range(n), 2)
    r = route[:]
    x = r.pop(i)
    r.insert(j, x)
    return r

def neigh_inversion(route):
    """Odwrócenie fragmentu między i..j (inversion / 2-opt-like)."""
    n = len(route)
    i, j = sorted(random.sample(range(n), 2))
    r = route[:]
    r[i:j+1] = reversed(r[i:j+1])
    return r

def two_opt_best_improvement(route, odleglosci, max_checks=None):
    """Klasyczny 2-opt: przegląda pary i,j i bierze najlepszą poprawę.
    max_checks: ograniczenie liczby sprawdzeń (żeby nie było mega wolno).
    """
    best = route[:]
    best_len = route_length(best, odleglosci)
    n = len(route)
    checks = 0
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            cand = route[:]
            cand[i:j+1] = reversed(cand[i:j+1])
            cand_len = route_length(cand, odleglosci)
            if cand_len < best_len:
                best, best_len = cand, cand_len
            checks += 1
            if max_checks is not None and checks >= max_checks:
                return best, best_len
    return best, best_len

def multi_start_hill_climb(odleglosci, starts=30, steps=5000, neigh_fn=neigh_swap):
    """Multi-start hill climbing: wiele restartów + local search.
    (To jest w prezentacjach jako 'wielostart' / dywersyfikacja.)
    """
    n = len(odleglosci)
    best_route = None
    best_len = float("inf")

    for _ in range(starts):
        route = list(range(n))
        random.shuffle(route)
        cur_len = route_length(route, odleglosci)

        for _ in range(steps):
            cand = neigh_fn(route)
            cand_len = route_length(cand, odleglosci)
            if cand_len < cur_len:
                route, cur_len = cand, cand_len

        if cur_len < best_len:
            best_route, best_len = route, cur_len

    return best_route, best_len

# ---------- Symulowane wyżarzanie (mog3) ----------

def cooling_linear(t, t0, t_end, k, k_max):
    """Chłodzenie liniowe."""
    return t0 + (t_end - t0) * (k / float(k_max))

def cooling_geometric(t, alpha=0.995):
    """Chłodzenie geometryczne: T <- alpha*T."""
    return t * alpha

def cooling_logarithmic(t0, k):
    """Chłodzenie logarytmiczne (wolne)."""
    return t0 / math.log(2.0 + k)

def simulated_annealing_tsp(odleglosci, iters=20000, t0=1000.0, t_end=1.0,
                           neigh_fn=neigh_swap, schedule="linear", alpha=0.995):
    """SA dla TSP - zapasowa implementacja (niepodpięta do main).
    schedule: 'linear' | 'geometric' | 'log'
    """
    n = len(odleglosci)
    cur = list(range(n))
    random.shuffle(cur)
    cur_len = route_length(cur, odleglosci)

    best = cur[:]
    best_len = cur_len

    T = t0
    for k in range(1, iters + 1):
        cand = neigh_fn(cur)
        cand_len = route_length(cand, odleglosci)
        delta = cand_len - cur_len  # minimalizacja

        if delta < 0:
            cur, cur_len = cand, cand_len
        else:
            p = math.exp(-delta / max(T, 1e-9))
            if random.random() < p:
                cur, cur_len = cand, cand_len

        if cur_len < best_len:
            best, best_len = cur[:], cur_len

        # aktualizacja temperatury
        if schedule == "linear":
            T = cooling_linear(T, t0, t_end, k, iters)
        elif schedule == "geometric":
            T = cooling_geometric(T, alpha)
            if T < t_end:
                T = t_end
        else:
            T = cooling_logarithmic(t0, k)
            if T < t_end:
                T = t_end

    return best, best_len

# ---------- Tabu Search (mog4) ----------

def tabu_search_tsp(odleglosci, iters=5000, tabu_size=50, neigh_samples=80):
    """Prosty Tabu Search dla TSP.
    - tabu zapisuje ruchy swap (i,j) jako pary.
    - aspiracja: jeśli kandydat bije global best, można złamać tabu.
    """
    n = len(odleglosci)
    cur = list(range(n))
    random.shuffle(cur)
    cur_len = route_length(cur, odleglosci)

    best = cur[:]
    best_len = cur_len

    tabu = deque(maxlen=tabu_size)

    for _ in range(iters):
        best_cand = None
        best_cand_len = float("inf")
        best_move = None

        for _s in range(neigh_samples):
            i, j = random.sample(range(n), 2)
            cand = cur[:]
            cand[i], cand[j] = cand[j], cand[i]
            cand_len = route_length(cand, odleglosci)

            move = (min(i, j), max(i, j))
            is_tabu = move in tabu

            if (not is_tabu and cand_len < best_cand_len) or (is_tabu and cand_len < best_len):
                best_cand = cand
                best_cand_len = cand_len
                best_move = move

        if best_cand is None:
            continue

        cur, cur_len = best_cand, best_cand_len
        tabu.append(best_move)

        if cur_len < best_len:
            best, best_len = cur[:], cur_len

    return best, best_len

# ---------- GA: selekcja (mog5) ----------

def select_roulette(pop, fitnesses):
    """Ruletka: fitnessy muszą być >= 0 (większe = lepsze)."""
    s = sum(fitnesses)
    if s <= 0:
        return random.choice(pop)
    r = random.random() * s
    acc = 0.0
    for ind, fit in zip(pop, fitnesses):
        acc += fit
        if acc >= r:
            return ind
    return pop[-1]

def select_tournament(pop, fitnesses, k=3):
    """Turniej: losuj k osobników i wybierz najlepszego."""
    idxs = random.sample(range(len(pop)), k)
    best_i = idxs[0]
    for i in idxs[1:]:
        if fitnesses[i] > fitnesses[best_i]:
            best_i = i
    return pop[best_i]

def select_rank(pop, fitnesses):
    """Selekcja rangowa: sortuj, nadaj rangi, losuj po rankach."""
    idx = list(range(len(pop)))
    idx.sort(key=lambda i: fitnesses[i])  # rosnąco
    ranks = list(range(1, len(pop) + 1))
    # najlepszy ma największy rank
    rank_fits = [0] * len(pop)
    for r, i in zip(ranks, idx):
        rank_fits[i] = r
    return select_roulette(pop, rank_fits)

def select_sus(pop, fitnesses, n_select):
    """Stochastic Universal Sampling: zwraca listę wybranych."""
    s = sum(fitnesses)
    if s <= 0:
        return [random.choice(pop) for _ in range(n_select)]
    step = s / float(n_select)
    start = random.random() * step
    points = [start + i * step for i in range(n_select)]
    chosen = []
    acc = 0.0
    j = 0
    for ind, fit in zip(pop, fitnesses):
        acc += fit
        while j < len(points) and acc >= points[j]:
            chosen.append(ind)
            j += 1
    while len(chosen) < n_select:
        chosen.append(pop[-1])
    return chosen

# ---------- GA: krzyżowanie permutacji (mog5) ----------

def crossover_ox(p1, p2):
    """Order Crossover (OX) dla permutacji."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b+1] = p1[a:b+1]
    fill = [x for x in p2 if x not in child]
    k = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill[k]
            k += 1
    return child

def crossover_pmx(p1, p2):
    """Partially Mapped Crossover (PMX) dla permutacji."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b+1] = p1[a:b+1]

    mapping = {}
    for i in range(a, b+1):
        mapping[p2[i]] = p1[i]

    for i in range(n):
        if i >= a and i <= b:
            continue
        x = p2[i]
        while x in mapping and x in child:
            x = mapping[x]
        if x in child:
            # awaryjne domknięcie
            for v in p2:
                if v not in child:
                    x = v
                    break
        child[i] = x
    return child

def crossover_cx(p1, p2):
    """Cycle Crossover (CX) dla permutacji."""
    n = len(p1)
    child = [-1] * n
    used = set()
    take_from_p1 = True

    while len(used) < n:
        # start cyklu
        start = next(i for i in range(n) if i not in used)
        i = start
        cycle = []
        while i not in used:
            used.add(i)
            cycle.append(i)
            val = p2[i]
            i = p1.index(val)

        src = p1 if take_from_p1 else p2
        for idx in cycle:
            child[idx] = src[idx]
        take_from_p1 = not take_from_p1

    return child

# ---------- GA: mutacje permutacji (mog5) ----------

def mutate_swap(route, p=0.05):
    if random.random() < p:
        return neigh_swap(route)
    return route

def mutate_inversion(route, p=0.05):
    if random.random() < p:
        return neigh_inversion(route)
    return route

def mutate_scramble(route, p=0.05):
    if random.random() < p:
        n = len(route)
        a, b = sorted(random.sample(range(n), 2))
        r = route[:]
        part = r[a:b+1]
        random.shuffle(part)
        r[a:b+1] = part
        return r
    return route

# ---------- ACO dla TSP (mog7) ----------

def aco_tsp(odleglosci, ants=30, iters=200, alpha=1.0, beta=3.0, rho=0.5, q=100.0):
    """Prosta wersja ACO (Ant System) dla TSP.
    - alpha: wpływ feromonu
    - beta: wpływ heurystyki 1/d
    - rho: parowanie feromonu
    - q: ilość feromonu odkładana ~ q / długość trasy
    """
    n = len(odleglosci)
    tau = [[1.0 for _ in range(n)] for _ in range(n)]
    eta = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and odleglosci[i][j] > 0:
                eta[i][j] = 1.0 / odleglosci[i][j]
            else:
                eta[i][j] = 0.0

    best_route = None
    best_len = float("inf")

    for _ in range(iters):
        all_routes = []
        all_lens = []

        for _a in range(ants):
            start = random.randrange(n)
            unvisited = set(range(n))
            unvisited.remove(start)
            route = [start]
            cur = start

            while unvisited:
                probs = []
                cities = list(unvisited)
                denom = 0.0
                for nxt in cities:
                    val = (tau[cur][nxt] ** alpha) * (eta[cur][nxt] ** beta)
                    probs.append(val)
                    denom += val
                r = random.random() * denom if denom > 0 else None
                acc = 0.0
                chosen = cities[-1]
                if r is None:
                    chosen = random.choice(cities)
                else:
                    for nxt, p in zip(cities, probs):
                        acc += p
                        if acc >= r:
                            chosen = nxt
                            break
                route.append(chosen)
                unvisited.remove(chosen)
                cur = chosen

            l = route_length(route, odleglosci)
            all_routes.append(route)
            all_lens.append(l)
            if l < best_len:
                best_len = l
                best_route = route[:]

        # parowanie
        for i in range(n):
            for j in range(n):
                tau[i][j] *= (1.0 - rho)

        # depozycja (Ant System)
        for route, l in zip(all_routes, all_lens):
            deposit = q / max(l, 1e-9)
            for i in range(n - 1):
                a, b = route[i], route[i + 1]
                tau[a][b] += deposit
                tau[b][a] += deposit
            a, b = route[-1], route[0]
            tau[a][b] += deposit
            tau[b][a] += deposit

    return best_route, best_len
