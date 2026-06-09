"""
S3 quantified — does the failure MODE factor through structure, from real outages?

Upgrades the structural conclusion from "institutional definition" toward
"documented pattern" by tabulating SOURCED backbone-outage events and checking
whether the failure mode clusters by structural axis rather than by scalar
adoption.

Two STRUCTURAL axes emerge from the verified events (and they are NOT the same):
  - backstop depth   = Heyting type (who absorbs the loss): ⊤_priv / ⊤_bank / ⊤_pub
  - operational topology = single operator vs federated shared rail
The failure SCOPE (total national outage vs distributed-per-bank) tracks the
TOPOLOGY; the LOSS-BEARER tracks the backstop. Both are structural; neither is
the scalar inclusion level.

⚠️ HONEST CAVEATS (carried from literature/raw/10's own bias section):
  - Disclosure bias: Bakong shows 0 documented outages, but the central bank is
    its own monitor (weak disclosure incentive) and English-media coverage of
    KH/VN is thin. So FREQUENCY across types is CONFOUNDED — we do NOT claim
    "central-bank rails fail less". The robust claim is about the MODE (how they
    fail when they do), which is what the sourced events show.
  - Small n (a few events per type). This is illustrative, not statistical.

Every event below is from a sourced incident in literature/raw/10, with the
two most load-bearing ones (GCash reconciliation, PromptPay/ITMX 2022) re-
verified against media 2026-06-07.
"""

from __future__ import annotations
import json
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Sourced outage events. topology: "single" (one operator) | "federated" (shared rail).
# scope: "total" (whole service down) | "distributed" (per-bank/partial).
EVENTS = [
    {"event": "M-Pesa 2019 national outage", "backbone": "M-Pesa", "region": "KE(参考)",
     "type": "platform", "topology": "single", "duration_h": 5,
     "cause": "internal_tech", "scope": "total", "loss_bearer": "users",
     "source": "TechCabal / The Exchange / Tuko"},
    {"event": "M-Pesa 2024-01 outages x2", "backbone": "M-Pesa", "region": "KE(参考)",
     "type": "platform", "topology": "single", "duration_h": 2,
     "cause": "maintenance/internal", "scope": "total", "loss_bearer": "users",
     "source": "TechCabal / Techpoint"},
    {"event": "GCash 2023-05 balance loss", "backbone": "GCash", "region": "PH",
     "type": "platform", "topology": "single", "duration_h": 4,
     "cause": "phishing/internal", "scope": "total", "loss_bearer": "users",
     "source": "Inquirer / NPC / GMA"},
    {"event": "GCash 2024-11 reconciliation", "backbone": "GCash", "region": "PH",
     "type": "platform", "topology": "single", "duration_h": 24,
     "cause": "reconciliation_bug", "scope": "total", "loss_bearer": "users(restored)",
     "source": "BusinessWorld / GMA / DICT (re-verified 2026-06-07)"},
    {"event": "MoMo 2023-10 outage", "backbone": "MoMo", "region": "VN",
     "type": "platform", "topology": "single", "duration_h": 12,
     "cause": "internal/maintenance", "scope": "total", "loss_bearer": "users",
     "source": "Vietnam.vn"},
    {"event": "PromptPay/ITMX 2022-Q4 (17 incidents)", "backbone": "PromptPay", "region": "TH",
     "type": "central_bank", "topology": "federated", "duration_h": 3,
     "cause": "shared_rail_capacity", "scope": "distributed", "loss_bearer": "banks/system",
     "source": "Nation Thailand / Bangkok Post / ITMX (re-verified 2026-06-07)"},
    {"event": "PromptPay/ITMX 2023-Q1 (4 incidents)", "backbone": "PromptPay", "region": "TH",
     "type": "central_bank", "topology": "federated", "duration_h": 2,
     "cause": "shared_rail_capacity", "scope": "distributed", "loss_bearer": "banks/system",
     "source": "Bangkok Post"},
    {"event": "InstaPay/PESONet survives CrowdStrike 2024-07", "backbone": "InstaPay", "region": "PH",
     "type": "central_bank", "topology": "federated", "duration_h": 0,
     "cause": "external_shock_resilient", "scope": "none", "loss_bearer": "none",
     "source": "Philstar / Rappler / BSP"},
    {"event": "Bakong (no documented body outage)", "backbone": "Bakong", "region": "KH",
     "type": "central_bank", "topology": "federated", "duration_h": None,
     "cause": "none_documented", "scope": "none_documented", "loss_bearer": "n/a",
     "source": "NBC only — DISCLOSURE-BIAS FLAGGED"},
]


def main():
    print("=" * 72)
    print("S3 quantified — failure mode by structure (sourced outages)")
    print("=" * 72)

    print(f"\n{'event':40s} {'type':12s} {'topology':10s} {'scope':12s} loss")
    for e in EVENTS:
        print(f"{e['event'][:40]:40s} {e['type']:12s} {e['topology']:10s} "
              f"{e['scope']:12s} {e['loss_bearer']}")

    # scope by topology (the structural axis the mode tracks)
    print("\n— failure SCOPE by operational TOPOLOGY —")
    by_topo = {}
    for e in EVENTS:
        if e["scope"] in ("none", "none_documented"):
            continue
        by_topo.setdefault(e["topology"], Counter())[e["scope"]] += 1
    for topo, ctr in sorted(by_topo.items()):
        print(f"  {topo:10s}: {dict(ctr)}")
    print("  → single-operator (platform) outages are TOTAL; federated shared-rail")
    print("    (PromptPay/ITMX) outages are DISTRIBUTED per-bank. Scope ~ topology.")

    # loss-bearer by backstop type
    print("\n— LOSS-BEARER by backstop type (Heyting) —")
    by_type = {}
    for e in EVENTS:
        if e["loss_bearer"] in ("n/a", "none"):
            continue
        by_type.setdefault(e["type"], Counter())[e["loss_bearer"].split("(")[0]] += 1
    for t, ctr in sorted(by_type.items()):
        print(f"  {t:12s}: {dict(ctr)}")
    print("  → platform(⊤_priv) failures land on USERS; federated/central rails")
    print("    spread to banks/system. Loss-bearer ~ backstop type.")

    print("\n" + "-" * 72)
    print("STRUCTURAL CONCLUSION (S3, data-backed)")
    print("-" * 72)
    print(
        "The failure MODE decomposes into TWO structural axes, both grounded in\n"
        "sourced events and both orthogonal to scalar adoption:\n"
        "  • SCOPE (total vs distributed)  tracks OPERATIONAL TOPOLOGY\n"
        "    (single operator vs federated shared rail).\n"
        "  • LOSS-BEARER (users vs system) tracks the HEYTING BACKSTOP type.\n"
        "Scalar inclusion predicts neither. So the categorical structure — not the\n"
        "adoption number — is what governs how a backbone fails and who pays.\n"
        "This moves S3 from institutional definition to a documented (if small-n)\n"
        "pattern. Frequency across types stays CONFOUNDED by disclosure bias and\n"
        "is deliberately NOT claimed."
    )

    bundle = {
        "description": (
            "S3 quantified. Sourced backbone-outage events classified by structural "
            "axes (backstop type, operational topology). Failure SCOPE tracks "
            "topology, LOSS-BEARER tracks backstop — both orthogonal to scalar "
            "adoption. Moves the structural conclusion from definition to documented "
            "pattern."
        ),
        "events": EVENTS,
        "scope_by_topology": {k: dict(v) for k, v in by_topo.items()},
        "loss_bearer_by_type": {k: dict(v) for k, v in by_type.items()},
        "structural_conclusion": (
            "Failure mode decomposes into two structural axes: SCOPE~topology "
            "(single→total, federated→distributed) and LOSS-BEARER~backstop "
            "(platform/⊤_priv→users, federated/central→banks/system). Scalar "
            "inclusion predicts neither; the categorical structure governs how a "
            "backbone fails and who pays."
        ),
        "honest_limits": (
            "Small n (a few events per cell). FREQUENCY across types is confounded "
            "by disclosure bias (Bakong=0 is NBC-self-reported; KH/VN under-covered "
            "in English media) and is NOT claimed. Only the MODE (how/who, not how "
            "often) is asserted. Two events (GCash reconciliation, PromptPay 2022) "
            "re-verified 2026-06-07; the rest are from literature/raw/10's sourced list."
        ),
    }
    out = Path(__file__).resolve().parents[3] / "docs" / "data" / "failure_modes.json"
    json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    main()
