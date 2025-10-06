"""Compatibility package for the relocated backend application."""
from importlib import import_module
import sys

_real_module = import_module("apps.backend")

# Replace this module with the relocated backend package so imports keep working.
sys.modules[__name__] = _real_module
