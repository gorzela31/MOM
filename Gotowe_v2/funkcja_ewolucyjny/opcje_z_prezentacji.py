# Biblioteka zapasowa metod z prezentacji (mog1–mog7).
# Metody są gotowe do podpięcia w main poprzez import.

# opcje_z_prezentacji.py
# ------------------------------------------------------------
# Zapasowe (niepodpięte) strategie i metody z prezentacji mog1–mog7
# dla optymalizacji funkcji (zmienne rzeczywiste w [0, PI]).
#
# Tu masz w zanadrzu:
# - multi-start / random restart (mog1)
# - dodatkowe harmonogramy SA i kroki sąsiedztwa (mog3)
# - alternatywne selekcje i krzyżowania do GA (mog5)
# - Strategie ewolucyjne ES: (1+1), (mu+lambda), reguła 1/5 (mog6)
# - PSO (mog7)
# - (opcjonalnie) szkic ACOR (ant colony for continuous) jako odpowiednik ACO (mog7)
# ------------------------------------------------------------

import math
import random

# ---------- Funkcje celu (możesz podmienić pod swoje projekty) ----------

def f_sin(x):
    """1000 * Π sin(xi) (maksymalizacja)."""
    s = 1.0
    for v in x:
        s *= math.sin(v)
    return 1000.0 * s

def f_cos_shift(x):
    """1000 + 1000 * Π cos(xi) (maksymalizacja, max=2000)."""
    s = 1.0
    for v in x:
        s *= math.cos(v)
    return 1000.0 + 1000.0 * s

def clamp_pi(x):
    """Ogranicza do [0, PI]."""
    out = []
    for v in x:
        if v < 0.0:
            out.append(0.0)
        elif v > math.pi:
            out.append(math.pi)
        else:
            out.append(v)
    return out

# ---------- Local search / multi-start (mog1) ----------

def neigh_small_step(x, step=0.05):
    """Losowo wybiera indeks i dodaje krok z [-step, +step]."""
    y = x[:]
    i = random.randrange(len(x))
    y[i] = y[i] + (random.random() * 2.0 - 1.0) * step
    return clamp_pi(y)

def hill_climb(x0, f, iters=2000, step=0.05):
    """Prosty hill climbing: przyjmuj tylko poprawę."""
    x = x0[:]
    best = x[:]
    best_fit = f(best)
    for _ in range(iters):
        cand = neigh_small_step(x, step)
        cand_fit = f(cand)
        if cand_fit > best_fit:
            x = cand
            best = cand
            best_fit = cand_fit
    return best, best_fit

def multi_start_hill_climb(dim, f, starts=30, iters=2000, step=0.05):
    """Wielostart: kilka losowych startów i hill climb."""
    best = None
    best_fit = -1e18
    for _ in range(starts):
        x0 = [random.random() * math.pi for _ in range(dim)]
        cand, cand_fit = hill_climb(x0, f, iters, step)
        if cand_fit > best_fit:
            best, best_fit = cand, cand_fit
    return best, best_fit

# ---------- Symulowane wyżarzanie (mog3) ----------

def cooling_linear(t0, t_end, k, k_max):
    return t0 + (t_end - t0) * (k / float(k_max))

def cooling_geometric(t, alpha=0.995):
    return t * alpha

def cooling_logarithmic(t0, k):
    return t0 / math.log(2.0 + k)

def simulated_annealing(x0, f, iters=10000, t0=10.0, t_end=1e-3,
                        step=0.1, schedule="geometric", alpha=0.995):
    """SA dla maksymalizacji.
    Przyjmuje gorsze z prawdopodobieństwem exp((new-old)/T) dla new<old.
    """
    x = x0[:]
    cur = f(x)
    best = x[:]
    best_fit = cur
    T = t0

    for k in range(1, iters + 1):
        cand = neigh_small_step(x, step)
        cand_fit = f(cand)
        delta = cand_fit - cur  # maksymalizacja

        if delta >= 0:
            x, cur = cand, cand_fit
        else:
            p = math.exp(delta / max(T, 1e-12))
            if random.random() < p:
                x, cur = cand, cand_fit

        if cur > best_fit:
            best, best_fit = x[:], cur

        if schedule == "linear":
            T = cooling_linear(t0, t_end, k, iters)
        elif schedule == "log":
            T = cooling_logarithmic(t0, k)
            if T < t_end:
                T = t_end
        else:
            T = cooling_geometric(T, alpha)
            if T < t_end:
                T = t_end

    return best, best_fit

# ---------- GA: selekcja (mog5) ----------

def select_roulette(pop, fits):
    s = sum(fits)
    if s <= 0:
        return random.choice(pop)
    r = random.random() * s
    acc = 0.0
    for ind, fit in zip(pop, fits):
        acc += fit
        if acc >= r:
            return ind
    return pop[-1]

def select_tournament(pop, fits, k=3):
    idxs = random.sample(range(len(pop)), k)
    best_i = idxs[0]
    for i in idxs[1:]:
        if fits[i] > fits[best_i]:
            best_i = i
    return pop[best_i]

def select_rank(pop, fits):
    idx = list(range(len(pop)))
    idx.sort(key=lambda i: fits[i])  # rosnąco
    ranks = list(range(1, len(pop) + 1))
    rank_fits = [0] * len(pop)
    for r, i in zip(ranks, idx):
        rank_fits[i] = r
    return select_roulette(pop, rank_fits)

def select_sus(pop, fits, n_select):
    s = sum(fits)
    if s <= 0:
        return [random.choice(pop) for _ in range(n_select)]
    step = s / float(n_select)
    start = random.random() * step
    points = [start + i * step for i in range(n_select)]
    chosen = []
    acc = 0.0
    j = 0
    for ind, fit in zip(pop, fits):
        acc += fit
        while j < len(points) and acc >= points[j]:
            chosen.append(ind)
            j += 1
    while len(chosen) < n_select:
        chosen.append(pop[-1])
    return chosen

# ---------- GA: krzyżowania dla real-valued (mog5) ----------

def crossover_uniform(p1, p2):
    """Krzyżowanie jednorodne: gen z p1 lub p2."""
    c = []
    for a, b in zip(p1, p2):
        c.append(a if random.random() < 0.5 else b)
    return c

def crossover_arithmetic(p1, p2, alpha=None):
    """Krzyżowanie arytmetyczne: alpha*p1 + (1-alpha)*p2."""
    if alpha is None:
        alpha = random.random()
    c1 = []
    c2 = []
    for a, b in zip(p1, p2):
        c1.append(alpha * a + (1.0 - alpha) * b)
        c2.append((1.0 - alpha) * a + alpha * b)
    return clamp_pi(c1), clamp_pi(c2)

def crossover_blx_alpha(p1, p2, alpha=0.5):
    """BLX-alpha: losuje gen z rozszerzonego przedziału [min-αd, max+αd]."""
    c = []
    for a, b in zip(p1, p2):
        lo = min(a, b)
        hi = max(a, b)
        d = hi - lo
        lo2 = lo - alpha * d
        hi2 = hi + alpha * d
        c.append(random.uniform(lo2, hi2))
    return clamp_pi(c)

# ---------- GA: mutacje dla real-valued (mog5) ----------

def mutate_gaussian(x, sigma=0.05, p=0.1):
    y = x[:]
    for i in range(len(y)):
        if random.random() < p:
            y[i] = y[i] + random.gauss(0.0, sigma)
    return clamp_pi(y)

def mutate_non_uniform(x, t, t_max, b=2.0, p=0.1):
    """Mutacja nieniejednorodna: z czasem krok maleje."""
    y = x[:]
    for i in range(len(y)):
        if random.random() < p:
            r = random.random()
            # malejący zakres
            delta = (math.pi) * (1.0 - (r ** ((1.0 - t / float(t_max)) ** b)))
            if random.random() < 0.5:
                y[i] = y[i] + delta
            else:
                y[i] = y[i] - delta
    return clamp_pi(y)

# ---------- Strategie ewolucyjne ES (mog6) ----------

def es_1plus1(dim, f, iters=20000, sigma=0.1, use_one_fifth=True, adapt_every=50):
    """(1+1)-ES dla maksymalizacji.
    - sigma: krok mutacji (odchylenie Gaussa).
    - reguła 1/5: co adapt_every iteracji dostosuj sigma.
    """
    x = [random.random() * math.pi for _ in range(dim)]
    fx = f(x)
    success = 0

    for t in range(1, iters + 1):
        y = [xi + random.gauss(0.0, sigma) for xi in x]
        y = clamp_pi(y)
        fy = f(y)

        if fy >= fx:
            x, fx = y, fy
            success += 1

        if use_one_fifth and t % adapt_every == 0:
            rate = success / float(adapt_every)
            # 1/5 success rule (heurystyka dydaktyczna)
            if rate > 0.2:
                sigma *= 1.2
            elif rate < 0.2:
                sigma /= 1.2
            success = 0

    return x, fx, sigma

def es_mu_lambda(dim, f, mu=10, lam=40, gens=300, sigma=0.15, plus=True):
    """(mu + lambda) albo (mu, lambda) ES.
    plus=True  -> (mu + lambda)
    plus=False -> (mu, lambda)
    """
    pop = [[random.random() * math.pi for _ in range(dim)] for _ in range(mu)]
    fits = [f(x) for x in pop]

    for _g in range(gens):
        children = []
        for _ in range(lam):
            parent = pop[random.randrange(mu)]
            child = [xi + random.gauss(0.0, sigma) for xi in parent]
            children.append(clamp_pi(child))

        child_fits = [f(x) for x in children]

        if plus:
            pool = pop + children
            pool_fits = fits + child_fits
        else:
            pool = children
            pool_fits = child_fits

        idx = list(range(len(pool)))
        idx.sort(key=lambda i: pool_fits[i], reverse=True)
        pop = [pool[i] for i in idx[:mu]]
        fits = [pool_fits[i] for i in idx[:mu]]

    best_i = max(range(mu), key=lambda i: fits[i])
    return pop[best_i], fits[best_i]

# ---------- PSO (mog7) ----------

def pso(dim, f, swarm=30, iters=200, w=0.7, c1=1.4, c2=1.4):
    """Particle Swarm Optimization dla maksymalizacji."""
    # inicjalizacja
    x = [[random.random() * math.pi for _ in range(dim)] for _ in range(swarm)]
    v = [[0.0 for _ in range(dim)] for _ in range(swarm)]
    pbest = [xi[:] for xi in x]
    pbest_fit = [f(xi) for xi in x]
    gbest_i = max(range(swarm), key=lambda i: pbest_fit[i])
    gbest = pbest[gbest_i][:]
    gbest_fit = pbest_fit[gbest_i]

    for _ in range(iters):
        for i in range(swarm):
            for d in range(dim):
                r1 = random.random()
                r2 = random.random()
                v[i][d] = (w * v[i][d] +
                           c1 * r1 * (pbest[i][d] - x[i][d]) +
                           c2 * r2 * (gbest[d] - x[i][d]))
                x[i][d] = x[i][d] + v[i][d]

            x[i] = clamp_pi(x[i])
            fit = f(x[i])

            if fit > pbest_fit[i]:
                pbest[i] = x[i][:]
                pbest_fit[i] = fit

                if fit > gbest_fit:
                    gbest = x[i][:]
                    gbest_fit = fit

    return gbest, gbest_fit

# ---------- (opcjonalnie) ACOR szkic (mog7) ----------
# W prezentacjach jest ACO głównie pod TSP, ale są też wersje dla ciągłych zmiennych (ACOR).
# Poniżej masz prosty szkic, żebyś miał to "pokryte" w każdym projekcie.

def acor_szkic(dim, f, archive_size=30, samples=20, iters=200, q=0.5, xi=0.85):
    """Szkic ACOR (Ant Colony Optimization for Continuous Domains).
    To nie jest agresywnie zoptymalizowane, ale pokazuje ideę:
    - trzymasz archiwum rozwiązań
    - losujesz nowe z mieszaniny Gaussów (wokół archiwum)
    - aktualizujesz archiwum.
    """
    archive = [[random.random() * math.pi for _ in range(dim)] for _ in range(archive_size)]
    fits = [f(x) for x in archive]

    for _ in range(iters):
        # sortuj archiwum (najlepsze pierwsze)
        idx = list(range(archive_size))
        idx.sort(key=lambda i: fits[i], reverse=True)
        archive = [archive[i] for i in idx]
        fits = [fits[i] for i in idx]

        # wagi (im lepszy, tym większa)
        weights = []
        for r in range(archive_size):
            # rozkład Gaussa na rangach (heurystyka)
            w = math.exp(- (r ** 2) / (2.0 * (q * archive_size) ** 2))
            weights.append(w)
        s = sum(weights)
        weights = [w / s for w in weights]

        new_points = []
        new_fits = []

        # oszacuj sigmy (średni dystans w wymiarze)
        sigmas = [0.0] * dim
        for d in range(dim):
            vals = [archive[i][d] for i in range(archive_size)]
            mean = sum(vals) / float(archive_size)
            var = sum((v - mean) ** 2 for v in vals) / float(archive_size)
            sigmas[d] = math.sqrt(var) * xi + 1e-6

        for _s in range(samples):
            # wybór komponentu (rozwiązania z archiwum) po wagach
            r = random.random()
            acc = 0.0
            k = 0
            for i, w in enumerate(weights):
                acc += w
                if acc >= r:
                    k = i
                    break

            base = archive[k]
            cand = []
            for d in range(dim):
                cand.append(base[d] + random.gauss(0.0, sigmas[d]))
            cand = clamp_pi(cand)

            new_points.append(cand)
            new_fits.append(f(cand))

        # połącz i przytnij
        pool = archive + new_points
        pool_fits = fits + new_fits
        idx2 = list(range(len(pool)))
        idx2.sort(key=lambda i: pool_fits[i], reverse=True)
        archive = [pool[i] for i in idx2[:archive_size]]
        fits = [pool_fits[i] for i in idx2[:archive_size]]

    best_i = max(range(len(archive)), key=lambda i: fits[i])
    return archive[best_i], fits[best_i]
