"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
import re
import trace
from tools import suggest_outfit, create_fit_card
from mcp_client import call_tool
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def _parse_query(query: str) -> dict:
    """Regex parse: price from 'under $30' or '$30', size from 'size M'."""
    max_price = None
    m = re.search(r"(?:under|below|less than|max)\s*\$?\s*(\d+(?:\.\d+)?)", query, re.I) \
        or re.search(r"\$\s*(\d+(?:\.\d+)?)", query)
    if m:
        max_price = float(m.group(1))

    size = None
    s = re.search(r"\bsize\s+([A-Za-z0-9/]+)", query, re.I)
    if s:
        size = s.group(1)

    description = re.sub(r"(?:under|below|less than|max)\s*\$?\s*\d+(?:\.\d+)?", " ", query, flags=re.I)
    description = re.sub(r"\$\s*\d+(?:\.\d+)?", " ", description)
    description = re.sub(r"\b(?:in\s+)?size\s+[A-Za-z0-9/]+", " ", description, flags=re.I)
    return {"description": description.strip(" ,."), "size": size, "max_price": max_price}


def run_agent(query: str, wardrobe: dict) -> dict:
    session = new_session(query, wardrobe)
    trace.start_trace()

    count = 0
    count += 1
    trace.check_iterations(count)

    session["parsed"] = _parse_query(query)
    p = session["parsed"]
    trace.step("parse_query", inputs=query, returned=p)

    session["search_results"] = call_tool("search_listings", {
        "description": p["description"],
        "size": p["size"],
        "max_price": p["max_price"],
    })
    trace.step("search_listings (via MCP)", inputs=p, returned=session["search_results"])

    # THE BRANCH: nothing found -> explain and stop before suggest_outfit
    if not session["search_results"]:
        session["error"] = (
            f"Nothing matched '{p['description']}'"
            + (f" in size {p['size']}" if p["size"] else "")
            + (f" under ${p['max_price']:.0f}" if p["max_price"] else "")
            + ". Try a higher price limit, drop the size, or use fewer keywords."
        )
        trace.step("branch", note="empty results, stopping before suggest_outfit")
        return session

    session["selected_item"] = session["search_results"][0]
    trace.step("branch", note="results found, continuing to suggest_outfit")

    try:
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"], session["wardrobe"]
        )
        trace.step("suggest_outfit", inputs=session["selected_item"], returned=session["outfit_suggestion"])

        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"], session["selected_item"]
        )
        trace.step("create_fit_card", inputs=session["outfit_suggestion"], returned=session["fit_card"])
    except ModelUnavailable as exc:
        session["error"] = (
            f"Found the item, but couldn't reach the model to finish: {exc} "
            "Try again in a moment, or check your API key."
        )
        trace.step("suggest_outfit/create_fit_card", note=f"ModelUnavailable caught: {exc}")

    return session

# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
