"""
Grounded sensitivity test for the 5 prediction-pair verdicts (notes/29).

pairs_enriched.py assigns the 26 generating-influence hom values BY AUTHOR
(notes/27 §7). backbone_facts.py showed how to PROMOTE author-assigned NODE
levels to data-grounded ones: a sourced legal "backing tier" + one explicit
rule mapping tier -> Heyting level. Here we apply the SAME discipline to the
prediction-pair EDGES and ask the only question that matters:

    do the strict / lax / broken verdicts survive consistent grounding?

Method (deliberately MINIMAL and auditable)
--------------------------------------------
1. Every influence edge is anchored on an INSTITUTION whose legal backing tier
   we take from a sourced fact (same 5-tier scheme as backbone_facts), via the
   single rule  hom(A,B) = tier(A) ∨ tier(B)  with NONINST = ⊥ (markets,
   economies, user bases are not financial institutions and contribute ⊥).
2. We RE-GROUND only the edges anchored on institutions whose tier we sourced
   independently AND which is contested vs the author (IMF, OpenAI, Maya, Yoma).
   Every other edge keeps the author's uncontested private-platform value, so
   any verdict change is attributable to ONE sourced tier, not to wholesale
   re-tuning. This is the conservative move: "even fixing just this tier flips
   the verdict."
3. Two nodes are genuinely AMBIGUOUS — two equally defensible readings each.
   We enumerate the verdict under EACH reading instead of picking one.
4. Pair 4 (geopolitical leverage) has NO financial backstop tier: the rule is
   semantically inapplicable. It is reported as ungroundable, not forced.

Sourced facts (verified via web search 2026-06-14; see SOURCES)
--------------------------------------------------------------
  OpenAI    non-bank for-profit Public Benefit Corp ("OpenAI Group PBC",
            restructured 2025-10-28). NOT a bank -> ⊤_priv. The author's
            ⊤_bank was a *reach/scale* up-grade, not a legal tier.
  Anthropic Delaware Public Benefit Corp, AI company, not a bank -> ⊤_priv.
  GCash     BSP-licensed NON-BANK EMI (EMI-NBFI); parent stated 2024 it is
            deliberately staying non-bank -> ⊤_priv (firm).
  Maya      AMBIGUOUS: consumer e-wallet / non-bank EMI (⊤_priv) OR "Maya Bank",
            a BSP-licensed digital bank since Sep-2021 (⊤_bank).
  Yoma      AMBIGUOUS: the 2022 acquirer of Telenor's 51% of Wave Money was
            Yoma MFS Holdings, a subsidiary of Yoma STRATEGIC HOLDINGS — a
            non-bank SGX-listed conglomerate (⊤_priv). The same Yoma/FMI group
            also contains Yoma Bank, a CBM-licensed commercial bank (⊤_bank).
  IMF       public international financial institution; its 1997 Thailand
            intervention was a sovereign-scale public bailout -> ⊤_pub. The
            author rated this edge ⊤_priv.

Finding (computed below, not asserted)
--------------------------------------
Only Pair 2 (both nodes unambiguously non-bank) keeps its verdict. Pairs 1, 3, 5
flip, and across the defensible readings Pair 3 spans strict<->broken while the
author chose lax — a verdict reproduced by NEITHER consistent legal-tier reading
(it needed OpenAI=⊤_bank [scale] together with Maya=⊤_priv [ignoring its bank
licence] at the same time: internally inconsistent tiering). The
prediction-strength spectrum is therefore an artifact of author node-tier
judgments, not a measured property — the concrete content of the (b)-not-(c)
caveat in pairs_enriched.py's own docstring and notes/27 §7 / §8.3.
"""

from __future__ import annotations
import json
import sys
from itertools import product
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from h_petri.core import FourLevelHA
from h_petri.category.enriched import EnrichedCategory, VFunctor
from h_petri.category.pairs_enriched import PAIRS

HA = FourLevelHA()
B, PRIV, BANK, PUB = HA.bottom, HA.T_PRIV, HA.T_BANK, HA.T_PUB

NONINST = B  # not a financial institution -> no legal backing tier -> ⊥


# ---------------------------------------------------------------------------
# Node legal backing tiers (sourced). Ambiguous nodes resolved per reading.
# ---------------------------------------------------------------------------

# Fixed (single sourced tier). Nodes absent here AND not ambiguous -> NONINST.
BASE_TIER = {
    # Pair 1
    "BIBF": BANK,   # Bangkok International Banking Facility — offshore bank scheme
    "IMF":  PUB,    # public international financial institution (contested edge)
    "Lehman": PRIV, # investment bank / broker-dealer, no retail deposit insurance
    "AIG":  PRIV,   # insurer (non-bank), Fed-rescued
    "TARP": PUB,    # US Treasury public bailout programme ($700bn)
    # Pair 2
    "Safaricom": PRIV,  # mobile-network operator (non-bank) running M-Pesa
    "Cloudflare": PRIV, # web-infrastructure company (non-bank)
    # Pair 3
    "GCash": PRIV,      # BSP-licensed NON-BANK EMI (deliberately stays non-bank)
    "OpenAI": PRIV,     # non-bank for-profit PBC (author rated ⊤_bank on scale)
    "Anthropic": PRIV,  # non-bank Delaware PBC
    # Pair 5
    "Wave": PRIV,       # licensed mobile-financial-services / e-money (non-bank)
    "TikTok": PRIV,     # ByteDance app (non-bank tech)
    "USowner": PRIV,    # prospective US owner candidates (non-bank)
    # everything else (TH, KR, ShadowBank, KEpay, KEeconomy, AIsvc, AImarket,
    # PHmarket, MMusers, USusers, and the entire Pair 4 cast) = NONINST
}

# Two defensible readings each, with the rationale that justifies the tier.
AMBIG = {
    "Maya": [
        (PRIV, "consumer e-wallet / non-bank EMI reading"),
        (BANK, "Maya Bank holds a BSP digital-bank licence (since Sep-2021)"),
    ],
    "Yoma": [
        (PRIV, "acquirer of record = Yoma Strategic Holdings, a non-bank "
               "SGX-listed conglomerate (via Yoma MFS Holdings, 2022)"),
        (BANK, "the Yoma/FMI group also contains Yoma Bank, a CBM-licensed "
               "commercial bank"),
    ],
}

# Edges anchored on these institutions are RE-GROUNDED; all others keep the
# author's uncontested value. (Maya/Yoma are also in AMBIG; that resolves their
# tier, CONTESTED says "reground edges that touch them".)
CONTESTED = {"IMF", "OpenAI", "Maya", "Yoma"}

# Pair whose edges carry coercive-leverage semantics, NOT a legal backstop tier.
UNGROUNDABLE = {"Pair 4 — Mekong dams → Russian gas"}

SOURCES = {
    "OpenAI": ["https://openai.com/our-structure/",
               "https://www.aljazeera.com/economy/2025/10/28/openai-restructures-into-public-benefit-firm-microsoft-takes-27-stake"],
    "Anthropic": ["https://www.anthropic.com/news/the-long-term-benefit-trust",
                  "https://time.com/6983420/anthropic-structure-openai-incentives/"],
    "GCash": ["https://en.wikipedia.org/wiki/GCash",
              "https://www.bworldonline.com/banking-finance/2024/08/15/613988/gcash-hesitant-on-digital-bank-license/"],
    "Maya": ["https://www.rappler.com/business/paymaya-gets-digital-bank-license/",
             "https://www.maya.ph/stories/maya-is-1-of-the-6-bsp-licensed-digital-banks-in-the-philippines-today"],
    "Yoma": ["https://www.globenewswire.com/en/news-release/2022/01/17/2367508/0/en/Telenor-Group-agrees-to-sell-its-stake-in-Wave-Money-to-Yoma-Strategic.html",
             "https://en.wikipedia.org/wiki/Yoma_Bank"],
    "IMF": ["https://www.imf.org/en/About",
            "https://www.imf.org/external/np/exr/facts/asia.htm"],
}


def tier(node: str, reading: dict[str, str]) -> str:
    """Legal backing tier of a node under the current ambiguous-node reading."""
    if node in reading:
        return reading[node]
    return BASE_TIER.get(node, NONINST)


def reground(author_gen: dict, reading: dict[str, str]) -> tuple[dict, list]:
    """Re-ground only edges anchored on a CONTESTED institution.

    Returns (new_generators, list-of-changes). Edge value for a regrounded edge
    is tier(A) ∨ tier(B); other edges keep the author's value.
    """
    new: dict = {}
    changes = []
    for (a, b), author_val in author_gen.items():
        if a in CONTESTED or b in CONTESTED:
            val = HA.join(tier(a, reading), tier(b, reading))
            new[(a, b)] = val
            if val != author_val:
                changes.append((a, b, author_val, val))
        else:
            new[(a, b)] = author_val
    return new, changes


def verdict_of(spec: dict, ea_gen: dict, dev_gen: dict) -> dict:
    ea = EnrichedCategory.from_generators(spec["name"] + "/EA",
                                          spec["ea_objs"], ea_gen, HA)
    dev = EnrichedCategory.from_generators(spec["name"] + "/Dev",
                                           spec["dev_objs"], dev_gen, HA)
    F = VFunctor(spec["name"], ea, dev, spec["F"], HA)
    return F.classify()


def ambiguous_nodes_in(spec: dict) -> list[str]:
    nodes = set(spec["ea_objs"]) | set(spec["dev_objs"])
    return [n for n in AMBIG if n in nodes]


def run_pair(spec: dict) -> dict:
    name = spec["name"]
    author = verdict_of(spec, spec["ea_gen"], spec["dev_gen"])

    if name in UNGROUNDABLE:
        return {
            "name": name,
            "author_verdict": author["verdict"],
            "groundable": False,
            "reason": "edges carry coercive-leverage semantics (resource "
                      "denial / weaponization), not a financial backstop tier; "
                      "the tier->Heyting rule is semantically inapplicable.",
            "readings": [],
            "robust": None,
        }

    amb = ambiguous_nodes_in(spec)
    # enumerate every combination of readings for the ambiguous nodes present
    option_lists = [[(n, t, why) for (t, why) in AMBIG[n]] for n in amb]
    combos = list(product(*option_lists)) if option_lists else [()]

    readings_out = []
    verdicts_seen = set()
    for combo in combos:
        reading = {n: t for (n, t, _why) in combo}
        ea_gen, ea_chg = reground(spec["ea_gen"], reading)
        dev_gen, dev_chg = reground(spec["dev_gen"], reading)
        cls = verdict_of(spec, ea_gen, dev_gen)
        verdicts_seen.add(cls["verdict"])
        readings_out.append({
            "reading": {n: t for (n, t, _why) in combo},
            "rationale": {n: why for (n, _t, why) in combo},
            "verdict": cls["verdict"],
            "distortion": cls["distortion"],
            "edge_changes": [
                {"side": "EA", "edge": f"{a}->{b}", "author": av, "grounded": gv}
                for (a, b, av, gv) in ea_chg
            ] + [
                {"side": "Dev", "edge": f"{a}->{b}", "author": av, "grounded": gv}
                for (a, b, av, gv) in dev_chg
            ],
        })

    robust = (len(verdicts_seen) == 1) and (verdicts_seen == {author["verdict"]})
    return {
        "name": name,
        "author_verdict": author["verdict"],
        "groundable": True,
        "ambiguous_nodes": amb,
        "grounded_verdicts": sorted(verdicts_seen),
        "robust": robust,
        "readings": readings_out,
    }


def main():
    results = [run_pair(p) for p in PAIRS]

    print("=" * 74)
    print("Prediction pairs — GROUNDED sensitivity of the strict/lax/broken verdict")
    print("notes/29  (applies backbone_facts.py's tier->level discipline to EDGES)")
    print("=" * 74)
    print("\nRule:  hom(A,B) = tier(A) ∨ tier(B),  NONINST = ⊥.  Only edges anchored")
    print("on a contested institution are re-grounded; others keep author values.\n")

    for r in results:
        print(f"[{r['name']}]")
        print(f"  author verdict : {r['author_verdict'].upper()}")
        if not r["groundable"]:
            print(f"  grounded       : UNGROUNDABLE — {r['reason']}")
            print()
            continue
        if r["ambiguous_nodes"]:
            print(f"  ambiguous nodes: {', '.join(r['ambiguous_nodes'])}")
        for rd in r["readings"]:
            tag = (", ".join(f"{n}={t}" for n, t in rd["reading"].items())
                   or "single grounding")
            print(f"    [{tag}] -> {rd['verdict'].upper()}"
                  f"  (distortion {rd['distortion']:+d})")
            for ch in rd["edge_changes"]:
                print(f"        regrounded {ch['side']} {ch['edge']}: "
                      f"{ch['author']} -> {ch['grounded']}")
        label = "ROBUST (verdict unchanged)" if r["robust"] else \
                f"FRAGILE (verdict moves: author={r['author_verdict']} -> " \
                f"grounded {r['grounded_verdicts']})"
        print(f"  => {label}")
        print()

    groundable = [r for r in results if r["groundable"]]
    robust = [r for r in groundable if r["robust"]]
    print("-" * 74)
    print(f"Groundable pairs : {len(groundable)}/{len(results)} "
          f"(Pair 4 ungroundable — geopolitical, no backstop tier)")
    print(f"Robust verdicts  : {len(robust)}/{len(groundable)}  "
          f"({', '.join(r['name'].split(' — ')[0] for r in robust) or 'none'})")
    print("\nThe prediction-strength spectrum is NOT robust to consistent")
    print("grounding: it is an artifact of author-assigned node tiers, which is")
    print("exactly the (b)-not-(c) limitation flagged in pairs_enriched.py.")

    bundle = {
        "description": (
            "Grounded sensitivity test of the 5 prediction-pair verdicts. Each "
            "contested influence edge is re-grounded from a SOURCED legal backing "
            "tier (same scheme as backbone_facts.py) via hom(A,B)=tier(A)∨tier(B); "
            "uncontested edges keep author values. Ambiguous nodes (Maya, Yoma) are "
            "enumerated over both defensible readings. Verdicts are computed, not "
            "asserted."
        ),
        "rule": "hom(A,B) = tier(A) ∨ tier(B);  NONINST = ⊥;  reground only edges "
                "anchored on a contested institution.",
        "sources": SOURCES,
        "pairs": results,
        "summary": {
            "groundable": len(groundable),
            "total": len(results),
            "robust": [r["name"] for r in robust],
            "ungroundable": list(UNGROUNDABLE),
        },
        "honest_limits": (
            "This does NOT prove the author's verdicts 'wrong'. It proves they are "
            "UNDER-DETERMINED: across equally-defensible, sourced legal-tier "
            "readings the verdict flips (Pair 3 spans strict<->broken). The single "
            "robust verdict is Pair 2 (both nodes unambiguously non-bank). The edge "
            "rule (∨ of tiers) and the 5-tier scheme are themselves modelling "
            "choices, inherited transparently from backbone_facts.py."
        ),
    }
    out = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "enriched_pairs_grounded.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
