# LING 185A Homework 4
# Instructor: Connor Mayer

from CFG import *


class Tree():
    def root(self):
        return self.nt


class Leaf(Tree):
    def __init__(self, nt, t):
        self.nt = nt
        self.t = t

    def __str__(self):
        return "Leaf {} {}".format(str(self.nt), str(self.t))

    def __repr__(self):
        return self.__str__()

    ##############
    # Question 1 #
    ##############
    ''' WORKS '''

    def to_rule_list(self):
        return Rule(NT(self.nt), [T(self.t)])

    ##############
    # Question 3 #
    ##############
    def to_derivation(self):
        return [[NT(self.nt)], [T(self.t)]]


class NonLeaf(Tree):
    def __init__(self, nt, left, right):
        self.nt = nt
        self.left = left
        self.right = right

    def __str__(self):
        return "NonLeaf {} ({}) ({})".format(
            str(self.nt), self.left.__str__(), self.right.__str__()
        )

    def __repr__(self):
        return self.__str__()

    ##############
    # Question 1 #
    ##############
    ''' WORKS '''

    def to_rule_list(self):
        rule = [Rule(NT(self.nt), [NT(self.left.nt), NT(self.right.nt)])]
        left_child = self.left.to_rule_list()
        right_child = self.right.to_rule_list()
        if isinstance(left_child, list):
            for el in left_child:
                rule.append(el)
        else:
            rule.append(left_child)
        if isinstance(right_child, list):
            for el in right_child:
                rule.append(el)
        else:
            rule.append(right_child)

        return rule

    ##############
    # Question 3 #
    ##############
    ''' WORKS '''

    def to_derivation(self):
        left_tree = self.left.to_derivation()
        right_tree = self.right.to_derivation()
        l_add_list = []
        for els in left_tree:
            l_add_list.append(els + [NT(self.right.nt)])
        r_add_list = []
        for els in right_tree[1:]:
            r_add_list.append(left_tree[-1] + els)
        return [[NT(self.nt)]] + l_add_list + r_add_list

  # additional things I tried
        return [[NT(self.nt)] + [NT(self.left.nt)] + [NT(self.right.nt)] +
                [get_terminals(self.left)] + [NT(self.right.nt)] + left_tree + right_tree]
    # return [[NT(self.nt)] + [left_tree + [NT(self.right.nt)]] + [get_terminals(self.left) + right_tree]]
    # if isinstance(self.right, NT):
    #     return [[NT(self.nt)]] + [left_tree + [NT(self.right.nt)]]
    # else:
    #     return [[NT(self.nt)]] + [get_terminals(self.left) + right_tree]


##############
# Question 2 #
##############
# helper function for getting just terminals
def get_terminals(tree):
    if isinstance(tree, Leaf):
        return [T(tree.t)]
    else:
        return get_terminals(tree.left) + get_terminals(tree.right)


''' WORKS (except for test case 2) '''


def rule_list_to_tree(rules):
    if len(rules) < 3 or rules[0].is_terminal():
        if isinstance(rules[0].rhs[0], NT):
            return None
        else:
            return Leaf(rules[0].lhs, rules[0].rhs)
    else:
        f_rule = rule_list_to_tree(rules[1:])
        s_rule = rule_list_to_tree(rules[2:])
        if not f_rule or not s_rule:
            return None
        else:
            return NonLeaf(rules[0].lhs, f_rule, s_rule)


##############
# Question 4 #
##############
''' WORKS '''


def split_at_leftmost(sequence):
    if len(sequence) == 0:
        return None
    if isinstance(sequence[0], NT):
        return [[], sequence[0], sequence[1:]]
    else:
        rec_split = split_at_leftmost(sequence[1:])
        if not rec_split:
            return None
        else:
            return [[sequence[0]] + rec_split[0], rec_split[1], rec_split[2]]


# Some helper functions
def concat(my_list):
    # Takes a list of lists concatenates them into a single list.
    return sum(my_list, [])


def labels_only(my_list):
    # Takes a list of symbols and returns just their associated labels.
    return [item.sym for item in my_list]


class CFG():
    def __init__(self, start, rules):
        self.start = start
        self.rules = rules

    ##############
    # Question 5 #
    ##############
    ''' WORKS '''

    def rewrite_leftmost(self, sequence):
        left_split = split_at_leftmost(sequence)
        if not left_split:
            return None
        else:
            if not self.rules:
                return []
            else:
                f_rule = self.rules[0]
                import copy
                cfg = copy.deepcopy(self)
                cfg.rules = self.rules[1:]
                rec_split = cfg.rewrite_leftmost(sequence)
                if not f_rule.is_terminal():
                    if f_rule.lhs == left_split[1]:
                        return [left_split[0] + [f_rule.rhs[0]] + [f_rule.rhs[1]] + left_split[2]] + rec_split
                    else:
                        return rec_split
                else:
                    if f_rule.lhs == left_split[1]:
                        return [left_split[0] + f_rule.rhs + left_split[2]] + rec_split
                    else:
                        return rec_split

    ##############
    # Question 6 #
    ##############
    ''' Does not work, is close, passes first three test cases '''

    def derivable_from(self, sequence, max_steps):
        if max_steps == 0:
            if isinstance(sequence[0], NT):
                return []
        else:
            rec_rewrite = self.rewrite_leftmost(sequence)
            if not rec_rewrite or len(rec_rewrite) == 0:
                return None
            without_NT = []
            with_NT = []
            for lists in rec_rewrite:
                for els in lists:
                    if els.is_terminal():
                        without_NT.append([els])
                    else:
                        with_NT.append(lists)
                        break
            # this is necessary, but it doesn't work beyond 1st recursion level
            # with_NT = concat(with_NT)

            der_list = []
            seen = []
            # for els in with_NT:
            #   if not els.is_terminal:
            exp = self.derivable_from(with_NT, max_steps - 1)
            if exp:
                der_list.append(exp)

            labels = []
            for item in without_NT:
                labels.append(labels_only(item))

            if len(der_list) > 0:
                return der_list + labels
            else:
                return labels

    def derivable(self, max_steps):
        return self.derivable_from([self.start], max_steps)


# Example CFGs
cfg1 = CFG(
    start=NT("S"),
    rules=[
        Rule(NT("S"), [NT("NP"), NT("VP")]),
        Rule(NT("NP"), [NT("D"), NT("N")]),
        Rule(NT("VP"), [NT("V"), NT("NP")]),
        Rule(NT("NP"), [T("John")]),
        Rule(NT("NP"), [T("Mary")]),
        Rule(NT("D"), [T("the")]),
        Rule(NT("D"), [T("a")]),
        Rule(NT("N"), [T("cat")]),
        Rule(NT("N"), [T("dog")]),
        Rule(NT("V"), [T("saw")]),
        Rule(NT("V"), [T("likes")])
    ]
)

cfg_anbn = CFG(
    start=NT(0),
    rules=[
        Rule(NT(0), [NT(10), NT(1)]),
        Rule(NT(1), [NT(0), NT(11)]),
        Rule(NT(0), [NT(10), NT(11)]),
        Rule(NT(10), [T('a')]),
        Rule(NT(11), [T('b')])
    ]
)

cfg_ambiguity = CFG(
    start=NT("NP"),
    rules=[
        Rule(NT("NP"), [NT("NP"), NT("X")]),
        Rule(NT("X"), [NT("CNJ"), NT("NP")]),
        Rule(NT("NP"), [T("apples")]),
        Rule(NT("NP"), [T("oranges")]),
        Rule(NT("NP"), [T("bananas")]),
        Rule(NT("CNJ"), [T("and")]),
        Rule(NT("CNJ"), [T("or")])
    ]
)

# testing
# print(Leaf("VP", "ran").to_rule_list())
# print(NonLeaf("S",
# Leaf("NP", "Mary"),
# Leaf("VP", "ran")).to_rule_list())
# [NT(S) => [NT(NP), NT(VP)], NT(NP) => [T(Mary)], NT(VP) => [T(ran)]]
# print( NonLeaf(1,
# NonLeaf(2, Leaf(4, "a"), Leaf(5, "b")),
# Leaf(3, "c")).to_rule_list())
# [NT(1) => [NT(2), NT(3)], NT(2) => [NT(4), NT(5)], NT(4) => [T(a)],
# NT(5) => [T(b)], NT(3) => [T(c)]]
# print(NonLeaf(1,
# Leaf(2, "a"),
# NonLeaf(3, Leaf(4, "b"), Leaf(5, "c"))).to_rule_list()
# )
# [NT(1) => [NT(2), NT(3)], NT(2) => [T(a)], NT(3) => [NT(4), NT(5)],
# NT(4) => [T(b)], NT(5) => [T(c)]]
# print("testing for 2")
# print(rule_list_to_tree([Rule(NT("VP"), [T("ran")])]))
# print(rule_list_to_tree(
# [Rule(NT("S"), [NT("NP"), NT("VP")]), Rule(NT("NP"), [T("Mary")]),
# Rule(NT("VP"), [T("ran")])]))
# NonLeaf NT(S) (Leaf NT(NP) [T(Mary)]) (Leaf NT(VP) [T(ran)])
# print(rule_list_to_tree(
# [Rule(NT(1), [NT(2), NT(3)]), Rule(NT(2), [NT(4), NT(5)]),
# Rule(NT(4), [T("a")]), Rule(NT(5), [T("b")]), Rule(NT(3), [T("c")])]))
# NonLeaf NT(1) (NonLeaf NT(2) (Leaf NT(4) [T(a)]) (Leaf NT(5) [T(b)]))
# (Leaf NT(3) [T(c)])
# print(rule_list_to_tree([Rule(NT(1), [NT(2), NT(3)]), Rule(NT(2), [T("a")]),
# Rule(NT(3), [NT(4), NT(5)]), Rule(NT(4), [T("b")]),
# Rule(NT(5), [T("c")])]))
# NonLeaf NT(1) (Leaf NT(2) [T(a)]) (NonLeaf NT(3) (Leaf NT(4) [T(b)])
# (Leaf NT(5) [T(c)]))
# print( rule_list_to_tree([Rule(NT(1), [NT(2), NT(3)]), Rule(NT(2), [T("a")]),
# Rule(NT(3), [NT(4), NT(5)]), Rule(NT(4), [T("b")])]))
# None
# print("testing for 3 - does not work")
print(NonLeaf(1,
              NonLeaf(2, Leaf(4, "a"), Leaf(5, "b")),
              Leaf(3, "c")).to_derivation())
# print(NonLeaf(1,
# Leaf(2, "a"),
# NonLeaf(3, Leaf(4, "b"), Leaf(5, "c"))).to_derivation())
# print("testing for 4")
# print(split_at_leftmost([T("apples"), T("and"), NT("NP"), T("or"), NT("NP")]))
# [[T(apples), T(and)], NT(NP), [T(or), NT(NP)]]
# print(split_at_leftmost([T("apples"), T("and"), T("oranges"), T("or"), NT("NP")]))
# [[T(apples), T(and), T(oranges), T(or)], NT(NP), []]
# print(split_at_leftmost([T("apples"),T("and"), T("oranges"),T("or"),T("bananas")]))
# None
# print("testing for 5")
# print(cfg1.rewrite_leftmost([NT("NP"), NT("VP")]))
# [[NT(D), NT(N), NT(VP)], [T(John), NT(VP)], [T(Mary), NT(VP)]]
# print(cfg1.rewrite_leftmost([T("John"), NT("VP")]))
# [[T(John), NT(V), NT(NP)]]
# print(cfg_anbn.rewrite_leftmost([NT(0)]))
# [[NT(10), NT(1)], [NT(10), NT(11)]]
# print(cfg_anbn.rewrite_leftmost([NT(10), NT(11)]))
# [[T(a), NT(11)]]
# print(cfg_anbn.rewrite_leftmost([T('a'), NT(11)]))
# [[T(a), T(b)]]
# print(cfg_anbn.rewrite_leftmost([T('a'), T('b')]))
# None
# print("testing for 6")
# print(cfg1.derivable_from([NT("NP")], 0))
# print(cfg1.derivable_from([NT("NP")], 1))
# print(cfg1.derivable_from([NT("NP")], 2))
# print(cfg1.derivable_from([NT("NP")], 3))
# [[’the’, ’cat’], [’the’, ’dog’], [’a’, ’cat’], [’a’, ’dog’], [’John’], [’Mary’]]
# print(cfg1.derivable_from([T("Mary"), NT("VP")], 3))
