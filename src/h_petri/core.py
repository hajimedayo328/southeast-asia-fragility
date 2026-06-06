"""
H-Petri Net (Heyting-valued Petri Net) core implementation.

Theoretical basis:
- notes/06_heyting_petri_net.md (mathematical formalization)
- notes/07_common_cpn_spec.md  (common CPN specification)

Reference:
- Standard Petri Nets: Petri 1962, Meseguer & Montanari 1990
- Open Petri Nets:     Baez & Master 2018 (arXiv:1808.05415)
- Heyting algebra:     Jia 2024 (Heyting Algebra in Flat Origami)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Hashable
from copy import deepcopy


# ---------------------------------------------------------------------------
# Heyting Algebra
# ---------------------------------------------------------------------------

class HeytingAlgebra:
    """Abstract base for a complete Heyting algebra.

    Subclasses must define:
      - top, bottom
      - join(a, b)
      - meet(a, b)
      - leq(a, b)  : partial order a ≤ b
    """

    @property
    def top(self):
        raise NotImplementedError

    @property
    def bottom(self):
        raise NotImplementedError

    def join(self, a, b):
        raise NotImplementedError

    def meet(self, a, b):
        raise NotImplementedError

    def leq(self, a, b) -> bool:
        raise NotImplementedError


class FourLevelHA(HeytingAlgebra):
    """Four-level Heyting algebra used to encode legal protection strength.

    Element order (bottom to top):
        BOTTOM < T_PRIV < T_BANK < T_PUB

    Interpretation:
        BOTTOM  : no evidence of trust
        T_PRIV  : private-platform-level evidence (e.g. company guarantee)
        T_BANK  : bank-consortium-level evidence (banking law + deposit insurance)
        T_PUB   : public/sovereign-level evidence (central bank, state)

    This embeds the half-order:
        ⊤_public ≥ ⊤_bank ≥ ⊤_private
    that the project relies on.
    """

    BOTTOM = "⊥"
    T_PRIV = "⊤_priv"
    T_BANK = "⊤_bank"
    T_PUB = "⊤_pub"

    ORDER = [BOTTOM, T_PRIV, T_BANK, T_PUB]  # ascending

    @property
    def top(self):
        return self.T_PUB

    @property
    def bottom(self):
        return self.BOTTOM

    def _rank(self, a) -> int:
        return self.ORDER.index(a)

    def join(self, a, b):
        return self.ORDER[max(self._rank(a), self._rank(b))]

    def meet(self, a, b):
        return self.ORDER[min(self._rank(a), self._rank(b))]

    def leq(self, a, b) -> bool:
        return self._rank(a) <= self._rank(b)

    def implies(self, a, b):
        """Heyting relative pseudocomplement a ⇒ b.

        For a totally-ordered (chain) Heyting algebra:
            a ⇒ b = ⊤   if a ≤ b
                  = b    otherwise
        Used by enriched right Kan extensions (notes/27 §5).
        """
        if self._rank(a) <= self._rank(b):
            return self.T_PUB
        return b


# ---------------------------------------------------------------------------
# Petri Net structures
# ---------------------------------------------------------------------------

@dataclass
class Marking:
    """Current state of an H-Petri Net.

    visible:    place_id -> int (token count, standard P/T)
    invisible:  place_id -> Heyting value
    """

    visible: dict[str, int] = field(default_factory=dict)
    invisible: dict[str, str] = field(default_factory=dict)

    def copy(self) -> "Marking":
        return Marking(
            visible=dict(self.visible),
            invisible=dict(self.invisible),
        )

    def __repr__(self):
        return f"Marking(visible={self.visible}, invisible={self.invisible})"


@dataclass
class HPetriNet:
    """Heyting-valued Petri Net.

    Following notes/06 §4 formalization:
        N = (P_v, P_h, T, F_v, F_h, M_0, H)

    Attributes:
        places_visible:  list of visible place IDs
        places_invisible:list of invisible (Heyting-valued) place IDs
        transitions:     list of transition IDs
        flow_in:         dict[(place, trans)] = weight     (P_v × T → ℕ)
        flow_out:        dict[(trans, place)] = weight     (T × P_v → ℕ)
        flow_heyting:    dict[(trans, place)] = H value    (T × P_h → H)
        initial:         initial marking M_0
        heyting:         the underlying Heyting algebra H
    """

    places_visible: list[str]
    places_invisible: list[str]
    transitions: list[str]
    flow_in: dict[tuple[str, str], int]
    flow_out: dict[tuple[str, str], int]
    flow_heyting: dict[tuple[str, str], str]
    initial: Marking
    heyting: HeytingAlgebra
    name: str = "unnamed"

    def pre_visible(self, t: str) -> dict[str, int]:
        return {p: w for (p, tt), w in self.flow_in.items() if tt == t}

    def post_visible(self, t: str) -> dict[str, int]:
        return {p: w for (tt, p), w in self.flow_out.items() if tt == t}

    def post_heyting(self, t: str) -> dict[str, str]:
        return {p: v for (tt, p), v in self.flow_heyting.items() if tt == t}


# ---------------------------------------------------------------------------
# Firing rule
# ---------------------------------------------------------------------------

def enabled(net: HPetriNet, marking: Marking, t: str) -> bool:
    """Check whether transition t is enabled at the given marking.

    Per notes/06 §4.2: enabledness is determined only by the visible layer.
    """
    pre = net.pre_visible(t)
    for p, w in pre.items():
        if marking.visible.get(p, 0) < w:
            return False
    return True


def fire(net: HPetriNet, marking: Marking, t: str) -> Marking:
    """Fire transition t and return the resulting marking.

    Per notes/06 §4.2:
      visible:   M'(p_v) = M(p_v) − F_v(p_v,t) + F_v(t,p_v)
      invisible: M'(p_h) = M(p_h) ∨ F_h(t,p_h)         (monotone join)
    """
    if not enabled(net, marking, t):
        raise ValueError(f"transition {t!r} not enabled at {marking}")

    new = marking.copy()

    # visible update
    for p, w in net.pre_visible(t).items():
        new.visible[p] = new.visible.get(p, 0) - w
    for p, w in net.post_visible(t).items():
        new.visible[p] = new.visible.get(p, 0) + w

    # invisible update (monotone join)
    H = net.heyting
    for p, incr in net.post_heyting(t).items():
        current = new.invisible.get(p, H.bottom)
        new.invisible[p] = H.join(current, incr)

    return new


def fire_sequence(net: HPetriNet, marking: Marking, seq: list[str]) -> list[Marking]:
    """Fire a sequence of transitions, returning the trajectory of markings."""
    trajectory = [marking.copy()]
    current = marking
    for t in seq:
        current = fire(net, current, t)
        trajectory.append(current)
    return trajectory


# ---------------------------------------------------------------------------
# Simple metrics
# ---------------------------------------------------------------------------

def trust_reached_at(
    trajectory: list[Marking],
    place: str,
    target_value: str,
    ha: HeytingAlgebra,
) -> int | None:
    """Return the step index at which marking[place] first reaches target_value
    (in the ≥ sense of the Heyting order). Returns None if never reached.
    """
    for i, m in enumerate(trajectory):
        v = m.invisible.get(place, ha.bottom)
        if ha.leq(target_value, v):
            return i
    return None


def systemic_load_curve(
    trajectory: list[Marking],
    place: str,
    ha: HeytingAlgebra,
) -> list[int]:
    """Return list of integer rank (in ORDER) of marking[place] over time.

    Only meaningful for FourLevelHA-style ordered algebras.
    """
    if not isinstance(ha, FourLevelHA):
        raise NotImplementedError("rank curve requires FourLevelHA")
    return [ha._rank(m.invisible.get(place, ha.bottom)) for m in trajectory]
