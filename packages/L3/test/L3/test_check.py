import pytest
from L3.check import Context, check_program, check_term
from L3.syntax import Immediate, Let, LetRec, Program, Reference


def test_check_reference_bound():
    term = Reference(name="x")

    context: Context = {
        "x": None,
    }

    check_term(term, context)


def test_check_reference_free():
    term = Reference(name="x")

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


def test_check_intermediate():
    term = Immediate(value=0)

    context: Context = {}

    check_term(term, context)


def test_check_term_let():
    term = Let(
        bindings=[
            ("x", Immediate(value=0)),
        ],
        body=Reference(name="x"),
    )

    context: Context = {}

    check_term(term, context)


def test_check_term_let_duplicate():
    term = Let(
        bindings=[
            ("x", Immediate(value=0)),
            ("x", Immediate(value=1)),
        ],
        body=Reference(name="x"),
    )

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


def test_check_term_not_avaliable_in_initializer():
    term = Let(
        bindings=[
            ("x", Immediate(value=0)),
            ("y", Reference(name="x")),
        ],
        body=Reference(name="x"),
    )

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


def test_check_term_letrec_avalible_in_initializers():
    term = LetRec(
        bindings=[
            ("x", Immediate(value=0)),
            ("y", Reference(name="x")),
        ],
        body=Reference(name="x"),
    )

    context: Context = {}

    with pytest.raises(ValueError):
        check_term(term, context)


def test_check_program_duplicate():
    program = Program(
        parameters=["x", "x"],
        body=Immediate(value=0),
    )

    with pytest.raises(ValueError):
        check_program(program)


def test_check_program():
    program = Program(
        parameters=["x"],
        body=Reference(name="x"),
    )

    check_program(program)
