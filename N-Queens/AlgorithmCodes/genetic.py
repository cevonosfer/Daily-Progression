import random
import time
import tracemalloc

def count_conflicts(state):
    n = len(state)
    conflicts = 0
    diag1 = {}
    diag2 = {}
    for i in range(n):
        d1 = state[i] - i
        d2 = state[i] + i
        diag1[d1] = diag1.get(d1, 0) + 1
        diag2[d2] = diag2.get(d2, 0) + 1
    for count in diag1.values():
        if count > 1:
            conflicts += count * (count - 1) // 2
    for count in diag2.values():
        if count > 1:
            conflicts += count * (count - 1) // 2
    return conflicts

def fitness(state):
    max_pairs = len(state) * (len(state) - 1) // 2
    return max_pairs - count_conflicts(state)

def create_individual(n):
    individual = list(range(n))
    random.shuffle(individual)
    return individual

def tournament_selection(population, k=5):  # bigger k for stronger selection pressure
    return max(random.sample(population, k), key=fitness)

def crossover(parent1, parent2):
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b] = parent1[a:b]
    fill = [gene for gene in parent2 if gene not in child]
    idx = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill[idx]
            idx += 1
    return child

def conflict_indices(state):
    n = len(state)
    conflict_rows = set()
    diag1 = {}
    diag2 = {}
    for i in range(n):
        d1 = state[i] - i
        d2 = state[i] + i
        diag1.setdefault(d1, []).append(i)
        diag2.setdefault(d2, []).append(i)
    for indices in diag1.values():
        if len(indices) > 1:
            conflict_rows.update(indices)
    for indices in diag2.values():
        if len(indices) > 1:
            conflict_rows.update(indices)
    return list(conflict_rows)

def conflict_driven_mutate(individual):
    conflicts = conflict_indices(individual)
    if len(conflicts) < 2:
        # fallback random swap
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
        return

    i = random.choice(conflicts)
    j = random.choice([x for x in range(len(individual)) if x != i])
    individual[i], individual[j] = individual[j], individual[i]

def genetic_algorithm_improved(n, population_size=40, max_generations=1000):
    population = [create_individual(n) for _ in range(population_size)]
    best = max(population, key=fitness)
    best_fitness = fitness(best)

    generation = 0
    while generation < max_generations and best_fitness < n*(n-1)//2:
        new_population = []
        # Elitism: keep top 2
        sorted_pop = sorted(population, key=fitness, reverse=True)
        new_population.extend(sorted_pop[:2])

        while len(new_population) < population_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            conflict_driven_mutate(child)
            new_population.append(child)

        population = new_population
        current_best = max(population, key=fitness)
        current_best_fitness = fitness(current_best)

        if current_best_fitness > best_fitness:
            best = current_best
            best_fitness = current_best_fitness

        generation += 1

    conflicts = count_conflicts(best)
    return best, conflicts, generation

def run_and_measure(n):
    tracemalloc.start()
    start_time = time.time()

    solution, conflicts, generations = genetic_algorithm_improved(n)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {n}")
    print(f"✅ Solution found in {generations} generations!" if conflicts == 0 else f"⚠️ Conflicts remaining: {conflicts}")
    print(f"⏱️ Time taken: {end_time - start_time:.4f} seconds")
    print(f"📦 Peak memory usage: {peak / 1024:.2f} KB\n")
    return end_time - start_time, peak / 1024

if __name__ == "__main__":
    for N in [10, 30, 50, 100, 200]:
        run_and_measure(N)
