"""
Place centrality measures for H-Petri Nets.

Per notes/16 specification.

Five measures implemented:
  - TCC  : Transition Coverage Centrality
  - BI   : Bottleneck Index (reachability loss when place removed)
  - HCC  : Heyting Concentration Centrality (project-specific)
  - HHI-AC : HHI Analog (sum of TCC squared)

TFC (eigenvector-based) is left as future work because it needs numpy
and a careful definition of the relevant adjacency matrix.
"""

from __future__ import annotations
from typing import Iterable

from h_petri.core import HPetriNet, Marking, HeytingAlgebra, fire, enabled


# ---------------------------------------------------------------------------
# Reachability helper
# ---------------------------------------------------------------------------

def reachable_visible_markings(
    net: HPetriNet, M_0: Marking, max_steps: int = 30
) -> set[tuple]:
    """Enumerate reachable visible-marking tuples via BFS.

    For bounded nets this terminates quickly. Returns a set of frozen
    visible-marking representations.
    """
    visited: set[tuple] = set()
    queue: list[Marking] = [M_0]
    seed = tuple(sorted(M_0.visible.items()))
    visited.add(seed)
    while queue:
        m = queue.pop(0)
        if len(visited) > 5000:
            break  # safety cap
        for t in net.transitions:
            if not enabled(net, m, t):
                continue
            m_new = fire(net, m, t)
            key = tuple(sorted(m_new.visible.items()))
            if key not in visited:
                visited.add(key)
                queue.append(m_new)
    return visited


# ---------------------------------------------------------------------------
# Centrality measures
# ---------------------------------------------------------------------------

def transition_coverage_centrality(net: HPetriNet, place: str) -> float:
    """TCC: |{t : place ∈ pre(t) ∪ post(t)}| / |T|

    Pre/post union with multiplicity ignored.
    """
    if not net.transitions:
        return 0.0
    pre_or_post = sum(
        1
        for t in net.transitions
        if place in net.pre_visible(t) or place in net.post_visible(t)
    )
    return pre_or_post / len(net.transitions)


def bottleneck_index(
    net: HPetriNet, place: str, max_steps: int = 30
) -> float:
    """BI: 1 - |reach(N without place)| / |reach(N)|

    Only meaningful for visible places (invisible places don't gate firing
    in H-Petri Nets per notes/06 §4.2).
    """
    if place in net.places_invisible:
        return 0.0

    full = reachable_visible_markings(net, net.initial, max_steps)
    if not full:
        return 0.0

    # Construct net without `place`: remove the place, and remove transitions
    # that need it (pre) or only produce it (post-only)
    surviving_transitions = [
        t for t in net.transitions if place not in net.pre_visible(t)
    ]
    if not surviving_transitions:
        return 1.0  # removing place kills all firing → maximum bottleneck

    reduced_flow_in = {
        (p, t): w
        for (p, t), w in net.flow_in.items()
        if t in surviving_transitions and p != place
    }
    reduced_flow_out = {
        (t, p): w
        for (t, p), w in net.flow_out.items()
        if t in surviving_transitions and p != place
    }
    reduced_flow_heyting = {
        (t, p): v
        for (t, p), v in net.flow_heyting.items()
        if t in surviving_transitions and p != place
    }
    reduced_initial = Marking(
        visible={p: v for p, v in net.initial.visible.items() if p != place},
        invisible=dict(net.initial.invisible),
    )

    reduced_net = HPetriNet(
        places_visible=[p for p in net.places_visible if p != place],
        places_invisible=list(net.places_invisible),
        transitions=surviving_transitions,
        flow_in=reduced_flow_in,
        flow_out=reduced_flow_out,
        flow_heyting=reduced_flow_heyting,
        initial=reduced_initial,
        heyting=net.heyting,
        name=f"{net.name} \\ {{{place}}}",
    )

    partial = reachable_visible_markings(reduced_net, reduced_net.initial, max_steps)
    return 1.0 - len(partial) / len(full)


def heyting_concentration_centrality(net: HPetriNet, place: str):
    """HCC: ⋁_{(t,p)∈F_h : p=place} F_h(t,p)

    The maximum Heyting value any transition writes to this place.
    """
    H = net.heyting
    value = H.bottom
    for (t, p), v in net.flow_heyting.items():
        if p == place:
            value = H.join(value, v)
    return value


def hhi_analog(net: HPetriNet) -> float:
    """HHI-AC = Σ_p TCC(p)² over visible places.

    Higher means more concentrated structure (one place dominates).
    """
    return sum(
        transition_coverage_centrality(net, p) ** 2 for p in net.places_visible
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def full_centrality_report(net: HPetriNet, max_steps: int = 30) -> dict:
    """Compute all centrality measures for every place."""
    report: dict[str, dict] = {}

    for p in net.places_visible:
        report[p] = {
            "kind": "visible",
            "TCC": round(transition_coverage_centrality(net, p), 4),
            "BI":  round(bottleneck_index(net, p, max_steps), 4),
            "HCC": "—",
        }

    for p in net.places_invisible:
        report[p] = {
            "kind": "invisible",
            "TCC": "—",
            "BI":  "—",
            "HCC": heyting_concentration_centrality(net, p),
        }

    return {
        "net": net.name,
        "places": report,
        "HHI_AC": round(hhi_analog(net), 4),
    }
