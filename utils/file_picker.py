import os
import sys


def get_resource_path(relative_path):
    """Get the path to the resource file."""
    if hasattr(sys, '_MEIPASS'):
        # When running in the PyInstaller binary
        return os.path.join(sys._MEIPASS, relative_path)
    # When running in a normal Python environment
    return os.path.join(os.path.abspath("."), relative_path)