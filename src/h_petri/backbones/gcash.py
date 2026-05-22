"""
GCash (Philippines, private-platform backbone) H-Petri Net.

Per notes/07 §4.2 specification.

backbone_type: platform
TrustHub upper bound: ⊤_private (corporate guarantee, Globe Telecom)
"""

from __future__ import annotations
from h_petri.core import HPetriNet, Marking, FourLevelHA


def build_gcash_net(initial_balance: int = 100, send_amount: int = 10) -> HPetriNet:
    H = FourLevelHA()

    places_visible = ["UserWallet", "PendingTx", "GlobeBackbone",
                      "SettledTx", "RecipientWallet"]
    places_invisible = ["TrustHub", "SystemicLoad"]

    transitions = ["t1_InitiateSend", "t2_GCashClear", "t3_Settle",
                   "t4_Reconciliation", "t5_AcknowledgeReceipt"]

    flow_in = {
        ("UserWallet",    "t1_InitiateSend"):       send_amount,
        ("PendingTx",     "t2_GCashClear"):         1,
        ("GlobeBackbone", "t2_GCashClear"):         1,
        ("GlobeBackbone", "t3_Settle"):             1,
        ("SettledTx",     "t4_Reconciliation"):     1,
        ("SettledTx",     "t5_AcknowledgeReceipt"): 1,
    }

    # GlobeBackbone is a "resource token" — recycled on each clear/settle.
    flow_out = {
        ("t1_InitiateSend",       "PendingTx"):       1,
        ("t2_GCashClear",         "GlobeBackbone"):   1,
        ("t3_Settle",             "GlobeBackbone"):   1,
        ("t3_Settle",             "SettledTx"):       1,
        ("t4_Reconciliation",     "SettledTx"):       1,
        ("t5_AcknowledgeReceipt", "RecipientWallet"): send_amount,
    }

    # Private platform: trust hub maxes out at ⊤_private.
    # Differences from Bakong:
    #   - δ2, δ3 are T_PRIV, not T_PUB
    #   - This is the *structural* expression of the legal-protection gap
    flow_heyting = {
        ("t2_GCashClear",     "TrustHub"):     H.T_PRIV,
        ("t3_Settle",         "TrustHub"):     H.T_PRIV,
        ("t1_InitiateSend",   "SystemicLoad"): H.T_PRIV,
        ("t4_Reconciliation", "SystemicLoad"): H.T_PRIV,  # batched, no real-time NBC backstop
    }

    initial = Marking(
        visible={
            "UserWallet": initial_balance,
            "PendingTx": 0,
            "GlobeBackbone": 1,
            "SettledTx": 0,
            "RecipientWallet": 0,
        },
        invisible={
            "TrustHub": H.bottom,
            "SystemicLoad": H.bottom,
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
        name="GCash (Philippines, platform)",
    )


STANDARD_TX_SEQUENCE = [
    "t1_InitiateSend",
    "t2_GCashClear",
    "t3_Settle",
    "t4_Reconciliation",
    "t5_AcknowledgeReceipt",
]
