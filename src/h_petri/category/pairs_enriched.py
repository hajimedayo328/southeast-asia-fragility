"""
The 5 prediction pairs as H-enriched categories + translation functors (notes/27 §4).

For each pair we build the EA side and the Developed side INDEPENDENTLY from
generating influences (no shared template — this is what breaks the circularity
of notes/23). We then test whether the object map F is a valid (lax) H-functor
    hom_EA(A,B) ≤ hom_Dev(FA,FB)
and classify it as strict / lax / broken.

⚠️ The hom values are AUTHOR-ASSIGNED (notes/27 §7). What the code establishes
objectively, given those assignments, is:
  (1) each side is a valid H-enriched category (axioms hold by closure), and
  (2) the verdict on F (strict / lax / broken) and its distortion.
It does NOT establish that the assignments themselves are correct.

Heyting levels:  ⊥ < ⊤_priv < ⊤_bank < ⊤_pub
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from h_petri.core import FourLevelHA
from h_petri.category.enriched import EnrichedCategory, VFunctor

HA = FourLevelHA()
B, PRIV, BANK, PUB = HA.bottom, HA.T_PRIV, HA.T_BANK, HA.T_PUB


# Each pair: (name, EA objects+gens, Dev objects+gens, F object map, note)
PAIRS = [
    {
        "name": "Pair 1 — 1997 AFC → 2008 Lehman",
        "ea_objs": ["TH", "BIBF", "KR", "IMF"],
        "ea_gen": {("TH", "BIBF"): BANK, ("BIBF", "KR"): PRIV, ("BIBF", "IMF"): PRIV},
        "dev_objs": ["ShadowBank", "Lehman", "AIG", "TARP"],
        "dev_gen": {("ShadowBank", "Lehman"): BANK, ("Lehman", "AIG"): PRIV,
                    ("Lehman", "TARP"): PUB},
        "F": {"TH": "ShadowBank", "BIBF": "Lehman", "KR": "AIG", "IMF": "TARP"},
        "note": "Bailout reach differs: IMF stays ⊤_priv, TARP rises to ⊤_pub "
                "→ Dev amplifies → expect lax.",
    },
    {
        "name": "Pair 2 — M-Pesa 2019 → Cloudflare 2025",
        "ea_objs": ["Safaricom", "KEpay", "KEeconomy"],
        "ea_gen": {("Safaricom", "KEpay"): PRIV, ("KEpay", "KEeconomy"): PRIV},
        "dev_objs": ["Cloudflare", "AIsvc", "AImarket"],
        "dev_gen": {("Cloudflare", "AIsvc"): PRIV, ("AIsvc", "AImarket"): PRIV},
        "F": {"Safaricom": "Cloudflare", "KEpay": "AIsvc", "KEeconomy": "AImarket"},
        "note": "Single private backbone outage, identical ranks → expect strict.",
    },
    {
        "name": "Pair 3 — GCash monopoly → GAFA-AI monopoly",
        "ea_objs": ["GCash", "Maya", "PHmarket"],
        "ea_gen": {("GCash", "PHmarket"): PRIV, ("Maya", "PHmarket"): PRIV,
                   ("GCash", "Maya"): PRIV},
        "dev_objs": ["OpenAI", "Anthropic", "AImarket"],
        "dev_gen": {("OpenAI", "AImarket"): BANK, ("Anthropic", "AImarket"): PRIV,
                    ("OpenAI", "Anthropic"): PRIV},
        "F": {"GCash": "OpenAI", "Maya": "Anthropic", "PHmarket": "AImarket"},
        "note": "National vs global scale: Dev reach broader (⊤_bank) → expect lax.",
    },
    {
        "name": "Pair 4 — Mekong dams → Russian gas",
        "ea_objs": ["ChinaDam", "Mekong5", "WaterLever"],
        "ea_gen": {("ChinaDam", "Mekong5"): BANK, ("ChinaDam", "WaterLever"): PRIV},
        "dev_objs": ["RusGas", "EU", "GasLever"],
        "dev_gen": {("RusGas", "EU"): BANK, ("RusGas", "GasLever"): PUB},
        "F": {"ChinaDam": "RusGas", "Mekong5": "EU", "WaterLever": "GasLever"},
        "note": "Hidden denial (⊤_priv) vs overt weaponization (⊤_pub) "
                "→ Dev amplifies → expect lax.",
    },
    {
        # CORRECTED 2026-06-12: the earlier framing 'Wave Money collapsed,
        # users migrated to KBZPay' was overstated. Sourced reality: the coup
        # cancelled Ant's $73.5M investment, Telenor sold its 51% to Yoma at a
        # distressed $53M, app MAU halved — a FORCED OWNERSHIP TRANSFER, with
        # the service surviving under local ownership. The Dev analogue
        # (TikTok divestment pressure: ByteDance → US owner candidates) maps
        # MORE cleanly onto this corrected reading: EA transfer COMPLETED
        # (Telenor→Yoma), Dev transfer UNRESOLVED.
        "name": "Pair 5 — Wave Money ownership transfer → TikTok divestment",
        "ea_objs": ["Wave", "Yoma", "MMusers"],
        "ea_gen": {("Wave", "MMusers"): PRIV, ("Wave", "Yoma"): BANK,
                   ("Yoma", "MMusers"): BANK},
        "dev_objs": ["TikTok", "USowner", "USusers"],
        "dev_gen": {("TikTok", "USusers"): PRIV, ("TikTok", "USowner"): PRIV,
                    ("USowner", "USusers"): PRIV},
        "F": {"Wave": "TikTok", "Yoma": "USowner", "MMusers": "USusers"},
        "note": "EA ownership transfer completed (Telenor→Yoma, ⊤_bank-backed "
                "local owner), Dev transfer unresolved (⊤_priv) → Dev "
                "attenuates → expect broken (functoriality leaks).",
    },
]


def run_pair(spec: dict) -> dict:
    ea = EnrichedCategory.from_generators(
        spec["name"] + " / EA", spec["ea_objs"], spec["ea_gen"], HA)
    dev = EnrichedCategory.from_generators(
        spec["name"] + " / Dev", spec["dev_objs"], spec["dev_gen"], HA)
    F = VFunctor(spec["name"], ea, dev, spec["F"], HA)

    ea_valid = ea.is_valid()
    dev_valid = dev.is_valid()
    classification = F.classify()

    return {
        "name": spec["name"],
        "note": spec["note"],
        "ea_axioms_ok": ea_valid["valid"],
        "dev_axioms_ok": dev_valid["valid"],
        "verdict": classification["verdict"],
        "is_valid_V_functor": classification["is_valid_V_functor"],
        "counts": classification["counts"],
        "distortion": classification["distortion"],
        "breaking_pairs": [
            p for p in classification["per_pair"] if p["kind"] == "attenuated"
        ],
        "amplifying_pairs": [
            {"a": p["a"], "b": p["b"], "hom_src": p["hom_src"], "hom_tgt": p["hom_tgt"]}
            for p in classification["per_pair"] if p["kind"] == "amplified"
        ],
    }


def main():
    results = [run_pair(p) for p in PAIRS]

    print("=" * 72)
    print("H-enriched prediction pairs — translation functor classification")
    print("notes/27 §4 (Lawvere-1973-style, Heyting-enriched)")
    print("=" * 72)
    print("\n⚠️ hom values are author-assigned; the code verifies category axioms")
    print("   and computes the V-functor verdict GIVEN those assignments.\n")

    rank_order = {"strict": 0, "lax": 1, "broken": 2}
    for r in results:
        ax = "✓" if (r["ea_axioms_ok"] and r["dev_axioms_ok"]) else "✗ AXIOM FAIL"
        print(f"[{r['name']}]")
        print(f"  category axioms (EA & Dev): {ax}")
        print(f"  F verdict: {r['verdict'].upper():7s}  "
              f"valid V-functor: {r['is_valid_V_functor']}  "
              f"distortion: {r['distortion']:+d}")
        print(f"  counts: {r['counts']}")
        if r["amplifying_pairs"]:
            for ap in r["amplifying_pairs"]:
                print(f"    amplified: hom({ap['a']},{ap['b']}) "
                      f"{ap['hom_src']} → {ap['hom_tgt']}")
        if r["breaking_pairs"]:
            for bp in r["breaking_pairs"]:
                print(f"    BREAKS:   hom({bp['a']},{bp['b']}) "
                      f"{bp['hom_src']} ↛ {bp['hom_tgt']} (Dev weaker)")
        print()

    # summary spectrum
    spectrum = {r["name"]: r["verdict"] for r in results}
    print("-" * 72)
    print("Prediction-strength spectrum (computed, not asserted):")
    for name, v in sorted(spectrum.items(), key=lambda kv: rank_order[kv[1]]):
        label = {"strict": "★★★★★ isometric (strongest)",
                 "lax": "★★★☆☆ lax (Dev amplifies)",
                 "broken": "★★☆☆☆ broken (Dev incomplete)"}[v]
        print(f"  {v:7s} {label:32s} {name}")

    bundle = {
        "description": (
            "5 prediction pairs as Heyting-enriched categories (notes/27). Each "
            "side built independently from generating influences via meet-transitive "
            "closure (free H-category), so the composition axiom holds by construction. "
            "The translation functor F is classified strict / lax / broken. Heyting "
            "hom values are author-assigned (notes/27 §7); the code verifies the "
            "category axioms and computes F's verdict given those assignments."
        ),
        "foundation": "Lawvere 1973, Metric spaces / generalized logic / closed "
                      "categories (TAC Reprints No.1); quantale-enriched categories.",
        "pairs": results,
        "spectrum": spectrum,
        "honest_limits": (
            "Verdicts reflect author-assigned hom matrices, not measured data. "
            "What is objective: (1) both sides satisfy the enriched-category axioms, "
            "(2) F's strict/lax/broken verdict follows deterministically from the "
            "assigned matrices. Replacing assignments with data-derived influence "
            "strengths is future work."
        ),
    }
    out_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "enriched_pairs.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
