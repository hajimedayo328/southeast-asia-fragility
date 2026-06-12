"""
Out-of-region corner test — trying to KILL the v×C bound with its strongest
counterexample candidates: India UPI, Brazil Pix, Kenya M-Pesa.

The surviving hypothesis from speed_test.py was the INEQUALITY reading:
"fast adoption AND decentralization cannot coexist" (empty high-v/low-C corner).
ASEAN alone had only ONE decentralized country, so the empty corner was weak
evidence. These three cases are the global stress test — Pix especially is the
best-documented candidate for "fast AND decentralized".

RESULT PREVIEW (computed below): the bound's fate depends on WHICH LEVEL
"concentration" is measured at — and that split is itself the structural
finding:
  - APP level (front-end):  Pix is the fastest payment adoption in history
    (~67pp of adults in year one) with NO dominant app → corner OCCUPIED →
    the app-level bound is FALSIFIED.
  - RAIL level (backbone):  every fast adopter everywhere rides a SINGLE
    shared rail (Pix=BCB, UPI=NPCI, M-Pesa=Safaricom, PromptPay=ITMX) →
    rail-level corner stays empty — but near-definitionally (speed comes FROM
    one interoperable rail), so it survives as a structural observation more
    than a risky prediction.
What fragility inherits: the single rail = single stalk (the sheaf/H¹ story
applies at rail level); what differs is the rail's Heyting backstop
(Pix ⊤_pub / UPI consortium / M-Pesa ⊤_priv) = who pays when the stalk fails.

DATA (all sourced, fetched/verified 2026-06-12):
- Pix: launched 2020-11 by the Central Bank of Brazil; 114M users = 67% of
  adults by Nov 2021 (Central Banking / BCB); ~91-93% of adults by 2025.
  Front-end: runs inside every bank/fintech app; no single dominant app
  (front-end share data not centrally published — flagged).
- UPI: NPCI (bank-consortium under RBI); PhonePe 47.7% + Google Pay 36.7% of
  UPI volume Dec 2024 (NPCI data via Statista/press) = duopoly, top app <50%;
  UPI carries the bulk of India's retail digital-payment volume (single rail).
- Kenya: mobile money 68.7% of adults (Findex 2021, WB API); M-Pesa ~96.5%
  market share (earlier-verified) — fast historically AND concentrated at
  every level; ⊤_priv.
- Findex 'mobileaccount' lens FAILS for UPI/Pix (India 10.4%, Brazil 27.0% in
  2021) because they are bank-rail systems, not "mobile money accounts" —
  itself evidence that the indicator measures a TYPE, not a function.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CASES = [
    {
        "case": "Brazil Pix", "rail_operator": "Central Bank of Brazil (BCB)",
        "backstop": "⊤_pub",
        "velocity_note": "0 → 67% of adults in ~1 year (114M by 2021-11) ≈ 67pp/yr; ~91-93% by 2025",
        "velocity_pp_per_yr": 67.0, "fast": True,
        "app_top_share_pct": None,
        "app_level": "decentralized (runs in every bank/fintech app; no dominant front-end; exact shares unpublished)",
        "rail_level": "maximally concentrated (single BCB-operated rail)",
        "sources": ["Central Banking (62%/67% adult usage)", "BCB", "Wikipedia Pix", "paymentscmi.com"],
    },
    {
        "case": "India UPI", "rail_operator": "NPCI (bank consortium, RBI-adjacent)",
        "backstop": "⊤_bank (consortium)",
        "velocity_note": "2016 launch → hundreds of millions of users; ~13B tx/month by 2024-12; clearly fast (≥4pp/yr of adults)",
        "velocity_pp_per_yr": 5.0, "fast": True,
        "app_top_share_pct": 47.7,
        "app_level": "duopoly: PhonePe 47.7% + Google Pay 36.7% (top app <50%, top-2 ~85%) — borderline",
        "rail_level": "concentrated (single NPCI rail carries the bulk of retail digital payments)",
        "sources": ["NPCI Dec-2024 data via Statista / theheadandtale", "BusinessToday (30% cap debate)"],
    },
    {
        "case": "Kenya M-Pesa", "rail_operator": "Safaricom (single private telco)",
        "backstop": "⊤_priv",
        "velocity_note": "2007 launch → 68.7% of adults with mobile money by 2021 (Findex); historically fast",
        "velocity_pp_per_yr": 5.0, "fast": True,
        "app_top_share_pct": 96.5,
        "app_level": "concentrated (M-Pesa ~96.5% market share)",
        "rail_level": "concentrated (same single private operator)",
        "sources": ["WB API Findex 2021 (68.66%)", "market share ~96.5% (earlier-verified)"],
    },
]


def main():
    print("=" * 76)
    print("Out-of-region corner test — can 'fast AND decentralized' exist?")
    print("=" * 76)

    for c in CASES:
        print(f"\n[{c['case']}]  rail = {c['rail_operator']}  backstop = {c['backstop']}")
        print(f"  velocity : {c['velocity_note']}")
        print(f"  app level: {c['app_level']}")
        print(f"  rail level: {c['rail_level']}")

    app_corner_breakers = [c["case"] for c in CASES
                           if c["fast"] and (c["app_top_share_pct"] is None or c["app_top_share_pct"] < 50)]
    rail_corner_breakers = [c["case"] for c in CASES
                            if c["fast"] and "concentrated" not in c["rail_level"]]

    print("\n" + "-" * 76)
    print("VERDICT — the bound splits by measurement level:")
    print(f"  APP-level corner breakers (fast & no dominant app): {app_corner_breakers}")
    print("    → Pix is the fastest payment adoption in history with NO dominant")
    print("      front-end; UPI's top app is 47.7% (<50). The APP-level bound is DEAD.")
    print(f"  RAIL-level corner breakers: {rail_corner_breakers or 'なし — 角は空のまま'}")
    print("    → every fast adopter, in ASEAN and globally, rides a SINGLE shared")
    print("      rail. The RAIL-level bound survives — but near-definitionally")
    print("      (interoperable speed COMES FROM one rail), so it is a structural")
    print("      observation, not a daring prediction.")
    print("\nWhat fragility inherits (the refined structural conclusion):")
    print("  speed ⇒ one rail = one stalk (H¹/single-point story applies at rail level).")
    print("  The remaining degree of freedom is the rail's Heyting backstop:")
    print("    Pix ⊤_pub (central bank) / UPI consortium / M-Pesa ⊤_priv (private).")
    print("  i.e. you cannot choose 'no stalk', only WHO STANDS BEHIND the stalk.")

    bundle = {
        "description": (
            "Out-of-region corner test of the v×C bound (India UPI, Brazil Pix, "
            "Kenya M-Pesa). The bound's fate splits by the level at which "
            "concentration is measured: app-level bound FALSIFIED (Pix, UPI), "
            "rail-level bound survives near-definitionally. The refined conclusion: "
            "speed requires a single rail (one stalk); the free choice is the "
            "stalk's Heyting backstop — who pays when it fails."
        ),
        "cases": CASES,
        "app_level_bound": {
            "verdict": "FALSIFIED",
            "breakers": app_corner_breakers,
            "detail": "Pix: ~67pp/yr with no dominant app; UPI: top app 47.7% (<50).",
        },
        "rail_level_bound": {
            "verdict": "survives (near-definitional)",
            "breakers": rail_corner_breakers,
            "detail": "All fast adopters ride a single shared rail (BCB/NPCI/Safaricom/ITMX).",
        },
        "refined_structural_conclusion": (
            "v×C is not one claim but two: at the app level it is FALSE (Pix/UPI "
            "prove fast+plural front-ends), at the rail level it is TRUE but almost "
            "by construction. Fragility therefore cannot be avoided by app plurality "
            "— the single stalk remains; the only real choice is its Heyting "
            "backstop type (⊤_pub vs consortium vs ⊤_priv), which determines who "
            "absorbs the failure. This sharpens Finding 5 and reconnects to the "
            "sheaf/single-stalk analysis (notes/25) at the rail level."
        ),
        "honest_limits": (
            "Velocity units are not perfectly commensurable across cases (Findex pp/yr "
            "for ASEAN vs platform-user growth for Pix/UPI). Pix front-end shares are "
            "not centrally published (decentralization inferred from its in-every-"
            "bank-app design). UPI top app 47.7% is borderline vs the 50% threshold. "
            "Also: the Findex 'mobileaccount' indicator misses UPI/Pix (IND 10.4%, "
            "BRA 27.0% in 2021) because they are bank-rail systems — the indicator "
            "measures an account TYPE, not the payment function."
        ),
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "corner_test.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
