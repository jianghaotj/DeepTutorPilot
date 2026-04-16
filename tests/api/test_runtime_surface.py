from __future__ import annotations

from types import SimpleNamespace

import pytest

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient


def test_plugins_list_keeps_shape_and_reports_no_dynamic_plugins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from deeptutor.api.routers import plugins_api

    fake_tool = SimpleNamespace(
        name="rag",
        description="Retrieve from KB",
        parameters=[
            SimpleNamespace(
                name="query",
                type="string",
                description="Search query",
                required=True,
                default=None,
                enum=None,
            )
        ],
    )
    fake_tool_registry = SimpleNamespace(get_definitions=lambda: [fake_tool])
    fake_capability_registry = SimpleNamespace(
        get_manifests=lambda: [
            {
                "name": "chat",
                "description": "Agentic chat",
                "stages": ["thinking", "acting", "observing", "responding"],
                "tools_used": ["rag"],
                "cli_aliases": ["chat"],
                "request_schema": None,
                "config_defaults": {},
            }
        ]
    )

    monkeypatch.setattr(plugins_api, "get_tool_registry", lambda: fake_tool_registry)
    monkeypatch.setattr(plugins_api, "get_capability_registry", lambda: fake_capability_registry)

    app = FastAPI()
    app.include_router(plugins_api.router, prefix="/api/v1/plugins")

    with TestClient(app) as client:
        response = client.get("/api/v1/plugins/list")

    assert response.status_code == 200
    payload = response.json()
    assert payload["tools"][0]["name"] == "rag"
    assert payload["capabilities"][0]["name"] == "chat"
    assert payload["plugins"] == []


def test_runtime_topology_reports_unified_runtime_without_legacy_routes() -> None:
    from deeptutor.api.routers import system

    app = FastAPI()
    app.include_router(system.router, prefix="/api/v1/system")

    with TestClient(app) as client:
        response = client.get("/api/v1/system/runtime-topology")

    assert response.status_code == 200
    payload = response.json()
    assert payload["primary_runtime"]["transport"] == "/api/v1/ws"
    assert payload["compatibility_routes"] == []
    assert payload["isolated_subsystems"] == [
        {"router": "guide", "mode": "independent_subsystem"},
        {"router": "co_writer", "mode": "independent_subsystem"},
        {"router": "plugins_api", "mode": "playground_transport"},
    ]
