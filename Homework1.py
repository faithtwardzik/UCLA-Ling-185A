# Homework 1
# LING 185A Summer C 2020
# Instructor: Connor Mayer

# We'll talk about what this does in lab on 08/07
from copy import deepcopy

###############################
# Formulas: Questions 1 and 3 #
###############################

class Formula():
    # Do not modify this code
    def __str__(self):
        raise Exception("__str__ is not defined")

    def __repr__(self):
        return self.__str__()

    def remove_negs(self):
        raise Exception("remove_negs is not defined")

    def evaluate(self):
        raise Exception("evaluate is not defined")

    def depth(self):
        raise Exception("depth is not defined")

class F(Formula):
    # Do not modify this code
    def remove_negs(self):
        return F()

    def __str__(self):
        return "F"

    # Add your code for Questions 1 and 3 below
    def evaluate(self):
        return False

    def depth(self):
        return S(Z())



class T(Formula):
    # Do not modify this code
    def remove_negs(self):
        return T()

    def __str__(self):
        return "T"

    # Add your code for Questions 1 and 3 below
    def evaluate(self):
        return True

    def depth(self):
        return S(Z())



class Neg(Formula):
    # Do not modify this code
    def __init__(self, sf):
        self.sf = sf

    def remove_negs(self):
        return self.sf.remove_negs()

    def __str__(self):
        return "!{}".format(self.sf)

    # Add your code for Questions 1 and 3 below
    def evaluate(self):
        return not self.sf.evaluate()

    def depth(self):
        return S(self.sf.depth())


class Cnj(Formula):
    # Do not modify this code
    def __init__(self, sf1, sf2):
        self.sf1 = sf1
        self.sf2 = sf2

    def remove_negs(self):
        return Cnj(self.sf1.remove_negs(), self.sf2.remove_negs())

    def __str__(self):
        return "({} ^ {})".format(self.sf1, self.sf2)

    # Add your code for Questions 1 and 3 below
    def evaluate(self):
        return self.sf1.evaluate() and self.sf2.evaluate()

    def depth(self):
        return self.sf1.depth().add(self.sf2.depth())


class Dsj(Formula):
    # Do not modify this code
    def __init__(self, sf1, sf2):
        self.sf1 = sf1
        self.sf2 = sf2

    def remove_negs(self):
        return Dsj(self.sf1.remove_negs(), self.sf2.remove_negs())

    def __str__(self):
        return "({} v {})".format(self.sf1, self.sf2)

    # Add your code for Questions 1 and 3 below
    def evaluate(self):
        return self.sf1.evaluate() or self.sf2.evaluate()

    def depth(self):
        return self.sf1.depth().add(self.sf2.depth())


####################
# Nums: Question 2 #
####################

class Num():
    # Do not modify this code
    def __init__(self):
        raise Exception("Cannot instantiate abstract class")
    def __str__(self):
        raise Exception("__str__ is not defined")

    def __repr__(self):
        return self.__str__()

    def is_zero(self):
        raise Exception("is_zero is not defined")

    def is_one(self):
        raise Exception("is_one is not defined")

    def double(self):
        raise Exception("double is not defined")

    def add(self, other):
        raise Exception("add is not defined")

    def times(self, other):
        raise Exception("times is not defined")

    def equals(self, other):
        raise Exception("equals is not defined")

    def bigger(self, other):
        raise Exception("bigger is not defined")
    
class Z(Num):
    # Do not modify this code
    def __init__(self):
        pass

    def __str__(self):
        return "Z"

    def is_zero(self):
        return True

    def is_one(self):
        return False

    def double(self):
        return Z()

    def add(self, other):
        return deepcopy(other)

    # Add your code for Question 2 below
    def times(self, other):
        return deepcopy(self)

    def equals(self, other):
        return other.is_zero()

    def bigger(self, other):
        return False

class S(Num):
    # Do not modify this code
    def __init__(self, subnum):
        self.subnum = subnum

    def __str__(self):
        return "S {}".format(self.subnum.__str__())

    def is_zero(self):
        return False

    def is_one(self):
        return self.subnum.is_zero()

    def double(self):
        return S(S(self.subnum.double()))

    def add(self, other):
        if other.is_zero():
            return deepcopy(self)
        else:
            return S(deepcopy(self).add(other.subnum))

    # Add your code for Question 2 below
    def times(self, other):
        if other.is_zero():
            return deepcopy(other)
        else:
            return (deepcopy(self).times(other.subnum)).add(deepcopy(self))

    def equals(self, other):
        return self == other

    def bigger(self, other):
        if self.is_zero():
            return False
        elif other.is_zero():
            return True
        else:
            return deepcopy(self.subnum).bigger(other.subnum)


# Some useful objects for testing
zero = Z()
one = S(Z())
two = S(S(Z()))
three = S(S(S(Z())))

#####################
# Filter: Question 4 #
#####################


class RegEx():
    def __init__(self, char):
        raise Exception("Cannot instantiate abstract base class")

    def __str__(self):
        raise Exception("__str__ is not defined")

    def __repr__(self):
        return self.__str__()

class Lit(RegEx):
    def __init__(self, char):
        self.char = char

    # Add your code for Question 4 below
    def __str__(self):
        return self.char


class Alt(RegEx):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2

    # Add your code for Question 4 below
    def __str__(self):
        return "({}|".format(self.r1.__str__()) + "{})".format(self.r2.__str__())


class Concat(RegEx):
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2

    def __str__(self):
        return self.r1

    # Add your code for Question 4 below
    def __str__(self):
        return "({}.".format(self.r1.__str__()) + "{})".format(self.r2.__str__())

class Star(RegEx):
    def __init__(self, r):
        self.r = r

    # Add your code for Question 4 below
    def __str__(self):
        return "{}*".format(self.r.__str__())

class Zero(RegEx):
    def __init__(self):
        pass

    # Add your code for Question 4 below
    def __str__(self):
        return "0"


class One(RegEx):
    def __init__(self):
        pass

    # Add your code for Question 4 below
    def __str__(self):
        return "1"


# for testing only
'''
if __name__ == "__main__":
    tr = T()
    neg = Neg(T())
    neg2 = Neg(F())
    cnj = Cnj(F(), F())
    dsj = Dsj(T(), F())
    print(dsj.evaluate())
    print(T().evaluate())
    print(F().evaluate())
    print(Neg(T()).evaluate())
    print(Cnj(F(), T()).evaluate())
    print(Dsj(Neg(F()), F()).evaluate())
    print(Dsj(Neg(T()), F()).evaluate())
    print(neg2.evaluate())
    print(zero.times(two))
    print(two.times(three))
    print(three.times(zero))
    print(two.times(one))
    print(zero.equals(zero))
    print(zero.equals(two))
    print(two.equals(two))
    print(zero.bigger(two))
    print(two.bigger(two))
    print(three.bigger(two))
    print(zero.bigger(zero))
    print(one.bigger(two))
    print(Cnj(T(), F()).depth())
    print(Neg(Cnj(T(), F())).depth())
    print(Cnj(T(), Dsj(Neg(F()), T())).depth())
    print(One())
    print(Zero())
    print(Star(Zero()))
    print(Lit('a'))
    print(Star(Concat(Zero(), One())))
    print(Concat(Lit('a'), Lit('b')))
    print(Alt(Lit('a'), Lit('b')))
    print(Star(Lit('a')))
    print(Alt(Concat(Lit('c'), Lit('d')), Star(Lit('e'))))
'''

