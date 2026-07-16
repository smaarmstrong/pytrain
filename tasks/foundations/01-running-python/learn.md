THE IDEA

  Python code runs in one of two places:

    1. A FILE (a "script"): you write lines of code into something.py,
       then hand the whole file to Python:

           python3 something.py

       Python runs the lines top to bottom, prints whatever you asked
       it to print, and exits. Same input, same output, every time.

    2. The REPL (Read-Evaluate-Print Loop): you type `python3` with no
       filename and get a `>>>` prompt. Now it's a conversation — you
       type one line, Python answers immediately, and waits for your
       next line.

  Files are for keeping work; the REPL is for asking quick questions.
  You will use both constantly, so this first lesson is just about
  getting comfortable running things.

---

WHY IT MATTERS

  Every task in this trainer works the same way: you edit a file called
  solution.py, and the trainer runs it. If you can't yet run a file
  yourself and see its output, nothing later makes sense — this is the
  ignition key. And the REPL is the fastest way to answer "what does
  this expression do?" without touching your file at all.

---

RUNNING CODE: print

  A script only shows you what it PRINTS. This is the one function you
  need on day one — print(...) writes its arguments to the screen:

```run
print("hello")
print(2 + 2)
```

  When you press Enter to run that, the trainer saves those two lines
  into a little temporary file and runs it with `python3` — exactly
  what you'll do with your own files. Two lines of code, two lines of
  output.

---

  Anything between the parentheses is evaluated first, then printed.
  So a print line can do real work:

```run
print(6 * 7)
print("six sevens are", 6 * 7)
```

  Note the second line: print takes several values separated by
  commas and prints them with spaces in between. A calculation and its
  label, in one line.

---

  One thing that surprises beginners: in a script, a bare expression
  on its own line is computed and then thrown away. Only print makes
  output:

```run
2 + 2          # computed... and silently discarded
print(2 + 2)   # computed and SHOWN
```

  One line of output, not two. If your script "does nothing", the
  first thing to check is whether you actually printed.

---

THE REPL — the other way to run Python

  The trainer can't type into an interactive prompt for you, so try
  this one in a second terminal. Run:

      python3

  You'll see a banner and the prompt:

      >>>

  Now type an expression and press Enter:

      >>> 2 + 2
      4
      >>> "py" + "train"
      'pytrain'

  Notice: NO print needed. The REPL's whole job is to show you the
  value of whatever you type — that's the "Print" in
  Read-Evaluate-Print Loop. This is the difference from a script,
  where bare expressions vanish.

  To leave the REPL, type:

      >>> exit()

  (or press Ctrl-D). Nothing you did in the REPL is saved — which is
  exactly why it's safe to experiment there.

---

  Use the REPL as your scratchpad while you work through this whole
  trainer. Wondering what `"abc".upper()` returns, or whether `7 / 2`
  gives 3 or 3.5? Don't guess and don't edit your file to find out —
  ask the REPL:

      >>> 7 / 2
      3.5
      >>> 7 // 2
      3

  Ten seconds, no risk, question answered. Then write the real line
  in your file.

---

CHECK IT WORKED

  The task asks for a two-line script:

      hello from pytrain
      the answer is 42

  That's two print calls. For the second line you must COMPUTE the 42
  (say, 6 * 7) and put it into the text — you've seen two ways:

      print("the answer is", 6 * 7)

  or an f-string, which you'll meet properly in the next domain:

      print(f"the answer is {6 * 7}")

  Either is fine — the grader only reads the output. Run your file
  yourself first (`python3 solution.py` from inside its folder, or the
  full path from the repo root), eyeball the two lines, then `check`.

---

GOTCHAS

  - `python3 solution.py` runs a FILE; bare `python3` starts the REPL.
    If you see `>>>` when you expected your script to run, you forgot
    the filename — exit() and try again.
  - Wrong folder: `can't open file 'solution.py'` means the file isn't
    where you are. Give the full path, or `cd` to the workspace folder
    the trainer printed.
  - In a script, no print means no output. In the REPL, values echo by
    themselves. Mixing these two rules up is the classic day-one trip.
  - print("2 + 2") prints the TEXT 2 + 2 — quotes mean "literally these
    characters". Drop the quotes to do arithmetic.
  - Output is compared exactly here: watch for stray spaces and make
    sure it's `the answer is 42`, not `The answer is 42`.
