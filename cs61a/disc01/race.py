def race(x, y):
    """乌龟每分钟走 x 步，兔子在前五分钟每分钟走 y 步，然后休息五分钟，依次
    往复，求多少分钟后乌龟追上兔子

    >> race(5, 7) # 7 分钟后都走 35 步
    7
    >> race(2, 4) # 10 分钟后都走 20 步
    10
    """

    assert y > x and y < x * 2, "兔子不能太快"
    tortoise, hare, minutes = 0, 0, 0
    while minutes == 0 or tortoise < hare:
        tortoise += x
        if minutes % 10 < 5:
            hare += y
        minutes += 1
    return minutes