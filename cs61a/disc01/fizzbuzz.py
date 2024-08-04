def fizzbuzz(n):
    """给定一个数字 n，对于从 1 到 n 的每个数字 i，应该满足以下要求
    1. 如果 i 能被 3 和 5 整除，打印 fizzbuzz。
    2. 如果 i 能被 3 整除而不能被 5 整除，打印 fizz。
    3. 如果 i 能被 5 整除而不能被 3 整除，打印 buzz。
    4. 其余情况打印 i。

    >>> result = fizzbuzz(16)
    1
    2
    fizz
    4
    buzz
    fizz
    7
    8
    fizz
    buzz
    11
    fizz
    13
    14
    fizzbuzz
    16
    >>> print(result)
    None
    """
    i  = 1
    while i <= n:
        if i % 3 == 0 and i % 5 == 0:
            print('fizzbuzz')
        elif i % 3 == 0:
            print('fizz')
        elif i % 5 == 0:
            print('buzz')
        else:
            print(i)
        i += 1