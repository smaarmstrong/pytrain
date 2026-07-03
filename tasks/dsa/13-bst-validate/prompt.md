# Binary search tree: insert, validate, in-order

A binary search tree (BST) is a binary tree — nodes with `value`, `left`,
`right` attributes — where for EVERY node, all values in its left subtree are
strictly smaller than its value and all values in its right subtree are
strictly larger. No duplicate values exist in a valid BST.

The starter gives you a `TreeNode`. As usual, the grader passes its own node
objects with the same three attributes, so rely only on those (no
`isinstance`).

In `solution.py`, implement:

```python
def bst_insert(root, value):
    """Insert `value` into the BST rooted at `root`; return the root.

    - root may be None (empty tree): return the new single node.
    - If `value` is already present, the tree is left unchanged (still
      return its root).
    - You may relink/mutate the given nodes or build fresh ones; the
      grader only inspects the returned tree via value/left/right.
    """

def inorder_values(root):
    """The values of the tree in in-order (left, node, right) as a list.

    [] for None. For a valid BST this comes out in strictly ascending
    order — but implement plain in-order; the grader also feeds trees
    that are NOT search trees.
    """

def is_valid_bst(root):
    """True iff the tree satisfies the BST invariant above.

    None -> True (an empty tree is valid). Watch out: EVERY value in the
    left subtree must be smaller than the node — not just the immediate
    child. Duplicate values anywhere make the tree invalid.
    """
```

Requirements:

- Values are integers.
- `is_valid_bst` must catch a grandchild that violates a grandparent's
  bound, e.g. `5 -> left 3 -> right 6` is INVALID (6 sits in 5's left
  subtree) even though 6 > 3 looks locally fine.
- Trees built by repeated `bst_insert` (possibly skewed ~200 deep from
  sorted input) must round-trip: `inorder_values` gives the sorted set of
  inserted values and `is_valid_bst` is True.

Examples:

```python
>>> root = None
>>> for v in [5, 3, 8, 3]: root = bst_insert(root, v)
>>> inorder_values(root)
[3, 5, 8]
>>> is_valid_bst(root)
True
```
