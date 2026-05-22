"""
Run Bakong vs GCash H-Petri Net comparison.

Output:
  - stdout summary
  - JSON written to docs/data/petri_comparison.json (for HTML viz later)
"""

from __future__ import annotations
import json
import os
import sys
from pathlib import Path

# Force UTF-8 stdout on Windows (cp932 can't render ⊤ etc.)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# allow running both as `python -m h_petri.compare` and `python compare.py`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from h_petri.core import fire_sequence, trust_reached_at, systemic_load_curve, FourLevelHA
from h_petri.backbones import bakong as bakong_mod
from h_petri.backbones import gcash as gcash_mod


def simulate(net, sequence: list[str]):
    return fire_sequence(net, net.initial, sequence)


def summarize(name: str, trajectory, ha: FourLevelHA) -> dict:
    final = trajectory[-1]
    trust_at_pub = trust_reached_at(trajectory, "TrustHub", ha.T_PUB, ha)
    trust_at_bank = trust_reached_at(trajectory, "TrustHub", ha.T_BANK, ha)
    trust_at_priv = trust_reached_at(trajectory, "TrustHub", ha.T_PRIV, ha)

    return {
        "name": name,
        "steps": len(trajectory) - 1,
        "final_visible": dict(final.visible),
        "final_invisible": dict(final.invisible),
        "trust_reached_T_PRIV_at_step": trust_at_priv,
        "trust_reached_T_BANK_at_step": trust_at_bank,
        "trust_reached_T_PUB_at_step":  trust_at_pub,
        "systemic_load_curve_ranks": systemic_load_curve(trajectory, "SystemicLoad", ha),
        "trust_curve_ranks": systemic_load_curve(trajectory, "TrustHub", ha),
    }


def run(num_tx: int = 3):
    """Run num_tx send transactions for both backbones and compare."""
    ha = FourLevelHA()

    bakong_net = bakong_mod.build_bakong_net(initial_balance=1000, send_amount=10)
    gcash_net = gcash_mod.build_gcash_net(initial_balance=1000, send_amount=10)

    bakong_seq = bakong_mod.STANDARD_TX_SEQUENCE * num_tx
    gcash_seq = gcash_mod.STANDARD_TX_SEQUENCE * num_tx

    bakong_traj = simulate(bakong_net, bakong_seq)
    gcash_traj = simulate(gcash_net, gcash_seq)

    bakong_summary = summarize(bakong_net.name, bakong_traj, ha)
    gcash_summary = summarize(gcash_net.name, gcash_traj, ha)

    return {
        "config": {"num_transactions": num_tx, "send_amount": 10, "initial_balance": 1000},
        "bakong": bakong_summary,
        "gcash":  gcash_summary,
        "interpretation": {
            "trust_gap": (
                "Bakong reaches T_PUB in steps after the first BakongClear/Settle, "
                "while GCash never exceeds T_PRIV no matter how many transactions fire. "
                "This is the structural expression of the legal-protection gap."
            ),
            "key_observation": (
                "Identical sequence length, identical visible-layer behavior, "
                "but invisible (Heyting) layer ranks differ permanently."
            ),
        },
    }


def main():
    result = run(num_tx=3)

    print("=" * 60)
    print("Bakong vs GCash H-Petri Net comparison")
    print("=" * 60)
    for backbone in ("bakong", "gcash"):
        s = result[backbone]
        print(f"\n[{s['name']}]")
        print(f"  steps fired:                  {s['steps']}")
        print(f"  TrustHub reached T_PRIV at:   {s['trust_reached_T_PRIV_at_step']}")
        print(f"  TrustHub reached T_BANK at:   {s['trust_reached_T_BANK_at_step']}")
        print(f"  TrustHub reached T_PUB  at:   {s['trust_reached_T_PUB_at_step']}")
        print(f"  Final TrustHub:               {s['final_invisible']['TrustHub']}")
        print(f"  Final SystemicLoad:           {s['final_invisible']['SystemicLoad']}")
        print(f"  TrustHub rank curve:          {s['trust_curve_ranks']}")
        print(f"  SystemicLoad rank curve:      {s['systemic_load_curve_ranks']}")

    print("\n" + "-" * 60)
    print("Interpretation:")
    print("  " + result["interpretation"]["trust_gap"])
    print("  " + result["interpretation"]["key_observation"])

    # write JSON for HTML viz
    out_path = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "petri_comparison.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nWrote JSON output: {out_path}")


if __name__ == "__main__":
    main()
