def multiply(m, n):
    """
    >>> multiply(5, 3)
    15
    """
    if n == 0:
        return 0
    return m + multiply(m, n-1)

def swipe(n):
    """
    >>> swipe(2837)
    7
    3
    8
    2
    8
    3
    7
    """
    if n >= 10:
        print(n % 10)
        swipe(n//10)
        print(n % 10)
    else:
        print(n)

def skip_factorial(n):
    """
    >>> skip_factorial(5)
    15
    >>> skip_factorial(8)
    384
    """
    if n <= 0:
        return 1
    return n * skip_factorial(n-2)

def hailstone(n):
    """
    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    >>> b = hailstone(1)
    1
    >>> b
    1
    """
    print(n)
    if n == 1:
        return 1
    if n % 2 == 0:
        return 1+hailstone(n//2)
    else:
        return 1+hailstone(n*3 + 1)

def count_stair_ways(n):
    if n <= 1:
        return 1
    if n == 2:
        return 2
    return count_stair_ways(n-1) + count_stair_ways(n-2)

def has_seven(n):
    if n == 0:
        return False
    elif n % 10 == 7:
        return True
    else:
        return has_seven(n // 10)

def sevens(n, k):
    def f(i, who, direction):
        if i == n:
            return who
        if has_seven(i) or i % 7 == 0:
            direction = -direction
        print("player %d says %d" % (who, i))
        who = who+direction
        if who == 0:
            who = k
        elif who == k+1:
            who = 1
        return f(i+1, who, direction)
    return f(1, 1, 1)
