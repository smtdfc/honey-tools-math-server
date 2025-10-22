from typing import Optional
from sympy import integrate, latex, diff, symbols
from sympy.simplify.simplify import simplify as sym_simplify
from core.coverter import SympyConverter
from sympy.core import Expr
from schema.entites import IntegrateResult, DiffResult, MathJSON, SimplifyResult


def integrate_expr(
    expr: MathJSON,
    var: str = "x",
    a: Optional[MathJSON] = None,
    b: Optional[MathJSON] = None,
) -> IntegrateResult:
    try:
        var_symbol = symbols(var)
        sympy_expression = SympyConverter([expr]).convert()[0]

        if not isinstance(sympy_expression, Expr):
            raise ValueError("Invalid mathematical expression")
        if len(a) != 0 and len(b) != 0:
            a_expr = SympyConverter([a]).convert()[0]
            b_expr = SympyConverter([b]).convert()[0]
            print(a_expr, b_expr)
            output = integrate(sympy_expression, (var_symbol, a_expr, b_expr))
        else:
            output = integrate(sympy_expression, var_symbol)

        latex_output = latex(output, mode="plain")

        return IntegrateResult(
            input=str(sympy_expression), var=var, output=latex_output, a=a, b=b
        )

    except Exception as e:
        return IntegrateResult(
            input=str(expr), var=var, output="", a=a, b=b, error=str(e)
        )


def derivative(expr: MathJSON, var: str = "x", order: int = 1) -> DiffResult:
    try:
        var_symbol = symbols(var)
        converter = SympyConverter([expr])
        sympy_expression = converter.convert()[0]
        print(sympy_expression)
        if not isinstance(sympy_expression, Expr):
            raise ValueError("Invalid mathematical expression")
        output = diff(sympy_expression, var_symbol, order)

        latex_output = latex(output, mode="plain")

        return DiffResult(
            input=str(sympy_expression), order=order, var=var, output=latex_output
        )

    except Exception as e:

        return DiffResult(
            input=str(expr), order=order, var=var, output="", error=str(e)
        )


def simplify(expr: MathJSON) -> SimplifyResult:
    try:
        converter = SympyConverter([expr])
        sympy_expression = converter.convert()[0]
        if not isinstance(sympy_expression, Expr):
            raise ValueError("Invalid mathematical expression")
        simplified = sym_simplify(sympy_expression)

        latex_output = latex(simplified, mode="plain")

        return SimplifyResult(input=str(sympy_expression), output=latex_output)

    except Exception as e:
        return SimplifyResult(input=str(sympy_expression), output="", error=str(e))
