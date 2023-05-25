def summ1(n):
    summe = 0

    for i in range(1, n):
        summe += i
    return summe

def summ2(n):
    return sum(range(1, n))

print(f'Summe1: {summ1(1000)}')
print(f'Summe2: {summ2(1000)}')