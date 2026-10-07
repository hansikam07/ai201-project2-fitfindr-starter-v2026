# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** My search matches on keyword overlap rather than strict
category rules. In testing, a query for "graphic tee" matched a pair of cargo
pants and a sweatshirt because their descriptions happened to use the words
"graphic" or "tee" in passing. That kind of loose matching means some phrasings
could miss or misfire, so I didn't expect a perfect 5 of 5.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** This branch is a plain Python check on whether the list
from search_listings is empty, with no model call involved. There's no
randomness in that check, so I expect it to behave the same way every time.

---

## 3. State carries through correctly

Given a query that matches at least one listing, the title of
`session["selected_item"]` appears in the prompt sent to `suggest_outfit` —
in 5 of 5 runs.

**Why this target:** The session is a plain dict assignment with no model call
involved in passing the item along, so I expect this to hold every time. If it
doesn't, that's a real bug in the loop, not model randomness.

---

## 4. The fit card stays grounded

Given the same item run across 5 tries, every fit card mentions the item and
the price, and names at least one piece of clothing that actually exists in
the wardrobe data — in 5 of 5 tries.

**Why this target:** The fit card runs at temperature 0.9, so the wording
changes every time, but the prompt explicitly includes the item and price, so
I expect those facts to survive even when the phrasing doesn't. I added the
wardrobe-grounding check because when I tested suggest_outfit, it named items
like a white ribbed tank top and combat boots that don't exist in the wardrobe
data at all — so I want to know if that invention carries through to the fit
card too.

---

## 5. The outfit only names real wardrobe items

Given a query that matches at least one listing, every item named in
`suggest_outfit`'s output actually appears in the wardrobe data — in 5 of 5
runs.

**Why this target:** I'm setting this at 5 of 5 on purpose, even though I
already have strong evidence it will fail. When I tested suggest_outfit
against the example wardrobe, it invented a white ribbed tank top, a black
crossbody bag, and combat boots — none of which are in the wardrobe schema.
Missing my own target here costs nothing, and a target I already suspect will
fail is more honest than lowering it to something I'm sure to hit.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
