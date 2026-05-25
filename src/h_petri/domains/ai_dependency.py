"""
AI dependence as an H-Petri Net (notes/18 §4).

Cross-domain isomorphism: ChatGPT/Claude/Llama in AI dependence is
structurally isomorphic to GCash/Bakong/PayNow in mobile money.

Common CPN spec (notes/07) applied to AI provider domain:
  p1: User           (人間ユーザー)
  p2: PromptInQueue  (送信されたプロンプト)
  p3: LLMBackbone    (Claude / GPT / Gemini / Llama)
  p4: ResponseReady  (生成された応答)
  p5: UserOutput     (人間が出力として使った)
  p_inv1: TrustInLLM        (LLM への信頼累積)
  p_inv2: AtrophyOfThinking (思考力外部化負債)
"""

from __future__ import annotations
from h_petri.core import HPetriNet, Marking, FourLevelHA


def _build_ai_net(
    name: str,
    backbone_place: str,
    trust_level: str,
    atrophy_level: str,
    backbone_type: str,
    initial_prompts: int = 100,
) -> HPetriNet:
    H = FourLevelHA()

    places_visible = ["User", "PromptInQueue", backbone_place,
                      "ResponseReady", "UserOutput"]
    places_invisible = ["TrustInLLM", "AtrophyOfThinking"]

    transitions = [
        "t1_ComposePrompt",
        "t2_LLMProcess",
        "t3_GenerateResponse",
        "t4_HumanReview",
        "t5_AdoptAsOwn",
    ]

    flow_in = {
        ("User",          "t1_ComposePrompt"): 1,
        ("PromptInQueue", "t2_LLMProcess"):    1,
        (backbone_place,  "t2_LLMProcess"):    1,
        (backbone_place,  "t3_GenerateResponse"): 1,
        ("ResponseReady", "t4_HumanReview"):   1,
        ("ResponseReady", "t5_AdoptAsOwn"):    1,
    }

    flow_out = {
        ("t1_ComposePrompt",    "PromptInQueue"): 1,
        ("t2_LLMProcess",       backbone_place):  1,  # backbone recycles
        ("t3_GenerateResponse", backbone_place):  1,
        ("t3_GenerateResponse", "ResponseReady"): 1,
        ("t4_HumanReview",      "ResponseReady"): 1,  # review loops
        ("t5_AdoptAsOwn",       "UserOutput"):    1,
    }

    flow_heyting = {
        ("t2_LLMProcess",       "TrustInLLM"):        trust_level,
        ("t3_GenerateResponse", "TrustInLLM"):        trust_level,
        ("t5_AdoptAsOwn",       "AtrophyOfThinking"): atrophy_level,
        # Reviewing reduces nothing (Heyting is monotone), but unreviewed
        # adoption directly bumps the atrophy counter.
    }

    initial = Marking(
        visible={
            "User": initial_prompts,
            "PromptInQueue": 0,
            backbone_place: 1,
            "ResponseReady": 0,
            "UserOutput": 0,
        },
        invisible={
            "TrustInLLM": H.bottom,
            "AtrophyOfThinking": H.bottom,
        },
    )

    return HPetriNet(
        places_visible=places_visible,
        places_invisible=places_invisible,
        transitions=transitions,
        flow_in=flow_in,
        flow_out=flow_out,
        flow_heyting=flow_heyting,
        initial=initial,
        heyting=H,
        name=name,
    )


def build_chatgpt_net(initial_prompts: int = 100) -> HPetriNet:
    """ChatGPT (OpenAI) - private platform = ⊤_priv."""
    H = FourLevelHA()
    return _build_ai_net(
        name="ChatGPT (OpenAI, private platform)",
        backbone_place="OpenAIBackbone",
        trust_level=H.T_PRIV,
        atrophy_level=H.T_PRIV,
        backbone_type="platform",
        initial_prompts=initial_prompts,
    )


def build_claude_net(initial_prompts: int = 100) -> HPetriNet:
    """Claude (Anthropic) - private platform with stronger review ethos = ⊤_priv (+)."""
    H = FourLevelHA()
    return _build_ai_net(
        name="Claude (Anthropic, private platform + safety focus)",
        backbone_place="AnthropicBackbone",
        trust_level=H.T_PRIV,
        atrophy_level=H.T_PRIV,  # same Heyting rank as ChatGPT
        backbone_type="platform",
        initial_prompts=initial_prompts,
    )


def build_llama_net(initial_prompts: int = 100) -> HPetriNet:
    """Llama (Meta open weights) - 'bank consortium-like' open distribution = ⊤_bank."""
    H = FourLevelHA()
    return _build_ai_net(
        name="Llama (Meta open weights, distributed)",
        backbone_place="OpenModelInfrastructure",
        trust_level=H.T_BANK,
        atrophy_level=H.T_BANK,
        backbone_type="bank_consortium",
        initial_prompts=initial_prompts,
    )


def build_govt_ai_net(initial_prompts: int = 100) -> HPetriNet:
    """Hypothetical government AI (e.g., UK BritishAI, future Japan AI) = ⊤_pub.

    This is a hypothetical reference — no actual govt AI yet meets this level.
    But it shows what 'central-bank-equivalent' AI would look like.
    """
    H = FourLevelHA()
    return _build_ai_net(
        name="Government AI (hypothetical, central-bank-equivalent)",
        backbone_place="StateAIInfrastructure",
        trust_level=H.T_PUB,
        atrophy_level=H.T_PUB,
        backbone_type="central_bank",
        initial_prompts=initial_prompts,
    )


STANDARD_TX_SEQUENCE = [
    "t1_ComposePrompt",
    "t2_LLMProcess",
    "t3_GenerateResponse",
    "t4_HumanReview",
    "t5_AdoptAsOwn",
]


# ---------------------------------------------------------------------------
# Comparison runner — same shape as h_petri.compare but for AI domain
# ---------------------------------------------------------------------------

def main():
    import json
    import sys
    from pathlib import Path

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

    from h_petri.core import fire_sequence, trust_reached_at, systemic_load_curve

    ha = FourLevelHA()

    AI_BACKBONES = [
        ("chatgpt",  build_chatgpt_net,  "platform"),
        ("claude",   build_claude_net,   "platform"),
        ("llama",    build_llama_net,    "bank_consortium"),
        ("govt_ai",  build_govt_ai_net,  "central_bank"),
    ]

    NUM_PROMPTS = 3
    results = {}

    for key, builder, btype in AI_BACKBONES:
        net = builder(initial_prompts=1000)
        seq = STANDARD_TX_SEQUENCE * NUM_PROMPTS
        traj = fire_sequence(net, net.initial, seq)
        final = traj[-1]
        results[key] = {
            "name": net.name,
            "backbone_type": btype,
            "steps": len(traj) - 1,
            "final_visible": dict(final.visible),
            "final_invisible": dict(final.invisible),
            "trust_curve_ranks": systemic_load_curve(traj, "TrustInLLM", ha),
            "atrophy_curve_ranks": systemic_load_curve(traj, "AtrophyOfThinking", ha),
        }

    # Bottleneck reversal for multi-agent LLM chain
    trust_uppers = {k: results[k]["final_invisible"]["TrustInLLM"] for k in results}
    meet_value = "⊤_pub"
    join_value = "⊥"
    for v in trust_uppers.values():
        if ha._rank(v) < ha._rank(meet_value):
            meet_value = v
        if ha._rank(v) > ha._rank(join_value):
            join_value = v

    out = {
        "config": {"num_prompts": NUM_PROMPTS},
        "ai_backbones": results,
        "isomorphism_with_finance": {
            "ChatGPT": "GCash (両方 ⊤_priv 民間集中)",
            "Claude": "GCash (同じ Heyting rank、ただし安全性重視で実質上位)",
            "Llama": "PayNow (両方 ⊤_bank 分散構造)",
            "Government AI (hypothetical)": "Bakong (両方 ⊤_pub 公的保証)",
        },
        "bottleneck_reversal_demo": {
            "trust_uppers": trust_uppers,
            "monoidal_⊗_bound (max)":   join_value,
            "cospan_▷_bound  (meet)":  meet_value,
            "rank_gap": ha._rank(join_value) - ha._rank(meet_value),
            "interpretation": (
                f"並列利用 (ユーザーが LLM を選べる、⊗): 最強は {join_value} "
                f"(政府AI想定 or Llama)。多重 agent chain (▷): 最弱に律速 → {meet_value} "
                f"(ChatGPT/Claude に律速)。AI ドメインでも Curry-Krishnan 律速逆転が成立。"
            ),
        },
        "interpretation": {
            "cross_domain": (
                "ChatGPT が止まれば全世界の AI ユーザーが詰むのは、"
                "M-Pesa 障害で Kenya 経済が止まるのと同型構造。"
                "同じ Heyting値の不可視層 (TrustInLLM) が単一企業に集中。"
            ),
        },
    }

    print("=" * 70)
    print("AI Dependence H-Petri Net Comparison")
    print("=" * 70)
    for key in ("govt_ai", "llama", "claude", "chatgpt"):
        s = out["ai_backbones"][key]
        print(f"\n[{s['name']}]  type={s['backbone_type']}")
        print(f"  Final TrustInLLM:         {s['final_invisible']['TrustInLLM']}")
        print(f"  Final AtrophyOfThinking:  {s['final_invisible']['AtrophyOfThinking']}")
        print(f"  TrustInLLM rank curve:    {s['trust_curve_ranks']}")

    print("\n" + "-" * 70)
    print("Bottleneck Reversal (notes/15) in AI domain:")
    br = out["bottleneck_reversal_demo"]
    print(f"  ⊗ (parallel, max):  {br['monoidal_⊗_bound (max)']}")
    print(f"  ▷ (chain, meet):    {br['cospan_▷_bound  (meet)']}")
    print(f"  Heyting rank gap:   {br['rank_gap']}")
    print(f"\n  {br['interpretation']}")

    print("\n" + "-" * 70)
    print("Isomorphism with mobile money:")
    for ai, fin in out["isomorphism_with_finance"].items():
        print(f"  {ai}  =  {fin}")

    out_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "ai_comparison.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
