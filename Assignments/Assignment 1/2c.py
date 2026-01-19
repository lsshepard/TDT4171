# Expected rounds played before going broke

import random
import matplotlib.pyplot as plt

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


N = 10000
initial_balance = 10
results = []
for i in range(N):
    results.append(playout(initial_balance))
results.sort()

print('MEAN:', sum(results) / len(results))
print('MEDIAN:',  results[len(results)//2])

plt.hist(results, bins=100)
plt.show()
    