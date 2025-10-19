from sympy import latex, diff, symbols
from sympy.parsing.latex import parse_latex
from sympy.simplify.simplify import simplify as sym_simplify
from schema import DiffResult, SimplifyResult
from sympy.core import Expr


def derivative(expr: str, var: str = "x", level: int = 1) -> DiffResult:
    try:
        var_symbol = symbols(var)
        sympy_expression = parse_latex(expr)
        if not isinstance(sympy_expression, Expr):
            raise ValueError("Invalid mathematical expression")
        simplified = diff(sympy_expression, var_symbol, level)

        latex_output = latex(simplified, mode="plain")

        return DiffResult(input=expr, level=level, var=var, output=latex_output)

    except Exception as e:
        return DiffResult(input=expr, level=level, var=var, output=expr, error=str(e))


def simplify(expr: str) -> SimplifyResult:
    try:
        sympy_expression = parse_latex(expr)
        if not isinstance(sympy_expression, Expr):
            raise ValueError("Invalid mathematical expression")
        simplified = sym_simplify(sympy_expression)

        latex_output = latex(simplified, mode="plain")

        return SimplifyResult(input=expr, output=latex_output)

    except Exception as e:
        return SimplifyResult(input=expr, output=expr, error=str(e))
