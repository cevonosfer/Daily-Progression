import random
import time
import math
import tracemalloc

def count_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def queen_conflict_counts(state):
    n = len(state)
    conflict_counts = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and (state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j)):
                conflict_counts[i] += 1
    return conflict_counts

def simulated_annealing(n, max_steps=20000, start_temp=400, cooling_rate=0.99, min_temp=1e-5):
    current_state = [random.randint(0, n - 1) for _ in range(n)]
    current_conflicts = count_conflicts(current_state)
    temperature = start_temp

    conflict_counts = queen_conflict_counts(current_state)

    for step in range(max_steps):
        if current_conflicts == 0 or temperature < min_temp:
            break

     
        if step % 5 == 0:
            conflict_counts = queen_conflict_counts(current_state)

        max_conflict = max(conflict_counts)
        if max_conflict == 0:
            break
        max_conflict_indices = [i for i, c in enumerate(conflict_counts) if c == max_conflict]
        row = random.choice(max_conflict_indices)

        new_col = random.randint(0, n - 1)
        while new_col == current_state[row]:
            new_col = random.randint(0, n - 1)

        new_state = current_state[:]
        new_state[row] = new_col
        new_conflicts = count_conflicts(new_state)

        delta = new_conflicts - current_conflicts
        accept_prob = math.exp(-delta / temperature) if delta > 0 else 1

        if delta < 0 or random.random() < accept_prob:
            current_state = new_state
            current_conflicts = new_conflicts

        temperature *= cooling_rate

    return current_state, current_conflicts

def run_and_measure(n):
    tracemalloc.start()
    start_time = time.time()

    solution, conflicts = simulated_annealing(n)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {n}")
    print("Solution found:" if conflicts == 0 else f"Conflicts remaining: {conflicts}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KB\n")
    return end_time - start_time, peak / 1024

if __name__ == "__main__":
    for N in [10, 30, 50, 100, 200]:
        run_and_measure(N)
