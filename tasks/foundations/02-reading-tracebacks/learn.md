THE IDEA

  When Python hits something it cannot do, it stops and prints a
  TRACEBACK — a report of what went wrong and exactly where. It looks
  alarming. It is actually the most helpful error report you'll ever
  get, once you know the reading order:

      READ IT BOTTOM-UP.

  The LAST line names the problem:

      NameError: name 'nmae' is not defined
      ^--------  ^-------------------------
      the TYPE   the MESSAGE (plain English!)

  The line(s) just above it tell you WHERE:

      File "shop.py", line 3, in greet
        return "Hello, " + nmae + "!"

  File, line number, function — and the offending line quoted. That's
  the whole skill: last line says WHAT, the line above says WHERE.

---

WHY IT MATTERS

  Beginners see a wall of red and start guessing. Programmers read the
  last line and go straight to the named file and line. It's the single
  highest-leverage habit in learning Python — every bug you'll ever
  write introduces itself this way, and this trainer's graders speak
  traceback too. Learn to read them now and every later task gets
  easier.

---

A REAL CRASH, ON PURPOSE

  Let's cause one. This code has a typo — `nmae` for `name`:

```run
def greet(name):
    return "Hello, " + nmae + "!"

print(greet("Bo"))
```

  Read what just printed, bottom-up:

    - Bottom line: `NameError: name 'nmae' is not defined`. Python is
      telling you, in English, that you used a variable that doesn't
      exist. That is WHAT went wrong.
    - Above it: `File ...lesson_snippet.py, line 2, in greet` plus the
      quoted line. That is WHERE — line 2, inside greet.

  Fix the typo and the same code just works:

```run
def greet(name):
    return "Hello, " + name + "!"

print(greet("Bo"))
```

---

WHY BOTTOM-UP? THE CALL CHAIN

  When function A calls B and B crashes, the traceback shows the whole
  chain, one frame per call, OLDEST AT THE TOP:

```run
def top(order):
    return middle(order)

def middle(order):
    return "total: " + order["total"]   # order has no "total" key

top({"item": "tea"})
```

  Read it bottom-up:

    - Last line: `KeyError: 'total'` — a dictionary was asked for a
      key it doesn't have.
    - One up: the crash happened in `middle`, at the quoted line.
    - One more up: `middle` was called from `top`. That's the header
      "Traceback (most recent call last)" — the most recent call, the
      one that actually blew up, is printed LAST. Hence: read from the
      bottom.

  The deepest frame is where the error fired; the frames above are how
  the program got there. Usually the fix is in the bottom one or two.

---

THE TYPES YOU'LL MEET FIRST

  Exception types are categories; each has a typical everyday cause.
  Watch each one happen — three tiny crashes in a row (each `try` block
  here catches the error and prints just its type and message, so all
  three fit in one run):

```run
try:
    "age: " + 7
except TypeError as e:
    print("TypeError:", e)

try:
    [3, 1, 4][3]
except IndexError as e:
    print("IndexError:", e)

try:
    int("twelve")
except ValueError as e:
    print("ValueError:", e)
```

    NameError   you used a name that doesn't exist — 90% typos
    TypeError   right idea, wrong TYPE — e.g. gluing text to a number
                with +. Fix: convert first (str(7)) or use an f-string.
    IndexError  asked a list for position it doesn't have. Remember
                positions start at 0, so a 3-item list has 0, 1, 2 —
                its last item is [2] or, better, [-1].
    ValueError  right type, impossible value — int("twelve").
    KeyError    dictionary version of IndexError — no such key.

  You do NOT need to memorise these. The message spells it out every
  time; the names just become familiar.

---

ONE MORE: SyntaxError IS DIFFERENT

  Everything above happened while the code was RUNNING. A SyntaxError
  means Python couldn't even read the file — so nothing ran at all:

```run
print("before")     # never prints!
if True
    print("hi")
```

  No "before" in the output: the whole file was rejected first. The
  `^` marker points at (or just after) the spot Python gave up —
  here a missing `:` at the end of the `if` line. If you ever get a
  SyntaxError, nothing in the file executed; fix the marked line
  before thinking about anything else.

---

CHECK IT WORKED

  The task hands you three functions, each hiding one of the errors
  you just met: a NameError, a TypeError, an IndexError. The workflow
  is exactly what you practised:

    1. Run the file (`python3 solution.py`).
    2. Read the traceback bottom-up: WHAT (last line), WHERE (above).
    3. Go to that line, make the one-line fix, run again.

  The file's demo section calls one function at a time — uncomment the
  next call after each fix. When all three run clean, `check`.

  (The demo lines sit under `if __name__ == "__main__":` — for now,
  read that as "only run this part when the file is executed directly,
  not when the grader imports it". It gets a proper explanation later
  in the course.)

---

GOTCHAS

  - Don't read tracebacks top-down. The top is history; the bottom is
    the news.
  - The quoted line is where the error FIRED, which is usually — not
    always — where the mistake lives. A TypeError inside a function can
    be caused by the caller passing the wrong thing; that's what the
    upper frames are for.
  - Line numbers refer to the file AS IT WAS when you ran it. Edited
    the file? Run it again before trusting the numbers.
  - "unsupported operand type(s) for +: 'int' and 'str'" reads oddly
    but says it plainly: you used + between an int and a str. The
    messages are always literal — trust them.
  - A 3-item list ends at index 2. `items[len(items)]` is ALWAYS one
    past the end — that's the classic off-by-one.
