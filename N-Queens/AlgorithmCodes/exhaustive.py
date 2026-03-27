import time
import tracemalloc

def is_safe(position, row, col):        
    for r in range(row):
        c = position[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def dfs(position, row, n, solutions):                            
    if row == n:
        solutions.append(position[:])
        return
    for col in range(n):
        if is_safe(position, row, col):
            position[row] = col
            dfs(position, row + 1, n, solutions)

def exhaustive_n_queens(n):
    solutions = []
    position = [-1] * n 
    dfs(position, 0, n, solutions)
    return solutions

if __name__ == "__main__":
    N = 13 

    tracemalloc.start()
    start_time = time.time()

    all_solutions = exhaustive_n_queens(N)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {N}")
    print(f"Total solutions found: {len(all_solutions)}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KB")
    print("Sample solution:", all_solutions[0] if all_solutions else "None")
