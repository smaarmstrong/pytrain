class TreeNode:
    """A binary tree node.

    The grader may pass its own objects exposing the same
    `value`/`left`/`right` attributes, so rely only on those.
    """

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build_tree(values):
    """Decode a compact level-order list into a tree; return the root."""
    raise NotImplementedError


def preorder(root):
    """Node, then left subtree, then right subtree."""
    raise NotImplementedError


def inorder(root):
    """Left subtree, then node, then right subtree."""
    raise NotImplementedError


def postorder(root):
    """Left subtree, then right subtree, then node."""
    raise NotImplementedError


def level_order(root):
    """List of lists of values, one per level (BFS)."""
    raise NotImplementedError
