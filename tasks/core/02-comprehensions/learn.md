THE IDEA

  A "comprehension" is a compact way to build a new list (or dict, or set)
  by looping over something. It is just a for-loop turned inside out.

  The long way to square some numbers:

      result = []
      for n in [1, 2, 3]:
          result.append(n * n)

  The comprehension way — same result, one line:

      result = [n * n for n in [1, 2, 3]]

  Read it left to right in plain English: "n times n, for each n in the
  list". The square brackets [ ] mean the answer is a list.

---

  Run both and see they agree:

```run
long = []
for n in [1, 2, 3]:
    long.append(n * n)

short = [n * n for n in [1, 2, 3]]

print(long)
print(short)
```

  Identical. The comprehension is just the loop's shape rearranged:
  what-you-collect first, then the for.

---

WHY IT MATTERS

  "Take a collection, transform each item, maybe drop some" is one of the
  most common things code does. Comprehensions say that in one readable line
  instead of four, and Python programmers expect to see them — reading them
  fluently is a basic literacy skill for the language.

---

FILTERING: add an `if`

  Put an `if` on the end to keep only some items. Here, only the even ones
  (a number is even when the remainder after dividing by 2 is zero, written
  `n % 2 == 0` — `%` gives the remainder):

```run
evens = [n for n in range(6) if n % 2 == 0]
print(evens)                       # [0, 2, 4]

squares_of_evens = [n * n for n in range(6) if n % 2 == 0]
print(squares_of_evens)            # [0, 4, 16]
```

  The `if` at the end decides whether an item is included at all. That is
  the whole of `squares_of_evens`.

---

CHOOSING per item: an `if/else` in FRONT

  A filter (`if` at the end) drops items. If instead you want to pick a
  *value* for every item, put a conditional expression at the front:

```run
labels = ["even" if n % 2 == 0 else "odd" for n in [1, 2, 3, 4]]
print(labels)                      # ['odd', 'even', 'odd', 'even']
```

  Note the difference: `if` at the END filters; `if ... else ...` at the
  FRONT chooses a value and keeps every item. `parity_labels` is the second
  kind.

---

DICTS and SETS: swap the brackets

  Use curly braces to build a dict (with a key: value) or a set:

```run
words = ["Hi", "there", "HI"]
lengths = {w.lower(): len(w) for w in words if w}
print(lengths)                     # {'hi': 2, 'there': 5}

initials = {name[0].upper() for name in ["ada", "Alan", ""] if name}
print(initials)                    # {'A'}
```

  For the dict, `w.lower()` is the key and `len(w)` is the value; the
  `if w` skips empty strings (an empty string is "falsy"). If two words
  produce the same key, the later one wins — that is normal dict behaviour.
  The set version keeps only distinct values automatically.

---

NESTED loops: two `for`s, left to right

  To flatten a list-of-lists, use two fors in the SAME order you'd nest
  them in a normal loop — outer first, inner second:

```run
matrix = [[1, 2], [3], []]
flat = [x for row in matrix for x in row]
print(flat)                        # [1, 2, 3]
```

  Reads as: "for each row in matrix, for each x in that row, collect x".
  The empty row simply contributes nothing.

---

CHECK IT WORKED

  You now have all five shapes this task needs:

    squares_of_evens  ->  [n*n for n in nums if n % 2 == 0]
    word_lengths      ->  {w.lower(): len(w) for w in words if w}
    distinct_initials ->  {name[0].upper() for name in names if name}
    flatten_matrix    ->  [x for row in matrix for x in row]
    parity_labels     ->  ["even" if n % 2 == 0 else "odd" for n in nums]

  The grader checks results and that you don't mutate the input — a
  comprehension always builds a brand-new collection, so that's free.

---

GOTCHAS

  - Filter vs choose: `[x for x in xs if cond]` drops items;
    `[a if cond else b for x in xs]` keeps every item and picks a value.
    Mixing them up is the classic slip.
  - Nested-for order matches a normal nested loop: outer for first.
  - Brackets pick the type: [ ] list, { } with `key: value` dict, { } with
    a single value set. `{}` alone is an empty dict, not a set.
  - A comprehension makes a new object; it never changes the thing you
    looped over, which is exactly what the "don't mutate" rule wants.
