def ordered_digits(x):
    """如果 x 从左往右是非递减的，返回 True，否则返回 False。

    疑问：乱序数字如何返回？假设乱序也返回 False

    从右往左是非递增数字
    >>> ordered_digits(5)
    True
    >>> ordered_digits(11)
    True
    >>> ordered_digits(127)
    True
    >>> ordered_digits(1357)
    True
    >>> ordered_digits(21)
    False
    >>> ordered_digits(212)
    False
    """
    last = 10
    while x > 0:
        cur = x % 10
        x = x // 10
        if cur > last:
            return False
        last = cur
    return True