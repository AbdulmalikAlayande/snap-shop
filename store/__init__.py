import sys


def fizzBuzz(n):
    for number in range(1, n+1):
        if number % 3 == 0 and number % 5 == 0:
            print(number, 'FizzBuzz')
        elif number % 3 != 0 and number % 5 != 0:
            print(number)
        elif number % 3 == 0:
            print('Fizz')
        else:
            print('Buzz')

if __name__ == '__main__':
    age = 20
    x = 20
    y = x
    z = age

    superheroes = ["Captain America", "Superman", "Batman"]

    sidekicks = ["Bucky", "Jimmy Oslen", "Robin"]

    superheroes.append(sidekicks)
    sidekicks.append(superheroes)

    del superheroes

    print(sidekicks[-1])

    print(id(age), id(x))
    print('age ref count', sys.getrefcount(age))
    # print('x ref count', sys.getrefcount(x))
    # print('x ref count at y', sys.getrefcount(x))
    print('age ref count at z', sys.getrefcount(age))
    n = int(input().strip())

    fizzBuzz(n)
