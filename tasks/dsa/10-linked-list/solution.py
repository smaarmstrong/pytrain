class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def build_linked(values):
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head


def to_list(head):
    out = []
    node = head
    while node is not None:
        out.append(node.value)
        node = node.next
    return out


def reverse_linked(head):
    prev = None
    node = head
    while node is not None:
        node.next, prev, node = prev, node, node.next
    return prev


def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
