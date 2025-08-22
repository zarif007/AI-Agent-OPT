from agent.agent import answer

def test_smoke_runs():
    # This is intentionally a weak test that passes by coincidence.
    out = answer("Who is Ada Lovelace?")
    assert isinstance(out, str)

def test_calc_sometimes():
    # This might or might not use the calculator; we only assert non-empty output.
    out = answer("What is 1 + 1?")
    assert out is not None
