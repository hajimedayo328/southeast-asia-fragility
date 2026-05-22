"""
Bakong (Cambodia, central-bank backbone) H-Petri Net.

Per notes/07 §4.1 specification.

backbone_type: central_bank
TrustHub upper bound: ⊤_public (state guarantee)
"""

from __future__ import annotations
from h_petri.core import HPetriNet, Marking, FourLevelHA


def build_bakong_net(initial_balance: int = 100, send_amount: int = 10) -> HPetriNet:
    H = FourLevelHA()

    places_visible = ["UserWallet", "PendingTx", "NBCBackbone",
                      "SettledTx", "RecipientWallet"]
    places_invisible = ["TrustHub", "SystemicLoad"]

    transitions = ["t1_InitiateSend", "t2_BakongClear", "t3_Settle",
                   "t4_Reconciliation", "t5_AcknowledgeReceipt"]

    # flow_in[(place, transition)] = weight (visible layer)
    flow_in = {
        ("UserWallet",   "t1_InitiateSend"):       send_amount,
        ("PendingTx",    "t2_BakongClear"):        1,
        ("NBCBackbone",  "t2_BakongClear"):        1,
        ("NBCBackbone",  "t3_Settle"):             1,
        ("SettledTx",    "t4_Reconciliation"):     1,
        ("SettledTx",    "t5_AcknowledgeReceipt"): 1,
    }

    # flow_out[(transition, place)] = weight (visible layer)
    # NBCBackbone is a "resource token" — every transition that consumes it
    # also returns it (the central bank doesn't disappear after a clear).
    flow_out = {
        ("t1_InitiateSend",       "PendingTx"):       1,
        ("t2_BakongClear",        "NBCBackbone"):     1,  # backbone token recycles
        ("t3_Settle",             "NBCBackbone"):     1,  # backbone token recycles
        ("t3_Settle",             "SettledTx"):       1,
        ("t4_Reconciliation",     "SettledTx"):       1,  # reconciliation loops
        ("t5_AcknowledgeReceipt", "RecipientWallet"): send_amount,
    }

    # flow_heyting[(transition, place)] = Heyting-value increment
    # Central-bank backbone: trust hub directly reaches ⊤_pub.
    flow_heyting = {
        ("t2_BakongClear",    "TrustHub"):    H.T_PUB,
        ("t3_Settle",         "TrustHub"):    H.T_PUB,
        ("t1_InitiateSend",   "SystemicLoad"): H.T_PRIV,  # tx pending = light load
        ("t4_Reconciliation", "SystemicLoad"): H.T_BANK,  # reconciled = bank-level
    }

    initial = Marking(
        visible={
            "UserWallet": initial_balance,
            "PendingTx": 0,
            "NBCBackbone": 1,        # central bank is always present
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
        name="Bakong (Cambodia, central_bank)",
    )


# A single "send 10 from user to recipient" requires this sequence
STANDARD_TX_SEQUENCE = [
    "t1_InitiateSend",
    "t2_BakongClear",
    "t3_Settle",
    "t4_Reconciliation",
    "t5_AcknowledgeReceipt",
]
