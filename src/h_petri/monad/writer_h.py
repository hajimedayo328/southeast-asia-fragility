"""
Writer H monad — invisible cost accumulation as a categorical structure.

Implements the construction described in notes/24:
  - Writer w a = (a, w)   where w is a monoid (here: 4-level Heyting algebra with ∨)
  - return x   = (x, ⊥)
  - bind f >>= g = (b, h_f ∨ h_g)   where (b, h_f) = f(a)

Order-independence of accumulated effect (notes/24 §3.3):
  The total effect of any composition  f_n >>= ... >>= f_1  is
      h_1 ∨ h_2 ∨ ... ∨ h_n
  which is independent of order/grouping. This is NOT a novel theorem — it is
  the standard property of a (bounded) join-semilattice: ∨ is associative,
  commutative and idempotent. (We previously over-labelled this an "Effect
  Accumulation Theorem"; it is just the semilattice law.)

This module checks that the implementation respects that law (720 permutations
all collapse to the same join) and shows that an H-Petri Net firing sequence
has the same accumulation signature as a chain of Writer-Kleisli arrows.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from h_petri.core import FourLevelHA


A = TypeVar("A")
B = TypeVar("B")


# ---------------------------------------------------------------------------
# Writer H monad
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Writer(Generic[A]):
    """A Writer-monad value: a pair (value, log) where log is a Heyting element.

    The Heyting algebra (4-level) acts as the monoid via (∨, ⊥).
    """
    value: A
    log: str  # one of {"⊥", "⊤_priv", "⊤_bank", "⊤_pub"}

    def bind(self, f: "Callable[[A], Writer[B]]", ha: FourLevelHA) -> "Writer[B]":
        """Monadic bind (>>=). Accumulates the log via Heyting join (∨)."""
        next_writer = f(self.value)
        return Writer(value=next_writer.value, log=ha.join(self.log, next_writer.log))


def unit(value: A, ha: FourLevelHA) -> Writer[A]:
    """η: pure value with no side effect."""
    return Writer(value=value, log=ha.bottom)


def kleisli_compose(
    arrows: list[Callable[[A], Writer[A]]],
    initial: A,
    ha: FourLevelHA,
) -> Writer[A]:
    """Compose a chain of Kleisli arrows left-to-right and return the result."""
    acc = unit(initial, ha)
    for f in arrows:
        acc = acc.bind(f, ha)
    return acc


# ---------------------------------------------------------------------------
# Convenience constructors for the 4-level Heyting alphabet
# ---------------------------------------------------------------------------

def cost(level: str) -> Callable[[A], Writer[A]]:
    """Build a Kleisli arrow that leaves the value unchanged but emits a Heyting cost."""
    def arrow(a: A) -> Writer[A]:
        return Writer(value=a, log=level)
    return arrow


# ---------------------------------------------------------------------------
# Order-independence check (join-semilattice law, notes/24 §3.3)
# ---------------------------------------------------------------------------

def verify_effect_accumulation(ha: FourLevelHA) -> dict:
    """Check the join-semilattice law (notes/24 §3.3) constructively.

    For every permutation of a fixed list of Heyting-valued costs, the
    accumulated log must be identical (= ∨ of all costs). This is a known
    property of ∨ (assoc/comm/idempotent), not a new theorem — the check
    just confirms the implementation respects it.
    """
    from itertools import permutations

    costs = [ha.T_PRIV, ha.T_BANK, ha.T_PRIV, ha.T_PUB, ha.bottom, ha.T_BANK]
    expected = costs[0]
    for c in costs[1:]:
        expected = ha.join(expected, c)

    results = {}
    for perm in permutations(range(len(costs))):
        arrows = [cost(costs[i]) for i in perm]
        out = kleisli_compose(arrows, initial=None, ha=ha)
        results[perm] = out.log

    all_match = all(v == expected for v in results.values())
    distinct_logs = sorted(set(results.values()), key=ha._rank)

    return {
        "costs": costs,
        "expected_join": expected,
        "num_permutations_tested": len(results),
        "all_permutations_yield_same_log": all_match,
        "distinct_logs_observed": distinct_logs,
    }


# ---------------------------------------------------------------------------
# Bridge to H-Petri Net: a firing sequence as a Writer chain
# ---------------------------------------------------------------------------

def petri_firing_as_writer_chain(net, initial_marking, sequence: list[str]) -> Writer[str]:
    """Reinterpret an H-Petri Net firing sequence as a Writer chain.

    Each transition contributes the join of all Heyting weights it writes to
    invisible places. The accumulated log is the overall systemic cost.
    """
    from h_petri.core import fire

    ha = net.heyting
    arrows: list[Callable[[str], Writer[str]]] = []
    for t_name in sequence:
        # Gather all Heyting weights this transition writes (over invisible places)
        weights = [
            w for (t, p), w in net.flow_heyting.items() if t == t_name
        ]
        if not weights:
            arrows.append(cost(ha.bottom))
        else:
            tx_cost = weights[0]
            for w in weights[1:]:
                tx_cost = ha.join(tx_cost, w)
            arrows.append(cost(tx_cost))

    return kleisli_compose(arrows, initial=net.name, ha=ha)


# ---------------------------------------------------------------------------
# CLI / sanity check
# ---------------------------------------------------------------------------

def main():
    import sys
    import json
    from pathlib import Path

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ha = FourLevelHA()

    print("=" * 70)
    print("Writer H Monad — join-semilattice order-independence check (notes/24 §3.3)")
    print("=" * 70)
    v = verify_effect_accumulation(ha)
    print(f"\nCosts emitted (in original order): {v['costs']}")
    print(f"Expected join (∨ all costs):       {v['expected_join']}")
    print(f"# permutations tested:             {v['num_permutations_tested']}")
    print(f"All permutations same log?         {v['all_permutations_yield_same_log']}")
    print(f"Distinct logs observed:            {v['distinct_logs_observed']}")
    print(
        "\n→ The join-semilattice law holds for the 4-level Heyting algebra:"
        " associativity/commutativity/idempotency of ∨ guarantee"
        " path-independence of total cost (known property, not a new theorem)."
    )

    # Bridge demo — apply to all 4 finance backbones
    print("\n" + "-" * 70)
    print("Bridge demo: H-Petri Net firing sequence as Writer chain")
    print("-" * 70)
    from h_petri.backbones import bakong, gcash, paynow, kbzpay

    SEQ = [
        "t1_InitiateSend",
        "t2_BackboneClear",
        "t3_Settle",
        "t4_Reconciliation",
        "t5_AcknowledgeReceipt",
    ] * 3

    bridge_results = []
    for builder, label in [
        (bakong.build_bakong_net, "Bakong"),
        (paynow.build_paynow_net, "PayNow"),
        (kbzpay.build_kbzpay_net, "KBZPay"),
        (gcash.build_gcash_net, "GCash"),
    ]:
        net = builder()
        w = petri_firing_as_writer_chain(net, net.initial, SEQ)
        bridge_results.append({"backbone": label, "kleisli_log": w.log})
        print(f"  {label:8s} → final Writer log = {w.log}")

    print(
        "\n→ Bakong's Kleisli chain accumulates to ⊤_pub, GCash to ⊤_priv."
        " Same chain length, structurally different total cost. This is the"
        " monadic restatement of the §P4 finding."
    )

    # Write JSON for Pages consumption
    bundle = {
        "description": (
            "Writer H monad — invisible cost accumulation as a categorical "
            "structure (notes/24 §3). Checked that for the 4-level Heyting "
            "algebra, all permutations of a fixed list of costs yield the "
            "same total log. This is the standard join-semilattice law "
            "(∨ assoc/comm/idempotent, §3.3), not a novel theorem."
        ),
        "effect_accumulation": v,
        "bridge_demo": {
            "sequence_length": len(SEQ),
            "results": bridge_results,
            "lesson": (
                "Same Kleisli chain length (15 arrows), but the accumulated "
                "log differs by Heyting rank because each transition emits a "
                "different cost level. The monadic ∨-accumulation re-derives "
                "the §P4 backbone separation without simulating tokens."
            ),
        },
    }
    out_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "data" / "writer_h.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
