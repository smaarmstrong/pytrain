class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def bst_insert(root, value):
    if root is None:
        return TreeNode(value)
    node = root
    while True:
        if value == node.value:
            return root
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                return root
            node = node.left
        else:
            if node.right is None:
                node.right = TreeNode(value)
                return root
            node = node.right


def inorder_values(root):
    out, stack, node = [], [], root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.value)
        node = node.right
    return out


def is_valid_bst(root):
    # iterative bound-checking so deep skewed trees don't hit recursion limits
    stack = [(root, None, None)]
    while stack:
        node, lo, hi = stack.pop()
        if node is None:
            continue
        if (lo is not None and node.value <= lo) or (hi is not None and node.value >= hi):
            return False
        stack.append((node.left, lo, node.value))
        stack.append((node.right, node.value, hi))
    return True
