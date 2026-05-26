"""
AI dependency comparison: ChatGPT / Claude / Llama / GovAI.

Demonstrates that:
1. The same common CPN spec applies — only flow_heyting differs.
2. Trust upper bounds differ structurally (notes/18 §4.3).
3. Multi-agent ▷ composition is meet-limited (Ghrist-Gould-Lopez 2024).
4. Cloudflare 2025-11 cascade hits all private backbones simultaneously.

Output:
  - stdout summary
  - JSON to docs/data/ai_comparison.json
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from h_petri.core import fire_sequence, trust_reached_at, systemic_load_curve, FourLevelHA
from h_petri.domains import ai_dependency as ai


BACKBONES = [
    ("chatgpt", ai.build_chatgpt_net,  "platform_private"),
    ("claude",  ai.build_claude_net,   "platform_private"),
    ("llama",   ai.build_llama_net,    "open_consortium"),
    ("govai",   ai.build_govt_ai_net,  "central_state_hypothetical"),
]


def simulate(net, sequence):
    return fire_sequence(net, net.initial, sequence)


def summarize(name: str, btype: str, trajectory, ha: FourLevelHA) -> dict:
    final = trajectory[-1]
    return {
        "name": name,
        "backbone_type": btype,
        "steps": len(trajectory) - 1,
        "final_invisible": dict(final.invisible),
        "trust_reached_T_PUB_at_step":  trust_reached_at(trajectory, "TrustInLLM", ha.T_PUB, ha),
        "trust_reached_T_BANK_at_step": trust_reached_at(trajectory, "TrustInLLM", ha.T_BANK, ha),
        "trust_reached_T_PRIV_at_step": trust_reached_at(trajectory, "TrustInLLM", ha.T_PRIV, ha),
        "trust_curve_ranks":         systemic_load_curve(trajectory, "TrustInLLM",        ha),
        "atrophy_curve_ranks":       systemic_load_curve(trajectory, "AtrophyOfThinking", ha),
    }


def run(num_queries: int = 3):
    ha = FourLevelHA()
    results = {}

    for key, builder, btype in BACKBONES:
        net = builder()
        seq = ai.STANDARD_TX_SEQUENCE * num_queries
        traj = simulate(net, seq)
        results[key] = summarize(net.name, btype, traj, ha)

    # Bottleneck reversal across LLMs
    trust_uppers = {k: results[k]["final_invisible"]["TrustInLLM"] for k in results}
    meet_value = "⊤_pub"
    join_value = "⊥"
    for v in trust_uppers.values():
        if ha._rank(v) < ha._rank(meet_value):
            meet_value = v
        if ha._rank(v) > ha._rank(join_value):
            join_value = v

    # Cloudflare 2025-11 hypothetical cascade — all private backbones lose Trust simultaneously
    # We model this as: take trust_curve, then "downgrade" private backbones to ⊥ for 1 step.
    cascade = {}
    for k in results:
        curve = list(results[k]["trust_curve_ranks"])
        # find midpoint and inject a single-step depression for private backbones
        mid = len(curve) // 2
        if results[k]["backbone_type"] == "platform_private":
            cascade_curve = curve[:mid] + [0] + curve[mid+1:]  # drop to ⊥ briefly
        else:
            cascade_curve = curve  # bank/state unaffected
        cascade[k] = cascade_curve

    return {
        "config": {"num_queries": num_queries},
        "backbones": results,
        "bottleneck_reversal_demo": {
            "trust_uppers": trust_uppers,
            "monoidal_⊗_bound (max, user picks best LLM)":  join_value,
            "cospan_▷_bound  (meet, multi-agent chain)":   meet_value,
            "rank_gap": ha._rank(join_value) - ha._rank(meet_value),
            "interpretation": (
                "If a user picks the strongest LLM (⊗), they get " + join_value + ". "
                "But if multi-agent chains require ALL LLMs (▷, e.g. ReAct or "
                "multi-step pipelines depending on different vendors), the system "
                "is bounded by the weakest = " + meet_value + ". "
                "Same set of LLMs, different composition direction, different bottleneck. "
                "Mirrors notes/15 / notes/26 for ASEAN backbones."
            ),
        },
        "cloudflare_2025_11_cascade": {
            "description": (
                "2025-11-18 Cloudflare Workers KV outage took ChatGPT, Claude, Sora, "
                "and other AI services down for ~5.5 hours, with Downdetector spiking "
                "to 11,183 reports. Modeled here by depressing TrustInLLM to ⊥ at a "
                "mid-step for backbones with type=platform_private (since they share "
                "Cloudflare CDN). Open-consortium and state backbones unaffected."
            ),
            "curves": cascade,
            "structural_lesson": (
                "Pair 2 from notes/23 (M-Pesa 2019 / Kenya 5h → Cloudflare 2025-11 / global 5.5h) "
                "is reproduced here at the code level: a single private backbone outage "
                "downgrades the visible Trust of all dependent services."
            ),
        },
        "isomorphism_with_asean": {
            "description": (
                "Per notes/18 §4.4: "
                "Bakong = GovAI (both ⊤_pub), "
                "PayNow = Llama (both ⊤_bank, consortium-like), "
                "GCash = ChatGPT/Claude (both ⊤_priv, single private). "
                "Same H-Petri Net structure (5 visible + 2 invisible places), "
                "different Heyting upper bounds. φ_P and φ_T (notes/23) are "
                "explicit at the code level."
            ),
        },
    }


def main():
    result = run(num_queries=3)

    print("=" * 70)
    print("AI Dependency H-Petri Net Comparison")
    print("=" * 70)
    for key in ("govai", "llama", "claude", "chatgpt"):
        s = result["backbones"][key]
        print(f"\n[{s['name']}]  type={s['backbone_type']}")
        print(f"  Steps fired:                  {s['steps']}")
        print(f"  Trust reached T_PRIV at step: {s['trust_reached_T_PRIV_at_step']}")
        print(f"  Trust reached T_BANK at step: {s['trust_reached_T_BANK_at_step']}")
        print(f"  Trust reached T_PUB  at step: {s['trust_reached_T_PUB_at_step']}")
        print(f"  Final TrustInLLM:             {s['final_invisible']['TrustInLLM']}")
        print(f"  Final AtrophyOfThinking:      {s['final_invisible']['AtrophyOfThinking']}")

    print("\n" + "-" * 70)
    print("Bottleneck Reversal (notes/26 translation functor, applied to AI):")
    br = result["bottleneck_reversal_demo"]
    print(f"  Trust uppers: {br['trust_uppers']}")
    print(f"  User picks best (⊗):       {br['monoidal_⊗_bound (max, user picks best LLM)']}")
    print(f"  Multi-agent chain (▷):     {br['cospan_▷_bound  (meet, multi-agent chain)']}")
    print(f"  Heyting rank gap:          {br['rank_gap']}")
    print(f"\n  {br['interpretation']}")

    print("\n" + "-" * 70)
    print("Cloudflare 2025-11 cascade:")
    cf = result["cloudflare_2025_11_cascade"]
    print(f"  {cf['description'][:100]}...")
    print(f"  ChatGPT curve: {cf['curves']['chatgpt']}")
    print(f"  Claude curve:  {cf['curves']['claude']}")
    print(f"  Llama curve:   {cf['curves']['llama']}")
    print(f"  GovAI curve:   {cf['curves']['govai']}")
    print(f"\n  {cf['structural_lesson']}")

    out_path = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "ai_comparison.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
