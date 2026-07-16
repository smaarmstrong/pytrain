THE IDEA

  Every time you run `check`, this trainer grades you with a tool
  called PYTEST — the standard Python testing tool. A test is nothing
  mysterious: it is an ordinary function whose name starts with test_,
  full of ASSERT statements:

      def test_greeting():
          assert greet("Bo") == "Hello, Bo!"

  `assert EXPRESSION` means: "I claim this is true." If it is, nothing
  happens and the next line runs. If it isn't, it raises an
  AssertionError — and the test FAILS. That's the entire mechanism.

  pytest's job is just bookkeeping: find files named test_*.py, run
  every test_ function inside, and report which asserted claims held.

---

WHY IT MATTERS

  You are going to read pytest output on every single task in this
  trainer — `check` runs a file called test_grade.py against your
  solution and shows you the report. If you can read that report, every
  failure tells you exactly which claim about your code was false, and
  with what values. If you can't, it's just red noise. Ten minutes here
  pays off for the next hundred tasks. (And writing tests is how real
  codebases stay honest — the `testing` domain digs deeper later.)

---

ASSERT — the one keyword

  Try the two faces of assert. A TRUE claim is silent; a FALSE one
  raises:

```run
assert 2 + 2 == 4
print("that one was fine — silence means the claim held")

assert 2 + 2 == 5, "arithmetic is broken?!"
print("this line never runs")
```

  Read the traceback the way the last lesson taught you: bottom line
  says AssertionError (plus our message), the line above shows exactly
  which claim failed. The first assert made no noise at all — passing
  tests are quiet.

---

  The optional part after the comma is the failure message. Plain
  `assert x == y` is usually enough — you'll see why in a moment:
  pytest shows you the values itself.

  One more pattern you need — asserting that something RAISES. You
  can't write `assert divide(1, 0) raises ZeroDivisionError`; instead
  you spring the trap on purpose and catch it:

```run
def divide(a, b):
    return a / b

try:
    divide(1, 0)
    assert False, "expected ZeroDivisionError"
except ZeroDivisionError:
    print("good — it raised, exactly as it should")
```

  Read it slowly: if divide(1, 0) raises ZeroDivisionError we jump to
  the except branch — the claim held. If it *returns* instead, the
  next line `assert False` fails the test. Wrong-way-round errors
  can't sneak through. (pytest has a shortcut for this, pytest.raises
  — you'll meet it in the testing domain; the try/except spells out
  what it does.)

---

HOW PYTEST RUNS THEM

  In a project you'd write test functions in a file like test_shop.py
  and run, in the terminal:

      pytest test_shop.py

  pytest imports the file, calls every function named test_*, and
  prints a report. A pass looks like:

      test_shop.py .                                    [100%]
      ========== 1 passed in 0.01s ==========

  One quiet dot per passing test. A failure is louder — and this is
  the part worth learning to read:

      test_shop.py F                                    [100%]
      =================== FAILURES ===================
      _________________ test_greeting ________________

          def test_greeting():
      >       assert greet("Bo") == "Hello, Bo"
      E       AssertionError: assert 'Hello, Bo!' == 'Hello, Bo'
      E         - Hello, Bo
      E         + Hello, Bo!

      ========== 1 failed, 1 passed in 0.02s ==========

  Three markers do all the work:

      _____   which TEST failed (test_greeting)
      >       the exact line that failed
      E       the evidence: both sides of the ==, actually evaluated —
              here greet really returned 'Hello, Bo!' and the - / +
              lines diff the two strings (the ! is the difference)

  That's why plain asserts are enough: pytest rewrites them so the
  report shows the real values on each side. You don't add print
  statements to a test — the E lines already show the data.

---

  You don't need to install or run pytest yourself for this trainer —
  `check` does it for you, in an isolated environment, pointing pytest
  at the task's test_grade.py and YOUR solution file. So the loop on
  every task is:

      edit solution.py  ->  check  ->  read the FAILURES block
      (which test? which line? what did E say the values were?)
      ->  fix  ->  check again

  A grader failure is never an insult — it is a claim about your code,
  with evidence attached.

---

CHECK IT WORKED

  The task has you build both halves of the contract:

    - divide(a, b): just `a / b`. Don't catch anything — `/` already
      raises ZeroDivisionError on b == 0, and that behaviour is wanted.
    - test_divide(): plain asserts for divide(10, 2) == 5.0 and
      divide(1, 4) == 0.25, then the try/except pattern from above to
      claim divide(1, 0) raises ZeroDivisionError.

  The grader runs your test_divide against your correct divide (must
  pass silently) — and then secretly swaps in broken divides and runs
  your test again: it must FAIL then. A test that asserts nothing
  real won't survive that.

---

GOTCHAS

  - assert greet("Bo") — with no comparison — only checks the result
    is truthy. Assert the actual expected value: == "Hello, Bo!".
  - Never wrap asserts in try/except AssertionError "to be safe" —
    that eats the failure and the test lies. The ONLY try/except in a
    test is the expected-exception pattern, catching the specific
    error you want raised.
  - A test that calls nothing (assert True, or asserting constants)
    passes against anything — including broken code. Every assert
    should exercise the function under test. The grader here checks
    exactly that.
  - Test functions take no arguments and return nothing; they
    communicate only by raising (or not). Don't `return True`.
  - In the report, read the E lines before touching code — they show
    what the values actually WERE. Half of all "impossible" failures
    dissolve right there.
