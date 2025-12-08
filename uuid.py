"""
Custom UUID module workaround for Streamlit Cloud compatibility.
This helps prevent potential threading issues with the standard uuid library on the platform.
"""

import random
import string

def uuid4():
    """Generates a pseudo-random UUID-like string."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(32))

class UUID:
    """Mock UUID class."""
    def __init__(self, hex):
        self.hex = hex

    def __str__(self):
        return self.hex

def uuid5(namespace, name):
    """Generates a pseudo-random UUID-like string, ignoring namespace."""
    # This is not a real UUID5, but it provides a compatible interface for the app.
    return UUID(uuid4())
