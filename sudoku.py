import numpy as np
import random 

def get_block(sud: np.ndarray, i: int, j: int):
  row = i // 3
  col = j // 3
  return sud[row*3:row*3+2, col*3:col*3+2]

def cell_ut(sud: np.ndarray, i: int, j: int):
  mask = (sud == sud[i][j])
  pt  = mask[i, :].sum() - 1
  pt += mask[:, j].sum() - 1
  pt += get_block(mask, i, j).sum() - 1
  return pt

def ut(sud: np.ndarray, inp):
  pts = 0
  for i in range(9):
    for j in range(9):
      if inp[i, j] == 0:
        pts -= cell_ut(sud, i, j)
  return pts

def fill_sud_random(sud: np.ndaray):
  out = sud[:,:]
  for i in range(9):
    for j in range(9):
      if sud[i][j] == 0:
        out[i][j] = np.random.randint(1, 10)
  return out

def reproduce1(p1, p2, inp):
  ch = inp[:,:]
  for i in range(9):
    for j in range(9):
      if ch[i, j] == 0:
        ch[i, j] = random.choice([p1[i, j], p2[i, j]])
  return ch

def reproduce2(p1, p2, inp):
  ch = inp[:,:]
  for i in range(9):
    for j in range(9):
      if ch[i, j] == 0:
        ch[i, j] = (p1[i, j] + p2[i, j]) // 2
  return ch

def reproduce3(p1, p2, inp):
  ch = inp[:,:]
  for i in range(9):
    for j in range(9):
      if ch[i, j] == 0:
        ch[i, j] = p1[i, j] if cell_ut(p1, i, j) >= cell_ut(p2, i, j) else p2[i, j]
  return ch

def mutate(sud, inp, cells_to_solve):
  n = cells_to_solve
  k = random.randint(1, n+1)
  out = sud[:,:]
  for i in range(9):
    for j in range(9):
      if inp[i, j] == 0:
        if random.randint() < (k / n):
          out[i, j] = random.randint(1, 10)         
          k -= 1
        n -= 1
  return out

def solve_sudoku(max_iter=100, pop_size=100):
  inp = np.empty((9, 9), dtype=int)
  populations = [fill_sud_random(inp) for _ in range(pop_size)]
  for iter in range(max_iter):
    weights = [ut(pop) for pop in populations]
    min_weight = min(weights)
    for i in range(len(weights)):
      if weights[i] == 0:
        return populations[i]
      weights[i] += min_weight + 1
    new_population = []
    for _ in range(pop_size):
      parents = random.choices(populations, weights, k=2)
      child = reproduce1(*parents)
      if random.random() >= 0.95:
        child = mutate(child, inp)
      new_population.append(child)
    populations = new_population
  return max(populations, key=lambda p: ut(p))
