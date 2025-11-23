"""
MkDocs Macro Plugin Entry Point

This module serves as the entry point for MkDocs macro registration.
It delegates to the actual implementation in onestep-static/main.py.

Note: This file exists at the root level for MkDocs compatibility.
The actual implementation is in onestep-static/main.py.
"""

from onestep_static.main import define_env

__all__ = ['define_env']
