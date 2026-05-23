"""
KBZPay (Myanmar, bank/private-border backbone) H-Petri Net.

Per notes/07 §4.4 specification.

backbone_type: bank (structurally) — but single-bank dominance (KBZ Bank),
functionally close to private platform.

This is the "grey-zone classification" example.
TrustHub upper bound: ⊤_bank (bank law) but with single-point risk.
"""

from __future__ import annotations
from h_petri.core import HPetriNet, Marking, FourLevelHA


def build_kbzpay_net(initial_balance: int = 100, send_amount: int = 10) -> HPetriNet:
    H = FourLevelHA()

    places_visible = ["UserWallet", "PendingTx", "KBZBank",
                      "SettledTx", "RecipientWallet"]
    places_invisible = ["TrustHub", "SystemicLoad"]

    transitions = ["t1_InitiateSend", "t2_KBZClear", "t3_Settle",
                   "t4_Reconciliation", "t5_AcknowledgeReceipt"]

    flow_in = {
        ("UserWallet", "t1_InitiateSend"):        send_amount,
        ("PendingTx",  "t2_KBZClear"):            1,
        ("KBZBank",    "t2_KBZClear"):            1,
        ("KBZBank",    "t3_Settle"):              1,
        ("SettledTx",  "t4_Reconciliation"):      1,
        ("SettledTx",  "t5_AcknowledgeReceipt"):  1,
    }

    flow_out = {
        ("t1_InitiateSend",       "PendingTx"):       1,
        ("t2_KBZClear",           "KBZBank"):         1,
        ("t3_Settle",             "KBZBank"):         1,
        ("t3_Settle",             "SettledTx"):       1,
        ("t4_Reconciliation",     "SettledTx"):       1,
        ("t5_AcknowledgeReceipt", "RecipientWallet"): send_amount,
    }

    # KBZ: bank-law-protected (⊤_bank) but single bank → similar concentration risk to private.
    flow_heyting = {
        ("t2_KBZClear",       "TrustHub"):     H.T_BANK,
        ("t3_Settle",         "TrustHub"):     H.T_BANK,
        ("t1_InitiateSend",   "SystemicLoad"): H.T_BANK,  # heavier load (no consortium spread)
        ("t4_Reconciliation", "SystemicLoad"): H.T_BANK,
    }

    initial = Marking(
        visible={
            "UserWallet": initial_balance,
            "PendingTx": 0,
            "KBZBank": 1,
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
        name="KBZPay (Myanmar, bank single-dominant)",
    )


STANDARD_TX_SEQUENCE = [
    "t1_InitiateSend",
    "t2_KBZClear",
    "t3_Settle",
    "t4_Reconciliation",
    "t5_AcknowledgeReceipt",
]
