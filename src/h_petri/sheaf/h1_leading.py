"""
H¹ as a LEADING indicator — resolving yesterday's future-work item.

h1_timeline.py established: with MARKET-VISIBLE Trust inputs, H¹ is a
coincident meter (it cannot move before the crisis because nothing in the
input does). The open question was whether a PRE-CRISIS observable could make
it leading. This script wires one in:

  OBSERVABLE: short-term external debt / FX reserves, END-JUNE 1997
  (RBA RDP 9805 Table 9, BIS-based; verified 2026-06-13):
      KR 3.0, ID 1.6, TH 1.1, MY 0.6, PH 0.7
  RULE: the Guidotti–Greenspan rule — reserves should cover short-term
  external debt (ratio ≤ 1). A NAMED standard from the early-warning
  literature, not an author-invented threshold.

  MAPPING: ratio > 1  →  effective (fundamentals-adjusted) Trust = ⊤_priv
           ("nominally ⊤_bank but liquidity reality is private-grade" —
            this operationalizes the project's own '⊤_priv が ⊤_bank を
            演じる' narrative with data)
           ratio ≤ 1  →  ⊤_bank

  TEST: compute H¹ at end-June 1997 (BEFORE the July 2 baht float) on
  (a) nominal stalks (all ⊤_bank)            → expect H¹ = 0
  (b) fundamentals-adjusted stalks            → expect H¹ > 0
  The adjusted-vs-nominal gap = hidden inconsistency measurable pre-crisis.

HONESTY CONSTRAINTS (stated up front):
  - RETRODICTION, not prediction: the Guidotti–Greenspan rule was formalized
    in 1999, AFTER (and partly because of) this crisis. So the claim is
    "fed this observable and rule, H¹ lights up pre-crisis", NOT "we would
    have predicted 1997 in real time".
  - One episode; no false-positive analysis (countries/years where adjusted
    H¹ was high but no crisis followed) — that's what a real early-warning
    validation would need.
  - SG is not in RBA Table 9; assigned ratio<1 (Singapore's reserves famously
    dwarf its short-term debt) — flagged as an assumption.
  - BIS data is published with a lag; 'end-June 1997' values weren't on desks
    on July 1. The fundamentals existed; the data product lagged.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from h_petri.core import FourLevelHA
from h_petri.sheaf.cech import Complex, h1_inconsistent_edges, h0

HA = FourLevelHA()
PRIV, BANK = HA.T_PRIV, HA.T_BANK

CX = Complex(
    nodes=("TH", "MY", "ID", "PH", "KR", "SG"),
    edges=(("TH", "MY"), ("TH", "ID"), ("TH", "PH"), ("MY", "ID"), ("MY", "SG"),
           ("ID", "PH"), ("KR", "TH"), ("KR", "MY"), ("KR", "ID"), ("SG", "ID")),
)

# Short-term external debt / reserves, end-June 1997 (RBA RDP 9805 Table 9).
RATIOS_JUN97 = {"TH": 1.1, "ID": 1.6, "KR": 3.0, "MY": 0.6, "PH": 0.7,
                "SG": 0.2}   # SG: not in Table 9; assumption (reserves >> short-term debt), flagged

GG_THRESHOLD = 1.0  # Guidotti–Greenspan rule


def main():
    nominal = {c: BANK for c in CX.nodes}
    adjusted = {c: (PRIV if RATIOS_JUN97[c] > GG_THRESHOLD else BANK) for c in CX.nodes}

    h1_nominal = h1_inconsistent_edges(CX, nominal)
    h1_adjusted = h1_inconsistent_edges(CX, adjusted)

    print("=" * 76)
    print("H¹ leading-indicator construction — end-June 1997, BEFORE the baht float")
    print("=" * 76)
    print("\n観測量: 短期外債/外貨準備 (1997-06末, RBA RDP9805 Table 9 / BIS):")
    for c in CX.nodes:
        flag = "⚠ >1 (Guidotti-Greenspan 違反)" if RATIOS_JUN97[c] > 1 else "OK"
        note = " (SG: Table 9 に無し、仮定)" if c == "SG" else ""
        print(f"  {c}: {RATIOS_JUN97[c]:4.1f}  {flag}{note}")

    print(f"\n(a) 名目 Trust (市場に見えていた姿、全員 ⊤_bank):  H¹ = {len(h1_nominal)}")
    print(f"(b) 実態調整 Trust (比率>1 → 実効 ⊤_priv):           H¹ = {len(h1_adjusted)}")
    print("    不整合エッジ(= 脆弱国と健全国の境界):")
    for a, va, b, vb in h1_adjusted:
        print(f"      {a}({va}) — {b}({vb})")

    gap = len(h1_adjusted) - len(h1_nominal)
    print(f"\n隠れた不整合ギャップ (adjusted − nominal) = {gap}")
    print("\n" + "-" * 76)
    print("VERDICT:")
    print(f"  ・ファンダメンタルズ入力なら、H¹ は発火**前**(1997-06)に既に {len(h1_adjusted)} 本")
    print("    立っていた — 昨日の『同時指標』は市場可視入力での結論で、観測量を")
    print("    Guidotti-Greenspan ルールで Trust に繋げば H¹ は**先行指標化できる**。")
    print("  ・不整合エッジは『比率>1 国 (TH/ID/KR) と <1 国 (MY/PH/SG) の境界』に立つ —")
    print("    これは実際の伝染経路・被害の濃淡 (KR/ID/TH 重傷、MY/PH 相対的に軽傷) と整合。")
    print("  ・ただし RETRODICTION: G-G ルールは1999年(危機後)に定式化されたもの。")
    print("    『当時リアルタイムで予言できた』とは主張しない。文献ベースの偽陽性分析は")
    print("    empirical/false_positive_test.py で実施(MY が in-sample 偽陰性)。真の偽陽性")
    print("    (高比率で危機が来なかった国・年)は非危機国パネルが必要で、なお未実施。")

    bundle = {
        "description": (
            "H¹ leading-indicator construction. Feeding a documented pre-crisis "
            "observable (short-term debt/reserves, end-June 1997, RBA RDP9805/BIS) "
            "through the named Guidotti-Greenspan rule (ratio<=1) into the Trust "
            "sheaf makes H¹ light up BEFORE the July 1997 onset (6 inconsistent "
            "edges vs 0 nominal) — exactly on the vulnerable/sound boundary."
        ),
        "observable": {"ratios_jun97": RATIOS_JUN97,
                       "source": "RBA RDP 9805 Table 9 (BIS-based), verified 2026-06-13",
                       "rule": "Guidotti-Greenspan (ratio <= 1), formalized 1999",
                       "sg_caveat": "SG not in Table 9; ratio<1 assumed (flagged)"},
        "h1_nominal_jun97": len(h1_nominal),
        "h1_adjusted_jun97": len(h1_adjusted),
        "hidden_inconsistency_gap": gap,
        "adjusted_edges": [{"a": a, "va": va, "b": b, "vb": vb}
                           for a, va, b, vb in h1_adjusted],
        "verdict": (
            "H¹ CAN be made leading when fed fundamentals through the G-G rule: "
            "adjusted H¹ = 6 pre-onset vs nominal 0, and the inconsistent edges "
            "sit on the vulnerable/sound boundary, consistent with the actual "
            "contagion severity pattern (KR/ID/TH severe, MY/PH milder). "
            "Yesterday's 'coincident' verdict stands for market-visible inputs."
        ),
        "honest_limits": (
            "Retrodiction (G-G rule postdates the crisis); one episode; "
            "false-positive analysis now done (empirical/false_positive_test.py: "
            "Malaysia is an in-sample FALSE NEGATIVE; true FP rate still needs a "
            "non-crisis panel); BIS publication lag; SG ratio assumed; "
            "the Trust mapping (ratio>1 -> effective T_priv) is one chosen rule, "
            "though a NAMED one from the early-warning literature rather than "
            "author-tuned."
        ),
    }
    out = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "h1_leading.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
