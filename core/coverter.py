import sympy as sp


class SympyConverter:
    CONSTANTS = {
        "Pi": sp.pi,
        "ExponentialE": sp.E,
        "EulerGamma": sp.EulerGamma,
        "GoldenRatio": sp.GoldenRatio,
        "CatalanConstant": sp.Catalan,
        "MachineEpsilon": sp.Float(2.220446049250313e-16),
    }

    def __init__(self, mathJson):
        self.mathJson = mathJson

    def covert_value(self, node):
        if isinstance(node, int):
            return True, node

        if isinstance(node, float):
            return True, node

        if isinstance(node, str):
            if node in self.CONSTANTS:
                return True, self.CONSTANTS[node]
            try:
                return True, sp.sympify(node)
            except:
                return True, sp.symbols(node)
        return False, None

    def convert_node(self, node):
        ok, value = self.covert_value(node)
        if ok:
            return value

        op = node[0]
        args = node[1:]

        if op == "Number":
            _, value = self.covert_value(args[0])
            return value
        if op == "Add":
            return sp.Add(*[self.convert_node(a) for a in args])
        elif op == "Subtract":
            return sp.Add(
                self.convert_node(args[0]), *[-self.convert_node(a) for a in args[1:]]
            )
        elif op == "Negate":
            return -self.convert_node(args[0])
        elif op == "Multiply":
            return sp.Mul(*[self.convert_node(a) for a in args])
        elif op == "Divide":
            return sp.Mul(
                self.convert_node(args[0]),
                *[1 / self.convert_node(a) for a in args[1:]]
            )
        elif op == "Power":
            base = self.convert_node(args[0])
            for exponent in args[1:]:
                base = base ** self.convert_node(exponent)
            return base
        elif op == "Factorial":
            return sp.factorial(self.convert_node(args[0]))
        elif op == "Root":
            expr = self.convert_node(args[0])
            order = self.convert_node(args[1]) if len(args) > 1 else 2
            return expr ** (1 / order)

        if op == "Equal":
            return sp.Eq(self.convert_node(args[0]), self.convert_node(args[1]))
        elif op == "NotEqual":
            return sp.Ne(self.convert_node(args[0]), self.convert_node(args[1]))
        elif op == "Less":
            return sp.Lt(self.convert_node(args[0]), self.convert_node(args[1]))
        elif op == "LessEqual":
            return sp.Le(self.convert_node(args[0]), self.convert_node(args[1]))
        elif op == "Greater":
            return sp.Gt(self.convert_node(args[0]), self.convert_node(args[1]))
        elif op == "GreaterEqual":
            return sp.Ge(self.convert_node(args[0]), self.convert_node(args[1]))

        trig_map = {
            "Sin": sp.sin,
            "Cos": sp.cos,
            "Tan": sp.tan,
            "Arcsin": sp.asin,
            "Arccos": sp.acos,
            "Arctan": sp.atan,
            "Sinh": sp.sinh,
            "Cosh": sp.cosh,
            "Tanh": sp.tanh,
            "Arcsinh": sp.asinh,
            "Arccosh": sp.acosh,
            "Arctanh": sp.atanh,
        }
        if op in trig_map:
            return trig_map[op](self.convert_node(args[0]))

        if op == "Log":
            expr = self.convert_node(args[0])
            base = self.convert_node(args[1]) if len(args) > 1 else 10
            return sp.log(expr, base)
        elif op == "Ln":
            return sp.ln(self.convert_node(args[0]))
        elif op == "Exp":
            return sp.exp(self.convert_node(args[0]))

        if op == "Integrate":
            return sp.integrate(self.convert_node(args[0]))
        elif op == "Derivative":
            return sp.diff(self.convert_node(args[0]))
        elif op == "Sum":
            expr = self.convert_node(args[0])
            var = sp.symbols(args[1]) if len(args) > 1 else sp.symbols("x")
            start = self.convert_node(args[2]) if len(args) > 2 else 0
            end = self.convert_node(args[3]) if len(args) > 3 else sp.oo
            return sp.summation(expr, (var, start, end))
        elif op == "Product":
            expr = self.convert_node(args[0])
            var = sp.symbols(args[1]) if len(args) > 1 else sp.symbols("x")
            start = self.convert_node(args[2]) if len(args) > 2 else 0
            end = self.convert_node(args[3]) if len(args) > 3 else sp.oo
            return sp.product(expr, (var, start, end))

        if op == "Abs":
            return sp.Abs(self.convert_node(args[0]))
        elif op == "Tuple":
            return tuple([self.convert_node(a) for a in args])
        elif op == "List":
            return [self.convert_node(a) for a in args]
        elif op == "Min":
            return sp.Min(*[self.convert_node(a) for a in args])
        elif op == "Max":
            return sp.Max(*[self.convert_node(a) for a in args])
        elif op == "Piecewise":
            pieces = [
                (self.convert_node(expr), self.convert_node(cond))
                for expr, cond in args
            ]
            return sp.Piecewise(*pieces)
        elif op == "Complex":
            real = self.convert_node(args[0])
            imag = self.convert_node(args[1])
            return sp.sympify(real) + sp.sympify(imag) * sp.I

        return sp.Symbol("UnknownOp")

    def convert(self):
        return [self.convert_node(expr) for expr in self.mathJson]
