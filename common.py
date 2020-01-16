"""Common file."""

# Utils
import yaml

__config = None


def config():
    """Get initial config."""
    global __config
    if not __config:
        with open('config.yml', mode='r') as file:
            __config = yaml.load(file)

    return __config
