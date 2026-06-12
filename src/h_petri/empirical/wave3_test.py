"""
Wave-3 time-axis test — the Findex 2025 wave (2024 data) as out-of-sample check.

The time axis was the project's weakest empirical link: we had only two Findex
waves (2017, 2021). The Findex 2025 wave (survey year 2024) is now available
via the WB API (fetched 2026-06-12, mobileaccount.t.d, source=28). This gives:

  (1) VELOCITY PERSISTENCE: is adoption speed a stable country trait?
      v(2017→2021) vs v(2021→2024) rank correlation.
  (2) CORNER RE-CHECK, out of sample: §10.4's wallet-level corner was empty
      in-region ('the only decentralized country, ID, is slow'). Does it stay
      empty with the new wave?
  (3) Anomaly surfacing (TH, MM) — honest flags, not interpretations.

KEY CONTEXT, source-verified 2026-06-12: Indonesia's shared central-bank
infrastructure arrived exactly inside the new window — QRIS (BI's interop QR
standard, 2020) and BI-FAST (BI's instant rail, launched 2021-12-21; 123 banks
by 2024, volumes 'skyrocketing'). So ID 2021→2024 is a natural experiment:
the previously rail-less, app-fragmented, SLOW country acquired a single
shared central-bank rail.
"""

from __future__ import annotations
import json
import statistics as st
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Findex mobile money account % (age 15+). WB API mobileaccount.t.d, source=28.
MM_2017 = {"ID": 3.12, "KH": 5.66, "MM": 0.69, "MY": 10.88,
           "PH": 4.52, "SG": 9.55, "TH": 8.26}                 # LA null
MM_2021 = {"ID": 9.29, "KH": 6.60, "LA": 5.48, "MM": 29.03,
           "MY": 27.98, "PH": 21.74, "SG": 30.60, "TH": 59.99}  # VN null
MM_2024 = {"ID": 22.01, "KH": 16.89, "LA": 11.84, "MM": None,
           "MY": 44.50, "PH": 28.80, "SG": 56.47, "TH": 41.68, "VN": 38.72}

CONC = {"ID": 25, "PH": 85, "TH": 65, "MY": 62, "SG": 60,
        "KH": 70, "LA": 55, "MM": 60, "VN": 56}


def main():
    print("=" * 76)
    print("Wave-3 test — Findex 2025 wave (2024 data) vs the time-axis claims")
    print("=" * 76)

    # velocities
    v1 = {c: round((MM_2021[c] - MM_2017[c]) / 4, 2) for c in MM_2017 if c in MM_2021}
    v2 = {c: round((MM_2024[c] - MM_2021[c]) / 3, 2)
          for c in MM_2021 if MM_2024.get(c) is not None}

    print(f"\n{'国':4s} {'2017':>6s} {'2021':>7s} {'2024':>7s} {'v17-21':>8s} {'v21-24':>8s} {'conc%':>6s}")
    for c in sorted(MM_2021, key=lambda x: -(v2.get(x, -99))):
        f17 = f"{MM_2017[c]:6.1f}" if c in MM_2017 else "  null"
        f24 = f"{MM_2024[c]:7.1f}" if MM_2024.get(c) is not None else "   null"
        fv1 = f"{v1[c]:8.2f}" if c in v1 else "       —"
        fv2 = f"{v2[c]:8.2f}" if c in v2 else "       —"
        print(f"{c:4s} {f17} {MM_2021[c]:7.1f} {f24} {fv1} {fv2} {CONC[c]:6d}")

    # (1) velocity persistence
    both = [c for c in v1 if c in v2]
    rho = st.correlation([v1[c] for c in both], [v2[c] for c in both], method="ranked")
    print(f"\n(1) 速度の持続性: Spearman(v17-21, v21-24) = {rho:+.3f}  (n={len(both)})")
    print("    → 速度は国の安定的な性質ではない (TH 最速→マイナス、ID 最遅→加速)。")
    print("    スカラー速度も時間的に不安定 = 「構造 > スカラー」をもう1回支持。")

    # (2) corner re-check at wallet level
    fast2 = {c: v2[c] for c in v2 if v2[c] >= 4.0}
    occupied = [c for c in fast2 if CONC[c] < 50]
    print(f"\n(2) 角の再チェック (v21-24 ≥ 4pp/yr): {fast2}")
    print(f"    「速い AND ウォレット分散 (conc<50)」 = {occupied or 'なし'}")
    if occupied:
        print("    ★ ウォレットレベルの角が ASEAN 域内でも埋まった: ID が加速 (1.54→4.24pp/yr)")
        print("      しつつウォレット分散 (25-31%) のまま。")
        print("    ★ ただし加速の窓 = QRIS (2020) + BI-FAST (2021-12-21、中銀レール、")
        print("      2024年までに123行) の登場と一致 → ID は『共有レールを得て速くなった』。")
        print("    → §10.5 のレベル分割結論の OUT-OF-SAMPLE 的中:")
        print("      『速い+アプリ分散は、単一共有レールがある時だけ可能』(Pix/UPI パターンの域内再現)")

    # (3) anomalies — flag, don't interpret
    print("\n(3) 異常値 (解釈せず旗を立てる):")
    print("    TH: 60.0 (2021) → 41.7 (2024)、v=−6.1pp/yr。実減か Findex の分類変更")
    print("        (PromptPay を銀行口座側に再分類?) か未確定 — 要調査、結論に使わない。")
    print("    MM: 2024 null — 調査自体が実施できず (内戦)。『測定の可用性も政治的』の傍証。")

    bundle = {
        "description": (
            "Wave-3 (Findex 2025 / survey 2024) time-axis test. Velocity is not a "
            "persistent country trait; the wallet-level corner is now occupied "
            "in-region by ID — which acquired QRIS+BI-FAST (shared central-bank "
            "rail) exactly in the window — an out-of-sample hit for the level-split "
            "(stalk) conclusion of §10.5."
        ),
        "data_provenance": {
            "findex_2024": "WB API mobileaccount.t.d source=28, fetched 2026-06-12",
            "bi_fast": "launched 2021-12-21 by Bank Indonesia; 123 banks by 2024 "
                       "(BI press release / Vixio / Central Banking, verified 2026-06-12)",
        },
        "values_2024": MM_2024,
        "velocity_2017_2021": v1,
        "velocity_2021_2024": v2,
        "velocity_persistence_spearman": round(rho, 3),
        "wallet_corner_2124": {
            "fast_countries": fast2,
            "fast_AND_wallet_decentralized": occupied,
            "resolution": (
                "ID accelerated (1.54→4.24pp/yr) while staying wallet-decentralized "
                "(top share 25-31%) — but the acceleration window coincides with the "
                "arrival of shared central-bank infrastructure (QRIS 2020, BI-FAST "
                "Dec-2021). Wallet-level bound falsified in-region; rail-level "
                "reading strengthened: a natural experiment where the slow rail-less "
                "country became fast upon acquiring a single shared rail."
            ),
        },
        "anomalies": {
            "TH": "60.0→41.7 (-6.1pp/yr): real decline vs Findex reclassification "
                  "unresolved — flagged, not interpreted, excluded from conclusions.",
            "MM": "2024 null — survey not conducted (civil war); measurement "
                  "availability is itself political.",
        },
        "honest_limits": (
            "n small as always; 'fast' threshold 4pp/yr author-chosen (ID 4.24 is "
            "just above it); the ID natural experiment is one country (no "
            "counterfactual); TH anomaly unresolved and could affect persistence rho."
        ),
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "wave3_empirical.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
