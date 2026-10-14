# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr lets people search for the piece they're looking for and searches through all the listings to get the best match. The user types something like "vintage graphic tee under $30, size M" and the agent filters the listings down to what fits the price, size, and keywords. From the best match, it suggests a full outfit based on what you already own, pulling from your wardrobe. It also writes a caption so you can post about it.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings data for items matching keywords, an optional size, and an optional price ceiling.
- **Inputs:** `description` (str) — keywords like "vintage graphic tee". `size` (str or None) — matched as whole tokens against the listing's size field, so "M" matches "S/M" but not "XL". `max_price` (float or None) — a listing matches if its price is <= max_price.
- **Returns:** A list of listing dicts (id, title, description, category, style_tags, size, condition, price, colors, brand, platform), sorted best match first by keyword overlap.
- **When it has nothing:** Returns an empty list `[]` — never None, never an exception.

### `suggest_outfit`

- **What it does:** Calls the model to suggest outfits pairing the found item with pieces from the user's wardrobe.
- **Inputs:** `new_item` (dict) — a listing dict from search_listings. `wardrobe` (dict) — has an `items` key holding a list of wardrobe item dicts.
- **Returns:** A str with 2 outfit ideas.
- **When it has nothing:** If `wardrobe["items"]` is empty, returns a str of general styling advice instead of failing.

### `create_fit_card`

- **What it does:** Calls the model to write a short, postable caption for the item and outfit, naming at least one real wardrobe piece.
- **Inputs:** `outfit` (str) — the output of suggest_outfit. `new_item` (dict) — the listing dict.
- **Returns:** A 2-4 sentence str caption mentioning the item, its price, and a piece from the outfit.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a message saying there's no outfit to caption yet, instead of raising an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->


**One full query**

\`\`\`
$ python app.py ask 'vintage graphic tee under $30, size M'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1: Casual Streetwear**
*   Y2K Baby Tee — Butterfly Print
*   Baggy straight-leg jeans, dark wash
*   Chunky white sneakers
*   Black cropped zip hoodie

**Outfit 2: Retro Casual**
*   Y2K Baby Tee — Butterfly Print
*   Wide-leg khaki trousers
*   Brown leather belt
*   Black combat boots

  Fit card: obsessed with this butterfly print Y2K baby tee 🦋 throwing it on with baggy denim and a zip hoodie for casual streetwear days, or dressing it down with khaki trousers and combat boots for a retro look. grab it on my depop for just $18 before I change my mind and keep it! ✨
\`\`\`

**The three tools, tested one at a time**

\`\`\`
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'price': 18.0, ...}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'price': 24.0, ...}, ...]
\`\`\`

\`\`\`
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

**Outfit 1: Casual Streetwear**
*   Vintage Levi's 501 Jeans — Medium Wash
*   White ribbed tank top
*   Vintage black denim jacket
*   Chunky white sneakers
*   Black crossbody bag

**Outfit 2: Cozy & Relaxed**
*   Vintage Levi's 501 Jeans — Medium Wash
*   Oversized grey crewneck sweatshirt
*   Black combat boots
*   Brown leather belt
\`\`\`

\`\`\`
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Found the ultimate vintage Levi's 501s and I'm lowkey obsessed with this wash. Pair them with a beat-up pair of white sneakers and you've got that effortless 90s off-duty model look down pat. Grab these for just $38 over on my Depop before I change my mind and keep them.
\`\`\`

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked AI to help me write the code for the tools — search_listings, suggest_outfit, create_fit_card — and the planning loop.
- *What came back:* It came back with code for each of these.
- *What I changed:* I implemented it, but checked and changed things when I saw how the search didn't actually match well.

**Moment 2**

- *What I asked for:* I asked it to test suggest_outfit against the example wardrobe given.
- *What came back:* It came back with some items that didn't actually exist in the wardrobe.
- *What I changed:* I realized it was coming up with things not in the wardrobe, so I used that as a criterion instead of patching it.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. State carries to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card stays grounded | 5 of 5 | PASS | PASS | PASS | FAIL | PASS | MISSED (4/5) |
| 5. Outfit only names real wardrobe items | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, produced by `tools.py::create_fit_card`, called from `agent.py::run_agent`:

\`\`\`
$ python3 run_eval.py --label before
(criterion 4, try 4)
Fit card: Found my new entire personality for just $22 on thredUp. This oversized
red and black flannel is giving major 90s grunge energy, but I'm just as obsessed
with tying it around my waist for streetwear days. Seriously never taking this off.
\`\`\`

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All 5 tries completed and returned a fit card. |
| 2 | Impossible query stops before second tool | 5 of 5 | MET (5/5) | All 5 tries stopped early with 0 model calls each. |
| 3 | State carries to suggest_outfit | 5 of 5 | MET (5/5) | In all 5 tries, the item suggest_outfit received matched the first item search_listings returned, by title and price. |
| 4 | Fit card stays grounded | 5 of 5 | MISSED (4/5) | Try 4's fit card named the item and price but didn't mention any clothing piece from the outfit suggestion — it stayed entirely on the flannel itself. |
| 5 | Outfit only names real wardrobe items | 5 of 5 | MET (5/5) | I checked every item named across all 5 tries against wardrobe_schema.json. Every one — tank top, hoodie, sneakers, crossbody bag, sweatshirt, denim jacket, combat boots, belt — is a real entry in the wardrobe data. |

**Diagnoses**

**Criterion 4 (the only miss):** `create_fit_card`'s prompt asks the model to mention the item, price, and platform, but never explicitly requires it to reference anything from the outfit suggestion it's given. In try 4, `suggest_outfit` returned a longer, differently-structured outfit (with parenthetical styling notes like "worn open" and "tied around the waist"), and when `create_fit_card` wrote from that, it produced a short, punchy caption that talked about the item's vibe but dropped every specific wardrobe piece. The tool worked — it got the item and price right — but the prompt doesn't force the caption to stay grounded in the actual outfit, so when the model chooses brevity, the outfit disappears.

**Reversal worth noting on criterion 5:** In Unit 3, I flagged `suggest_outfit` as inventing wardrobe items — "white ribbed tank top," "black combat boots" — because the only wardrobe field reference I had seen was `python app.py fields`, which only prints item 1 of the wardrobe. Running the actual test against the full `wardrobe_schema.json` (10 items) in this unit, every single item named across all 25 outfit-suggestion runs is real. My original diagnosis was wrong, and criterion 5 passes cleanly. This is exactly the kind of thing Milestone 4 asks for — arguing the opposite verdict surfaced that the original assumption didn't hold.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

\`\`\`
$ python3 app.py ask 'vintage graphic tee under $30, size M' --trace
[1] parse_query
      in:  vintage graphic tee under $30, size M
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 8 items: Y2K Baby Tee — Butterfly Print, Mesh Long-Sleeve Top — Black, 90s Silk Slip Dress — Floral, Midi Length … +5 more
[3] branch
      →    results found, continuing to suggest_outfit
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: **Outfit 1: Casual Streetwear** *   Y2K Baby Tee — Butterfly Print *   Baggy straight-leg jeans, dark wash *  …
[5] create_fit_card
      in:  **Outfit 1: Casual Streetwear** *   Y2K Baby Tee — Butterfly Print *   Baggy straight-leg jeans, dark wash *  …
      out: obsessed with this butterfly print Y2K baby tee 🦋 throwing it on with baggy denim and a zip hoodie for casual …
\`\`\`

**Empty search**

\`\`\`
$ python3 app.py ask 'designer ballgown size XXS under $5' --trace
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch
      →    empty results, stopping before suggest_outfit
\`\`\`

**On the MCP move:** I moved `search_listings` to run through `mcp_client.call_tool` in `run_agent`, registered as a tool in `mcp_server.py` with its name, description, and typed inputs matching the Tool Inventory. I tested it before and after the swap on the same query — the result was identical (same item, same outfit, same fit card), confirming the tool's return shape didn't change when the call method did.

**Failure modes triggered:**

- **Empty search:** `python3 app.py ask 'designer ballgown size XXS under $5'` → "Nothing matched 'designer ballgown' in size XXS under $5. Try a higher price limit, drop the size, or use fewer keywords." No crash, no model call.
- **Empty wardrobe:** `python3 app.py ask 'vintage graphic tee under $30' --empty-wardrobe` → completed normally, with suggest_outfit returning general styling advice instead of crashing or returning an empty string.
- **Model unavailable:** Broke one character of `GEMINI_API_KEY` in `.env`, ran a new query. `run_agent`'s try/except around `suggest_outfit`/`create_fit_card` caught `ModelUnavailable` and produced: "Found the item, but couldn't reach the model to finish: The model rejected your API key... Try again in a moment, or check your API key." Restored the real key and confirmed the same query completed normally afterward.


---

## The Improvement

**What I changed:** In `tools.py::create_fit_card`, I added one line to the prompt requiring the model to "name at least one specific clothing piece from the outfit idea above — don't just describe the vibe without naming anything from it."

**Which failure it was meant to fix:** Criterion 4 (fit card stays grounded) missed 4/5 in the before run because one try's caption mentioned only the item and price, with no reference to the outfit's wardrobe pieces.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. State carries to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card stays grounded | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Outfit only names real wardrobe items | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** Yes. Criterion 4 went from 4/5 to 5/5 — every fit card across the after-run names at least one specific wardrobe piece (a ribbed tank top, a cropped hoodie) alongside the item and price. I also hit a real bug along the way: my first attempt at this fix accidentally left the `prompt = (...)` line nested inside an `if` block, so `create_fit_card` crashed with `UnboundLocalError` on every call. All 5 scenarios failed completely on that first after-run. I caught it from the trace output, fixed the indentation, and reran — the second after-run completed cleanly with the result shown above. That failed attempt is worth keeping in mind: an "improvement" can break the whole tool, and a full rerun is what caught it.

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

All five criteria passed in the after-run, so nothing's actually missed. But a couple targets were probably set lower than they needed to be.

**Criterion 1 (4 of 5):** I picked 4/5 because I thought my keyword search would mess up on some phrasings. It hit 5/5 both runs, so honestly the search handled it better than I expected — next time I'd just set this to 5/5.

**Criteria 2, 3, 5 (5 of 5):** These are just plain code logic, not model output, so they stayed at 5/5 the whole time. No reason to loosen or tighten these.

**Criterion 4:** This actually missed before and is fixed now. If I had more time I'd want to test it on an outfit suggestion that's less detailed (like a single item, no layering) since all my after-run tries happened to get richer outfits to pull from.

**If I had more time:** I'd move suggest_outfit onto MCP too, since it's a stretch feature I skipped to make sure I got the required stuff done first.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
