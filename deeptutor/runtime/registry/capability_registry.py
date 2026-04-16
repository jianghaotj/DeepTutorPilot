"""Capability registry for the unified runtime."""

from __future__ import annotations

import importlib
import logging
from typing import Any

from deeptutor.core.capability_protocol import BaseCapability
from deeptutor.runtime.bootstrap.builtin_capabilities import BUILTIN_CAPABILITY_CLASSES

logger = logging.getLogger(__name__)


def _import_capability_class(path: str) -> type[BaseCapability]:
    module_path, class_name = path.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class CapabilityRegistry:
    """Registry of available capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[str, BaseCapability] = {}

    def register(self, capability: BaseCapability) -> None:
        self._capabilities[capability.name] = capability

    def load_builtins(self) -> None:
        for name, class_path in BUILTIN_CAPABILITY_CLASSES.items():
            if name in self._capabilities:
                continue
            try:
                cls = _import_capability_class(class_path)
                self.register(cls())
            except Exception:
                logger.warning("Failed to load capability %s", name, exc_info=True)

    def load_plugins(self) -> None:
        """Legacy hook retained as a no-op while the runtime is built-in only."""
        return

    def get(self, name: str) -> BaseCapability | None:
        return self._capabilities.get(name)

    def list_capabilities(self) -> list[str]:
        return list(self._capabilities.keys())

    def get_manifests(self) -> list[dict[str, Any]]:
        return [
            {
                "name": c.manifest.name,
                "description": c.manifest.description,
                "stages": c.manifest.stages,
                "tools_used": c.manifest.tools_used,
                "cli_aliases": c.manifest.cli_aliases,
                "request_schema": c.manifest.request_schema,
                "config_defaults": c.manifest.config_defaults,
            }
            for c in self._capabilities.values()
        ]


_default_registry: CapabilityRegistry | None = None


def get_capability_registry() -> CapabilityRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = CapabilityRegistry()
        _default_registry.load_builtins()
        _default_registry.load_plugins()
    return _default_registry
