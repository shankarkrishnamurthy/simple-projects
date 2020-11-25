import concurrent.futures as p
import math
 
PRIMES = [
    112582705942171*112272535095293,
    112272535095293,
    115280095190773,
    115797848077099*112272535095293,
    1099726899285419]
 
def is_prime(n):
    if n % 2 == 0:
        return False
 
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True
 
def main():
    with p.ProcessPoolExecutor() as e:
        for number, prime in zip(PRIMES, e.map(is_prime, PRIMES,timeout=5)):
            print('%d is prime: %s' % (number, prime))
 
if __name__ == '__main__':
    main()
