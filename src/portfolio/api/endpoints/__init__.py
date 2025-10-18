"""API endpoints module.

Exports health router.
"""
from .health import router as health_router

__all__ = ["health_router"]
