# Binary tree: build & four traversals

A binary tree node is any object with three attributes:

- `value` — the payload
- `left` / `right` — child nodes, or `None`

The starter gives you a `TreeNode` class. IMPORTANT: the grader passes in its
*own* node objects exposing the same three attributes (not instances of your
class), so rely only on `value`/`left`/`right` — never on `isinstance`.

In `solution.py`, implement:

```python
def build_tree(values):
    """Build a tree from a compact level-order list and return the root.

    Read `values` left to right. The first value is the root; return None
    for an empty list. Then, walking the already-created nodes in creation
    (level) order, each node takes the next two values as its left and
    right children. A None value means "no child there" (and produces no
    node, so nothing is queued for it). The list may simply end early —
    every remaining slot is then "no child".

    build_tree([1, 2, 3, None, 4]) is:
            1
           / \\
          2   3
           \\
            4
    """

def preorder(root):   # node, left subtree, right subtree
def inorder(root):    # left subtree, node, right subtree
def postorder(root):  # left subtree, right subtree, node
    """Each returns the list of values in that DFS order. [] for None."""

def level_order(root):
    """BFS by depth: a list of lists, one per level, top to bottom,
    left to right within a level. [] for None.

    level_order(build_tree([1, 2, 3, None, 4])) == [[1], [2, 3], [4]]
    """
```

Requirements:

- All five accept `root=None` / `values=[]` gracefully.
- Values may repeat and may be any object (including None is NOT required —
  a None *value* never occurs; None always means "no node").
- Trees can be skewed ~100 deep; simple recursion is fine for the DFS
  traversals.

Examples:

```python
>>> t = build_tree([1, 2, 3, None, 4])
>>> preorder(t), inorder(t), postorder(t)
([1, 2, 4, 3], [2, 4, 1, 3], [4, 2, 3, 1])
>>> level_order(t)
[[1], [2, 3], [4]]
>>> build_tree([]) is None
True
```
