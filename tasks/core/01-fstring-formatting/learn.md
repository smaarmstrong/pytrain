THE IDEA

  An f-string is a normal string with the letter f stuck on the front:

      name = "Bo"
      f"hi {name}"        ->  "hi Bo"

  Anything you put inside the curly braces { } is ordinary Python: it gets
  evaluated, and its result is dropped into the text. Without the f, the
  braces are just literal characters — the f is what turns them on.

---

  Let's see that. This prints a greeting built from a variable:

```run
name = "Bo"
print(f"hi {name}")
```

  The value of `name` replaced `{name}`. That is the whole basic idea; the
  rest of this lesson is about controlling *how* a value is written out.

---

WHY IT MATTERS

  Almost every program has to turn numbers and values into text a human
  reads: prices, percentages, table columns, log lines. Doing that by hand
  (rounding, padding with spaces, adding thousands commas) is fiddly and
  error-prone. f-strings have a tiny built-in "format spec" language that
  does all of it for you — once you can read it, this whole task is four
  one-liners.

---

THE FORMAT SPEC

  Inside the braces you can add a colon, then instructions:

      f"{value:SPEC}"

  The SPEC is read in this order (every part is optional):

      align   <  left     >  right     ^  centre
      width   a number — the minimum number of characters to fill to
      ,       group thousands with commas   (1234 -> 1,234)
      .Nf     show a float with exactly N decimal places
      .N%     multiply by 100 and add a % sign, N decimals

  You only write the parts you need, in that order. Let's try each.

---

  Alignment and width. We pad a word into a field 12 characters wide, left
  then right, wrapping in | pipes so you can see the spaces:

```run
print(f"|{'tea':<12}|")     # left-aligned in 12
print(f"|{'tea':>12}|")     # right-aligned in 12
```

  `<12` means "at least 12 wide, text on the left". `>12` pushes it right.

---

  Numbers: commas for thousands, and a fixed number of decimals.

```run
print(f"{1234.5:,.2f}")     # comma groups + exactly 2 decimals
print(f"{3.5:>8,.2f}")      # ...also right-aligned in a field of 8
```

  Read that second one left to right: right-align (`>`), width 8, group
  thousands (`,`), 2 decimal places (`.2f`). That is exactly what
  `receipt_line` needs for the price.

---

  Percentages. The `%` spec multiplies by 100 and appends the sign, so you
  hand it the fraction, not the number:

```run
print(f"{0.256:.1%}")       # -> 25.6%
print(f"{1.0:.1%}")         # -> 100.0%
```

---

  Two more small tricks the task uses.

  `!r` asks for the *repr* of a value — how Python would show it in code, so
  a string keeps its quotes. Compare:

```run
value = "bo"
print(f"{value}")           # bo      (plain text)
print(f"{value!r}")         # 'bo'    (repr — quotes kept)
```

  And quotes-inside-quotes: if the text you want contains ", wrap the whole
  f-string in ' single quotes (or vice versa) so they don't clash:

```run
nickname = "Ace"
print(f'is called "{nickname}"')
```

---

CHECK IT WORKED

  That is everything the four functions need:

    receipt_line  ->  f"{item:<12}£{price:>8,.2f}"
    percent       ->  f"{fraction:.1%}"
    debug_line    ->  f"{name}={value!r}"
    quoted        ->  wrap in single quotes, put "{nickname}" inside

  The grader just calls each function and compares the exact string, so the
  widths and decimals have to match the spec precisely.

---

GOTCHAS

  - Don't forget the leading f. "hi {name}" (no f) prints the braces
    literally — a very common first mistake.
  - `.2f` always shows 2 decimals (1.5 -> "1.50"); plain `.2` without the f
    means something different. Include the f for money.
  - The percent spec expects a fraction: 0.5 gives "50.0%", not 50 giving
    "5000.0%". Pass the raw fraction straight in.
  - `!r` vs plain: debug_line wants repr, so numbers stay bare (42) but
    strings gain quotes ('bo'). That is the point of the `=` debug style.
