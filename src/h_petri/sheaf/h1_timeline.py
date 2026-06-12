"""
H¹ time-derivative test — is H¹ a LEADING indicator (前兆) or a COINCIDENT one?

notes/25 made two temporal claims that were never tested:
  §3.2/§6.1  "H¹ の急増が伝染の前兆 or 同時指標" (left as an either/or)
  §6.1-6.2   "H¹ の time-derivative が予言可能性を測る" (proposed validation:
             correlate with the lag-shrinkage trend)

This script settles the first and retires the second:

  - The second claim's validation target (the lag-shrinkage trend) was
    WITHDRAWN on 2026-06-12 (truncation artifact, see notes/20 §10.8), so the
    time-derivative-measures-predictability hypothesis currently has nothing
    to be validated against → RETIRED until a better target exists.

  - The first claim is testable INSIDE the model using the (c)-grade textbook
    chronology of the 1997-98 contagion (the ORDERING is unimpeachable):
        1997-07  Thailand floats the baht        (crisis onset)
        1997-08  Indonesia floats the rupiah
        1997-11/12  Korea crisis (IMF deal Dec 1997)
        1998-09  Malaysia imposes capital controls
    We compute H¹ on a monthly-grained snapshot sequence. The question:
    does H¹ move BEFORE 1997-07?  By the model's construction it cannot —
    H¹ only changes when a Trust value changes, and Trust values change at
    the documented events. So within this model H¹ is a COINCIDENT contagion
    meter, and the '前兆' (leading) reading has NO support. Claiming
    otherwise would require an input signal that precedes the crisis, which
    the model does not have. This is an internal-consistency verification
    (like the Kan adjunction checks): even granting the author-assigned Trust
    values, the leading-indicator reading does not follow.
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
B, PRIV, BANK = HA.bottom, HA.T_PRIV, HA.T_BANK

CX = Complex(
    nodes=("TH", "MY", "ID", "PH", "KR", "SG"),
    edges=(("TH", "MY"), ("TH", "ID"), ("TH", "PH"), ("MY", "ID"), ("MY", "SG"),
           ("ID", "PH"), ("KR", "TH"), ("KR", "MY"), ("KR", "ID"), ("SG", "ID")),
)

# Monthly-grained snapshots. Trust LEVELS are author-assigned (b) as before;
# the TIMING/ORDERING is textbook chronology (c).
TIMELINE = [
    ("1996-12 (baseline)",            {"TH": BANK, "MY": BANK, "ID": BANK, "PH": BANK, "KR": BANK, "SG": BANK}),
    ("1997-03 (pre-crisis)",          {"TH": BANK, "MY": BANK, "ID": BANK, "PH": BANK, "KR": BANK, "SG": BANK}),
    ("1997-06 (eve of crisis)",       {"TH": BANK, "MY": BANK, "ID": BANK, "PH": BANK, "KR": BANK, "SG": BANK}),
    ("1997-07 (THB floats — onset)",  {"TH": PRIV, "MY": BANK, "ID": BANK, "PH": BANK, "KR": BANK, "SG": BANK}),
    ("1997-08 (IDR floats)",          {"TH": PRIV, "MY": BANK, "ID": PRIV, "PH": BANK, "KR": BANK, "SG": BANK}),
    ("1997-12 (KR crisis / IMF)",     {"TH": PRIV, "MY": PRIV, "ID": PRIV, "PH": PRIV, "KR": PRIV, "SG": BANK}),
    ("1998-06 (ID collapse deepens)", {"TH": PRIV, "MY": PRIV, "ID": B,    "PH": PRIV, "KR": PRIV, "SG": BANK}),
    ("1998-09 (MY capital controls)", {"TH": PRIV, "MY": PRIV, "ID": B,    "PH": PRIV, "KR": PRIV, "SG": BANK}),
]

# Malaysia's capital controls cut its edges out of the sheaf (notes/25 §3.4)
CX_AFTER_CONTROLS = Complex(
    nodes=CX.nodes,
    edges=tuple(e for e in CX.edges if "MY" not in e),
)


def main():
    print("=" * 76)
    print("H¹ timeline — leading indicator (前兆) or coincident meter (同時指標)?")
    print("=" * 76)
    print("\nTrust levels: author-assigned (b). Timing/ordering: textbook chronology (c).")
    print(f"\n{'snapshot':34s} {'H¹':>4s} {'ΔH¹':>5s}  H⁰(meet)")

    onset_index = 3  # 1997-07
    rows = []
    prev = None
    for i, (label, stalks) in enumerate(TIMELINE):
        cx = CX_AFTER_CONTROLS if "capital controls" in label else CX
        h1 = len(h1_inconsistent_edges(cx, stalks))
        d = None if prev is None else h1 - prev
        rows.append({"snapshot": label, "h1": h1, "delta_h1": d,
                     "h0_meet": h0(stalks, HA)})
        print(f"{label:34s} {h1:4d} {('' if d is None else f'{d:+d}'):>5s}  {h0(stalks, HA)}")
        prev = h1

    pre_onset_movement = any(r["delta_h1"] not in (None, 0) for r in rows[:onset_index])
    print("\n" + "-" * 76)
    print(f"H¹ moved BEFORE the 1997-07 onset?  {'YES' if pre_onset_movement else 'NO — H¹ is flat (0) through 1996-12, 1997-03, 1997-06'}")
    print("VERDICT:")
    print("  ・モデル内で H¹ は『同時指標 (coincident contagion meter)』。")
    print("    最初の上昇は危機の発火 (1997-07) と同時で、それ以前には一切動かない。")
    print("  ・notes/25 §3.2 の『前兆 or 同時指標』の either/or は『同時指標』側に確定。")
    print("    『前兆』を主張するには危機に先行する入力信号が必要だが、本モデルには無い。")
    print("  ・notes/25 §6 の『H¹ の time-derivative が予言可能性を測る』仮説は、")
    print("    検証先だったラグ縮小トレンドが撤回済み (notes/20 §10.8) のため RETIRED。")

    bundle = {
        "description": (
            "H¹ timeline over the documented 1997-98 contagion chronology. Settles "
            "notes/25's open either/or: within the model H¹ is a COINCIDENT "
            "contagion meter, not a leading indicator — it never moves before the "
            "1997-07 onset. The time-derivative-predictability hypothesis is "
            "retired (its validation target, the lag trend, was withdrawn)."
        ),
        "timeline": rows,
        "h1_moved_before_onset": pre_onset_movement,
        "verdict": {
            "leading_indicator": False,
            "coincident_meter": True,
            "time_derivative_hypothesis": "RETIRED (validation target withdrawn 2026-06-12)",
        },
        "honest_limits": (
            "Trust levels are author-assigned (b); only the event ORDERING is "
            "(c)-grade chronology. The conclusion is about the model's logical "
            "structure: even granting the assignments, the leading reading does "
            "not follow. A real leading-indicator test would need a pre-crisis "
            "observable (e.g. short-term external debt ratios) mapped to Trust — "
            "future work, and notes/25 §3.1's '見かけは安定' hints at it but no "
            "such input exists in the model today."
        ),
    }
    out = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "h1_timeline.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
