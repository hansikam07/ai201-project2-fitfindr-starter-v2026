"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
import re

import config
from generate import generate
from utils.data_loader import load_listings

STOPWORDS = {
    "a", "an", "the", "in", "for", "under", "below", "over", "looking", "i",
    "want", "need", "and", "with", "size", "of", "to", "me", "find", "some",
    "something", "that", "is", "my", "on", "max", "less", "than",
}


def _tokens(text: str) -> set[str]:
    """Lowercase word tokens, with a trailing 's' stripped so tees == tee."""
    out = set()
    for t in re.findall(r"[a-z0-9]+", str(text).lower()):
        if len(t) > 3 and t.endswith("s"):
            t = t[:-1]
        out.add(t)
    return out


def _size_matches(want: str, listing_size: str) -> bool:
    """Whole-token match: 'M' matches 'S/M' but not 'XL' or 'US 9'."""
    want_tokens = set(re.findall(r"[a-z0-9]+", want.lower()))
    have_tokens = set(re.findall(r"[a-z0-9]+", str(listing_size).lower()))
    return bool(want_tokens) and want_tokens <= have_tokens


def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """Filter listings by price and size, score by keyword overlap, best first."""
    keywords = _tokens(description) - STOPWORDS
    scored = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size and not _size_matches(size, listing["size"]):
            continue
        haystack = _tokens(
            " ".join(
                [
                    listing["title"],
                    listing["description"],
                    listing["category"],
                    " ".join(listing["style_tags"]),
                    " ".join(listing["colors"]),
                    listing["brand"] or "",
                ]
            )
        )
        score = len(keywords & haystack)
        if score > 0:
            scored.append((score, listing))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [l for _, l in scored[: config.SEARCH_RESULT_LIMIT]]


def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """Ask the model for outfits using the new item plus the user's wardrobe."""
    item_line = (
        f"{new_item['title']} ({new_item['category']}, "
        f"colors: {', '.join(new_item['colors'])}, "
        f"tags: {', '.join(new_item['style_tags'])})"
    )
    items = (wardrobe or {}).get("items", [])

    if not items:
        prompt = (
            f"Someone is thinking about buying this thrifted item: {item_line}.\n"
            "They have no wardrobe saved. Give general styling advice: 2 outfit "
            "ideas using common basics. Keep it short and casual."
        )
        return generate(prompt) or "Pair it with simple basics like jeans and white sneakers."

    wardrobe_lines = "\n".join(
        f"- {w['name']} ({w['category']}, {', '.join(w['colors'])})" for w in items
    )
    prompt = (
        f"New thrifted item: {item_line}.\n\nTheir wardrobe:\n{wardrobe_lines}\n\n"
        "Suggest 2 outfits using the new item with pieces from the wardrobe. "
        "Name the wardrobe pieces exactly as listed. Do not invent clothes they "
        "don't own. Keep it short and casual."
    )
    return generate(prompt)


def create_fit_card(outfit: str, new_item: dict) -> str:
    """Write a short, postable caption for the find."""
    if not outfit or not outfit.strip():
        return (
            f"No outfit to caption yet for {new_item['title']}. "
            "Run suggest_outfit first."
        )
    prompt = (
        f"Write a 2-4 sentence social media caption for a thrift find.\n"
        f"Item: {new_item['title']}\nPrice: ${new_item['price']:.0f}\n"
        f"Platform: {new_item['platform']}\nOutfit idea: {outfit}\n\n"
        "Sound like a real person posting, not a product description. Mention "
        "the item, the price, and the platform once each. Be specific about "
        "the vibe."
    )
    return generate(prompt)