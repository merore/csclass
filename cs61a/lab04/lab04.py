LAB_SOURCE_FILE=__file__


def flatten(s):
    """Returns a flattened version of list s.

    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> deep = [1, [[2], 3], 4, [5, 6]]
    >>> flatten(deep)
    [1, 2, 3, 4, 5, 6]
    >>> deep                                # input list is unchanged
    [1, [[2], 3], 4, [5, 6]]
    >>> very_deep = [['m', ['i', ['n', ['m', 'e', ['w', 't', ['a'], 't', 'i', 'o'], 'n']], 's']]]
    >>> flatten(very_deep)
    ['m', 'i', 'n', 'm', 'e', 'w', 't', 'a', 't', 'i', 'o', 'n', 's']
    """
    "*** YOUR CODE HERE ***"

    ns = []
    for e in s:
        if type(e) == list:
            ns = ns + flatten(e)
        else:
            ns = ns + [e]
    return ns



def merge(s, t):
    """Merges two sorted lists.

    >>> s1 = [1, 3, 5]
    >>> s2 = [2, 4, 6]
    >>> merge(s1, s2)
    [1, 2, 3, 4, 5, 6]
    >>> s1
    [1, 3, 5]
    >>> s2
    [2, 4, 6]
    >>> merge([], [2, 4, 6])
    [2, 4, 6]
    >>> merge([1, 2, 3], [])
    [1, 2, 3]
    >>> merge([5, 7], [2, 4, 6])
    [2, 4, 5, 6, 7]
    >>> merge([2, 3, 4], [2, 4, 6])
    [2, 2, 3, 4, 4, 6]
    >>> from construct_check import check
    >>> check(LAB_SOURCE_FILE, 'merge', ['While', 'For'])    # ban iteration
    True
    """
    "*** YOUR CODE HERE ***"
    
    """
    递归合并，merge(s, t) 返回一个新列表 ns
    判断 s[0] 和 t[0]，ns 追加小的那一个，然后 ns 再追加 merge(s,t)
    一旦 s 长度为 0，ns 追加 t 并返回，反之亦然
    """

    ns = []
    if len(s) == 0:
        ns = ns + t
        return ns
    if len(t) == 0:
        ns = ns + s
        return ns

    if s[0] <= t[0]:
        ns = ns + [s[0]]
        ns = ns + merge(s[1:], t)
    else:
        ns = ns + [t[0]]
        ns = ns + merge(s, t[1:])

    return ns


def size_of_tree(t):
    """Return the number of entries in the tree.
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    >>> size_of_tree(numbers)
    7
    """
    "*** YOUR CODE HERE ***"

    """
    一个数的大小，是所有子树和 +1
    f(t) = f(child 1) + ... f(child n) + 1
    当 t 为子节点时，返回 1
    因为当 t 为子节点时，branches(t) 为空不会循环，所以可忽略
    """
    n = 1
    for branch in branches(t):
        n += size_of_tree(branch)

    return n


def replace_loki_at_leaf(t, lokis_replacement):
    """Returns a new tree where every leaf value equal to "loki" has
    been replaced with lokis_replacement.

    >>> yggdrasil = tree('odin',
    ...                  [tree('balder',
    ...                        [tree('loki'),
    ...                         tree('freya')]),
    ...                   tree('frigg',
    ...                        [tree('loki')]),
    ...                   tree('loki',
    ...                        [tree('sif'),
    ...                         tree('loki')]),
    ...                   tree('loki')])
    >>> laerad = copy_tree(yggdrasil)    # copy yggdrasil for testing purposes
    >>> print_tree(replace_loki_at_leaf(yggdrasil, 'freya'))
    odin
      balder
        freya
        freya
      frigg
        freya
      loki
        sif
        freya
      freya
    >>> laerad == yggdrasil    # Make sure original tree is unmodified
    True
    """
    "*** YOUR CODE HERE ***"

    """
    replace_loki_at_leaf 返回一棵新树 nt，新树的所有子树等于递归各个子数
    如果 t 是叶子节点，判断替换并返回新树
    """
    if is_leaf(t) and label(t) == 'loki':
        return tree(lokis_replacement)

    nbranches = []

    for branch in branches(t):
        """
        nbranches += replace_loki_at_leaf(branch, lokis_replacement)
        replace_loki_at_leaf  返回子树的时候，应该用 [] 扩起来，否则
        子树在 + 的时候是扩展的
        """
        nbranches += [replace_loki_at_leaf(branch, lokis_replacement)]

    return tree(label(t), nbranches)



def divide(quotients, divisors):
    """Return a dictonary in which each quotient q is a key for the list of
    divisors that it divides evenly.

    >>> divide([3, 4, 5], [8, 9, 10, 11, 12])
    {3: [9, 12], 4: [8, 12], 5: [10]}
    >>> divide(range(1, 5), range(20, 25))
    {1: [20, 21, 22, 23, 24], 2: [20, 22, 24], 3: [21, 24], 4: [20, 24]}
    """
    return {x:[y for y in divisors if y % x == 0] for x in quotients}



# Tree Data Abstraction

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """Return the label value of a tree."""
    return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

