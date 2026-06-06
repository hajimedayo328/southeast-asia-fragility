"""
Data-grounded backbone Trust levels (the (b) -> (c) promotion).

The four backbone TrustHub Heyting levels used everywhere in this project
(Bakong=⊤_pub, PayNow=⊤_bank, KBZPay=⊤_bank, GCash=⊤_priv) were ORIGINALLY
author-assigned. Here we re-derive them from:

  1. DOCUMENTED institutional facts (operator + regulatory status), each with a
     source URL — verified via web search 2026-06-06.
  2. A SINGLE explicit rule mapping "legal backing tier" -> Heyting level.

So the level is no longer a vibe: given the (checkable) facts and the (stated)
rule, the level follows deterministically. Anyone can audit either input.

What this DOES establish: the foundational TrustHub levels are reproducible
from sourced facts + an explicit rule, and they MATCH the prior assignment
(so the earlier work is vindicated, not overturned).
What it does NOT establish: that this particular 4-tier rule is the only
reasonable one. The rule itself is a transparent modelling choice.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from h_petri.core import FourLevelHA

HA = FourLevelHA()


# ---------------------------------------------------------------------------
# 1. Documented facts (verified 2026-06-06 via web search; sources included)
# ---------------------------------------------------------------------------

FACTS = {
    "bakong": {
        "name": "Bakong (Cambodia)",
        "operator": "National Bank of Cambodia (the central bank)",
        "ownership": "State / central bank",
        "regulator": "National Bank of Cambodia (operator = regulator)",
        "backing_tier": "central_bank",
        "notes": "Launched Oct 2020 by NBC as the national payments backbone "
                 "(built with Soramitsu on Hyperledger Iroha).",
        "sources": [
            "https://bakong.nbc.gov.kh/en/",
            "https://www.weforum.org/stories/2021/08/cambodias-digital-currency-ishowing-other-central-banks-the-way/",
        ],
    },
    "paynow": {
        "name": "PayNow (Singapore)",
        "operator": "Participating banks via the Association of Banks in Singapore (ABS)",
        "ownership": "Bank consortium",
        "regulator": "Monetary Authority of Singapore; deposits insured by SDIC up to S$100,000",
        "backing_tier": "bank_with_deposit_insurance",
        "notes": "All full banks in Singapore are mandatory members of the SDIC "
                 "Deposit Insurance Scheme; PayNow rides on those insured bank deposits.",
        "sources": [
            "https://www.abs.org.sg/e-payments/pay-now",
            "https://www.sdic.org.sg/di_overview/",
        ],
    },
    "kbzpay": {
        "name": "KBZPay (Myanmar)",
        "operator": "KBZ Bank (Myanmar's largest privately-owned bank)",
        "ownership": "Single private bank",
        "regulator": "Central Bank of Myanmar (banking licence). Deposit-insurance "
                     "strength NOT established/weak; post-2021 political risk.",
        "backing_tier": "licensed_private_bank",
        "notes": "Licensed bank (so banking-law tier) but a SINGLE private bank "
                 "without the deposit-insurance strength of PayNow — weaker ⊤_bank.",
        "sources": [
            "https://www.kbzpay.com/en/about",
            "https://www.kbzbank.com/en/blog/news-en/kbz-bank-introduces-kbzpay-bringing-a-new-digital-wallet-and-p2p-transactions-to-the-masses-across-myanmar/",
        ],
    },
    "gcash": {
        "name": "GCash (Philippines)",
        "operator": "G-Xchange, Inc. (subsidiary of Mynt / Globe Fintech Innovations)",
        "ownership": "Private JV: Ant Group + Ayala Corporation + Globe Telecom",
        "regulator": "BSP-licensed NON-BANK Electronic Money Issuer (EMI-NBFI)",
        "backing_tier": "non_bank_emi",
        "notes": "Not a bank; a private e-money issuer. No bank-grade deposit "
                 "insurance on the e-money float.",
        "sources": [
            "https://en.wikipedia.org/wiki/GCash",
            "https://www.bsp.gov.ph/Lists/Directories/Attachments/7/emi.pdf",
        ],
    },
}


# ---------------------------------------------------------------------------
# 2. The single explicit rule:  legal backing tier  ->  Heyting level
# ---------------------------------------------------------------------------

BACKING_RULE = {
    "central_bank":                HA.T_PUB,   # sovereign / central-bank guarantee
    "bank_with_deposit_insurance": HA.T_BANK,  # banking law + deposit insurance
    "licensed_private_bank":       HA.T_BANK,  # banking licence (weaker: single, no DI)
    "non_bank_emi":                HA.T_PRIV,  # private company guarantee only
    "none":                        HA.BOTTOM,  # no formal backing
}

# What the project assigned BEFORE this grounding (to check for agreement).
PRIOR_ASSIGNMENT = {
    "bakong": HA.T_PUB,
    "paynow": HA.T_BANK,
    "kbzpay": HA.T_BANK,
    "gcash":  HA.T_PRIV,
}


def derive_level(key: str) -> str:
    return BACKING_RULE[FACTS[key]["backing_tier"]]


def main():
    print("=" * 72)
    print("Backbone TrustHub levels — DATA-GROUNDED derivation")
    print("(fact + explicit rule -> level), verified 2026-06-06")
    print("=" * 72)

    rows = []
    all_match = True
    for key, fact in FACTS.items():
        derived = derive_level(key)
        prior = PRIOR_ASSIGNMENT[key]
        match = derived == prior
        all_match = all_match and match
        rows.append({
            "backbone": fact["name"],
            "operator": fact["operator"],
            "backing_tier": fact["backing_tier"],
            "derived_level": derived,
            "prior_assignment": prior,
            "agrees": match,
            "sources": fact["sources"],
            "notes": fact["notes"],
        })
        print(f"\n[{fact['name']}]")
        print(f"  operator:     {fact['operator']}")
        print(f"  backing tier: {fact['backing_tier']}")
        print(f"  rule -> level: {derived}   (prior author-assigned: {prior})   "
              f"{'✓ agree' if match else '✗ DIFFERS'}")
        print(f"  sources: {', '.join(fact['sources'])}")

    print("\n" + "-" * 72)
    print(f"All data-derived levels agree with the prior assignment: {all_match}")
    if all_match:
        print("=> The foundational TrustHub levels are vindicated by sourced facts.")
        print("   They are now (c)-grade: reproducible from documented facts + an")
        print("   explicit rule, not author vibes.")

    bundle = {
        "description": (
            "Data-grounded derivation of the four backbone TrustHub Heyting levels. "
            "Each backing tier comes from a documented institutional fact (operator + "
            "regulator), source-cited and verified 2026-06-06. A single explicit rule "
            "maps the tier to a Heyting level. This promotes the levels from "
            "author-assigned (b) to reproducible-from-sourced-facts (c)."
        ),
        "backing_rule": {k: v for k, v in BACKING_RULE.items()},
        "backbones": rows,
        "all_agree_with_prior": all_match,
        "honest_limits": (
            "What is grounded: operator/regulator facts (sourced) and the "
            "deterministic tier->level mapping. What remains a modelling choice: "
            "the 4-tier rule itself (e.g. treating a single licensed private bank "
            "and a deposit-insured bank consortium both as ⊤_bank). KBZPay is the "
            "weakest ⊤_bank (single bank, weak/unverified deposit insurance, "
            "political risk) — flagged in its notes, not silently equated to PayNow."
        ),
    }
    out_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "backbone_trust_grounding.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
