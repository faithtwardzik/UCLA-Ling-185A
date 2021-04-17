# Homework 2
# LING 185A Summer C 2020
# Instructor: Connor Mayer

# Make sure Automaton.py is in the same folder as this file
from Automaton import *

def ensure_unused(reserved_ints, efsa):
    # Given a list of reserved integers and an e-FSA with integer states, 
    # returns a new FSA with no state labels from that list of integers.
    def map_states(f, efsa):
        new_start = f(efsa.start)
        new_ends = [f(end) for end in efsa.ends]
        new_deltas = [(f(q1), x, f(q2)) for (q1, x, q2) in efsa.deltas]
        return EpsAutomaton(new_start, new_ends, new_deltas)

    max_reserved = max(reserved_ints)
    nonneg_efsa = map_states(lambda x: 2 * (-x) - 1 if x < 0 else 2 * x, efsa)
    return map_states(lambda x: x + 1 + max_reserved, nonneg_efsa)


###############
# EPSAUTOMATA #
###############

EPSILON = ""

class EpsAutomaton(Automaton):
    def hat(self, q, w):
        # Corresponds directly to the definition in (11) in the handout:
        # hat takes a starting state and a string, and outputs all the 
        # states that can be reached by emitting that string from the
        # starting state. Includes epsilon transitions.
        if not w:
            return self.epsilon_closure(q)
        else:
            first = w[0]
            rest = w[1:]
            return remove_duplicates(
                [q3 for q1 in self.epsilon_closure(q)
                    for q2 in self.targets(q1, first) 
                    for q3 in self.hat(q2, rest)]
            )

    def epsilon_closure(self, q):
        # Corresponds to definition (6) in handout
        closure = False
        result = [q]
        while not closure:
            prev_result = result
            result = result + [
                q2 for q1 in prev_result
                   for q2 in self.targets(q1, EPSILON) 
                   if not q2 in prev_result
            ]
            closure = (prev_result == result)
        return result

    def remove_epsilons(self):
        # Corresponds to definition (7) in handout
        new_deltas = [
            (q1, x, q3)
            for q1 in self.all_states()
            for x in self.all_labels()
            for q2 in self.epsilon_closure(q1)
            for q3 in self.targets(q2, x)
            if x is not EPSILON
        ]
        new_ends = [
            q
            for q in self.all_states()
            for q1 in self.epsilon_closure(q)
            if q1 in self.ends
        ]
        return Automaton(self.start, remove_duplicates(new_ends), new_deltas)

    def union_fsas(self, other):
        # Add your code for question 4 below
        unused_other = ensure_unused(self.all_states(), other)
        exc_start = 0
        for num in range(0, 100):
            if num not in (self.all_states() + unused_other.all_states()):
                exc_start = num
                break

        return EpsAutomaton(
            start = exc_start,
            ends = self.ends + unused_other.ends,
            deltas = [(exc_start, EPSILON, self.start),
                      (exc_start, EPSILON, unused_other.start)
                      ] + self.deltas + unused_other.deltas
        )


    def concat_fsas(self, other):
        # Add your code for question 4 below
        unused_other = ensure_unused(self.all_states(), other)
        new_transitions = []
        for end_state in self.ends:
            new_transitions.append((end_state, EPSILON, unused_other.start))

        return EpsAutomaton(
            start = self.start,
            ends = unused_other.ends,
            deltas = self.deltas + unused_other.deltas + new_transitions
        )


    def star_fsa(self):
        # Add your code for question 4 below
        new_start = 0
        for num in range(0, 100):
            if num not in self.all_states():
                new_start = num
                break

        new_transitions = []
        for end_state in self.ends:
            new_transitions.append((end_state, EPSILON, self.start))

        return EpsAutomaton(
            start = new_start,
            ends = [new_start] + self.ends,
            deltas = [(new_start, EPSILON, self.start)] + self.deltas + new_transitions
        )

# Test FSAs
odd_Cs = Automaton(
    start = False,
    ends = [True],
    deltas = [(False, 'C', True), 
              (False, 'V', False), 
              (True, 'C', False),
              (True, 'V', True)]
)
even_Vs = Automaton(
    start = False,
    ends = [False],
    deltas = [(False, 'C', False), 
              (False, 'V', True), 
              (True, 'C', True),
              (True, 'V', False)]
)

efsa_handout4 = EpsAutomaton(
    start = 10,
    ends = [20, 30],
    deltas = [(10, 'a', 10),
              (10, EPSILON, 20),
              (10, EPSILON, 30),
              (20, 'b', 21),
              (21, 'b', 20),
              (30, 'b', 31),
              (31, 'b', 32),
              (32, 'b', 30)]
)

efsa_handout5 = EpsAutomaton(
    start = 0,
    ends= [2],
    deltas = [(0, 'a', 0),
              (0, EPSILON, 1),
              (1, 'b', 1),
              (1, EPSILON, 2),
              (2, 'c', 2)]
)

efsa_xyz = EpsAutomaton(
    start = 0,
    ends = [1],
    deltas = [(0, 'x', 0),
              (0, 'y', 1),
              (0, EPSILON, 1),
              (1, 'z', 1)]
)

#################
# REGEX CLASSES #
#################

class RegEx():
    def __init__(self, char):
        raise Exception("Cannot instantiate abstract base class")

    def __str__(self):
        raise Exception("__str__ is not defined")

    def __repr__(self):
        return self.__str__()

    def to_fsa(self):
        raise Exception("to_fsa is not defined")

class Lit(RegEx):
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return self.char

    def to_fsa(self):
        # Add your code for question 4 below
        return EpsAutomaton(
            start = 0,
            ends = [1],
            deltas = [(0, self.char, 1)]
        )

class Alt(RegEx):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2

    def __str__(self):
        return "({}|{})".format(self.r1, self.r2)

    def to_fsa(self):
        # Add your code for question 4 below
        return (self.r1.to_fsa()).union_fsas(self.r2.to_fsa())

class Concat(RegEx):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2

    def __str__(self):
        return "({}.{})".format(self.r1, self.r2)

    def to_fsa(self):
        # Add your code for question 4 below
        return (self.r1.to_fsa()).concat_fsas(self.r2.to_fsa())

class Star(RegEx):
    def __init__(self, r):
        self.r = r

    def __str__(self):
        return "{}*".format(self.r)

    def to_fsa(self):
        # Add your code for question 4 below
        return self.r.to_fsa().star_fsa()

class Zero(RegEx):
    def __init__(self):
        pass

    def __str__(self):
        return "0"

    def to_fsa(self):
        # Add your code for question 4 below
        return EpsAutomaton(
            start = 0,
            ends = [],
            deltas = []
        )

class One(RegEx):
    def __init__(self):
        pass

    def __str__(self):
        return "1"

    def to_fsa(self):
        # Add your code for question 4 below
        return EpsAutomaton(
            start = 0,
            ends = [0],
            deltas = []
        )

# Test RegExes
re1 = Concat(Alt(Lit('a'), Lit('b')), Lit('c'))
re2 = Star(re1)
re3 = Star(Concat(Zero(), Lit(3)))
re4 = Concat(Alt(Lit(0), Lit(1)), Star(Lit(2)))
re5 = Star(Lit('a'))
re6 = Lit('a')
re7 = Alt(Lit('a'), Lit('b'))
re8 = Concat(Lit('a'), Lit('b'))
re9 = Star(Lit('a'))
re10 = Star(Concat(Lit('a'), Lit('b')))

# Add your code for questions 1-3 below
fsa_1 = Automaton(
    start = 54,
    ends = [38],
    deltas = [(54, False, 54),
              (54, True, 73),
              (73, False, 73),
              (73, True, 21),
              (21, False, 21),
              (21, True, 54),
              (21, True, 38),
              (38, False, 38)]
)
fsa_2 = Automaton(
    start = 1,
    ends = [4],
    deltas = [(1, 'C', 1),
              (1, 'V', 1),
              (1, 'C', 2),
              (2, 'C', 3),
              (2, 'V', 3),
              (3, 'C', 4),
              (3, 'V', 4)]
)
fsa_3 = Automaton(
    start = 1,
    ends = [1, 2],
    deltas = [(1, 'P', 1),
              (1, 'K', 1),
              (1, 'I', 1),
              (1, 'P', 2),
              (2, 'P', 2),
              (2, 'K', 2),
              (2, 'I', 2),
              (2, 'U', 2)]
)

# testing

print(re2.to_fsa().recognize("acacbcac"))
print(re2.to_fsa().recognize("acacbca"))
print(re3.to_fsa().recognize([]))
print(re3.to_fsa().recognize([3]))
print(re4.to_fsa().recognize([0,2,2,2]))
print(re4.to_fsa().recognize([1,2,2]))
print(re4.to_fsa().recognize([0,1,2,2,2,2,2]))
print(Star(re4).to_fsa().recognize([0,1,2,2,2,2,2]))
print(efsa_handout4.concat_fsas(efsa_handout5).ends)
print(efsa_handout4.concat_fsas(efsa_handout5).start)
print(efsa_handout4.concat_fsas(efsa_handout5).deltas)
# print(efsa_handout4.concat_fsas(efsa_handout5).recognize('abbbc'))
# print(efsa_handout4.union_fsas(efsa_handout5).deltas)
print(Zero().to_fsa().recognize(''))
print(One().to_fsa().recognize(''))
print(re10.to_fsa().recognize('abab'))
print(re9.to_fsa().recognize('aaa'))
print(re8.to_fsa().recognize('ab'))
print(re7.to_fsa().recognize('b'))
print(re6.to_fsa().recognize('a'))
print(re5.to_fsa().recognize('aa'))
print("fsa_3")
print(fsa_3.recognize("KPIUPK"))
print(fsa_3.recognize("PU"))
print(fsa_3.recognize("UP"))
print(fsa_3.recognize("PKKKKKKU"))
print(fsa_3.recognize("KKKKKKKK"))
print("fsa_2")
print(fsa_2.recognize("CCCVC"))
print(fsa_2.recognize("CCVVC"))
print(fsa_2.recognize('CCCV'))
print(fsa_2.recognize('VC'))
print("fsa_1")
print(fsa_1.recognize([True, False, True, True, False]))
print(fsa_1.recognize([True, True, True, False, True, True]))
print(fsa_1.hat(54, [True, False, True, True]))
print(fsa_1.hat(73, [True, False, True, True]))
