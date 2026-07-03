class TreeNode:
    """A binary tree node; the grader's own nodes expose the same attrs."""

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def bst_insert(root, value):
    """Insert value (ignoring duplicates); return the tree's root."""
    raise NotImplementedError


def inorder_values(root):
    """In-order values as a list ([] for None)."""
    raise NotImplementedError


def is_valid_bst(root):
    """True iff the whole tree satisfies the strict BST invariant."""
    raise NotImplementedError
