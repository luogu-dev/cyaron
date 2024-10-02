"""
This is a module that includes some useful math functions.

Functions:
    factorial(n): The factorial of n
    is_perm(a,b): Check if number a and b share the same digits
    is_palindromic(n): Check if n is palindromic(i.e. The number does not change if you reverse it)
    is_pandigital(n,s=9): Check if number n is made from sequence 1 to s
    d(n): Calculate the sum of proper divisors for n
    pal_list(k): Create a list of all palindromic numbers with k digits
    sof_digits(n): Sum of factorial's digits
    fibonacci(n): Find the nth Fibonacci number
    sos_digits(n): Sum of squares of digits
    pow_digits(n,e): Sum of the digits to a power e
    is_prime(n): Check n for prime
    miller_rabin(n): Miller-Rabin primality test
    factor(n): Factor a number into primes and frequency
    perm(n,s): Find the nth pemutation of string s
    binomial(n,k): Calculate C(n,k)
    catalan_number(n): Calculate the nth Catalan number
    prime_sieve(n): Return a list of prime numbers from 2 to a prime < n
    exgcd(a,b): Bézout coefficients. Returns (u, v, gcd(a,b))
    mod_inverse(a,b): returns u of exgcd(a,b)
    phi(x): The PHI function of x
    miu(x): The MIU function of x
    dec2base(n,base): Number base conversion
    n2words(num,join=True): Number to words

forked from https://blog.dreamshire.com/common-functions-routines-project-euler/
"""

from __future__ import absolute_import
from math import sqrt, factorial
import random
import itertools
from typing import Union, Tuple, List

fact = (1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880)


def is_perm(a: int, b: int):
    """
    Check if two numbers are permutations of each other.

    This function takes two numbers, converts them to strings, sorts the characters
    in each string, and then compares the sorted strings to determine if the numbers
    are permutations of each other.
    Args:
        a: The first number to compare.
        b: The second number to compare.
    Returns:
        bool: True if the numbers are permutations of each other, False otherwise.
    """

    return sorted(str(a)) == sorted(str(b))


def is_palindromic(n: Union[int, str]):
    """
    Check if a given number or string is palindromic.

    A palindromic number or string is one that reads the same backward as forward.
    Parameters:
        n: The number or string to check.
    Returns:
        True if the input is palindromic, False otherwise.
    """
    n = str(n)
    return n == n[::-1]


def is_pandigital(n: Union[int, str], s: int = 9):
    """
    Check if a number is pandigital.

    A number is considered pandigital if it contains each digit from 1 to s exactly once.
    Parameters:
        n: The number to check.
        s (optional): The length of the pandigital number. Default is 9.
    Returns:
        True if the number is pandigital, False otherwise.
    """

    n = str(n)
    return len(n) == s and not '1234567890'[:s].strip(n)


def d(n: int):
    """
    Calculate the sum of the divisors of a given number `n`.

    This function computes the sum of all divisors of `n`, including 1 and `n` itself.

    It iterates from 2 to the square root of `n`, adding both the divisor and its
    corresponding quotient to the sum. If `n` is a perfect square, the square root
    is subtracted from the sum to correct for double-counting.
    Parameters:
        n: The number for which to calculate the sum of divisors.
    Returns:
        The sum of the divisors of `n`.
    """
    s = 1
    t = sqrt(n)
    for i in range(2, int(t) + 1):
        if n % i == 0:
            s += i + n // i
    if t == int(t):
        s -= int(t)  #correct s if t is a perfect square
    return s


def pal_list(k: int):
    """
    Generate a list of palindromic numbers of length `k`.
    Parameters:
        k: The length of the palindromic numbers to generate.
    Returns:
        A list of palindromic numbers of length `k`.
    """
    if k == 1:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return [
        sum(n * (10**i)
            for i, n in enumerate(([x] + list(ys) + [z] + list(ys)[::-1] +
                                   [x]) if k % 2 else ([x] + list(ys) +
                                                       list(ys)[::-1] + [x])))
        for x in range(1, 10)
        for ys in itertools.product(range(10), repeat=int(k / 2) - 1)
        for z in (range(10) if k % 2 else (None, ))
    ]


def sof_digits(n: int):
    """
    Calculate the sum of the factorials of the digits of a given number.
    Args:
        n: The input number.
    Returns:
        The sum of the factorials of the digits of the input number.
    """

    if n == 0:
        return 1
    s = 0
    while n > 0:
        s, n = s + fact[n % 10], n // 10
    return s


def fibonacci(n: int):
    """
    Find the nth number in the Fibonacci series.
    Args:
        n: The position in the Fibonacci series to retrieve.
    Returns:
        The nth Fibonacci number.
    Raises:
        ValueError: If the input is a negative integer.
    Example:
        >>> fibonacci(100)
        354224848179261915075
    References:
        Algorithm & Python source: Copyright (c) 2013 Nayuki Minase  
        Fast doubling Fibonacci algorithm  
        http://nayuki.eigenstate.org/page/fast-fibonacci-algorithms
    """
    if n < 0:
        raise ValueError("Negative arguments not implemented")
    return _fib(n)[0]


def _fib(n: int) -> Tuple[int, int]:
    """Returns a tuple of fibonacci (F(n), F(n+1))."""
    if n == 0:
        return (0, 1)
    a, b = _fib(n // 2)
    c = a * (2 * b - a)
    e = b * b + a * a
    return (c, e) if n % 2 == 0 else (e, c + e)


def sos_digits(n: int):
    """
    Calculate the sum of squares of the digits of a given number.
    Args:
        n: The number whose digits' squares are to be summed.
    Returns:
        The sum of the squares of the digits of the number.
    """
    return pow_digits(n, 2)


def pow_digits(n: int, e: int):
    """
    Calculate the sum of each digit of a number raised to a specified power.
    Args:
        n: The number whose digits will be processed.
        e: The exponent to which each digit will be raised.
    Returns:
        The sum of each digit of the number raised to the specified power.
    """
    s: int = 0
    while n > 0:
        s, n = s + (n % 10)**e, n // 10
    return s


def is_prime(n: int):
    """
    Check if a number is a prime number.

    This function uses a trial division method to determine if the number is prime.
    Parameters:
        n: The number to check for primality.
    Returns:
        True if the number is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    r = int(sqrt(n))
    f = 5
    while f <= r:
        if n % f == 0 or n % (f + 2) == 0:
            return False
        f += 6
    return True


def miller_rabin(n: int, repeat_time: int = 20):
    """
    Check if a number is prime using the Miller-Rabin primality test.
    Args:
        n: The number to be tested for primality.
        repeat_time: The number of iterations to perform. Default is 20.
    Returns:
        True if n is a probable prime, False if n is composite.
    Example:
        >>> miller_rabin(162259276829213363391578010288127)  # Mersenne prime #11
        True
    Note:
        This function uses a probabilistic algorithm to determine primality.
        It performs 20 iterations to reduce the probability of a false positive.
    References:
        Algorithm & Python source:
        http://en.literateprograms.org/Miller-Rabin_primality_test_(Python)
    """
    if (n & 1) == 0 or n < 3:
        return n == 2
    if (n % 3) == 0:
        return n == 3
    f = n - 1
    s = 0
    while (f & 1) == 0:
        f >>= 1
        s += 1
    for _ in range(repeat_time):
        a = random.randint(2, n - 1)
        if not _miller_rabin_pass(a, s, f, n):
            return False
    return True


def _miller_rabin_pass(a: int, s: int, f: int, n: int):
    a_to_power = pow(a, f, n)
    if a_to_power == 1:
        return True
    for _ in range(s - 1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n - 1


def factor(n: int) -> List[Tuple[int, int]]:
    """
    Find the prime factors of a given number along with their frequencies.
    Args:
        n: The number to factorize.
    Returns:
        A list of tuples where each tuple contains a prime factor and its frequency.
    Example:
        >>> factor(786456)
        [(2, 3), (3, 3), (11, 1), (331, 1)]
    Note:
        This function uses a specific sequence of prime gaps to optimize the factorization process.
        Source: Project Euler forums for problem #3
    """
    f = 1
    factors = []
    prime_gaps = [2, 4, 2, 4, 6, 2, 6, 4]
    if n < 1:
        return []
    while True:
        for gap in ([1, 1, 2, 2, 4] if f < 11 else prime_gaps):
            f += gap
            if f * f > n:  # If f > sqrt(n)
                return factors + ([] if n == 1 else [(n, 1)])
            if not n % f:
                e = 1
                n //= f
                while not n % f:
                    n //= f
                    e += 1
                factors.append((f, e))


def perm(n: int, s: str) -> str:
    """
    Find the nth permutation of the string s.
    Parameters:
        n: The permutation index (0-based).
        s: The string for which the permutation is to be found.
    Returns:
        The nth permutation of the string s.
    Example:
        >>> perm(30, 'abcde')
        'bcade'
    """
    if len(s) == 1:
        return s
    q, r = divmod(n, factorial(len(s) - 1))
    return s[q] + perm(r, s[:q] + s[q + 1:])


def binomial(n: int, k: int):
    """
    Calculate C(n, k), the number of ways to choose k elements from a set of n elements.

    This function computes the binomial coefficient, which is the number of ways to choose
    k elements from a set of n elements without regard to the order of selection.
    Parameters:
        n: The total number of elements.
        k: The number of elements to choose.
    Returns:
        The binomial coefficient C(n, k).
    Example:
        >>> binomial(30, 12)
        86493225
    """
    nt = 1
    for t in range(min(k, n - k)):
        nt = nt * (n - t) // (t + 1)
    return nt


def catalan_number(n: int):
    """
    Calculate the nth Catalan number.

    The Catalan numbers are a sequence of natural numbers that occur in various counting problems, 
    often involving recursively defined objects.
    Parameters:
        n: The index of the Catalan number to calculate.
    Returns:
        The nth Catalan number.
    Example:
        >>> catalan_number(10)
        16796
    """
    nm = dm = 1
    for k in range(2, n + 1):
        nm, dm = (nm * (n + k), dm * k)
    return nm // dm


def prime_sieve(n):
    """
    Return a list of prime numbers from 2 to a prime < n.
    Args:
        n: The upper limit (exclusive) for generating prime numbers.
    Returns:
        A list of prime numbers less than n.
    Example:
        >>> prime_sieve(25)
        [2, 3, 5, 7, 11, 13, 17, 19, 23]
    Algorithm & Python source: Robert William Hanks
    http://stackoverflow.com/questions/17773352/python-sieve-prime-numbers
    """
    sieve = [True] * (n // 2)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [2 * i + 1 for i in range(1, n // 2) if sieve[i]]


def exgcd(a: int, b: int):
    """
    Bézout coefficients (u, v) of (a, b) as:
        a * u + b * v = gcd(a, b)

    Result is the tuple: (u, v, gcd(a, b)).
    Parameters:
        a: First integer.
        b: Second integer.
    Returns:
        A tuple containing the Bézout coefficients (u, v) and gcd(a, b).
    Examples:
        >>> exgcd(7*3, 15*3)
        (-2, 1, 3)
        >>> exgcd(24157817, 39088169)  # sequential Fibonacci numbers
        (-14930352, 9227465, 1)
    Algorithm source: Pierre L. Douillet
    http://www.douillet.info/~douillet/working_papers/bezout/node2.html
    """
    u, v, s, t = 1, 0, 0, 1
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        u, s = s, u - q * s
        v, t = t, v - q * t

    return (u, v, a)


def mod_inverse(a: int, b: int):
    """
    Calculate the modular inverse of a with respect to b.

    The modular inverse of a is the number x such that (a * x) % b == 0.

    Parameters:
        a: The number for which to find the modular inverse.
        b: The modulus.
    Returns:
        The modular inverse of a with respect to b.
    Raises:
        ValueError: If the modular inverse does not exist.
    """
    return pow(a, -1, b)


def phi(x: int):
    """
    Calculate Euler's Totient function for a given integer x.

    Euler's Totient function, φ(x), is defined as the number of positive integers 
    less than or equal to x that are relatively prime to x.
    Args:
        x: The integer for which to calculate the Totient function.
    Returns:
        The value of Euler's Totient function for the given integer x.
    """
    if x == 1:
        return 1
    factors = factor(x)
    ans = x
    for prime in factors:
        ans = ans // prime[0] * (prime[0] - 1)
    return ans


def miu(x: int):
    """
    Calculate the Möbius function value for a given integer x.

    The Möbius function μ(x) is defined as:
    - μ(1) = 1
    - μ(x) = 0 if x has a squared prime factor
    - μ(x) = (-1)^k if x is a product of k distinct prime factors
    Args:
        x: The integer for which to calculate the Möbius function.
    Returns:
        The Möbius function value for the given integer x.
    """
    if x == 1:
        return 1
    factors = factor(x)
    for prime in factors:
        if prime[1] > 1:
            return 0
    return 1 - (len(factors) and 1) * 2


#source:
# http://interactivepython.org/runestone/static/pythonds/Recursion/pythondsConvertinganIntegertoaStringinAnyBase.html
def dec2base(n: int, base: int) -> str:
    """
    Convert a decimal number to a specified base.
    Args:
        n: The decimal number to convert.
        base: The base to convert the number to. Must be between 2 and 16.
    Returns:
        The number represented in the specified base.
    Raises:
        ValueError: If the base is not between 2 and 16.
    """
    convert_string = "0123456789ABCDEF"
    if n < base:
        return convert_string[n]
    return dec2base(n // base, base) + convert_string[n % base]


#this function copied from stackoverflow user: Developer, Oct 5 '13 at 3:45
def n2words(num: int, join: bool = True):
    """
    Convert a number into words.
    Args:
        num: The number to convert.
        join (bool, optional): If True, join the words with spaces. Defaults to True.
    Returns:
        The number in words as a single string if join is True,  otherwise as a list of words.
    """
    units = [
        '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
        'Nine'
    ]
    teens = ['','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen', \
             'Seventeen','Eighteen','Nineteen']
    tens = ['','Ten','Twenty','Thirty','Forty','Fifty','Sixty','Seventy', \
            'Eighty','Ninety']
    thousands = ['','Thousand','Million','Billion','Trillion','Quadrillion', \
                 'Quintillion','Sextillion','Septillion','Octillion', \
                 'Nonillion','Decillion','Undecillion','Duodecillion', \
                 'Tredecillion','Quattuordecillion','Sexdecillion', \
                 'Septendecillion','Octodecillion','Novemdecillion', \
                 'Vigintillion']
    words: List[str] = []
    if num == 0:
        words.append('zero')
    else:
        num_str = '%d' % num
        num_str_len = len(num_str)
        groups = int((num_str_len + 2) / 3)
        num_str = num_str.zfill(groups * 3)
        for i in range(0, groups * 3, 3):
            h, t, u = int(num_str[i]), int(num_str[i + 1]), int(num_str[i + 2])
            g = groups - (int(i / 3) + 1)
            if h >= 1:
                words.append(units[h])
                words.append('Hundred')
            if t > 1:
                words.append(tens[t])
                if u >= 1:
                    words.append(units[u])
            elif t == 1:
                if u >= 1:
                    words.append(teens[u])
                else:
                    words.append(tens[t])
            else:
                if u >= 1:
                    words.append(units[u])
            if (g >= 1) and ((h + t + u) > 0):
                words.append(thousands[g] + '')
    if join:
        return ' '.join(words)
    return words
