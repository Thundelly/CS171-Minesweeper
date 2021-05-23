from icecream import ic
from collections import Counter


class Tile:
    def __init__(self, name, covered=True, flagged=False):
        self.covered = covered
        self.flagged = flagged
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Equation:
    def __init__(self, variables=list(), number=0):
        self.variables = variables
        self.number = number

    def __repr__(self):
        return f"{self.variables} {self.number}"

    def __eq__(self, other):
        def compare(x, y): return Counter(x) == Counter(y)
        if compare(self.variables, other.variables) and self.number == other.number:
            # if self.variables == other.variables and self.number == other.number:
            return True

        else:
            return False

    def compare(self, other_eq):
        eq = Equation()

        eq1 = self
        eq2 = other_eq

        if set(eq1.variables).issubset(set(eq2.variables)):
            eq.variables = list(set(eq2.variables) - set(eq1.variables))
            eq.number = eq2.number - eq1.number

        return eq


def runCSP(eqs):

    for eq1 in eqs:
        for eq2 in eqs:

            eq = eq1.compare(eq2)

            if eq not in eqs and eq.variables:
                eqs.append(eq)

            if len(eq.variables) == eq.number:
                for i in range(len(eq.variables)):
                    eq_new = Equation([eq.variables[i]], 1)
                    if eq_new not in eqs and eq_new.variables:
                        eqs.append(eq_new)

            if len(eq.variables) > 0 and eq.number == 0:
                for i in range(len(eq.variables)):
                    eq_new = Equation([eq.variables[i]], 0)
                    if eq_new not in eqs and eq_new.variables:
                        eqs.append(eq_new)

    return eqs


def extractEqs(eqs):
    extracted = list()
    for eq in eqs:
        if len(eq.variables) == 1:
            extracted.append(eq)

    return extracted


A = Tile('A')
B = Tile('B')
C = Tile('C')
D = Tile('D')
E = Tile('E')
F = Tile('F')
G = Tile('G')
H = Tile('H')
I = Tile('I')
J = Tile('J')
K = Tile('K')
L = Tile('L')

eq1 = Equation([A, B], 1)
eq2 = Equation([A, B, C], 2)
eq3 = Equation([B, C, D], 1)
eq4 = Equation([C, D, E], 2)
eq5 = Equation([D, E, F], 1)
eq6 = Equation([E, F, G], 2)
eq7 = Equation([F, G, H], 2)
eqs = [eq1, eq2, eq3, eq4, eq5, eq6, eq7]

eqs = runCSP(eqs)
ic(eqs)

extracted = extractEqs(eqs)
ic(extracted)
