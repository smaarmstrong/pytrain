import importlib.metadata


def installed_version(package):
    """Version string of `package` in this environment, or None if absent."""
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return None
