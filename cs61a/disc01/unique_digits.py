def unique_digits(n):
    """返回正整数 n 中出现数字的数量
    
    要返回出现数字的数量，由于每一位数字都是 0-9 所以可以检索每一位
    出现的次数，如果出现 1 次，则计算该数字。所以可以有一个函数
    has_digit(n, k)，表示数字 n 中 k 出现的次数。

    >>> unique_digits(8675309)
    7
    >>> unique_digits(13173131)
    3
    >>> unique_digits(101)
    2
    """
    k, count = 0, 0
    while k <= 9:
        num = has_digit(n, k)
        if num >= 1:
            count += 1
        k += 1
    return count

def has_digit(n, k):
    """数字 n 中数字 k 出现的次数, 0 <= k <= 9

    >>> has_digit(10, 1)
    1
    >>> has_digit(11, 1)
    2
    >>> has_digit(11, 2)
    0
    """
    count = 0
    while n > 0:
        m = n % 10
        if m == k:
            count += 1
        n = n // 10
    return count
