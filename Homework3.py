from Semiring import (
    Semiring, remove_duplicates, BoolSemiring, DoubleSemiring
)
from math import inf

# Here's a generic automaton type that takes a semiring
# and uses it to perform operations on its values.
class GenericAutomaton():
    def __init__(self, starts, ends, deltas, semiring):
        self.starts = starts
        self.ends = ends
        self.deltas = deltas
        self.sr = semiring

    def all_states(self):
        # Returns all states in the FSA
        return remove_duplicates(
            [q for (q, _) in self.starts] + 
            [q for (q, _) in self.ends] + 
            [q for (q1, _, _, q2) in self.deltas for q in (q1, q2)]
        )

    def init(self, q):
        return self.sr.big_gdisj([v for (q1, v) in self.starts if q == q1])

    def fin(self, q):
        return self.sr.big_gdisj([v for (q1, v) in self.ends if q == q1])

    def tr(self, q1, x, q2):
        return self.sr.big_gdisj(
            [p for (q3, y, p, q4) in self.deltas if (q3, y, q4) == (q1, x, q2)]
        )

    def backward(self, sequence, q):
        if not sequence:
            return self.fin(q)
        first = sequence[0]
        rest = sequence[1:]
        return self.sr.big_gdisj(
            [self.sr.gconj(self.tr(q, first, q1), self.backward(rest, q1)) 
             for q1 in self.all_states() if self.tr(q, first, q1) != self.sr.gfalse]
        )

    def val_b(self, sequence):
        return self.sr.big_gdisj(
            [self.sr.gconj(self.init(q), self.backward(sequence, q)) 
             for q in self.all_states() if self.init(q) != self.sr.gfalse]
        )
    #####################
    # QUESTIONS 1 and 2 #
    #####################
    def forward(self, sequence, q):
        if not sequence:
            return self.init(q)
        last = sequence[-1]
        rest = sequence[:-1]
        return self.sr.big_gdisj(
            [self.sr.gconj(self.forward(rest, qn), self.tr(qn, last, q))
             for qn in self.all_states() if self.tr(qn, last, q) != self.sr.gfalse]
        )

    def val_f(self, sequence):
        return self.sr.big_gdisj(
            [self.sr.gconj(self.forward(sequence, q), self.fin(q))
             for q in self.all_states() if self.fin(q) != self.sr.gfalse]
        )


# Corresponds to the PFSA used in examples in class
gfsa1 = GenericAutomaton(
    starts = [("Edge", 1.0)],
    ends = [("Edge", 0.5)],
    deltas = [
      #  ("Edge", 'a', 0.015, "Edge"),       ("Internal", 'a', 0.042, "Edge"),
        ("Edge", 'i', 0.015, "Edge"),       ("Internal", 'e', 0.056, "Edge"),
                                            ("Internal", 'i', 0.014, "Edge"),
                                            ("Internal", 'n', 0.098, "Edge"),
                                            ("Internal", 't', 0.084, "Edge"),
                                            ("Internal", 's', 0.154, "Edge"), 
        ("Edge", 'a', 0.103, "Internal"),   ("Internal", 'a', 0.085, "Internal"),
        ("Edge", 'e', 0.029, "Internal"),   ("Internal", 'e', 0.149, "Internal"),
        ("Edge", 'i', 0.088, "Internal"),   ("Internal", 'i', 0.149, "Internal"),
        ("Edge", 'n', 0.029, "Internal"),   ("Internal", 'n', 0.085, "Internal"),
        ("Edge", 't', 0.103, "Internal"),   ("Internal", 't', 0.021, "Internal"),
        ("Edge", 's', 0.118, "Internal"),   ("Internal", 's', 0.064, "Internal")
    ],
    semiring = DoubleSemiring()
)

# Corresponds to the FSA over the alphabet {C,V} that requires either two Cs or
# two Vs (or both), now expressed as a generic automaton that has booleans as
# its values
gfsa2 = GenericAutomaton(
    starts = [(40, True)],
    ends = [(43, True)],
    deltas = [
        (40, 'C', True, 40),      (41, 'C', True, 43),
        (40, 'V', True, 40),      (42, 'V', True, 43),
        (40, 'C', True, 41),      (43, 'C', True, 43),
        (40, 'V', True, 42),      (43, 'V', True, 43)
    ],
    semiring = BoolSemiring()
)

##############
# QUESTION 3 #
##############

class CostSemiring(Semiring):
    # Replace these with your own values
    gtrue = 0
    gfalse = inf

    def gconj(self, x, y):
        if x == inf or y == inf:
            return inf
        else:
            return x + y


    def gdisj(self, x, y):
        if x == y:
            return x
        elif x == inf:
            return y
        elif y == inf:
            return x
        elif x > y:
            return y
        else:
            return x


# You don't need to modify gfsa3
gfsa3 = GenericAutomaton(
    starts = [(10, 0)],
    ends = [(12, 0)],
    deltas = [
        (10, 'C', 5, 10),
        (10, 'V', 4, 10),
        (10, 'C', 0, 11),
        (11, 'C', 0, 12),
        (12, 'C', 7, 12),
        (12, 'V', 8, 12)
    ],
    semiring = CostSemiring()
)

##############
# QUESTION 4 #
##############

class SetOfStringsSemiring(Semiring):
    # Replace these with your own values
    gtrue = ['']
    gfalse = []

    def gconj(self, x, y):
        conj_list = []
        for f_el in x:
            for s_el in y:
                conj_list.append(f_el + s_el)
        return conj_list

    def gdisj(self, x, y):
        return x + y


##############
# QUESTION 5 #
##############

# Add your definition of the FST here
gfsa4 = GenericAutomaton(
    starts = [(0, [''])],
    ends = [(0, ['']), (1, ['']), (2, ['t'])],
    deltas = [
        (0, 'n', ['n'], 0),
        (0, 't', ['t'], 0),
        (0, 'a', ['a'], 1),
        (1, 'a', ['a'], 1),
        (1, 'n', ['n'], 0),
        (1, 't', [''], 2),
        (2, 'a', ['ta', 'Ta'], 1),
        (2, 'n', ['tn'], 0),
        (2, 't', ['tt'], 0)
    ],
    semiring = SetOfStringsSemiring()
)

# testing

print(gfsa2.forward("CC", 42))
print(gfsa2.forward("CC", 41))
print(gfsa2.forward("CC", 40))
print(gfsa2.forward("V", 42))
print(gfsa2.forward("V", 41))
print(gfsa2.forward("V", 40))
print(gfsa1.forward("en", "Internal"))
print(1.0 * 0.029 * 0.085)
print(gfsa1.forward("at", "Internal"))
print(1.0 * 0.015 * 0.103 + 1.0 * 0.103 * 0.021)
print("val_f testing")
print(gfsa1.val_f("eta"))
print(gfsa1.val_f("ena"))
print(gfsa2.val_f("CCC"))
print(gfsa2.val_f("CVC"))
print(gfsa2.val_f("CVCC"))
print("cost_semiring testing")
cost_semiring = CostSemiring()
print(cost_semiring.gconj(3, 4))
print(cost_semiring.gconj(3, inf))
print(cost_semiring.gconj(inf, 4))
print(cost_semiring.gdisj(3, 4))
print(cost_semiring.gdisj(3, inf))
print(cost_semiring.gdisj(inf, 4))
print(cost_semiring.gdisj(inf, inf))
print(cost_semiring.distrib_rhs(3, 4, 5))
print(cost_semiring.distrib_lhs(3, 4, 5))
print(cost_semiring.dotprod([3, 4, inf], [inf, 10, inf]))
print(cost_semiring.dotprod([3, inf, inf], [inf, 10, inf]))
print(cost_semiring.expn(2, 3))
print(cost_semiring.big_gconj([0, 5, 0, 0, 0]))
print(cost_semiring.big_gdisj([5, 7, inf]))
print(gfsa3.tr(10, 'C', 10))
print(gfsa3.tr(10, 'V', 11))
print(gfsa3.init(11))
print(gfsa3.fin(12))
print(gfsa3.val_f('CCC'))
print(gfsa3.val_f('CC'))
print(gfsa3.val_f('CV'))
print(gfsa3.val_f('CCCVC'))
print(gfsa3.val_f('CVCCC'))
print("setofstring testing")
ss_semiring = SetOfStringsSemiring()
print(ss_semiring.gdisj(['hello', 'world'], ['foo', 'bar']))
print(ss_semiring.gconj(['hello', 'world'], ['foo', 'bar']))
print(ss_semiring.gdisj(['hello', 'world'], []))
print(ss_semiring.gconj(['hello', 'world'], []))
print(ss_semiring.gconj(['hello', 'world'], ['']))
print(ss_semiring.big_gconj([['tic', 'tac', 'toe'], ['do', 're', 'mi'],
['foo']]))
print(ss_semiring.big_gdisj([['tic', 'tac', 'toe'], ['do', 're', 'mi'],
['foo']]))
print(ss_semiring.dotprod([['hello', 'world'], ['one', 'two']], [['x'],
['foo', 'bar']]))
print(ss_semiring.expn(['aaa', 'bb'], 3))
print("gfsa4 testing")
print(gfsa4.tr(2, 'a', 1))
print(gfsa4.init(1))
print(gfsa4.fin(1))
print(gfsa4.val_f('atan'))
print(gfsa4.val_f('atat'))
print(gfsa4.val_f('atnat'))
print(gfsa4.val_f('tatatnat'))
print(gfsa4.val_b('atan'))
print(gfsa4.val_b('atat'))
print(gfsa4.val_b('atnat'))
print(gfsa4.val_b('tatatnat'))

print(gfsa1.forward('aa', "Internal"))