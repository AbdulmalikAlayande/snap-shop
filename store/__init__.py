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
    n = int(input().strip())

    fizzBuzz(n)
