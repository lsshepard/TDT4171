# Expected number of people for all birthdays to be covered
import random

def simulate_group_formation():
    bdays = set()
    group_count = 0
    while len(bdays) != 365:
        bdays.add(random.randint(1, 365))
        group_count += 1
    return group_count

results = []
for i in range(10000):
    results.append(simulate_group_formation())

print("Expected group size:", sum(results) / len(results))