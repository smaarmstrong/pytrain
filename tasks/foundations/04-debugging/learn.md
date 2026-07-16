THE IDEA

  The last lesson's bugs announced themselves with a traceback. The
  nastier kind doesn't: the program runs to the end and simply gives
  the WRONG ANSWER. No error, no line number — just a result you know
  is false.

  For those you need to see inside the program while it runs. Two
  tools, in the order you should learn them:

    1. PRINT-DEBUGGING: add temporary print(...) lines to watch a
       variable change. Crude, universal, and what most working
       programmers actually reach for first.
    2. THE DEBUGGER (pdb): put breakpoint() in your code and Python
       pauses the program THERE, alive, and lets you inspect it and
       step forward one line at a time.

  Both answer the same question: "what are the values REALLY, at this
  moment?" — because every wrong answer is a variable holding
  something you didn't expect, somewhere.

---

WHY IT MATTERS

  Staring at code and re-reading your own assumption ("this must be
  right...") is how beginners lose hours. Debugging replaces guessing
  with looking: you find the exact loop iteration where reality parts
  company with your expectation, and the bug is standing right there.
  Every failing `check` in this trainer becomes a five-minute job once
  observing values is a reflex.

---

PRINT-DEBUGGING, HONESTLY

  Here's a function that should sum as it goes — running_total([1, 2,
  3]) should give [1, 3, 6] — but doesn't. Watch it fail:

```run
def running_total(nums):
    totals = []
    total = 0
    for n in nums:
        total = n
        totals.append(total)
    return totals

print(running_total([1, 2, 3]))   # want [1, 3, 6]
```

  Wrong, but no crash. So: put a print INSIDE the loop and watch
  `total` evolve. The neatest way is an f-string with `=` after the
  variable name — f"{total=}" prints both the name and the value:

```run
def running_total(nums):
    totals = []
    total = 0
    for n in nums:
        total = n
        print(f"  {n=} {total=}")     # temporary spy line
        totals.append(total)
    return totals

print(running_total([1, 2, 3]))
```

  Read the spy lines: after seeing n=2, total is 2 — but the sum so
  far should be 3. THAT is the moment expectation and reality split,
  and it points straight at the line above the print: `total = n`
  replaces the total instead of adding to it. `total += n` is the fix.

  The discipline that makes this honest debugging rather than mess:

    - print names WITH values (f"{x=}"), not bare mystery numbers
    - put the print where the value CHANGES (inside the loop)
    - once fixed, DELETE the spy lines — they're scaffolding

---

THE DEBUGGER: breakpoint()

  Prints answer one question per run. The debugger answers as many as
  you like, live. Write breakpoint() on the line where you want to
  stop; when Python reaches it, the program FREEZES there and you get
  a (Pdb) prompt inside the running program.

  You drive it with one-letter commands:

      p expr    print the value of any expression (p total, p nums)
      n         next — run the current line, pause on the next one
      s         step — like n, but steps INTO a function call
      c         continue running until the next breakpoint (or the end)
      q         quit — abandon the run entirely

  That's the whole survival kit: p to look, n to walk, c to run on,
  q to bail out.

---

  The next snippet has a real breakpoint() in it, so when you run it
  the (Pdb) prompt is YOURS — the lesson hands you the controls. A
  good first flight, typed one at a time at the (Pdb) prompt:

      p total     (what's the total before this iteration?)
      p n         (and the incoming value?)
      n           (run one line — the buggy total = n)
      p total     (look again: it REPLACED, not added)
      c           (let it finish)

  Then it pauses again on the loop's next pass — inspect once more, or
  just c through to the end. Remember q abandons ship if you get lost.

```run
def running_total(nums):
    totals = []
    total = 0
    for n in nums:
        breakpoint()          # pauses HERE, every pass of the loop
        total = n
        totals.append(total)
    return totals

print(running_total([1, 2, 3]))
```

  What you just did — pausing a live program and interrogating its
  variables — is the same skill whether it's three lines or three
  hundred thousand. (breakpoint() drops you into pdb, Python's
  built-in debugger; fancier IDE debuggers are the same idea with
  buttons.)

---

  When to reach for which:

    - Quick suspicion, one variable?  A print(f"{x=}") is faster.
    - Loop with many iterations, or you don't know WHAT to look at
      yet?  breakpoint() — you can poke at everything while paused.
    - Either way, remove them when done. A leftover breakpoint() will
      freeze your program (and a grader) waiting for input; a leftover
      print pollutes output. Both are scaffolding, never furniture.

---

CHECK IT WORKED

  The task gives you two quietly-wrong functions:

    - running_total — the very bug you just hunted. You know its
      shape now; find the line and fix it.
    - count_vowels("debug") says 3 instead of 2 — it counts exactly
      the wrong letters. Spy on ch inside the loop (f"{ch=}") or pause
      with breakpoint() and `p ch` — watch WHICH characters make the
      count go up, and the one-character fix reveals itself.

  Run `python3 solution.py` while you work — the demo lines at the
  bottom print both answers next to what they should be. Fix, observe,
  confirm, then strip your spy lines and `check`.

---

GOTCHAS

  - Print the NAME with the value — f"{total=}" — or ten anonymous
    numbers later you won't know which spy said what.
  - A leftover breakpoint() halts anything that runs your file,
    including this trainer's grader, until the input times out. Search
    your file for "breakpoint" before you `check`.
  - Debug with the SMALLEST failing input ([1, 2, 3], not a
    500-element list) — three loop passes are readable, five hundred
    are not.
  - At the (Pdb) prompt, a bare variable name usually works, but `p x`
    is the reliable spelling (bare `c`, `n`, `s`, `q` are COMMANDS —
    to inspect a variable actually named n, you must write `p n`).
  - Fix the bug where the value goes wrong, not where you noticed it.
    The wrong return value was manufactured earlier, inside the loop —
    that's why the spy goes there.
