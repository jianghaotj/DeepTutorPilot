"""
Lightweight API-localized fixed strings.

Used for route-layer messages that are shown directly in the UI.
Keeps response shapes unchanged while switching copy based on the current
interface language.
"""

from __future__ import annotations

from fastapi import HTTPException

from deeptutor.services.settings.interface_settings import get_ui_language

_MESSAGES: dict[str, dict[str, str]] = {
    "output_not_found": {"en": "Output not found", "zh": "输出内容不存在"},
    "book_not_found": {"en": "Book not found", "zh": "未找到书籍"},
    "spine_not_found": {"en": "Spine not found", "zh": "未找到章节骨架"},
    "page_not_found": {"en": "Page not found", "zh": "未找到页面"},
    "user_intent_required": {"en": "user_intent is required", "zh": "必须提供 user_intent"},
    "block_not_found": {"en": "Block not found", "zh": "未找到内容块"},
    "page_or_chapter_not_found": {
        "en": "Page or chapter not found",
        "zh": "未找到页面或章节",
    },
    "parent_page_not_found": {"en": "Parent page not found", "zh": "未找到父页面"},
    "session_not_found": {"en": "Session not found", "zh": "未找到会话"},
    "entry_not_found": {"en": "Entry not found", "zh": "未找到条目"},
    "notebook_not_found": {"en": "Notebook not found", "zh": "未找到笔记本"},
    "record_not_found": {"en": "Record not found", "zh": "未找到记录"},
    "upsert_failed": {"en": "Upsert failed", "zh": "写入失败"},
    "no_fields_to_update": {"en": "No fields to update", "zh": "没有可更新的字段"},
    "failed_to_add_to_category": {
        "en": "Failed to add to category",
        "zh": "添加到分类失败",
    },
    "link_not_found": {"en": "Link not found", "zh": "未找到关联"},
    "category_name_exists": {
        "en": "Category name already exists",
        "zh": "分类名称已存在",
    },
    "category_not_found": {"en": "Category not found", "zh": "未找到分类"},
    "quiz_results_required": {
        "en": "Quiz results are required",
        "zh": "必须提供测验结果",
    },
    "invalid_proposal": {"en": "Invalid proposal: {error}", "zh": "提案无效：{error}"},
    "invalid_spine": {"en": "Invalid spine: {error}", "zh": "章节骨架无效：{error}"},
    "unknown_block_type": {"en": "Unknown block type: {name}", "zh": "未知区块类型：{name}"},
    "unknown_content_type": {
        "en": "Unknown content type: {name}",
        "zh": "未知内容类型：{name}",
    },
    "invalid_file": {"en": "Invalid file: {file}", "zh": "无效文件：{file}"},
    "notebook_deleted_successfully": {
        "en": "Notebook deleted successfully",
        "zh": "笔记本删除成功",
    },
    "record_removed_successfully": {
        "en": "Record removed successfully",
        "zh": "记录移除成功",
    },
    "soul_exists": {"en": "Soul '{id}' already exists", "zh": "Soul '{id}' 已存在"},
    "soul_not_found": {"en": "Soul not found", "zh": "未找到 Soul"},
    "bot_not_found": {"en": "Bot not found", "zh": "未找到 Bot"},
    "bot_not_found_or_not_running": {
        "en": "Bot not found or not running",
        "zh": "未找到 Bot，或 Bot 未运行",
    },
    "invalid_channels_config": {
        "en": "Invalid channels config",
        "zh": "无效的渠道配置",
    },
    "invalid_channels_config_with_reason": {
        "en": "Invalid channels config: {error}",
        "zh": "无效的渠道配置：{error}",
    },
    "channels_saved_but_failed_to_restart": {
        "en": (
            "Channels saved but failed to restart listeners ({error_type}); "
            "try stopping and starting the bot."
        ),
        "zh": "渠道已保存，但重启监听器失败（{error_type}）；请尝试停止后再启动 Bot。",
    },
    "not_editable_file": {
        "en": "Not an editable file: {filename}",
        "zh": "该文件不可编辑：{filename}",
    },
    "untitled": {"en": "Untitled", "zh": "未命名"},
    "llm_connection_successful": {
        "en": "LLM connection successful",
        "zh": "LLM 连接成功",
    },
    "llm_connection_failed_empty_response": {
        "en": "LLM connection failed: Empty response",
        "zh": "LLM 连接失败：返回为空",
    },
    "llm_configuration_error": {
        "en": "LLM configuration error: {error}",
        "zh": "LLM 配置错误：{error}",
    },
    "llm_connection_failed": {
        "en": "LLM connection failed: {error}",
        "zh": "LLM 连接失败：{error}",
    },
    "embeddings_connection_successful_provider": {
        "en": "Embeddings connection successful ({provider} provider)",
        "zh": "Embeddings 连接成功（{provider} 提供方）",
    },
    "embeddings_connection_failed_empty_response": {
        "en": "Embeddings connection failed: Empty response",
        "zh": "Embeddings 连接失败：返回为空",
    },
    "embeddings_configuration_error": {
        "en": "Embeddings configuration error: {error}",
        "zh": "Embeddings 配置错误：{error}",
    },
    "embeddings_connection_failed": {
        "en": "Embeddings connection failed: {error}",
        "zh": "Embeddings 连接失败：{error}",
    },
    "search_not_configured": {"en": "Search not configured", "zh": "未配置搜索"},
    "search_provider_unsupported": {
        "en": "Search provider `{provider}` is deprecated/unsupported.",
        "zh": "搜索提供方 `{provider}` 已弃用或不受支持。",
    },
    "search_provider_missing_credentials": {
        "en": "Search provider `{provider}` missing credentials.",
        "zh": "搜索提供方 `{provider}` 缺少凭证。",
    },
    "search_provider_returned_no_content": {
        "en": "Search provider returned no content",
        "zh": "搜索提供方未返回内容",
    },
    "search_connection_successful": {
        "en": "Search connection successful",
        "zh": "搜索连接成功",
    },
    "search_configuration_error": {
        "en": "Search configuration error: {error}",
        "zh": "搜索配置错误：{error}",
    },
    "search_connection_check_failed": {
        "en": "Search connection check failed: {error}",
        "zh": "搜索连接检查失败：{error}",
    },
}

_ENGLISH_TO_KEY: dict[str, str] = {
    bundle["en"]: key for key, bundle in _MESSAGES.items() if "en" in bundle
}


def current_ui_language(default: str = "en") -> str:
    language = str(get_ui_language(default=default) or default).lower()
    return "zh" if language.startswith("zh") else "en"


def localize(key: str, default: str | None = None, **kwargs) -> str:
    language = current_ui_language()
    bundle = _MESSAGES.get(key)
    template = (bundle or {}).get(language, default or key)
    try:
        return template.format(**kwargs)
    except Exception:
        return template


def localize_known_text(text: str) -> str:
    key = _ENGLISH_TO_KEY.get(text)
    if not key:
        return text
    return localize(key, default=text)


def http_error(status_code: int, key: str, **kwargs) -> HTTPException:
    return HTTPException(status_code=status_code, detail=localize(key, **kwargs))
