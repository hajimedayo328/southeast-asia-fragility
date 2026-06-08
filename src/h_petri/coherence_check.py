"""
T2 — coherence check across the project's categorical structures.

The project uses TWO Heyting operations in different roles:
  - ∨ (join)  = cost / trust ACCUMULATION (monotone up): H-Petri firing,
                Writer H monad, ⊗ parallel composition.
  - ∧ (meet)  = BOTTLENECK (weakest link): enriched composition, ▷ cospan,
                sheaf H⁰.
This script verifies the foundations are sound and the structures AGREE, rather
than silently contradicting each other. A failure here is a real bug, not a
cosmetic issue.

Checks:
  C4  Foundation: FourLevelHA actually satisfies the Heyting/lattice laws that
      EVERYTHING depends on — exhaustively. Most important: the Heyting
      adjunction  a∧b ≤ c  ⟺  a ≤ (b⇒c), which is what makes `implies`
      (hence the Kan extensions) correct.
  C1  H-Petri firing is monotone on invisible places (∨ accumulation).
  C2  Writer H monad log ≡ the join of the Petri firing's invisible finals
      (the monad and the simulator agree on total accumulated cost).
  C3  meet-composition agrees across open_net.py and category/from_petri.py.
"""

from __future__ import annotations
import json
import sys
from itertools import product
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from h_petri.core import FourLevelHA, fire_sequence
from h_petri.backbones import bakong, paynow, kbzpay, gcash
from h_petri.monad.writer_h import petri_firing_as_writer_chain
from h_petri.category import from_petri

HA = FourLevelHA()
ELEMS = HA.ORDER  # [⊥, ⊤_priv, ⊤_bank, ⊤_pub]

BUILDERS = {
    "bakong": bakong.build_bakong_net, "paynow": paynow.build_paynow_net,
    "kbzpay": kbzpay.build_kbzpay_net, "gcash": gcash.build_gcash_net,
}
SEQ = ["t1_InitiateSend", "t2_BackboneClear", "t3_Settle",
       "t4_Reconciliation", "t5_AcknowledgeReceipt"] * 3


# ---------------------------------------------------------------------------
# C4 — Heyting / lattice foundation (exhaustive)
# ---------------------------------------------------------------------------

def check_foundation() -> dict:
    fails = []

    def leq(a, b): return HA.leq(a, b)

    # commutativity, idempotency
    for a, b in product(ELEMS, repeat=2):
        if HA.meet(a, b) != HA.meet(b, a): fails.append(("meet comm", a, b))
        if HA.join(a, b) != HA.join(b, a): fails.append(("join comm", a, b))
    for a in ELEMS:
        if HA.meet(a, a) != a: fails.append(("meet idem", a))
        if HA.join(a, a) != a: fails.append(("join idem", a))
        # identities
        if HA.meet(a, HA.T_PUB) != a: fails.append(("meet unit ⊤", a))
        if HA.join(a, HA.BOTTOM) != a: fails.append(("join unit ⊥", a))
        # bounds
        if not leq(HA.BOTTOM, a): fails.append(("⊥ lower", a))
        if not leq(a, HA.T_PUB): fails.append(("⊤ upper", a))

    # associativity + distributivity
    for a, b, c in product(ELEMS, repeat=3):
        if HA.meet(HA.meet(a, b), c) != HA.meet(a, HA.meet(b, c)):
            fails.append(("meet assoc", a, b, c))
        if HA.join(HA.join(a, b), c) != HA.join(a, HA.join(b, c)):
            fails.append(("join assoc", a, b, c))
        if HA.meet(a, HA.join(b, c)) != HA.join(HA.meet(a, b), HA.meet(a, c)):
            fails.append(("distributivity", a, b, c))

    # THE Heyting adjunction: a∧b ≤ c  ⟺  a ≤ (b⇒c)
    heyting_fails = []
    for a, b, c in product(ELEMS, repeat=3):
        lhs = leq(HA.meet(a, b), c)
        rhs = leq(a, HA.implies(b, c))
        if lhs != rhs:
            heyting_fails.append((a, b, c))
    if heyting_fails:
        fails.append(("HEYTING ADJUNCTION a∧b≤c ⟺ a≤b⇒c", len(heyting_fails)))

    return {
        "passed": not fails,
        "num_triples_checked": len(ELEMS) ** 3,
        "heyting_adjunction_ok": not heyting_fails,
        "failures": fails[:10],
    }


# ---------------------------------------------------------------------------
# C1 — H-Petri firing monotone on invisible places
# ---------------------------------------------------------------------------

def check_firing_monotone() -> dict:
    bad = []
    for key, build in BUILDERS.items():
        net = build()
        traj = fire_sequence(net, net.initial, SEQ)
        for p in net.places_invisible:
            prev = HA.BOTTOM
            for m in traj:
                v = m.invisible.get(p, HA.BOTTOM)
                if not HA.leq(prev, v):  # value decreased
                    bad.append((key, p))
                    break
                prev = v
    return {"passed": not bad, "violations": bad}


# ---------------------------------------------------------------------------
# C2 — Writer H monad log ≡ join of Petri invisible finals
# ---------------------------------------------------------------------------

def check_monad_equiv_petri() -> dict:
    rows, ok = [], True
    for key, build in BUILDERS.items():
        net = build()
        traj = fire_sequence(net, net.initial, SEQ)
        final = traj[-1]
        petri_join = HA.BOTTOM
        for p in net.places_invisible:
            petri_join = HA.join(petri_join, final.invisible.get(p, HA.BOTTOM))
        monad_log = petri_firing_as_writer_chain(net, net.initial, SEQ).log
        match = (monad_log == petri_join)
        ok = ok and match
        rows.append({"backbone": key, "monad_log": monad_log,
                     "petri_join_of_invisibles": petri_join, "match": match})
    return {"passed": ok, "rows": rows}


# ---------------------------------------------------------------------------
# C3 — meet-composition agrees across open_net and from_petri
# ---------------------------------------------------------------------------

def check_meet_agreement() -> dict:
    trust = {k: from_petri.trust_from_petri(k) for k in BUILDERS}
    meet_all = HA.T_PUB
    join_all = HA.BOTTOM
    for v in trust.values():
        meet_all = HA.meet(meet_all, v)
        join_all = HA.join(join_all, v)
    open_path = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "open_petri_composition.json"
    open_meet = open_join = None
    if open_path.exists():
        with open(open_path, encoding="utf-8") as f:
            br = json.load(f).get("bottleneck_reversal", {})
        open_meet, open_join = br.get("cospan_bound"), br.get("parallel_bound")
    return {
        "passed": (open_meet == meet_all and open_join == join_all),
        "from_petri_meet": meet_all, "open_net_meet": open_meet,
        "from_petri_join": join_all, "open_net_join": open_join,
    }


def main():
    print("=" * 72)
    print("T2 — coherence check across the project's structures")
    print("=" * 72)

    c4 = check_foundation()
    c1 = check_firing_monotone()
    c2 = check_monad_equiv_petri()
    c3 = check_meet_agreement()

    print(f"\nC4 foundation (Heyting/lattice laws, exhaustive {c4['num_triples_checked']} triples)")
    print(f"   all laws hold: {c4['passed']}   Heyting adjunction a∧b≤c⟺a≤b⇒c: {c4['heyting_adjunction_ok']}")
    if c4["failures"]:
        print(f"   FAILURES: {c4['failures']}")

    print(f"\nC1 H-Petri firing monotone on invisible places: {c1['passed']}")
    if c1["violations"]:
        print(f"   violations: {c1['violations']}")

    print(f"\nC2 Writer H monad log ≡ join of Petri invisible finals: {c2['passed']}")
    for r in c2["rows"]:
        print(f"   {r['backbone']:7s} monad={r['monad_log']:8s} petri-join={r['petri_join_of_invisibles']:8s} {'✓' if r['match'] else '✗'}")

    print(f"\nC3 meet/join agree (open_net vs from_petri): {c3['passed']}")
    print(f"   meet: from_petri={c3['from_petri_meet']} open_net={c3['open_net_meet']} ; "
          f"join: from_petri={c3['from_petri_join']} open_net={c3['open_net_join']}")

    all_ok = c4["passed"] and c1["passed"] and c2["passed"] and c3["passed"]
    print("\n" + "-" * 72)
    print(f"OVERALL COHERENCE: {'✓ all checks pass' if all_ok else '✗ INCONSISTENCY FOUND'}")
    print("Interpretation: ∨ (accumulation) and ∧ (bottleneck) are used in distinct")
    print("roles and the structures (Petri / monad / enriched / open_net) agree on")
    print("the SAME 4-level Heyting algebra, whose laws are exhaustively verified.")

    bundle = {
        "description": (
            "Coherence check (T2). Verifies the foundational Heyting/lattice laws "
            "exhaustively (incl. the adjunction a∧b≤c ⟺ a≤b⇒c that makes `implies` "
            "and the Kan extensions correct), that H-Petri firing is monotone, that "
            "the Writer H monad agrees with the simulator on accumulated cost, and "
            "that meet/join composition agrees across open_net and from_petri."
        ),
        "C4_foundation": c4, "C1_firing_monotone": c1,
        "C2_monad_equiv_petri": c2, "C3_meet_agreement": c3,
        "overall_coherent": all_ok,
    }
    out_path = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "coherence_check.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
