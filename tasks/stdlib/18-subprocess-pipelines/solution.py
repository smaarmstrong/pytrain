import subprocess
import sys


def _cmd(code):
    return [sys.executable, "-c", code]


def run_code(code):
    proc = subprocess.run(_cmd(code), capture_output=True, text=True)
    return proc.stdout, proc.stderr, proc.returncode


def checked_output(code):
    proc = subprocess.run(_cmd(code), capture_output=True, text=True, check=True)
    return proc.stdout


def pipeline(code1, code2):
    first = subprocess.run(_cmd(code1), capture_output=True, text=True)
    second = subprocess.run(
        _cmd(code2), input=first.stdout, capture_output=True, text=True
    )
    return second.stdout
