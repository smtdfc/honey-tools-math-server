from sympy import latex
from sympy.parsing.latex import parse_latex
from sympy.simplify.simplify import simplify as sym_simplify
from schema import SimplifyResult
from sympy.core import Expr


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
