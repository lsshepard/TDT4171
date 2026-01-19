# Probability of colliding birthdays given N people

import random
import numpy as np


def simulate_birthday_overlap(N):
    bdays = []
    for i in range (N):
        bday = random.randint(1, 365)
        if bday in bdays: return 1
        else: bdays.append(bday)

    return 0

def estimate_overlap_probs(N, M):
    results = []
    for i in range(M):
        results.append(simulate_birthday_overlap(N))
    
    return sum(results) / len(results)

results = []
smallest_n = None
for n in range(10, 51):
    p = estimate_overlap_probs(n, 1000)
    results.append(p)
    if smallest_n == None and p >= 0.5: smallest_n = n

results = np.array(results)

proportion = (results > 0.5).sum() / len(results)

print('Proportion:', proportion)
print('Smallest N:', smallest_n)