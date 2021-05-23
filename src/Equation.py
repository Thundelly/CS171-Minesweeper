from collections import Counter

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