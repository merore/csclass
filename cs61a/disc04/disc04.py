from tree import *

def insect_combinatorics(m, n):
    """在一个 (m,n) 的网格里，一只昆虫从左下角
    开始往右上角爬，每次只能向上或向右，一共有多
    少种方法。

    设从 （1, 1）到 （m ,n）总方法数为f
    f(1,1,m,n) = f(2,1,m,n) + f(1,2,m,n)
    即
    f(x,y) = f(x+1,x) + f(x,y+1)
    if x == m or y == n
    return 1
    >>> insect_combinatorics(2, 2)
    2
    >>> insect_combinatorics(5, 7)
    210
    >>> insect_combinatorics(117, 1)
    1
    >>> insect_combinatorics(1, 157)
    1
    """
    def crawl(x,y):
        if x == m or y == n:
            return 1
        
        return crawl(x+1, y) + crawl(x, y+1)
    return crawl(1,1)


def even_weighted_loop(s):
    """编写一个函数，接受一个列表 s 并返回一个
    新列表，新的列表保留 s 的偶数索引元素并乘
    以索引。
    >>> x = [1, 2, 3, 4, 5, 6]
    >>> even_weighted_loop(x)
    [0, 6, 20]
    """
    length = len(s)
    
    i = 0
    ns = []
    while i < length:
        if i % 2 == 0:
            ts = [s[i]*i]
            ns = ns + ts
        i += 1
    return ns

def even_weighted_comprehension(s):
    """
    >>> x = [1, 2, 3, 4, 5, 6]
    >>> even_weighted_loop(x)
    [0, 6, 20]
    """
    return [s[x]*x for x in range(0,len(s)) if x % 2 == 0]

def has_path(t, p):
    """传入一个树和一个路径，判断这个树是否包含这个路径

    f(t, p) t.v == p[0] and (f[p[1][i],p[1:]] or f[p[1][i+1], p[1:]] ...)
    t = [x, [...]]
    p = [1,2,3,4]

    >>> t2 = tree(5, [tree(6), tree(7)])
    >>> t1 = tree(3, [tree(4), t2])
    >>> has_path(t1, [5,6])
    False
    >>> has_path(t2, [5, 6])        # This path is from the root of t2
    True
    >>> has_path(t1, [3, 5])        # This path does not go to a leaf, but that's ok
    True
    >>> has_path(t1, [3, 5, 6])     # This path goes to a leaf
    True
    >>> has_path(t1, [3, 4, 5, 6])  # There is no path with these labels
    False
    """
    if label(t) != p[0]:
        return False

    # 没有到子节点，不查询了
    if len(p) == 1:
        return True

    for branch in branches(t):
        if has_path(branch, p[1:]):
            return True

    return False


def find_path(t, x):
    """
    为什么这个函数可以不使用 if_leaf?
    因为循环本身代替了 if_leaf 的功能，和 has_path 一样

    >>> t2 = tree(5, [tree(6), tree(7)])
    >>> t1 = tree(3, [tree(4), t2])
    >>> find_path(t1, 5)
    [3, 5]
    >>> find_path(t1, 4)
    [3, 4]
    >>> find_path(t1, 6)
    [3, 5, 6]
    >>> find_path(t2, 6)
    [5, 6]
    >>> print(find_path(t1, 2))
    None
    """
    if label(t) == x:
        return [x]

    for branch in branches(t):
        p = find_path(branch, x)
        if p != None:
            return [label(t)] + p

    return None

def sprout_leaves(t, leaves):
    """
    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    """
    def append_tree(root, branch):
        bs = branches(root)
        bs = bs + [branch]
        return tree(label(root), bs)

    # 这里应该构造一个新的树，而不是使用 nt = t，否则会造成子节点重复
    nt = tree(label(t))
    if is_leaf(t):
        for leaf in leaves:
            nt = append_tree(nt, tree(leaf))
        return nt

    for branch in branches(t):
        nt = append_tree(nt, sprout_leaves(branch, leaves))
    return nt
