def find_files(root, pattern):
    """Relative posix paths of files under root matching the glob pattern."""
    raise NotImplementedError


def total_size(root):
    """Total bytes of all files under root, recursively."""
    raise NotImplementedError


def backup_path(path):
    """Path arithmetic only: sibling path with '.bak' appended to the name."""
    raise NotImplementedError


def concat_texts(root, out_path):
    """Concatenate all *.txt under root (sorted) into out_path; return the text."""
    raise NotImplementedError
