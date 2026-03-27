import random
import time
import tracemalloc        

def count_conflicts(state):
    """Count number of attacking pairs of queens."""
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i+1, n):
            if state[i] == state[j]: 
                conflicts += 1
            elif abs(state[i] - state[j]) == abs(i - j): 
                conflicts += 1
    return conflicts

def greedy_hill_climbing(n, max_steps=1000):
    current_state = [random.randint(0, n-1) for _ in range(n)]
    current_conflicts = count_conflicts(current_state)
    
    for step in range(max_steps):
        if current_conflicts == 0:
            break 
        
        best_state = current_state[:]
        best_conflicts = current_conflicts
        
   
        for row in range(n):
            original_col = current_state[row]
            for col in range(n):
                if col == original_col:
                    continue
                current_state[row] = col
                conflicts = count_conflicts(current_state)
                if conflicts < best_conflicts:
                    best_conflicts = conflicts
                    best_state = current_state[:]
            current_state[row] = original_col
        
        if best_conflicts == current_conflicts:
            break
        else:
            current_state = best_state
            current_conflicts = best_conflicts
    
    return current_state, current_conflicts

if __name__ == "__main__":
    N = 50

    tracemalloc.start()
    start_time = time.time()

    solution, conflicts = greedy_hill_climbing(N)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {N}")
    if conflicts == 0:
        print("Solution found:")
    else:
        print(f"No perfect solution found, conflicts = {conflicts}")
    print(solution)
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KB")
