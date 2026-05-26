"""
Open H-Petri Net composition — numerical verification of Bottleneck Reversal.

Theory:
  notes/10 — Open Petri Net (cospan version, Baez-Master 2018, arXiv:1808.05415)
  notes/15 — Lattice-Valued Bottleneck Duality (Ghrist-Gould-Lopez 2024, arXiv:2410.00315)

This module implements the *operational core* of the Bottleneck Reversal Theorem
applied to ASEAN5 cross-border payment integration. Full cospan-pushout would
require carrying boundary morphisms; here we encode the two compositions that
matter for the claim:

  - parallel  (⊗): users pick their own backbone independently
                    → final Trust = join (max) over all backbones
  - cospan    (▷): all backbones must agree on the shared boundary place
                    (e.g. Project Nexus settlement hub)
                    → final Trust = meet (min) over all backbones

The theorem (Ghrist-Gould-Lopez 2024 applied to our 4-level Heyting algebra):
  join(⊤_pub, ⊤_bank, ⊤_priv, ⊤_priv) = ⊤_pub
  meet(⊤_pub, ⊤_bank, ⊤_priv, ⊤_priv) = ⊤_priv
  → Heyting rank gap = 2 (max distance in our 4-element lattice)

This is the "ASEAN cross-border integration paradox": joining strong + weak
backbones into a unified rail downgrades the whole system to the weakest.
"""

from __future__ import annotations
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from h_petri.core import FourLevelHA, fire_sequence, HPetriNet
from h_petri.backbones import bakong, paynow, kbzpay, gcash


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


STANDARD_TX_SEQUENCE = [
    "t1_InitiateSend",
    "t2_BackboneClear",
    "t3_Settle",
    "t4_Reconciliation",
    "t5_AcknowledgeReceipt",
]


# ---------------------------------------------------------------------------
# Open-Petri composition operators (operational form)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CompositionResult:
    operator: str                  # "⊗" or "▷"
    name: str                      # human-readable name
    components: tuple[str, ...]    # backbone names that were composed
    component_trusts: dict[str, str]
    final_trust: str               # the composed Heyting value
    final_load: str
    interpretation: str


def _simulate_one(builder, num_tx: int = 3) -> tuple[str, str]:
    """Run the standard CPN sequence and return (TrustHub, SystemicLoad) finals."""
    net: HPetriNet = builder()
    seq = STANDARD_TX_SEQUENCE * num_tx
    traj = fire_sequence(net, net.initial, seq)
    final = traj[-1]
    return final.invisible["TrustHub"], final.invisible["SystemicLoad"]


def compose_parallel(
    backbones: list[tuple[str, callable]],
    ha: FourLevelHA,
    num_tx: int = 3,
) -> CompositionResult:
    """⊗ — parallel composition. User chooses ANY backbone → strongest wins (join)."""
    trusts: dict[str, str] = {}
    loads: dict[str, str] = {}
    for name, builder in backbones:
        t, l = _simulate_one(builder, num_tx=num_tx)
        trusts[name] = t
        loads[name] = l

    join_trust = ha.bottom
    for v in trusts.values():
        join_trust = ha.join(join_trust, v)
    join_load = ha.bottom
    for v in loads.values():
        join_load = ha.join(join_load, v)

    return CompositionResult(
        operator="⊗",
        name="Parallel (user picks any backbone)",
        components=tuple(name for name, _ in backbones),
        component_trusts=trusts,
        final_trust=join_trust,
        final_load=join_load,
        interpretation=(
            f"ユーザーは {len(backbones)} 個の backbone を自由に選べるので、"
            f"全体の Trust は最強の backbone に支配される (join)。最終 Trust = {join_trust}。"
        ),
    )


def compose_cospan(
    backbones: list[tuple[str, callable]],
    ha: FourLevelHA,
    num_tx: int = 3,
    shared_place: str = "SettlementHub",
) -> CompositionResult:
    """▷ — cospan composition over a shared place. All backbones must agree → meet."""
    trusts: dict[str, str] = {}
    loads: dict[str, str] = {}
    for name, builder in backbones:
        t, l = _simulate_one(builder, num_tx=num_tx)
        trusts[name] = t
        loads[name] = l

    meet_trust = ha.top
    for v in trusts.values():
        meet_trust = ha.meet(meet_trust, v)
    meet_load = ha.top
    for v in loads.values():
        meet_load = ha.meet(meet_load, v)

    return CompositionResult(
        operator="▷",
        name=f"Cospan over '{shared_place}' (Project-Nexus-style integration)",
        components=tuple(name for name, _ in backbones),
        component_trusts=trusts,
        final_trust=meet_trust,
        final_load=meet_load,
        interpretation=(
            f"全 backbone が共通の決済 hub '{shared_place}' で同期するので、"
            f"Trust は最弱の backbone に律速される (meet)。最終 Trust = {meet_trust}。"
        ),
    )


# ---------------------------------------------------------------------------
# Main — ASEAN4 (Bakong / PayNow / KBZPay / GCash) Bottleneck Reversal
# ---------------------------------------------------------------------------

def main():
    ha = FourLevelHA()

    asean4 = [
        ("Bakong (KH, ⊤_pub central bank)", bakong.build_bakong_net),
        ("PayNow (SG, ⊤_bank consortium)",  paynow.build_paynow_net),
        ("KBZPay (MM, ⊤_bank single)",      kbzpay.build_kbzpay_net),
        ("GCash (PH, ⊤_priv private)",      gcash.build_gcash_net),
    ]

    parallel = compose_parallel(asean4, ha, num_tx=3)
    cospan   = compose_cospan(asean4, ha, num_tx=3, shared_place="ASEANSettlementHub")

    rank_gap = ha._rank(parallel.final_trust) - ha._rank(cospan.final_trust)

    bundle = {
        "description": (
            "Open H-Petri Net composition for ASEAN4 cross-border payment integration. "
            "Verifies the Bottleneck Reversal Theorem (notes/15, Ghrist-Gould-Lopez "
            "2024) numerically: parallel composition (⊗) is bounded by the join (max), "
            "cospan composition (▷) is bounded by the meet (min). The Heyting rank "
            "difference gives the 'integration paradox' cost."
        ),
        "components": [
            {"name": name, "trust": parallel.component_trusts[name]}
            for name, _ in asean4
        ],
        "parallel_otimes": {
            "operator": parallel.operator,
            "name": parallel.name,
            "final_trust": parallel.final_trust,
            "final_load": parallel.final_load,
            "interpretation": parallel.interpretation,
        },
        "cospan_triangleright": {
            "operator": cospan.operator,
            "name": cospan.name,
            "final_trust": cospan.final_trust,
            "final_load": cospan.final_load,
            "interpretation": cospan.interpretation,
        },
        "bottleneck_reversal": {
            "parallel_bound": parallel.final_trust,
            "cospan_bound":   cospan.final_trust,
            "rank_gap":       rank_gap,
            "lesson": (
                "同じ 4 backbone でも、合成方向で律速が逆転する。"
                f"⊗ 並列 = {parallel.final_trust} (最強 Bakong に支配)、"
                f"▷ 統合 = {cospan.final_trust} (最弱 GCash に律速)。"
                f"Heyting 階数差 = {rank_gap}。"
                "ASEAN 域内決済統合 (Project Nexus 等) は構造的に脆弱性を増やすという反直観的予言。"
            ),
        },
    }

    print("=" * 70)
    print("Open H-Petri Net composition — ASEAN4 Bottleneck Reversal")
    print("=" * 70)
    print(f"\nComponents (TrustHub finals):")
    for c in bundle["components"]:
        print(f"  {c['name']:50s} → {c['trust']}")

    print(f"\n⊗ Parallel:  {parallel.final_trust}  ({parallel.name})")
    print(f"▷ Cospan:    {cospan.final_trust}  ({cospan.name})")
    print(f"Rank gap:    {rank_gap}")
    print(f"\n{bundle['bottleneck_reversal']['lesson']}")

    out_path = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "open_petri_composition.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
