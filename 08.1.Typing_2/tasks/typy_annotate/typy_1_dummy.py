def f(a: float) -> float:
    return a / 2


TEST_SAMPLES = """
# ERROR
f("dd")

# ERROR
f(1j)

# SUCCESS
f(1)

# SUCCESS
f(1.0)

# SUCCESS
class R(float):
    pass

f(R(1))
"""
