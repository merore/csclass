def tree(label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_leaf(tree):
    return not branches(tree)

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def print_tree(tree):
    """横向上按缩进打印树，第 n 层树的缩进为 n (n从 0 开始)。
    纵向上按从中序规则打印树
    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    """
    def print_tree_layer(tree, n):
        # 打印缩进
        for i in range(2*n):
            print(" ", end='')
       
        # 打印当前节点
        print(label(tree))
        
        # 打印子树
        for branch in branches(tree):
            print_tree_layer(branch, n+1)

    print_tree_layer(tree, 0)

def append_tree(root, branch):
    bs = branches(root)
    bs = bs + branch
    return tree(label(root), bs)
