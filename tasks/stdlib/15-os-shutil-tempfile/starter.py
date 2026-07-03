def env_flag(name):
    """True iff env var `name` is a truthy flag ('1', 'true', 'yes', 'on')."""
    raise NotImplementedError


def copy_tree_filtered(src, dst, suffix):
    """Copy the tree, keeping only files ending with suffix; return the count."""
    raise NotImplementedError


def with_temp_dir(fn):
    """Run fn(temp_dir_path); always clean up; return fn's result."""
    raise NotImplementedError
