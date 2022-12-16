import timeit

testcode1 = '''
def summe(n):
    summe = 0
    for i in range(1, n):
        summe += i
    return summe

summe(1_000_000)
'''

testcode2 = '''
def summe(n):
    return sum(range(1, n))

summe(1_000_000)
'''

testcode3 = '''
def summe(n):
    return n * (n-1) / 2

summe(1_000_000)
'''

print("Variante1: " + timeit.repeat(stmt=testcode1, repeat=5))
print("Variante2: " + timeit.repeat(stmt=testcode2, repeat=5))
print("Variante3: " + timeit.repeat(stmt=testcode3, repeat=5))