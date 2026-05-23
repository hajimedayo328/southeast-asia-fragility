"""
4-backbone H-Petri Net comparison.

Compares Bakong (central bank) / GCash (private) / PayNow (bank consortium)
/ KBZPay (single-bank-dominant) using the common CPN spec (notes/07).

Output:
  - stdout summary (per-backbone trajectories + centrality)
  - JSON written to docs/data/petri_comparison.json for HTML viz.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

# Force UTF-8 stdout on Windows (cp932 can't render ⊤ etc.)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from h_petri.core import (
    fire_sequence,
    trust_reached_at,
    systemic_load_curve,
    FourLevelHA,
)
from h_petri.centrality import full_centrality_report
from h_petri.backbones import bakong as bakong_mod
from h_petri.backbones import gcash as gcash_mod
from h_petri.backbones import paynow as paynow_mod
from h_petri.backbones import kbzpay as kbzpay_mod


BACKBONES = [
    ("bakong",  bakong_mod,  "central_bank"),
    ("gcash",   gcash_mod,   "platform"),
    ("paynow",  paynow_mod,  "bank_consortium"),
    ("kbzpay",  kbzpay_mod,  "bank_single"),
]


def simulate(net, sequence):
    return fire_sequence(net, net.initial, sequence)


def summarize(name: str, btype: str, trajectory, ha: FourLevelHA, net) -> dict:
    final = trajectory[-1]
    trust_at_pub = trust_reached_at(trajectory, "TrustHub", ha.T_PUB, ha)
    trust_at_bank = trust_reached_at(trajectory, "TrustHub", ha.T_BANK, ha)
    trust_at_priv = trust_reached_at(trajectory, "TrustHub", ha.T_PRIV, ha)

    centrality = full_centrality_report(net, max_steps=20)

    return {
        "name": name,
        "backbone_type": btype,
        "steps": len(trajectory) - 1,
        "final_visible": dict(final.visible),
        "final_invisible": dict(final.invisible),
        "trust_reached_T_PRIV_at_step": trust_at_priv,
        "trust_reached_T_BANK_at_step": trust_at_bank,
        "trust_reached_T_PUB_at_step":  trust_at_pub,
        "systemic_load_curve_ranks": systemic_load_curve(trajectory, "SystemicLoad", ha),
        "trust_curve_ranks": systemic_load_curve(trajectory, "TrustHub", ha),
        "centrality": centrality,
    }


def run(num_tx: int = 3):
    ha = FourLevelHA()
    results = {}

    for key, mod, btype in BACKBONES:
        net = mod.__getattribute__(f"build_{key}_net")(initial_balance=1000, send_amount=10)
        seq = mod.STANDARD_TX_SEQUENCE * num_tx
        traj = simulate(net, seq)
        results[key] = summarize(net.name, btype, traj, ha, net)

    # Cross-backbone comparison
    trust_uppers = {k: results[k]["final_invisible"]["TrustHub"] for k in results}
    meet_value = "⊤_pub"
    join_value = "⊥"
    for v in trust_uppers.values():
        if ha._rank(v) < ha._rank(meet_value):
            meet_value = v
        if ha._rank(v) > ha._rank(join_value):
            join_value = v

    return {
        "config": {"num_transactions": num_tx, "send_amount": 10, "initial_balance": 1000},
        "backbones": results,
        # backward-compat top-level keys for the existing HTML viz
        "bakong": results.get("bakong"),
        "gcash":  results.get("gcash"),
        "bottleneck_reversal_demo": {
            "trust_uppers": trust_uppers,
            "monoidal_⊗_bound (max)":   join_value,
            "cospan_▷_bound  (meet)":  meet_value,
            "rank_gap": ha._rank(join_value) - ha._rank(meet_value),
            "interpretation": (
                "If the 4 backbones are placed side-by-side (⊗ = monoidal product), "
                "the strongest one carries the system → ⊤ = " + join_value + ". "
                "But if they are integrated into a cross-border system (▷ = cospan-pushout), "
                "the weakest one drags the rest down → ⊥' = " + meet_value + ". "
                "Same set, different composition direction, different bottleneck. "
                "(notes/15 Theorem: Bottleneck Reversal)"
            ),
        },
        "interpretation": {
            "trust_gap": (
                "4 backbone types reach different Heyting upper bounds: "
                "Bakong (central bank) → ⊤_pub, "
                "PayNow & KBZPay (bank) → ⊤_bank, "
                "GCash (platform) → ⊤_priv. "
                "Identical structural form (5 places + 2 invisible, 5 transitions), "
                "but invisible-layer caps differ permanently."
            ),
        },
    }


def main():
    result = run(num_tx=3)

    print("=" * 70)
    print("4-Backbone H-Petri Net Comparison")
    print("=" * 70)
    for key in ("bakong", "paynow", "kbzpay", "gcash"):
        s = result["backbones"][key]
        print(f"\n[{s['name']}]  type={s['backbone_type']}")
        print(f"  Steps fired:                  {s['steps']}")
        print(f"  TrustHub reached T_PRIV at:   {s['trust_reached_T_PRIV_at_step']}")
        print(f"  TrustHub reached T_BANK at:   {s['trust_reached_T_BANK_at_step']}")
        print(f"  TrustHub reached T_PUB  at:   {s['trust_reached_T_PUB_at_step']}")
        print(f"  Final TrustHub:               {s['final_invisible']['TrustHub']}")
        print(f"  Final SystemicLoad:           {s['final_invisible']['SystemicLoad']}")
        print(f"  HHI-AC (structural concentration): {s['centrality']['HHI_AC']}")

    print("\n" + "-" * 70)
    print("Bottleneck Reversal Demo (notes/15 Theorem):")
    br = result["bottleneck_reversal_demo"]
    print(f"  Trust uppers per backbone: {br['trust_uppers']}")
    print(f"  ⊗ (parallel, max bound):   {br['monoidal_⊗_bound (max)']}")
    print(f"  ▷ (composed, meet bound):  {br['cospan_▷_bound  (meet)']}")
    print(f"  Heyting rank gap:          {br['rank_gap']}")
    print(f"\n  {br['interpretation']}")

    # write JSON for HTML viz
    out_path = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "petri_comparison.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nWrote JSON output: {out_path}")


if __name__ == "__main__":
    main()
