# Collected code from 2c.py, 3a.py, and 3b.py for hand-in

import random
import numpy as np

# 2c)
# Expected rounds played before going broke

def play_game():
    X1 = random.randint(0, 3)
    X2 = random.randint(0, 3)
    X3 = random.randint(0, 3)

    if X1 == X2 == X3:
        if X1 == 0: return 20
        elif X1 == 1: return 15
        elif X1 == 2: return 5
        elif X1 == 3: return 3
    
    elif X1 == 3:
        if X2 == 3: return 2
        return 1
    return 0


def playout(initial_balance):
    balance = initial_balance
    round_count = 0
    while balance > 0:
        balance -= 1
        balance += play_game()
        round_count += 1

    return round_count


def two_c(M):
    initial_balance = 10
    results = []
    for i in range(M):
        results.append(playout(initial_balance))
    results.sort()

    print('MEAN:', sum(results) / len(results))
    print('MEDIAN:',  results[len(results)//2])


#3 part 1

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


def three_a(M):
    results = []
    smallest_n = None
    for n in range(10, 51):
        p = estimate_overlap_probs(n, M)
        results.append(p)
        if smallest_n == None and p >= 0.5: smallest_n = n

    results = np.array(results)

    proportion = (results > 0.5).sum() / len(results)

    print('Proportion:', proportion)
    print('Smallest N:', smallest_n)


# 3 part 2

def simulate_group_formation():
    bdays = set()
    group_count = 0
    while len(bdays) != 365:
        bdays.add(random.randint(1, 365))
        group_count += 1
    return group_count


def three_b(M):
    results = []
    for i in range(M):
        results.append(simulate_group_formation())

    print("Expected group size:", sum(results) / len(results))


M = 1000
print("\n2c:")
two_c(M)
print("\n3 part 1:")
three_a(M)
print("\n3 part 2:")
three_b(M)