def register(name):
    """Decorator factory: @register("csv") registers the class under "csv"
    and returns the class unchanged. Duplicate names raise ValueError."""
    raise NotImplementedError


def create(name, *args, **kwargs):
    """Instantiate the class registered under `name`, forwarding arguments.
    Unknown names raise ValueError."""
    raise NotImplementedError


def registered_names():
    """Sorted list of all registered names."""
    raise NotImplementedError
