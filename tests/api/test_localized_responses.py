from __future__ import annotations

import asyncio
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient

book_router_mod = importlib.import_module("deeptutor.api.routers.book")
localization_mod = importlib.import_module("deeptutor.api.utils.localization")
main_mod = importlib.import_module("deeptutor.api.main")
question_notebook_mod = importlib.import_module("deeptutor.api.routers.question_notebook")
sessions_mod = importlib.import_module("deeptutor.api.routers.sessions")
system_mod = importlib.import_module("deeptutor.api.routers.system")

from deeptutor.services.session.sqlite_store import SQLiteSessionStore


def _set_ui_language(monkeypatch, language: str) -> None:
    monkeypatch.setattr(
        localization_mod,
        "get_ui_language",
        lambda default="en": language,
    )


def _build_book_app(monkeypatch) -> FastAPI:
    class FakeBookEngine:
        def load_book(self, book_id: str):
            return None

        def load_spine(self, book_id: str):
            return None

        def load_page(self, book_id: str, page_id: str):
            return None

    monkeypatch.setattr(book_router_mod, "get_book_engine", lambda: FakeBookEngine())
    app = FastAPI()
    app.include_router(book_router_mod.router, prefix="/api/v1/book")
    return app


def _build_question_notebook_app(store: SQLiteSessionStore) -> FastAPI:
    app = FastAPI()
    app.include_router(question_notebook_mod.router, prefix="/api/v1/question-notebook")
    app.include_router(sessions_mod.router, prefix="/api/v1/sessions")
    return app


def _build_system_app() -> FastAPI:
    app = FastAPI()
    app.include_router(system_mod.router, prefix="/api/v1/system")
    return app


@pytest.fixture
def store(tmp_path: Path, monkeypatch) -> SQLiteSessionStore:
    instance = SQLiteSessionStore(db_path=tmp_path / "localized-router.db")
    monkeypatch.setattr(
        question_notebook_mod,
        "get_sqlite_session_store",
        lambda: instance,
    )
    monkeypatch.setattr(
        sessions_mod,
        "get_sqlite_session_store",
        lambda: instance,
    )
    return instance


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Session not found"),
        ("zh", "未找到会话"),
    ],
)
def test_localize_known_text_respects_ui_language(monkeypatch, language: str, expected: str) -> None:
    _set_ui_language(monkeypatch, language)
    assert localization_mod.localize_known_text("Session not found") == expected


@pytest.mark.parametrize(
    ("language", "path", "expected_detail"),
    [
        ("en", "/api/v1/book/books/missing", "Book not found"),
        ("zh", "/api/v1/book/books/missing", "未找到书籍"),
        ("en", "/api/v1/book/books/missing/spine", "Spine not found"),
        ("zh", "/api/v1/book/books/missing/spine", "未找到章节骨架"),
        ("en", "/api/v1/book/books/missing/pages/page-1", "Page not found"),
        ("zh", "/api/v1/book/books/missing/pages/page-1", "未找到页面"),
    ],
)
def test_book_router_localizes_missing_resources(
    monkeypatch,
    language: str,
    path: str,
    expected_detail: str,
) -> None:
    _set_ui_language(monkeypatch, language)
    with TestClient(_build_book_app(monkeypatch)) as client:
        response = client.get(path)
    assert response.status_code == 404
    assert response.json()["detail"] == expected_detail


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Entry not found"),
        ("zh", "未找到条目"),
    ],
)
def test_question_notebook_localizes_missing_entry(
    monkeypatch,
    store: SQLiteSessionStore,
    language: str,
    expected: str,
) -> None:
    _set_ui_language(monkeypatch, language)
    with TestClient(_build_question_notebook_app(store)) as client:
        response = client.get("/api/v1/question-notebook/entries/999")
    assert response.status_code == 404
    assert response.json()["detail"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Session not found"),
        ("zh", "未找到会话"),
    ],
)
def test_sessions_router_localizes_missing_session(
    monkeypatch,
    store: SQLiteSessionStore,
    language: str,
    expected: str,
) -> None:
    _set_ui_language(monkeypatch, language)
    with TestClient(_build_question_notebook_app(store)) as client:
        response = client.get("/api/v1/sessions/missing")
    assert response.status_code == 404
    assert response.json()["detail"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Quiz results are required"),
        ("zh", "必须提供测验结果"),
    ],
)
def test_sessions_router_localizes_quiz_results_required(
    monkeypatch,
    store: SQLiteSessionStore,
    language: str,
    expected: str,
) -> None:
    session = asyncio.run(store.create_session(title="Quiz session"))
    _set_ui_language(monkeypatch, language)
    with TestClient(_build_question_notebook_app(store)) as client:
        response = client.post(
            f"/api/v1/sessions/{session['id']}/quiz-results",
            json={"answers": []},
        )
    assert response.status_code == 400
    assert response.json()["detail"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Output not found"),
        ("zh", "输出内容不存在"),
    ],
)
def test_outputs_mount_localizes_not_found(monkeypatch, tmp_path: Path, language: str, expected: str) -> None:
    class FakePathService:
        @staticmethod
        def is_public_output_path(path: str) -> bool:
            return False

    _set_ui_language(monkeypatch, language)
    outputs_dir = tmp_path / "outputs"
    outputs_dir.mkdir()

    app = FastAPI()
    app.mount(
        "/api/outputs",
        main_mod.SafeOutputStaticFiles(
            directory=str(outputs_dir),
            path_service=FakePathService(),
        ),
        name="outputs",
    )

    with TestClient(app) as client:
        response = client.get("/api/outputs/private.txt")
    assert response.status_code == 404
    assert response.json()["detail"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "LLM connection successful"),
        ("zh", "LLM 连接成功"),
    ],
)
def test_system_llm_success_message_localized(monkeypatch, language: str, expected: str) -> None:
    async def fake_complete(**kwargs):
        return "OK"

    _set_ui_language(monkeypatch, language)
    monkeypatch.setattr(
        system_mod,
        "get_llm_config",
        lambda: SimpleNamespace(
            model="gpt-test",
            base_url="https://example.test/v1",
            api_key="sk-test",
            binding="openai",
        ),
    )
    monkeypatch.setattr(system_mod, "get_token_limit_kwargs", lambda model, max_tokens=200: {})
    monkeypatch.setattr(system_mod, "llm_complete", fake_complete)

    with TestClient(_build_system_app()) as client:
        response = client.post("/api/v1/system/test/llm")
    assert response.status_code == 200
    assert response.json()["message"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "LLM connection failed: Empty response"),
        ("zh", "LLM 连接失败：返回为空"),
    ],
)
def test_system_llm_empty_message_localized(monkeypatch, language: str, expected: str) -> None:
    async def fake_complete(**kwargs):
        return "   "

    _set_ui_language(monkeypatch, language)
    monkeypatch.setattr(
        system_mod,
        "get_llm_config",
        lambda: SimpleNamespace(
            model="gpt-test",
            base_url="https://example.test/v1",
            api_key="sk-test",
            binding="openai",
        ),
    )
    monkeypatch.setattr(system_mod, "get_token_limit_kwargs", lambda model, max_tokens=200: {})
    monkeypatch.setattr(system_mod, "llm_complete", fake_complete)

    with TestClient(_build_system_app()) as client:
        response = client.post("/api/v1/system/test/llm")
    assert response.status_code == 200
    assert response.json()["message"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Embeddings connection successful (test-provider provider)"),
        ("zh", "Embeddings 连接成功（test-provider 提供方）"),
    ],
)
def test_system_embeddings_success_message_localized(
    monkeypatch,
    language: str,
    expected: str,
) -> None:
    class FakeEmbeddingClient:
        async def embed(self, texts):
            return [[0.1, 0.2]]

    _set_ui_language(monkeypatch, language)
    monkeypatch.setattr(
        system_mod,
        "get_embedding_config",
        lambda: SimpleNamespace(model="embed-test", binding="test-provider"),
    )
    monkeypatch.setattr(system_mod, "get_embedding_client", lambda: FakeEmbeddingClient())

    with TestClient(_build_system_app()) as client:
        response = client.post("/api/v1/system/test/embeddings")
    assert response.status_code == 200
    assert response.json()["message"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Embeddings connection failed: Empty response"),
        ("zh", "Embeddings 连接失败：返回为空"),
    ],
)
def test_system_embeddings_empty_message_localized(
    monkeypatch,
    language: str,
    expected: str,
) -> None:
    class FakeEmbeddingClient:
        async def embed(self, texts):
            return [[]]

    _set_ui_language(monkeypatch, language)
    monkeypatch.setattr(
        system_mod,
        "get_embedding_config",
        lambda: SimpleNamespace(model="embed-test", binding="test-provider"),
    )
    monkeypatch.setattr(system_mod, "get_embedding_client", lambda: FakeEmbeddingClient())

    with TestClient(_build_system_app()) as client:
        response = client.post("/api/v1/system/test/embeddings")
    assert response.status_code == 200
    assert response.json()["message"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Search connection successful"),
        ("zh", "搜索连接成功"),
    ],
)
def test_system_search_success_message_localized(monkeypatch, language: str, expected: str) -> None:
    _set_ui_language(monkeypatch, language)
    monkeypatch.setattr(
        system_mod,
        "resolve_search_runtime_config",
        lambda: SimpleNamespace(
            requested_provider="brave",
            provider="brave",
            unsupported_provider=False,
            deprecated_provider=False,
            missing_credentials=False,
            fallback_reason=None,
        ),
    )
    monkeypatch.setattr(system_mod, "web_search", lambda *args, **kwargs: {"answer": "ok"})

    with TestClient(_build_system_app()) as client:
        response = client.post("/api/v1/system/test/search")
    assert response.status_code == 200
    assert response.json()["message"] == expected


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en", "Search not configured"),
        ("zh", "未配置搜索"),
    ],
)
def test_system_search_not_configured_message_localized(
    monkeypatch,
    language: str,
    expected: str,
) -> None:
    _set_ui_language(monkeypatch, language)
    monkeypatch.setattr(
        system_mod,
        "resolve_search_runtime_config",
        lambda: SimpleNamespace(
            requested_provider=None,
            provider=None,
            unsupported_provider=False,
            deprecated_provider=False,
            missing_credentials=False,
            fallback_reason=None,
        ),
    )

    with TestClient(_build_system_app()) as client:
        response = client.post("/api/v1/system/test/search")
    assert response.status_code == 200
    assert response.json()["message"] == expected
