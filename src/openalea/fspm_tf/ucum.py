"""
Units as UCUM codes (https://ucum.org), the subset fspm-TF accepts: SI and common atoms, metric prefixes on the
metric ones, products ('.'), quotients ('/'), integer exponents, parentheses, annotations ({...}, dimensionless) and
'1'. dimension(code) gives a unit's dimension, to check that two units are convertible.

    dimension("mm3/(s.MPa)") == dimension("m4.s.kg-1")      True: the same physical dimension
"""
import re

# Dimensions: length, mass, time, temperature, amount, luminous intensity, current
BASE = ("L", "M", "T", "Θ", "N", "J", "I")


def _dims(**exponents) -> tuple:
    return tuple(exponents.get(name, 0) for name in ("L", "M", "T", "Th", "N", "J", "I"))


NONE = _dims()
METRIC_ATOMS = {
    "m": _dims(L=1), "g": _dims(M=1), "s": _dims(T=1), "K": _dims(Th=1), "mol": _dims(N=1), "cd": _dims(J=1),
    "A": _dims(I=1), "rad": NONE, "sr": NONE, "Hz": _dims(T=-1), "N": _dims(M=1, L=1, T=-2),
    "Pa": _dims(M=1, L=-1, T=-2), "J": _dims(M=1, L=2, T=-2), "W": _dims(M=1, L=2, T=-3), "C": _dims(I=1, T=1),
    "V": _dims(M=1, L=2, T=-3, I=-1), "Ohm": _dims(M=1, L=2, T=-3, I=-2), "S": _dims(M=-1, L=-2, T=3, I=2),
    "F": _dims(M=-1, L=-2, T=4, I=2), "T": _dims(M=1, T=-2, I=-1), "Wb": _dims(M=1, L=2, T=-2, I=-1),
    "lm": _dims(J=1), "lx": _dims(J=1, L=-2), "Bq": _dims(T=-1), "Gy": _dims(L=2, T=-2), "Sv": _dims(L=2, T=-2),
    "L": _dims(L=3), "l": _dims(L=3), "bar": _dims(M=1, L=-1, T=-2), "ar": _dims(L=2), "t": _dims(M=1),
    "eq": _dims(N=1), "Cel": _dims(Th=1),
}
ATOMS = dict(METRIC_ATOMS, **{
    "min": _dims(T=1), "h": _dims(T=1), "d": _dims(T=1), "wk": _dims(T=1), "mo": _dims(T=1), "a": _dims(T=1),
    "deg": NONE, "%": NONE, "[ppm]": NONE, "[ppb]": NONE,
})
SPECIAL = {"Cel"}                                   # an offset scale: not allowed in products, quotients, powers
PREFIXES = ("da", "Y", "Z", "E", "P", "T", "G", "M", "k", "h", "d", "c", "m", "u", "n", "p", "f", "a", "z", "y")

_TOKEN = re.compile(r"\{[^{}]*\}|\(|\)|\.|/|[+-]?\d+|\[[^\]]+\]|%|[A-Za-z]+")


class UnitError(ValueError):
    pass


def _atom(text: str) -> tuple:
    """(dimension, special) of a unit symbol, with its prefix."""
    if text in ATOMS:
        return ATOMS[text], text in SPECIAL
    for prefix in PREFIXES:
        if text.startswith(prefix) and text[len(prefix):] in METRIC_ATOMS:
            return METRIC_ATOMS[text[len(prefix):]], text[len(prefix):] in SPECIAL
    raise UnitError(f"unknown unit symbol '{text}'")


def dimension(code: str) -> tuple:
    """The dimension of the UCUM *code* (exponents of L, M, T, Θ, N, J, I); raises UnitError if not a unit fspm-TF
    accepts."""
    if not isinstance(code, str) or not code or code != code.strip() or " " in code:
        raise UnitError(f"'{code}' is not a UCUM code (no spaces: write 'mol/(m2.s)' or 'mol.m-2.s-1')")
    tokens = _TOKEN.findall(code)
    if "".join(tokens) != code:
        raise UnitError(f"'{code}' is not a UCUM code")
    position = 0

    def term():
        nonlocal position
        total, special_seen, count = [0] * 7, False, 0
        sign = 1
        if position < len(tokens) and tokens[position] == "/":
            sign, position = -1, position + 1
        while True:
            dims, special = component()
            count += 1
            special_seen = special_seen or special
            total = [a + sign * b for a, b in zip(total, dims)]
            if position < len(tokens) and tokens[position] in (".", "/"):
                sign = 1 if tokens[position] == "." else -1
                position += 1
                continue
            break
        if special_seen and count > 1:
            raise UnitError(f"'{code}': Cel (a temperature scale) cannot be combined with other units; use K")
        return tuple(total), special_seen

    def component():
        nonlocal position
        if position >= len(tokens):
            raise UnitError(f"'{code}' ends too early")
        token = tokens[position]
        position += 1
        if token == "(":
            dims, special = term()
            if position >= len(tokens) or tokens[position] != ")":
                raise UnitError(f"'{code}': unbalanced parenthesis")
            position += 1
        elif token.startswith("{"):
            return NONE, False
        elif re.fullmatch(r"[+-]?\d+", token):
            if int(token) != 1 and not token.lstrip("+-").startswith("10"):
                raise UnitError(f"'{code}': numbers other than 1 are not units")
            return NONE, False
        elif token in (".", "/", ")"):
            raise UnitError(f"'{code}': unexpected '{token}'")
        else:
            dims, special = _atom(token)
        if position < len(tokens) and re.fullmatch(r"[+-]?\d+", tokens[position]):
            exponent = int(tokens[position])
            position += 1
            if special:
                raise UnitError(f"'{code}': Cel cannot have an exponent")
            dims = tuple(exponent * value for value in dims)
        if position < len(tokens) and tokens[position].startswith("{"):
            position += 1
        return dims, special

    dims, _ = term()
    if position != len(tokens):
        raise UnitError(f"'{code}': unexpected '{tokens[position]}'")
    return dims


def is_valid(code: str) -> bool:
    try:
        dimension(code)
        return True
    except UnitError:
        return False


def convertible(code: str, other: str) -> bool:
    """Whether the two UCUM codes have the same dimension (a value in one can be converted to the other)."""
    return dimension(code) == dimension(other)
