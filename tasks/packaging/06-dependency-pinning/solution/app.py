"""Your application (context only — the task is constraints.txt).

In production this app does:

    import spanner   # needs the tighten_ex() API added in spanner 1.5
    import gearbox   # needs gearbox >= 1.5; gearbox 2.0 is critically buggy

The packages are fictional; nothing is installed in this task.
"""


def main():
    print("imagine: spanner.tighten_ex() + gearbox.shift()")


if __name__ == "__main__":
    main()
