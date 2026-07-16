def installed_version(package):
    """Version string of `package` in this environment, or None if absent.

    Hint: importlib.metadata.version raises PackageNotFoundError for
    packages that aren't installed.
    """
    raise NotImplementedError
