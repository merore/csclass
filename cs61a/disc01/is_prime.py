def is_prime(n):
    """判断 n 是否为素数
    >>> is_prime(10)
    False
    >>> is_prime(7)
    True
    >>> is_prime(1)
    False
    """
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k+=1
    return True