def run_code(code):
    """Run python -c `code`; return (stdout, stderr, returncode) as text."""
    raise NotImplementedError


def checked_output(code):
    """Stdout of python -c `code`; CalledProcessError on non-zero exit."""
    raise NotImplementedError


def pipeline(code1, code2):
    """Feed code1's stdout into code2's stdin; return code2's stdout."""
    raise NotImplementedError
