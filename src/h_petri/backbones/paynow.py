"""
PayNow (Singapore, bank-consortium backbone) H-Petri Net.

Per notes/07 §4.3 specification.

backbone_type: bank
TrustHub upper bound: ⊤_bank (bank consortium + deposit insurance)

Note: PayNow is MAS-supervised, ABS-operated. The bank consortium
backbone differs from a single-bank backbone (KBZPay) — multiple banks
must agree on each clearing.
"""

from __future__ import annotations
from h_petri.core import HPetriNet, Marking, FourLevelHA


def build_paynow_net(initial_balance: int = 100, send_amount: int = 10) -> HPetriNet:
    H = FourLevelHA()

    places_visible = ["UserWallet", "PendingTx", "BankConsortium",
                      "SettledTx", "RecipientWallet"]
    places_invisible = ["TrustHub", "SystemicLoad"]

    transitions = ["t1_InitiateSend", "t2_PayNowClear", "t3_Settle",
                   "t4_Reconciliation", "t5_AcknowledgeReceipt"]

    flow_in = {
        ("UserWallet",     "t1_InitiateSend"):       send_amount,
        ("PendingTx",      "t2_PayNowClear"):        1,
        ("BankConsortium", "t2_PayNowClear"):        1,
        ("BankConsortium", "t3_Settle"):             1,
        ("SettledTx",      "t4_Reconciliation"):     1,
        ("SettledTx",      "t5_AcknowledgeReceipt"): 1,
    }

    flow_out = {
        ("t1_InitiateSend",       "PendingTx"):       1,
        ("t2_PayNowClear",        "BankConsortium"):  1,
        ("t3_Settle",             "BankConsortium"):  1,
        ("t3_Settle",             "SettledTx"):       1,
        ("t4_Reconciliation",     "SettledTx"):       1,
        ("t5_AcknowledgeReceipt", "RecipientWallet"): send_amount,
    }

    # Bank consortium: trust hub maxes out at ⊤_bank (banking law + deposit insurance).
    flow_heyting = {
        ("t2_PayNowClear",    "TrustHub"):     H.T_BANK,
        ("t3_Settle",         "TrustHub"):     H.T_BANK,
        ("t1_InitiateSend",   "SystemicLoad"): H.T_PRIV,
        ("t4_Reconciliation", "SystemicLoad"): H.T_BANK,  # bank-level reconciliation
    }

    initial = Marking(
        visible={
            "UserWallet": initial_balance,
            "PendingTx": 0,
            "BankConsortium": 1,
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
        name="PayNow (Singapore, bank consortium)",
    )


STANDARD_TX_SEQUENCE = [
    "t1_InitiateSend",
    "t2_PayNowClear",
    "t3_Settle",
    "t4_Reconciliation",
    "t5_AcknowledgeReceipt",
]
