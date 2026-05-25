"""
Trust timeline as a Time-functor (notes/17, 19, 20).

Builds Trust: Time → H for various payment backbones (ASEAN + developed
countries), and computes speed-concentration metrics (notes/20).

Output: docs/data/trust_timeline.json for the temporal visualization.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from h_petri.core import FourLevelHA

H = FourLevelHA()


# ---------------------------------------------------------------------------
# Trust timeline data (year, Heyting-value)
# ---------------------------------------------------------------------------
# Values are best-effort historical estimates based on:
# - Central bank establishment / digital push milestones
# - Bank-consortium formation
# - Mobile money launch dates and adoption inflection points
# - Crisis events (e.g., M-Pesa outages) treated at coarse (yearly) resolution

TRUST_TIMELINES: dict[str, dict] = {
    # === ASEAN backbones ===
    "Bakong (KH)": {
        "type": "central_bank",
        "region": "ASEAN",
        "country": "Cambodia",
        "data": [
            (2019, H.BOTTOM),
            (2020, H.T_PRIV),   # launched, limited
            (2022, H.T_BANK),   # mainstream merchants
            (2024, H.T_PUB),    # 75M tx H1, NBC mandate
        ],
        "concentration": 0.7,
    },
    "PromptPay (TH)": {
        "type": "central_bank",
        "region": "ASEAN",
        "country": "Thailand",
        "data": [
            (2015, H.BOTTOM),
            (2016, H.T_PRIV),   # BoT mandate, beta
            (2018, H.T_BANK),   # bank integration completed
            (2022, H.T_PUB),    # 74M tx/day
        ],
        "concentration": 0.9,
    },
    "GCash (PH)": {
        "type": "platform",
        "region": "ASEAN",
        "country": "Philippines",
        "data": [
            (2003, H.BOTTOM),
            (2004, H.T_PRIV),   # Globe Telecom launch
            (2018, H.T_PRIV),   # Ant Group investment, scale up
            (2024, H.T_PRIV),   # 85% market share, plateau
        ],
        "concentration": 0.85,
    },
    "MoMo (VN)": {
        "type": "platform",
        "region": "ASEAN",
        "country": "Vietnam",
        "data": [
            (2009, H.BOTTOM),
            (2010, H.T_PRIV),
            (2019, H.T_PRIV),   # unicorn status
            (2024, H.T_PRIV),   # 31M active users
        ],
        "concentration": 0.56,
    },
    "PayNow (SG)": {
        "type": "bank_consortium",
        "region": "ASEAN",
        "country": "Singapore",
        "data": [
            (2016, H.BOTTOM),
            (2017, H.T_PRIV),
            (2019, H.T_BANK),   # MAS-supervised, 5M+ registrations
            (2024, H.T_BANK),
        ],
        "concentration": 0.6,
    },
    "KBZPay (MM)": {
        "type": "bank_single",
        "region": "ASEAN",
        "country": "Myanmar",
        "data": [
            (2017, H.BOTTOM),
            (2018, H.T_PRIV),
            (2022, H.T_BANK),   # KBZ Bank single-dominant, replaced Wave Money
            (2024, H.T_BANK),
        ],
        "concentration": 0.6,
    },

    # === Developed-country reference points ===
    "US Federal Reserve (US)": {
        "type": "central_bank",
        "region": "developed",
        "country": "United States",
        "data": [
            (1912, H.BOTTOM),
            (1913, H.T_PRIV),    # Federal Reserve Act
            (1933, H.T_BANK),    # FDIC established, banking reform
            (1971, H.T_PUB),     # Bretton Woods end, fiat backed by sovereign
            (2024, H.T_PUB),
        ],
        "concentration": 0.5,
    },
    "Japan Banking (JP)": {
        "type": "bank_consortium",
        "region": "developed",
        "country": "Japan",
        "data": [
            (1872, H.BOTTOM),
            (1873, H.T_PRIV),    # First National Bank
            (1900, H.T_BANK),    # bank network matured
            (1950, H.T_PUB),     # postwar BoJ reform
            (2024, H.T_PUB),
        ],
        "concentration": 0.4,
    },
    "EU SEPA (EU)": {
        "type": "bank_consortium",
        "region": "developed",
        "country": "European Union",
        "data": [
            (2007, H.BOTTOM),
            (2008, H.T_PRIV),    # SEPA Credit Transfer launch
            (2014, H.T_BANK),    # SCT mandatory EU-wide
            (2024, H.T_BANK),    # still bank-level, not sovereign-fused
        ],
        "concentration": 0.3,
    },
    "Bitcoin (global)": {
        "type": "decentralized",
        "region": "global",
        "country": "—",
        "data": [
            (2008, H.BOTTOM),
            (2009, H.T_PRIV),    # genesis block
            (2017, H.T_PRIV),    # mainstream awareness, still volatile
            (2024, H.T_PRIV),    # institutional adoption but legal uncertainty
        ],
        "concentration": 0.2,    # mining concentration, but protocol decentralized
    },

    # === 1990s ASEAN banking systems (for 1997 crisis study) ===
    # These overlap with later digital backbones, but capture the legacy
    # banking sector that *was* the backbone in 1985-2000.
    # Per literature/raw/16_1997_crisis_analysis.md:
    # Apparent ⊤_pub (USD-peg) collapsed to ⊤_priv during 1997.
    "Thailand Banking (1985-)": {
        "type": "bank_consortium",
        "region": "ASEAN",
        "country": "Thailand (legacy)",
        "data": [
            (1984, H.T_PRIV),    # USD peg starts
            (1993, H.T_BANK),    # BIBF opens, apparent ⊤_bank
            (1996, H.T_BANK),    # peak credit boom
            (1997, H.T_PRIV),    # ★ baht devaluation Jul 2 — meet ▷ propagates
            (1999, H.T_PRIV),    # bottom
            (2002, H.T_BANK),    # IMF program ends, BoT regains
            (2010, H.T_BANK),
            (2024, H.T_BANK),
        ],
        "concentration": 0.85,   # 15 chaebol-linked banks
    },
    "Indonesia Banking (1985-)": {
        "type": "bank_single",
        "region": "ASEAN",
        "country": "Indonesia (legacy)",
        "data": [
            (1985, H.T_PRIV),    # conglomerate-controlled banks
            (1995, H.T_BANK),
            (1997, H.BOTTOM),    # ★ rupiah crashes 80%, 16 banks suspended Nov
            (1998, H.BOTTOM),    # banking system collapse (deepest)
            (2002, H.T_PRIV),    # IBRA program
            (2010, H.T_BANK),
            (2024, H.T_BANK),
        ],
        "concentration": 0.7,
    },
    "Korea Banking (1985-)": {
        "type": "bank_consortium",
        "region": "developed",
        "country": "South Korea (chaebol)",
        "data": [
            (1985, H.T_PRIV),
            (1992, H.T_BANK),
            (1996, H.T_BANK),
            (1997, H.T_PRIV),    # ★ won devaluation, chaebol bankruptcies
            (1998, H.T_PRIV),
            (2001, H.T_BANK),    # IMF program ends
            (2010, H.T_BANK),
            (2024, H.T_PUB),     # KRX maturity, BoK independence
        ],
        "concentration": 0.6,
    },
    "Malaysia Banking (1985-)": {
        "type": "bank_consortium",
        "region": "ASEAN",
        "country": "Malaysia",
        "data": [
            (1985, H.T_PRIV),
            (1993, H.T_BANK),
            (1996, H.T_BANK),
            (1997, H.T_BANK),    # capital controls Sep 1998 — Heyting value preserved
            (1998, H.T_PRIV),    # but real economy hit
            (2001, H.T_BANK),    # quick recovery via controls
            (2010, H.T_BANK),
            (2024, H.T_BANK),
        ],
        "concentration": 0.5,
    },
}


# Crisis events: Heyting value temporarily depresses then recovers.
# These are reflected directly in the data above (years marked with ★).
# Cataloged here for the UI overlay.
CRISIS_EVENTS = [
    {"year": 1997, "label": "AFC (Asian Financial Crisis)",
     "affected": ["Thailand Banking (1985-)", "Indonesia Banking (1985-)",
                  "Korea Banking (1985-)", "Malaysia Banking (1985-)"],
     "note": "USD peg collapse cascades via ▷-merged trade/credit network. "
             "Meet bottleneck reversal in action: weakest country drags rest down."},
    {"year": 2008, "label": "GFC (Global Financial Crisis)",
     "affected": ["US Federal Reserve (US)"],
     "note": "Subprime cascade. Fed's ⊤_pub remained nominal but TARP "
             "showed legal-protection invocation."},
    {"year": 2011, "label": "March 11 (Tohoku)",
     "affected": ["Japan Banking (JP)"],
     "note": "Operational shock to banking system, recovered quickly via BoJ."},
    {"year": 2010, "label": "Greek crisis",
     "affected": ["EU SEPA (EU)"],
     "note": "Sovereign debt crisis pressured EU banking framework."},
    {"year": 2021, "label": "Myanmar coup",
     "affected": ["KBZPay (MM)"],
     "note": "Telco-dominant Wave Money collapsed; KBZPay (bank) took over."},
    {"year": 2019, "label": "M-Pesa outage",
     "affected": [],
     "note": "5-hour Safaricom outage caused ~KES billions in economic loss "
             "(referenced, not in chart)."},
]


# ---------------------------------------------------------------------------
# Time-functor operations
# ---------------------------------------------------------------------------

def trust_at(backbone: str, year: int) -> str:
    """Trust(year) — left-continuous step function (notes/19 §2.3).

    Returns the most recent value at or before `year`.
    """
    timeline = TRUST_TIMELINES[backbone]["data"]
    value = H.BOTTOM
    for y, v in timeline:
        if y <= year:
            value = v
    return value


def trust_speed(backbone: str, end_year: int = 2026) -> float:
    """Average speed v = Δrank / Δyear (notes/20 §3.3)."""
    data = TRUST_TIMELINES[backbone]["data"]
    if not data:
        return 0.0
    start_year = data[0][0]
    duration = end_year - start_year
    if duration <= 0:
        return 0.0
    final_rank = H._rank(trust_at(backbone, end_year))
    return final_rank / duration


def speed_x_concentration(backbone: str, end_year: int = 2026) -> float:
    """Test the proposed trade-off v × C ≥ K_const (notes/20 §4)."""
    return trust_speed(backbone, end_year) * TRUST_TIMELINES[backbone]["concentration"]


def trust_timeseries_for_chart(backbone: str, year_range: tuple[int, int]) -> list[tuple[int, int]]:
    """Produce (year, rank) pairs for plotting as a step chart."""
    y_start, y_end = year_range
    points = []
    for y in range(y_start, y_end + 1):
        rank = H._rank(trust_at(backbone, y))
        points.append((y, rank))
    return points


def end_value(backbone: str) -> str:
    """end = ⋀_t Trust(t) (notes/19 §5.1)."""
    data = TRUST_TIMELINES[backbone]["data"]
    if not data:
        return H.BOTTOM
    return min((v for _, v in data), key=H._rank)


def coend_value(backbone: str) -> str:
    """coend = ⋁_t Trust(t) (notes/19 §5.2)."""
    data = TRUST_TIMELINES[backbone]["data"]
    if not data:
        return H.BOTTOM
    return max((v for _, v in data), key=H._rank)


# ---------------------------------------------------------------------------
# Bottleneck reversal across time (notes/19 §7)
# ---------------------------------------------------------------------------

def trust_max_at(year: int, backbones: list[str]) -> str:
    """⊗_∨ = pointwise join — max bound for parallel composition."""
    return max((trust_at(b, year) for b in backbones), key=H._rank)


def trust_meet_at(year: int, backbones: list[str]) -> str:
    """⊗_∧ = pointwise meet — meet bound for integrated composition."""
    return min((trust_at(b, year) for b in backbones), key=H._rank)


# ---------------------------------------------------------------------------
# Export for HTML viz
# ---------------------------------------------------------------------------

def export_all(year_range: tuple[int, int] = (1870, 2030)) -> dict:
    result = {
        "year_range": list(year_range),
        "backbones": {},
        "asean_max_meet_over_time": [],
        "metrics": {},
    }

    for name, meta in TRUST_TIMELINES.items():
        series = trust_timeseries_for_chart(name, year_range)
        result["backbones"][name] = {
            "type": meta["type"],
            "region": meta["region"],
            "country": meta["country"],
            "concentration": meta["concentration"],
            "data_points": [{"year": y, "rank": r} for y, r in series],
            "milestones": [
                {"year": y, "value": v, "rank": H._rank(v)}
                for y, v in meta["data"]
            ],
            "end": end_value(name),
            "coend": coend_value(name),
            "trust_2026": trust_at(name, 2026),
            "speed_per_year": round(trust_speed(name), 4),
            "speed_x_concentration": round(speed_x_concentration(name), 4),
        }

    # Bottleneck reversal demo across ASEAN5
    asean5 = ["Bakong (KH)", "PromptPay (TH)", "GCash (PH)", "MoMo (VN)", "PayNow (SG)"]
    for y in range(year_range[0], year_range[1] + 1):
        result["asean_max_meet_over_time"].append({
            "year": y,
            "max_⊗": H._rank(trust_max_at(y, asean5)),
            "meet_▷": H._rank(trust_meet_at(y, asean5)),
            "gap": H._rank(trust_max_at(y, asean5)) - H._rank(trust_meet_at(y, asean5)),
        })

    # Aggregate metrics
    result["metrics"] = {
        "speed_x_concentration_per_backbone": {
            name: round(speed_x_concentration(name), 4) for name in TRUST_TIMELINES
        },
        "min_v_times_C":   round(min(speed_x_concentration(b) for b in TRUST_TIMELINES), 4),
        "max_v_times_C":   round(max(speed_x_concentration(b) for b in TRUST_TIMELINES), 4),
        "trade_off_note": (
            "v × C across all backbones ranges (notes/20 §4.2). "
            "If a lower bound K_const > 0 exists, it supports the "
            "time-concentration trade-off hypothesis."
        ),
    }

    # 1997-era backbones for crisis study
    crisis_1997_backbones = [
        "Thailand Banking (1985-)",
        "Indonesia Banking (1985-)",
        "Korea Banking (1985-)",
        "Malaysia Banking (1985-)",
    ]
    result["crisis_1997"] = {
        "backbones": crisis_1997_backbones,
        "max_meet_over_time": [],
    }
    for y in range(1985, 2031):
        row = {
            "year": y,
            "max_⊗": H._rank(trust_max_at(y, crisis_1997_backbones)),
            "meet_▷": H._rank(trust_meet_at(y, crisis_1997_backbones)),
        }
        row["gap"] = row["max_⊗"] - row["meet_▷"]
        result["crisis_1997"]["max_meet_over_time"].append(row)

    # Crisis events for UI overlay
    result["crisis_events"] = CRISIS_EVENTS

    return result


def main():
    out = export_all(year_range=(1870, 2030))

    print("=" * 70)
    print("Trust Timeline Summary")
    print("=" * 70)
    for name, m in out["backbones"].items():
        print(f"\n[{name}]  type={m['type']}, region={m['region']}")
        print(f"  Trust 2026:       {m['trust_2026']}  (rank {H._rank(m['trust_2026'])})")
        print(f"  Speed (rank/yr):  {m['speed_per_year']}")
        print(f"  Concentration:    {m['concentration']}")
        print(f"  v × C:            {m['speed_x_concentration']}")
        print(f"  End (min):        {m['end']}")
        print(f"  Coend (max):      {m['coend']}")
        print(f"  Milestones:       {[(ms['year'], ms['value']) for ms in m['milestones']]}")

    print("\n" + "-" * 70)
    print("v × C trade-off across all backbones:")
    print(f"  Min v×C: {out['metrics']['min_v_times_C']}")
    print(f"  Max v×C: {out['metrics']['max_v_times_C']}")
    print(f"  Hypothesis (notes/20 §4): v × C ≥ K_const")
    print(f"  Lower bound (empirical): {out['metrics']['min_v_times_C']}")

    print("\n" + "-" * 70)
    print("ASEAN5 Bottleneck Reversal across time (sample years):")
    for y in [2010, 2016, 2020, 2024, 2026]:
        row = next(r for r in out["asean_max_meet_over_time"] if r["year"] == y)
        print(f"  {y}: max(⊗)={row['max_⊗']}, meet(▷)={row['meet_▷']}, gap={row['gap']}")

    out_path = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "trust_timeline.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
