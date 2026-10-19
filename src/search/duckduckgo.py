from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    """Search DuckDuckGo and return a compact text block of results, or "" on failure."""
    try:
        results = DDGS().text(query, max_results=max_results)
    except Exception:
        return ""

    if not results:
        return ""

    lines = []
    for r in results:
        title = r.get("title", "").strip()
        body = r.get("body", "").strip()
        href = r.get("href", "").strip()
        lines.append(f"- {title}: {body} ({href})")

    return "\n".join(lines)
