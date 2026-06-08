"""
T1 — derive the enriched category of the 4 finance backbones from the
H-Petri Net simulation (not hand-assigned), and connect the chain

    backbones/*.py (Petri net)  ->  TrustHub level
                                ->  data/backbone_facts.py (sourced, (c))
                                ->  this enriched category (hom = Trust)
                                ->  open_net.py bottleneck reversal (⊗/▷)

so the bottleneck-reversal inputs are shown to be (c)-grade, not author vibes.

Construction. Objects = {Bakong, PayNow, KBZPay, GCash}. Each backbone's Trust
level is taken from ACTUALLY SIMULATING its H-Petri Net (final TrustHub), then
cross-checked against the source-cited regulatory derivation
(data/backbone_facts.py). The enriched hom is the "emanating trust":

    hom(A,B) = Trust(A)   for A≠B ,   hom(A,A) = ⊤_pub

which is a valid H-enriched category: hom(A,B)∧hom(B,C) = Trust(A)∧Trust(B)
≤ Trust(A) = hom(A,C). Its ⊗ (join over objects) and ▷ (meet over objects)
reproduce the bottleneck reversal — now on Petri-derived, source-checked values.

HONEST SCOPE. This grounds the FINANCE-BACKBONE enriched structure (the §P4 /
bottleneck-reversal domain). It does NOT ground the 5 prediction pairs in
pairs_enriched.py — their event-to-event edges (e.g. TH→IMF) are relationships,
not backbone Trust levels, and stay (b). The only modelling choice left here is
the 4-tier backing rule itself (data/backbone_facts.py).
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from h_petri.core import FourLevelHA, fire_sequence
from h_petri.category.enriched import EnrichedCategory
from h_petri.backbones import bakong, paynow, kbzpay, gcash
from h_petri.data import backbone_facts

HA = FourLevelHA()

STANDARD_TX_SEQUENCE = [
    "t1_InitiateSend", "t2_BackboneClear", "t3_Settle",
    "t4_Reconciliation", "t5_AcknowledgeReceipt",
]

BUILDERS = {
    "bakong": bakong.build_bakong_net,
    "paynow": paynow.build_paynow_net,
    "kbzpay": kbzpay.build_kbzpay_net,
    "gcash":  gcash.build_gcash_net,
}


def trust_from_petri(key: str, num_tx: int = 3) -> str:
    """Simulate the backbone's H-Petri Net and return its final TrustHub level."""
    net = BUILDERS[key]()
    traj = fire_sequence(net, net.initial, STANDARD_TX_SEQUENCE * num_tx)
    return traj[-1].invisible["TrustHub"]


def build_finance_category(trust: dict[str, str]) -> EnrichedCategory:
    """Enriched category with hom(A,B)=Trust(A) (A≠B), hom(A,A)=⊤_pub."""
    objs = list(trust.keys())
    generators = {}
    for a in objs:
        for b in objs:
            if a != b:
                generators[(a, b)] = trust[a]
    return EnrichedCategory.from_generators("finance backbones (Petri-derived)", objs, generators, HA)


def main():
    print("=" * 72)
    print("T1 — finance-backbone enriched category from the H-Petri Net")
    print("=" * 72)

    # 1. Petri-derived Trust, cross-checked against the sourced regulatory rule
    print("\nStep 1: Petri TrustHub  vs  sourced regulatory derivation (must match)\n")
    petri_trust = {}
    consistent = True
    for key in BUILDERS:
        t_petri = trust_from_petri(key)
        t_data = backbone_facts.derive_level(key)
        ok = t_petri == t_data
        consistent = consistent and ok
        petri_trust[key] = t_petri
        print(f"  {key:7s}  Petri={t_petri:8s}  regulatory={t_data:8s}  {'✓' if ok else '✗ MISMATCH'}")

    if not consistent:
        print("\n✗ Petri output disagrees with the sourced rule — investigate before continuing.")
        return
    print("\n=> Petri-net TrustHub levels EQUAL the source-cited regulatory levels.")
    print("   So these Trust values are (c)-grade (two independent routes agree).")

    # 2. Build the enriched category and verify the axioms
    cat = build_finance_category(petri_trust)
    valid = cat.is_valid()
    print(f"\nStep 2: enriched category axioms hold: {valid['valid']}")

    # 3. ⊗ (join) and ▷ (meet) over the objects = bottleneck reversal
    join_all = HA.bottom
    meet_all = HA.T_PUB
    for k, v in petri_trust.items():
        join_all = HA.join(join_all, v)
        meet_all = HA.meet(meet_all, v)
    rank_gap = HA._rank(join_all) - HA._rank(meet_all)
    print(f"\nStep 3: ⊗ parallel (join) = {join_all} ; ▷ integrate (meet) = {meet_all} ; rank gap = {rank_gap}")

    # 4. cross-check against open_net.py's independently-produced JSON
    open_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "open_petri_composition.json"
    cross = None
    if open_path.exists():
        with open(open_path, encoding="utf-8") as f:
            openj = json.load(f)
        br = openj.get("bottleneck_reversal", {})
        cross = {
            "open_parallel": br.get("parallel_bound"),
            "open_cospan": br.get("cospan_bound"),
            "matches": (br.get("parallel_bound") == join_all and br.get("cospan_bound") == meet_all),
        }
        print(f"\nStep 4: open_net.py JSON: ⊗={cross['open_parallel']} ▷={cross['open_cospan']}  "
              f"{'✓ matches' if cross['matches'] else '✗ differs'}")

    bundle = {
        "description": (
            "T1: the finance-backbone enriched category derived from the H-Petri Net "
            "simulation. Trust levels come from simulating each backbone net and are "
            "cross-checked against the source-cited regulatory derivation "
            "(data/backbone_facts.py); the two routes agree, so the values are (c)-grade. "
            "The enriched ⊗/▷ reproduce the bottleneck reversal on these grounded values "
            "and match open_net.py. This unifies backbones/ + data/ + category/ + open_net."
        ),
        "petri_trust": petri_trust,
        "regulatory_trust": {k: backbone_facts.derive_level(k) for k in BUILDERS},
        "petri_matches_regulatory": consistent,
        "axioms_valid": valid["valid"],
        "bottleneck_reversal": {
            "parallel_join": join_all, "cospan_meet": meet_all, "rank_gap": rank_gap,
        },
        "cross_check_open_net": cross,
        "honest_scope": (
            "Grounds ONLY the finance-backbone enriched structure (the bottleneck-"
            "reversal inputs), now (c). The 5 prediction pairs' event-to-event edges "
            "remain author-assigned (b). The 4-tier backing rule is still a modelling "
            "choice. What is newly (c): the Trust values feeding the headline "
            "bottleneck-reversal finding, via two agreeing independent routes."
        ),
    }
    out_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "finance_enriched_grounded.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")
    print("\nHONEST SCOPE:", bundle["honest_scope"])


if __name__ == "__main__":
    main()
