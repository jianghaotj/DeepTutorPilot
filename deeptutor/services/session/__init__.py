"""
Session Management Module
=========================

Provides the SQLite-backed session store and turn runtime used by the
unified chat surface. ``BaseSessionManager`` remains available for any
internal extensions that still need the shared persistence contract.
"""

from .base_session_manager import BaseSessionManager
from .sqlite_store import SQLiteSessionStore, get_sqlite_session_store
from .turn_runtime import TurnRuntimeManager, get_turn_runtime_manager

__all__ = [
    "BaseSessionManager",
    "SQLiteSessionStore",
    "TurnRuntimeManager",
    "get_sqlite_session_store",
    "get_turn_runtime_manager",
]
