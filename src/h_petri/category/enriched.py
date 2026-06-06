"""
H-enriched category + H-functor (notes/27).

An H-enriched category (a Heyting-valued preorder, i.e. a category enriched
over the commutative quantale (H, ∨, ∧, ⊤_pub)) is given by:
  - a finite object set
  - hom(A,B) ∈ H = "influence strength of A on B"
  - axioms:  ⊤_pub ≤ hom(A,A)            (identity)
             hom(A,B) ∧ hom(B,C) ≤ hom(A,C)   (composition = meet bottleneck)

We build categories the SAFE way: from a set of *generating* influences
(a directed H-labelled graph) we take the meet-transitive closure
(widest-path: hom(A,B) = ⋁_paths ⋀_edges).  This is the free H-enriched
category on the graph and SATISFIES THE AXIOMS BY CONSTRUCTION, so the
hom matrix is always a legitimate category — no hand-tuning that secretly
breaks transitivity.

An H-functor F: 𝓒 → 𝓓 is an object map with the lax functoriality law
    hom_𝓒(A,B) ≤ hom_𝓓(FA,FB).
It is *strict* (isometric) when equality holds everywhere.

Reference: Lawvere 1973 "Metric spaces, generalized logic, and closed
categories"; quantale-enriched categories (Stubbe 2005).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from itertools import product

from h_petri.core import FourLevelHA


@dataclass
class EnrichedCategory:
    """A finite H-enriched category given by its hom matrix."""
    name: str
    objects: tuple[str, ...]
    hom: dict[tuple[str, str], str]          # (A,B) -> H value (closed)
    ha: FourLevelHA = field(default_factory=FourLevelHA)

    # ---- construction -----------------------------------------------------

    @classmethod
    def from_generators(
        cls,
        name: str,
        objects: list[str],
        generators: dict[tuple[str, str], str],
        ha: FourLevelHA | None = None,
    ) -> "EnrichedCategory":
        """Build the free H-enriched category from generating influences.

        hom(A,B) = widest path = ⋁ over directed paths A→B of ⋀ edge weights.
        Diagonal = ⊤_pub. Computed by a (∨,∧) Floyd–Warshall.
        Guarantees the identity + composition axioms.
        """
        ha = ha or FourLevelHA()
        objs = list(objects)
        # init: diagonal = ⊤_pub, given generators, else ⊥
        h: dict[tuple[str, str], str] = {}
        for a, b in product(objs, objs):
            if a == b:
                h[(a, b)] = ha.T_PUB
            else:
                h[(a, b)] = generators.get((a, b), ha.bottom)
        # Floyd–Warshall with (join = ∨, along-path = ∧)
        for k in objs:
            for i in objs:
                for j in objs:
                    through_k = ha.meet(h[(i, k)], h[(k, j)])
                    h[(i, j)] = ha.join(h[(i, j)], through_k)
        return cls(name=name, objects=tuple(objs), hom=h, ha=ha)

    # ---- queries ----------------------------------------------------------

    def hom_of(self, a: str, b: str) -> str:
        return self.hom.get((a, b), self.ha.bottom)

    # ---- axiom verification (should always pass after closure) ------------

    def check_identity_axiom(self) -> list[str]:
        """Return list of objects violating ⊤_pub ≤ hom(A,A)."""
        bad = []
        for a in self.objects:
            if not self.ha.leq(self.ha.T_PUB, self.hom_of(a, a)):
                bad.append(a)
        return bad

    def check_composition_axiom(self) -> list[tuple[str, str, str]]:
        """Return triples (A,B,C) violating hom(A,B)∧hom(B,C) ≤ hom(A,C)."""
        bad = []
        for a, b, c in product(self.objects, repeat=3):
            lhs = self.ha.meet(self.hom_of(a, b), self.hom_of(b, c))
            if not self.ha.leq(lhs, self.hom_of(a, c)):
                bad.append((a, b, c))
        return bad

    def is_valid(self) -> dict:
        idv = self.check_identity_axiom()
        cmv = self.check_composition_axiom()
        return {
            "valid": not idv and not cmv,
            "identity_violations": idv,
            "composition_violations": cmv,
        }


@dataclass
class VFunctor:
    """An H-functor F: source → target given by an object map."""
    name: str
    source: EnrichedCategory
    target: EnrichedCategory
    object_map: dict[str, str]
    ha: FourLevelHA = field(default_factory=FourLevelHA)

    def _pairs(self):
        for a, b in product(self.source.objects, repeat=2):
            fa = self.object_map[a]
            fb = self.object_map[b]
            yield a, b, self.source.hom_of(a, b), self.target.hom_of(fa, fb)

    def classify(self) -> dict:
        """Classify F per object pair and overall.

        Per pair:
          equal       : hom_src == hom_tgt
          amplified   : hom_src <  hom_tgt   (Dev strengthens the influence)
          attenuated  : hom_src >  hom_tgt   (Dev weakens it) -> breaks lax law
        Overall:
          strict      : all equal (isometric V-functor) -> strongest prediction
          lax         : all hom_src ≤ hom_tgt, some <    -> valid V-functor, Dev amplifies
          broken      : some hom_src > hom_tgt            -> NOT a (lax) V-functor;
                        the prediction leaks at those pairs
        distortion = Σ (rank(hom_tgt) - rank(hom_src))   (signed total skew)
        """
        per_pair = []
        amplified = attenuated = equal = 0
        distortion = 0
        for a, b, hs, ht in self._pairs():
            rs, rt = self.ha._rank(hs), self.ha._rank(ht)
            distortion += rt - rs
            if rs == rt:
                kind = "equal"; equal += 1
            elif rs < rt:
                kind = "amplified"; amplified += 1
            else:
                kind = "attenuated"; attenuated += 1
            per_pair.append({
                "a": a, "b": b, "F(a)": self.object_map[a], "F(b)": self.object_map[b],
                "hom_src": hs, "hom_tgt": ht, "kind": kind,
            })

        if attenuated > 0:
            verdict = "broken"
        elif amplified > 0:
            verdict = "lax"
        else:
            verdict = "strict"

        return {
            "functor": self.name,
            "verdict": verdict,
            "counts": {"equal": equal, "amplified": amplified, "attenuated": attenuated},
            "distortion": distortion,
            "is_valid_V_functor": attenuated == 0,
            "per_pair": per_pair,
        }
