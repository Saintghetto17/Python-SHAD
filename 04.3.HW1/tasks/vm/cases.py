from dataclasses import dataclass


@dataclass
class Case:
    name: str
    text_code: str


###################################
# BASIC TESTS WITHOUT ANY STRUCTURE
###################################

BASIC_UNSTRUCTURED_CASES = [
    Case(
        name="simple",
        text_code=r"""
def f():
    print(17)
f()
"""),
    Case(
        name="constant",
        text_code=r"""
print(17)
"""),
    Case(
        name="globals",
        text_code=r"""
global xyz
xyz=2106

def abc():
    global xyz
    xyz+=1
    print("Midst:",xyz)


print("Pre:",xyz)
abc()
print("Post:",xyz)
"""),
    Case(
        name="for_loop",
        text_code=r"""
out = ""
for i in range(5):
    out = out + str(i)
print(out)
"""),
    Case(
        name="inplace_operators",
        text_code=r"""
x, y = 2, 3
x **= y
assert x == 8 and y == 3
x *= y
assert x == 24 and y == 3
x //= y
assert x == 8 and y == 3
x %= y
assert x == 2 and y == 3
x += y
assert x == 5 and y == 3
x -= y
assert x == 2 and y == 3
x <<= y
assert x == 16 and y == 3
x >>= y
assert x == 2 and y == 3
x = 0x8F
x &= 0xA5
# assert x == 0x85
x |= 0x10
# assert x == 0x95
x ^= 0x33
assert x == 0xA6
print("Assert test case for inplace operators")
"""),
    Case(
        name="inplace_division",
        text_code=r"""
x, y = 24, 3
x /= y
assert x == 8.0 and y == 3
assert isinstance(x, float)
x /= y
assert x == (8.0/3.0) and y == 3
assert isinstance(x, float)
print("Assert test case for inplace division")
"""),
    Case(
        name="slice_a_b",
        text_code=r"""
print("hello, world"[3:8])
"""),
    Case(
        name="slice_b",
        text_code=r"""
print("hello, world"[:8])
"""),
    Case(
        name="slice_a",
        text_code=r"""
print("hello, world"[3:])
"""),
    Case(
        name="slice",
        text_code=r"""
print("hello, world"[:])
"""),
    Case(
        name="slice_c",
        text_code=r"""
print("hello, world"[::-1])
"""),
    Case(
        name="slice_a_b_c",
        text_code=r"""
print("hello, world"[3:8:2])
"""),
    Case(
        name="slice_assignment_a_b",
        text_code=r"""
l = list(range(10))
l[3:8] = ["x"]
print(l)
"""),
    Case(
        name="slice_assignment_b",
        text_code=r"""
l = list(range(10))
l[:8] = ["x"]
print(l)
"""),
    Case(
        name="slice_assignment_a",
        text_code=r"""
l = list(range(10))
l[3:] = ["x"]
print(l)
"""),
    Case(
        name="slice_assignment",
        text_code=r"""
l = list(range(10))
l[:] = ["x"]
print(l)
"""),
    Case(
        name="slice_deletion_a_b",
        text_code=r"""
l = list(range(10))
del l[3:8]
print(l)
"""),
    Case(
        name="slice_deletion_b",
        text_code=r"""
l = list(range(10))
del l[:8]
print(l)
"""),
    Case(
        name="slice_deletion_a",
        text_code=r"""
l = list(range(10))
del l[3:]
print(l)
"""),
    Case(
        name="slice_deletion",
        text_code=r"""
l = list(range(10))
del l[:]
print(l)
"""),
    Case(
        name="slice_deletion_c",
        text_code=r"""
l = list(range(10))
del l[::2]
print(l)
"""),
    Case(
        name="slice_deletion_a_b_c",
        text_code=r"""
l = list(range(10))
del l[1:8:2]
print(l)
"""),
    Case(
        name="building_tuple",
        text_code=r"""
print((1+1, 2+2, 3+3))
"""),
    Case(
        name="building_list",
        text_code=r"""
print([1+1, 2+2, 3+3])
"""),
    Case(
        name="building_dict",
        text_code=r"""
print({1:1+1, 2:2+2, 3:3+3})
"""),
    Case(
        name="building_set",
        text_code=r"""
print({1+1, 2+2, 3+3})
"""),
    Case(
        name="subscripting_extraction",
        text_code=r"""
l = list(range(10))
print("%s %s %s" % (l[0], l[3], l[9]))
"""),
    Case(
        name="subscripting_assigment",
        text_code=r"""
l = list(range(10))
l[5] = 17
print(l)
"""),
    Case(
        name="subscripting_deletion",
        text_code=r"""
l = list(range(10))
del l[5]
print(l)
"""),
    Case(
        name="generator_expression_in_join",
        text_code=r"""
x = "-".join(str(z) for z in range(5))
assert x == "0-1-2-3-4"
print("Assert test case for generator_expression_in_join")
"""),
    Case(
        name="generator_expression_complex",
        text_code=r"""
from textwrap import fill
x = set(['test_str'])
width = 70
indent = 4
blanks = ' ' * indent
res = fill(' '.join(str(elt) for elt in sorted(x)), width,
            initial_indent=blanks, subsequent_indent=blanks)
print(res)
"""),
    Case(
        name="list_comprehension",
        text_code=r"""
x = [z*z for z in range(5)]
assert x == [0, 1, 4, 9, 16]
print("Assert test case for list_comprehension")
"""),
    Case(
        name="dict_comprehension",
        text_code=r"""
x = {z:z*z for z in range(5)}
assert x == {0:0, 1:1, 2:4, 3:9, 4:16}
print("Assert test case for dict_comprehension")
"""),
    Case(
        name="set_comprehension",
        text_code=r"""
x = {z*z for z in range(5)}
assert x == {0, 1, 4, 9, 16}
print("Assert test case for set_comprehension")
"""),
    Case(
        name="strange_sequence_ops",
        text_code=r"""
x = [1,2]
x += [3,4]
x *= 2

assert x == [1, 2, 3, 4, 1, 2, 3, 4]

x = [1, 2, 3]
y = x
x[1:2] *= 2
y[1:2] += [1]

assert x == [1, 2, 1, 2, 3]
assert x is y
print("Assert test case for strange_sequence_ops")
"""),
    Case(
        name="unary_operators",
        text_code=r"""
x = 8
print(-x, ~x, not x)
"""),
    Case(
        name="attributes",
        text_code=r"""
l = lambda: 1   # Just to have an object...
l.foo = 17
print(hasattr(l, "foo"), l.foo)
del l.foo
print(hasattr(l, "foo"))
"""),
    Case(
        name="attribute_inplace_ops",
        text_code=r"""
l = lambda: 1   # Just to have an object...
l.foo = 17
l.foo -= 3
print(l.foo)
"""),
    Case(
        name="deleting_names",
        text_code=r"""
g = 17
assert g == 17
del g
g
"""),
    Case(
        name="deleting_local_names",
        text_code=r"""
def f():
    l = 23
    assert l == 23
    del l
    l
f()
"""),
    Case(
        name="import",
        text_code=r"""
import math
print(math.pi, math.e)
from math import sqrt
print(sqrt(2))
from math import *
print(sin(2))
"""),
    Case(
        name="classes",
        text_code=r"""
class Thing(object):
    def __init__(self, x):
        self.x = x
    def meth(self, y):
        return self.x * y
thing1 = Thing(2)
thing2 = Thing(3)
print(thing1.x, thing2.x)
print(thing1.meth(4), thing2.meth(5))
"""),
    Case(
        name="calling_methods_wrong",
        text_code=r"""
class Thing(object):
    def __init__(self, x):
        self.x = x
    def meth(self, y):
        return self.x * y
thing1 = Thing(2)
print(Thing.meth(14))
"""),
    Case(
        name="calling_subclass_methods",
        text_code=r"""
class Thing(object):
    def foo(self):
        return 17

class SubThing(Thing):
    pass

st = SubThing()
print(st.foo())
"""),
    Case(
        name="subclass_attribute",
        text_code=r"""
class Thing(object):
    def __init__(self):
        self.foo = 17
class SubThing(Thing):
    pass
st = SubThing()
print(st.foo)
"""),
    Case(
        name="subclass_attributes_not_shared",
        text_code=r"""
class Thing(object):
    foo = 17
class SubThing(Thing):
    foo = 25
st = SubThing()
t = Thing()
assert st.foo == 25
assert t.foo == 17
print("Assert test case for subclass_attributes_not_shared")
"""),
    Case(
        name="object_attrs_not_shared_with_class",
        text_code=r"""
class Thing(object):
    pass
t = Thing()
t.foo = 1
Thing.foo
"""),
    Case(
        name="data_descriptors_precede_instance_attributes",
        text_code=r"""
class Foo(object):
    pass
f = Foo()
f.des = 3
class Descr(object):
    def __get__(self, obj, cls=None):
        return 2
    def __set__(self, obj, val):
        raise NotImplementedError
Foo.des = Descr()
assert f.des == 2
print("Assert test case for data_descriptors_precede_instance_attributes")
"""),
    Case(
        name="instance_attrs_precede_non_data_descriptors",
        text_code=r"""
class Foo(object):
    pass
f = Foo()
f.des = 3
class Descr(object):
    def __get__(self, obj, cls=None):
        return 2
Foo.des = Descr()
assert f.des == 3
print("Assert test case for instance_attrs_precede_non_data_descriptors")
"""),
    Case(
        name="subclass_attributes_dynamic",
        text_code=r"""
class Foo(object):
    pass
class Bar(Foo):
    pass
b = Bar()
Foo.baz = 3
assert b.baz == 3
print("Assert test case for subclass_attributes_dynamic")
"""),
    Case(
        name="attribute_access",
        text_code=r"""
class Thing(object):
    z = 17
    def __init__(self):
        self.x = 23
t = Thing()
print(Thing.z)
print(t.z)
print(t.x)
"""),
    Case(
        name="attribute_access_AttributeError",
        text_code=r"""
class Thing(object):
    z = 17
    def __init__(self):
        self.x = 23
t = Thing()
print(t.xyzzy)
"""),
    Case(
        name="staticmethods",
        text_code=r"""
class Thing(object):
    @staticmethod
    def smeth(x):
        print(x)
    @classmethod
    def cmeth(cls, x):
        print(x)

Thing.smeth(1492)
Thing.cmeth(1776)
"""),
    Case(
        name="unbound_methods",
        text_code=r"""
class Thing(object):
    def meth(self, x):
        print(x)
m = Thing.meth
m(Thing(), 1815)
"""),
    Case(
        name="bound_methods",
        text_code=r"""
class Thing(object):
    def meth(self, x):
        print(x)
t = Thing()
m = t.meth
m(1815)
"""),
    Case(
        name="callback",
        text_code=r"""
def lcase(s):
    return s.lower()
l = ["xyz", "ABC"]
l.sort(key=lcase)
print(l)
assert l == ["ABC", "xyz"]
print("Assert test case for callback")
"""),
    Case(
        name="unpacking",
        text_code=r"""
a, b, c = (1, 2, 3)
assert a == 1
assert b == 2
assert c == 3
print("Assert test case for unpacking")
"""),
    Case(
        name="exec_statement",
        text_code=r"""
g = {}
exec("a = 11", g, g)
assert g['a'] == 11
print("Assert test case for exec_statement")
"""),
    Case(
        name="jump_if_true_or_pop",
        text_code=r"""
def f(a, b):
    return a or b
assert f(17, 0) == 17
assert f(0, 23) == 23
assert f(0, "") == ""
print("Assert test case for jump_if_true_or_pop")
"""),
    Case(
        name="jump_if_false_or_pop",
        text_code=r"""
def f(a, b):
    return not(a and b)
assert f(17, 0) is True
assert f(0, 23) is True
assert f(0, "") is True
assert f(17, 23) is False
print("Assert test case for jump_if_false_or_pop")
"""),
    Case(
        name="pop_jump_if_true",
        text_code=r"""
def f(a):
    if not a:
        return 'foo'
    else:
        return 'bar'
assert f(0) == 'foo'
assert f(1) == 'bar'
print("Assert test case for pop_jump_if_true")
"""),
    Case(
        name="decorator",
        text_code=r"""
def verbose(func):
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return _wrapper

@verbose
def add(x, y):
    return x+y

add(7, 3)
print("Test case decorator")
"""),
    Case(
        name="multiple_classes",
        text_code=r"""
class A(object):
    def __init__(self, a, b, c):
        self.sum = a + b + c

class B(object):
    def __init__(self, x):
        self.x = x

a = A(1, 2, 3)
b = B(7)
print(a.sum)
print(b.x)
"""),
    Case(
        name="for",
        text_code=r"""
for i in range(10):
    print(i)
print("done")
"""),
    Case(
        name="break",
        text_code=r"""
for i in range(10):
    print(i)
    if i == 7:
        break
print("done")
"""),
    Case(
        name="continue",
        text_code=r"""
for i in range(10):
    if i % 3 == 0:
        continue
    print(i)
print("done")
"""),
    Case(
        name="continue_in_try_except",
        text_code=r"""
for i in range(10):
    try:
        if i % 3 == 0:
            continue
        print(i)
    except ValueError:
        pass
print("done")
"""),
    Case(
        name="continue_in_try_finally",
        text_code=r"""
for i in range(10):
    try:
        if i % 3 == 0:
            continue
        print(i)
    finally:
        print(".")
print("done")
"""),
    Case(
        name="in",
        text_code=r"""
assert "x" in "xyz"
assert "x" not in "abc"
assert "x" in ("x", "y", "z")
assert "x" not in ("a", "b", "c")
print("Assert test case for in")
"""),
    Case(
        name="is",
        text_code=r"""
x = ["apple", "banana", "cherry"]
y = x
assert x is y
z = ["apple", "banana", "cherry"]
assert x is not z
a, b = None, 0
assert a is None
assert not (b is not None) == False
print("Assert test case for is")
"""),
    Case(
        name="less",
        text_code=r"""
assert 1 < 3
assert 1 <= 2 and 1 <= 1
assert "a" < "b"
assert "a" <= "b" and "a" <= "a"
print("Assert test case for less")
"""),
    Case(
        name="greater",
        text_code=r"""
assert 3 > 1
assert 3 >= 1 and 3 >= 3
assert "z" > "a"
assert "z" >= "a" and "z" >= "z"
print("Assert test case for greater")
""")
]


###################################
# FUNCTION CASES
###################################


FUNCTION_CASES = [
    Case(
        name="functions",
        text_code=r"""
def fn(a, b=17, c="Hello", d=[]):
    d.append(99)
    print(a, b, c, d)
fn(1)
fn(2, 3)
fn(3, c="Bye")
fn(4, d=["What?"])
fn(5, "b", "c")
"""),
    Case(
        name="recursion",
        text_code=r"""
def fact(n):
    if n <= 1:
        return 1
    else:
        return n * fact(n-1)
f6 = fact(6)
print(f6)
assert f6 == 720
print("Assert test case for recursion")
"""),
    Case(
        name="nested_names",
        text_code=r"""
def one():
    x = 1
    def two():
        x = 2
        print(x)
    two()
    print(x)
one()
"""),
    Case(
        name="calling_functions_with_args_kwargs",
        text_code=r"""
def fn(a, b=17, c="Hello", d=[]):
    d.append(99)
    print(a, b, c, d)
fn(6, *[77, 88])
fn(**{'c': 23, 'a': 7})
fn(6, *[77], **{'c': 23, 'd': [123]})
"""),
    Case(
        name="defining_functions_with_args",
        text_code=r"""
def fn(*args):
    print("args is %r" % (args,))
fn(1, 2)
"""),
    Case(
        name="defining_functions_with_kwargs",
        text_code=r"""
def fn(**kwargs):
    print("kwargs is %r" % sorted(kwargs.items()))
fn(red=True, blue=False)
"""),
    Case(
        name="defining_functions_with_args_kwargs",
        text_code=r"""
def fn(*args, **kwargs):
    print("args is %r" % (args,))
    print("kwargs is %r" % sorted(kwargs.items()))
fn(1, 2, red=True, blue=False)
"""),
    Case(
        name="defining_functions_with_positional_args_kwargs",
        text_code=r"""
def fn(x, y, *args, **kwargs):
    print("x is %r, y is %r" % (x, y))
    print("args is %r" % (args,))
    print("kwargs is %r" % sorted(kwargs.items()))
fn('a', 'b', 1, 2, red=True, blue=False)
"""),
    Case(
        name="defining_functions_with_keyword_only",
        text_code=r"""
def fn(*, x, y):
    print("x is %r, y is %r" % (x, y))
fn(x=1, y=2)
"""),
    Case(
        name="defining_functions_with_positional_only_ordinary_and_keyword_only",
        text_code=r"""
def fn(pos1, pos2, /, any1, any2, *, kw1, kw2):
    print("x is %r, y is %r" % (pos1, pos2, any1, any2, kw1, kw2))
fn(1, 2, 3, any2=4, kw1=5, kw2=6)
fn(1, 2, any1=3, any2=4, kw1=5, kw2=6)
fn(1, 2, any2=3, any1=4, kw1=5, kw2=6)
fn(1, 2, 3, 4, kw1=5, kw2=6)
"""),
    Case(
        name="defining_functions_with_empty_args",
        text_code=r"""
def fn(*args):
    print("args is %r" % (args,))
fn()
"""),
    Case(
        name="defining_functions_with_empty_kwargs",
        text_code=r"""
def fn(**kwargs):
    print("kwargs is %r" % sorted(kwargs.items()))
fn()
"""),
    Case(
        name="defining_functions_with_empty_args_kwargs",
        text_code=r"""
def fn(*args, **kwargs):
    print("args is %r, kwargs is %r" % (args, kwargs))
fn()
"""),
    Case(
        name="partial",
        text_code=r"""
from _functools import partial

def f(a,b):
    return a-b

f7 = partial(f, 7)
four = f7(3)
assert four == 4
print("Assert test case for partial")
"""),
    Case(
        name="partial_with_kwargs",
        text_code=r"""
from _functools import partial

def f(a,b,c=0,d=0):
    return (a,b,c,d)

f7 = partial(f, b=7, c=1)
them = f7(10)
assert them == (10,7,1,0)
print("Assert test case for partial_with_kwargs")
"""),
    Case(
        name="wraps",
        text_code=r"""
from functools import wraps
def my_decorator(f):
    dec = wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    wrapper = dec(wrapper)
    return wrapper

@my_decorator
def example():
    '''Docstring'''
    return 17

assert example() == 17
print("Assert test case for wraps")
"""),
    Case(
        name="closures",
        text_code=r"""
def make_adder(x):
    def add(y):
        return x+y
    return add
a = make_adder(10)
print(a(7))
assert a(7) == 17
print("Assert test case for closures")
"""),
    Case(
        name="closures_store_deref",
        text_code=r"""
def make_adder(x):
    z = x+1
    def add(y):
        return x+y+z
    return add
a = make_adder(10)
print(a(7))
assert a(7) == 28
print("Assert test case for closures_store_deref")
"""),
    Case(
        name="closures_in_loop",
        text_code=r"""
def make_fns(x):
    fns = []
    for i in range(x):
        fns.append(lambda i=i: i)
    return fns
fns = make_fns(3)
for f in fns:
    print(f())
assert (fns[0](), fns[1](), fns[2]()) == (0, 1, 2)
print("Assert test case for closures_in_loop")
"""),
    Case(
        name="closures_with_defaults",
        text_code=r"""
def make_adder(x, y=13, z=43):
    def add(q, r=11):
        return x+y+z+q+r
    return add
a = make_adder(10, 17)
print(a(7))
assert a(7) == 88
print("Assert test case for closures_with_defaults")
"""),
    Case(
        name="deep_closures",
        text_code=r"""
def f1(a):
    b = 2*a
    def f2(c):
        d = 2*c
        def f3(e):
            f = 2*e
            def f4(g):
                h = 2*g
                return a+b+c+d+e+f+g+h
            return f4
        return f3
    return f2
answer = f1(3)(4)(5)(6)
print(answer)
assert answer == 54
print("Assert test case for deep_closures")
""")
]

###################################
# GENERATORS CASES
###################################

GENERATOR_CASES = [
    Case(
        name="first",
        text_code=r"""
def two():
    yield 1
    yield 2
for i in two():
    print(i)
"""),
    Case(
        name="partial_generator",
        text_code=r"""
from _functools import partial

def f(a,b):
    num = a+b
    while num:
        yield num
        num -= 1

f2 = partial(f, 2)
three = f2(1)
assert list(three) == [3,2,1]
print("Assert test case for partial_generator")
"""),
    Case(
        name="yield_multiple_values",
        text_code=r"""
def triples():
    yield 1, 2, 3
    yield 4, 5, 6

for a, b, c in triples():
    print(a, b, c)
"""),
    Case(
        name="simple_generator",
        text_code=r"""
g = (x for x in [0,1,2])
print(list(g))
"""),
    Case(
        name="generator_from_generator",
        text_code=r"""
g = (x*x for x in range(5))
h = (y+1 for y in g)
print(list(h))
"""),
    Case(
        name="generator_from_generator2",
        text_code=r"""
class Thing(object):
    RESOURCES = ('abc', 'def')
    def get_abc(self):
        return "ABC"
    def get_def(self):
        return "DEF"
    def resource_info(self):
        for name in self.RESOURCES:
            get_name = 'get_' + name
            yield name, getattr(self, get_name)

    def boom(self):
        #d = list((name, get()) for name, get in self.resource_info())
        d = [(name, get()) for name, get in self.resource_info()]
        return d

print(Thing().boom())
"""),
    Case(
        name="yield_from",
        text_code=r"""
def main():
    x = outer()
    next(x)
    y = x.send("Hello, World")
    print(y)

def outer():
    yield from inner()

def inner():
    y = yield
    yield y

main()
"""),
    Case(
        name="yield_from_tuple",
        text_code=r"""
def main():
    for x in outer():
        print(x)

def outer():
    yield from (1, 2, 3, 4)

main()
"""),
    Case(
        name="generator",
        text_code=r"""
next(i for i in range(10))
print("Test case generator")
"""),
    Case(
        name="distinguish_iterators_and_generators",
        text_code=r"""
class Foo(object):
    def __iter__(self):
        return FooIter()

class FooIter(object):
    def __init__(self):
        self.state = 0

    def __next__(self):
        if self.state >= 10:
            raise StopIteration
        self.state += 1
        return self.state

    def send(self, n):
        print("sending")

def outer():
    yield from Foo()

for x in outer():
    print(x)
"""),
    Case(
        name="nested_yield_from",
        text_code=r"""
def main():
    x = outer()
    next(x)
    y = x.send("Hello, World")
    print(y)

def outer():
    yield from middle()

def middle():
    yield from inner()

def inner():
    y = yield
    yield y

main()
"""),
    Case(
        name="return_from_generator",
        text_code=r"""
def gen():
    yield 1
    return 2

x = gen()
while True:
    try:
        print(next(x))
    except StopIteration as e:
        print(e.value)
        break
"""),
    Case(
        name="return_from_generator_with_yield_from",
        text_code=r"""
def returner():
    if False:
        yield
    return 1

def main():
    y = yield from returner()
    print(y)

list(main())
""")
]


###################################
# OLD PHILL CASES
###################################

PHILL_CASES = [
    Case(
        name="test1",
        text_code=r"""
a = 698
print(a)
"""),
    Case(
        name="test2",
        text_code=r"""
def test(x):
    return x ** 2
print(test(10))
"""),
    Case(
        name="test3",
        text_code=r"""
a = '212'
print(a, '6', sep='')
"""),
    Case(
        name="test4",
        text_code=r"""
a = 10
a /= 2
print(a)
"""),
    Case(
        name="test5",
        text_code=r"""
print(1 in {1: 2})
"""),
    Case(
        name="test6",
        text_code=r"""
print(2 not in {1: 2})
"""),
    Case(
        name="test7",
        text_code=r"""

print("Big empty test case")
"""),
    Case(
        name="test8",
        text_code=r"""
a = 27
b = 38
print(-a + (a + 2) + 2 * b)
"""),
    Case(
        name="test10",
        text_code=r"""
a = 2
b = 3
print(a ** a ** b ** a)
"""),
    Case(
        name="test11",
        text_code=r"""
a = True
b = False
print(a or b or a)
"""),
    Case(
        name="test12",
        text_code=r"""
a = 7
b = False
print(b or a)
"""),
    Case(
        name="test13",
        text_code=r"""
a = 7
b = False
print(True or False and (a or b))
"""),
    Case(
        name="test14",
        text_code=r"""
a = (1,)
print(a)
"""),
    Case(
        name="test15",
        text_code=r"""
a = (1,2)
print(a)
"""),
    Case(
        name="test16",
        text_code=r"""
a = (1,)
b = (2,)
print(a + b)
"""),
    Case(
        name="test17",
        text_code=r"""
a = (1,)
b = (2,)
print(a * 10 + b * 20)
"""),
    Case(
        name="test18",
        text_code=r"""
a = (4, 4)
cond = (2 ** 2, 2 ** 2) == a
print(cond)
"""),
    Case(
        name="test19",
        text_code=r"""
a = 6
a *= 2
print(a)
"""),
    Case(
        name="test20",
        text_code=r"""
a = "Hell"
print(a * 20 + 'o, World!')
"""),
    Case(
        name="test21",
        text_code=r"""
a = '1 2 3 4 5'
b = a.strip().split()
print(b[1] + b[3])
"""),
    Case(
        name="test22",
        text_code=r"""
a = '1:2:3\n\n\n\n\n'
print(a.strip().split())
"""),
    Case(
        name="test23",
        text_code=r"""
a = 'hi, my name is phill'
print(a.upper())
"""),
    Case(
        name="test24",
        text_code=r"""
print([1, 2, 3] == [1, 2, 4])
"""),
    Case(
        name="test25",
        text_code=r"""
a = [1]
a += [2]
a += [3]
a += [4]
print(a * 2)
"""),
    Case(
        name="test26",
        text_code=r"""
a = [1, 2, 3, 4, 'Test', 'Me']
print(str(a[0] + a[2]) + a[5])
"""),
    Case(
        name="test27",
        text_code=r"""
a = [1,[1]]
a[1] += [2]
print(a[1][1])
"""),
    Case(
        name="test28",
        text_code=r"""
a = (1, 2, 3)
b = (4, 5, 6)
print((a + b)[3])
"""),
    Case(
        name="test29",
        text_code=r"""
a = ([1], )
a[0].append(2)

print(a[0][-1])
"""),
    Case(
        name="test30",
        text_code=r"""
a = list(range(10))
a[1:] = a[:1:-1]
print(a[1] + a[3])
"""),
    Case(
        name="test31",
        text_code=r"""
a = (1, 2, 1)
print(sorted(a)[-1])
"""),
    Case(
        name="test32",
        text_code=r"""
a, b = [1, 4]
print(a + b)
"""),
    Case(
        name="test34",
        text_code=r"""
a, b = 1, 3
b, a = a, b
print(a ** b)
"""),
    Case(
        name="test35",
        text_code=r"""
a, b = 1, 3
b,b,b = a, a, b
print(a ** b)
"""),
    Case(
        name="test36",
        text_code=r"""
a = 2
b = 1

a, b = a + b, a
a, b = a + b, a
a, b = a + b, a
a, b = a + b, a
print(b)
"""),
    Case(
        name="test37",
        text_code=r"""
a = 27
b = 38
print(a + b)
"""),
    Case(
        name="test38",
        text_code=r"""
def sort(array=[12,4,5,6,7,3,1,15]):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:
        # You need to hande the part at the end of the recursion - when you only have one element in your array,
        # just return the array.
        return array

print(sort()[3])
"""),
    Case(
        name="test39",
        text_code=r"""
if True:
    print(2)
else:
    print(3)
"""),
    Case(
        name="test40",
        text_code=r"""
if False:
    print(1)
else:
    print(10)
"""),
    Case(
        name="test41",
        text_code=r"""
a = 2
if (True and 1):
    a *= 2
print(a)
"""),
    Case(
        name="test42",
        text_code=r"""
a = 2
if (7 and 1):
    a *= 2
print(a)
"""),
    Case(
        name="test43",
        text_code=r"""
a = 7 or False
print(a)
"""),
    Case(
        name="test44",
        text_code=r"""
a = 2
if (7 and (True or False)):
    a *= 2
print(a)
"""),
    Case(
        name="test45",
        text_code=r"""
a = 2
if not a % 3:
    print(1)
elif not a %2:
    print(2)
else:
    print(4)
"""),
    Case(
        name="test46",
        text_code=r"""
def f(x):
    return x

print(f(10))
"""),
    Case(
        name="test47",
        text_code=r"""
def f(*args, **kwargs):
    return sum(args)

print(f(10, 20, 30, 40))
"""),
    Case(
        name="test48",
        text_code=r"""
a = 27
b = 38
print(a * b)
"""),
    Case(
        name="test49",
        text_code=r"""
def f(*args, **kwargs):
    return sum(kwargs.values())

print(f(a=10, b=20, c=30, d=40))
"""),
    Case(
        name="test50",
        text_code=r"""
def f(*args, **kwargs):
    return kwargs['a']

print(f(a=1))
"""),
    Case(
        name="test51",
        text_code=r"""
def test1(x):
    return x ** 2
def test2(x):
    return test1(x) ** 2
print(test1(10))
"""),
    Case(
        name="test52",
        text_code=r"""
def test1(x):
    return x ** 2

def test2(x):
    return test1(x) ** 2

print(test2(10))
"""),
    Case(
        name="test53",
        text_code=r"""
def t1():
    def t2(y):
        return y * 3
    return t2

print(t1()(2))
"""),
    Case(
        name="test54",
        text_code=r"""
def t1(x):
    def t2(y):
        return x + y
    return t2

print(t1(2)(3))
"""),
    Case(
        name="test55",
        text_code=r"""
def decorator(function_to_decorate):
    def wrapper():
        print("1")
        function_to_decorate()
        print("3")
    return wrapper

@decorator
def foo():
    print("2")

foo()
"""),
    Case(
        name="test56",
        text_code=r"""
print([i for i in range(10)])
"""),
    Case(
        name="test57",
        text_code=r"""
print([i for i in range(10) if i % 2])
print([i for i in range(10) if i is None])  # POP_JUMP_BACKWARD_IF_NONE
print([i for i in range(10) if i is not None])  # POP_JUMP_BACKWARD_IF_NOT_NONE
"""),
    Case(
        name="test58",
        text_code=r"""
print([i ** 2 for i in range(10) if i % 2])
"""),
    Case(
        name="test59",
        text_code=r"""
a = 27
b = 38
print(a * b ** 2)
"""),
    Case(
        name="test60",
        text_code=r"""
for i in (i for i in range(10)):
    print(i)
"""),
    Case(
        name="test61",
        text_code=r"""
class T(object):
    def __init__(self):
        self._a = 1

t = T()
print(t._a)
"""),
    Case(
        name="test62",
        text_code=r"""
class T(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def f(self):
        return self._a + self._b

t = T(10, 20)
print(t.f())
"""),
    Case(
        name="test63",
        text_code=r"""
class T(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def m(self, c):
        self._b = c

    def f(self):
        return self._a + self._b

t = T(10, 20)
t.m(100)
print(t.f())
"""),
    Case(
        name="test64",
        text_code=r"""
class T(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def m(self, c):
        self._b = c

    def f(self):
        return self._a + self._b

class TT(T):

    def m(self, c):
        self._b = c * 1000


t = TT(10, 20)
t.m(100)
print(t.f())
"""),
    Case(
        name="test65",
        text_code=r"""
# commentary
print('fooo')
"""),
    Case(
        name="test66",
        text_code=r"""
'dummy string'
print('zu-zu-zu')
"""),
    Case(
        name="test67",
        text_code=r"""
while(True):
    print(1)
    break
"""),
    Case(
        name="test68",
        text_code=r"""
while(False):
    print('in loop')
    break
print('after loop')
"""),
    Case(
        name="test69",
        text_code=r"""
print(len('12345'))
"""),
    Case(
        name="test70",
        text_code=r"""
a = 27
b = 38
print(a * b + a)
"""),
    Case(
        name="test71",
        text_code=r"""
def myfunc(alist):
    return len(alist)
print(myfunc([1, 2, 3]))
"""),
    Case(
        name="test72",
        text_code=r"""
a = 1
b = 2
a, b = b, a
print(a, b)
"""),
    Case(
        name="test73",
        text_code=r"""
for i in (1, 2, 3):
    print(i)
"""),
    Case(
        name="test74",
        text_code=r"""
print(1);print(2);print(3)
"""),
    Case(
        name="test75",
        text_code=r"""
l = [1, 2, 3, 4, 5]
i = 0
while i < 3:
    i += 1
    print(l[i])
"""),
    Case(
        name="test76",
        text_code=r"""
l=[1, 2, 3, 4, 5]
for i in l:
    print(i)
    if i == 3:
        break
"""),
    Case(
        name="test77",
        text_code=r"""
for i in range(10):
    if i % 3 == 0:
        continue
    print(i)
print("finished")
"""),
    Case(
        name="test78",
        text_code=r"""
print('qw' in 'qwerty')
"""),
    Case(
        name="test79",
        text_code=r"""
print('zuzuzu' not in 'qwerty')
"""),
    Case(
        name="test80",
        text_code=r"""
print(1 < 2)
"""),
    Case(
        name="test81",
        text_code=r"""
a = 27
b = 38
print((a + b) * b)
"""),
    Case(
        name="test82",
        text_code=r"""
print(10 > 3)
"""),
    Case(
        name="test83",
        text_code=r"""
print(10 >= 3)
"""),
    Case(
        name="test84",
        text_code=r"""
print(1 <= 7)
"""),
    Case(
        name="test85",
        text_code=r"""
print(2**3 < 4)
"""),
    Case(
        name="test86",
        text_code=r"""
print('a' < 'b')
"""),
    Case(
        name="test87",
        text_code=r"""
print('qwe' > 'a')
"""),
    Case(
        name="test88",
        text_code=r"""
print('fasdfasdfasdf' >= 'a')
"""),
    Case(
        name="test89",
        text_code=r"""
c = (1, 2, 3, 4, 5, 6)
a, b = c[0], c[1:]
print(a)
print(b)
"""),
    Case(
        name="test90",
        text_code=r"""
c = (1, 2, 3, 4, 5, 6)
a, b = c[::2], c[1::2]
print(a)
print(b)
"""),
    Case(
        name="test91",
        text_code=r"""
c = (1, 2, 3, 4, 5, 6)
a, b = c[1:3], c[2:-1]
print(a)
print(b)
"""),
    Case(
        name="test92",
        text_code=r"""
a = 3
a += 2
print(a)
"""),
    Case(
        name="test93",
        text_code=r"""
print('Hello, %s!' % 'guest')
"""),
    Case(
        name="test94",
        text_code=r"""
print('%d %s, %d %s' % (6, 'bananas', 10, 'lemons'))
"""),
    Case(
        name="test95",
        text_code=r"""
print('%(language)s has %(number)03d quote types.' % {"language": "Python", "number": 2})
"""),
    Case(
        name="test96",
        text_code=r"""
print('Hello {0}'.format('guest'))
"""),
    Case(
        name="test97",
        text_code=r"""
print('%+10f' % 25)
"""),
    Case(
        name="test98",
        text_code=r"""
print(1 in (1, 2, 3))
"""),
    Case(
        name="test99",
        text_code=r"""
print(5 not in (1, 2, 3))
"""),
    Case(
        name="test100",
        text_code=r"""
print(1 in [1, 2, 3])
"""),
    Case(
        name="test101",
        text_code=r"""
print(5 not in [1, 3])
"""),
    Case(
        name="test102",
        text_code=r"""
d = {1: 2, 3: 4}
print(d[1])
"""),
    Case(
        name="test103",
        text_code=r"""
a = 42
print(f'{a}, {"does it mean something"}?')
"""),
]

WITH_CASES = [
    Case(
        name="simple_context_manager",
        text_code=r"""
class NullContext(object):
    def __enter__(self):
        l.append('i')
        # __enter__ usually returns self, but doesn't have to.
        return 17

    def __exit__(self, exc_type, exc_val, exc_tb):
        l.append('o')
        return False

l = []
for i in range(3):
    with NullContext() as val:
        assert val == 17
        l.append('w')
    l.append('e')
l.append('r')
s = ''.join(l)
print("Look: %r" % s)
assert s == "iwoeiwoeiwoer"
"""),
    Case(
        name="raise_in_context_manager",
        text_code=r"""
class NullContext(object):
    def __enter__(self):
        l.append('i')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert exc_type is ValueError, "Expected ValueError: %r" % exc_type
        l.append('o')
        return False

l = []
try:
    with NullContext():
        l.append('w')
        raise ValueError("Boo!")
    l.append('e')
except ValueError:
    l.append('x')
l.append('r')
s = ''.join(l)
print("Look: %r" % s)
assert s == "iwoxr"
"""),
    Case(
        name="suppressed_raise_in_context_manager",
        text_code=r"""
class SuppressingContext(object):
    def __enter__(self):
        l.append('i')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert exc_type is ValueError, "Expected ValueError: %r" % exc_type
        l.append('o')
        return True

l = []
try:
    with SuppressingContext():
        l.append('w')
        raise ValueError("Boo!")
    l.append('e')
except ValueError:
    l.append('x')
l.append('r')
s = ''.join(l)
print("Look: %r" % s)
assert s == "iwoer"
"""),
    Case(
        name="return_in_with",
        text_code=r"""
class NullContext(object):
    def __enter__(self):
        l.append('i')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        l.append('o')
        return False

l = []
def use_with(val):
    with NullContext():
        l.append('w')
        return val
    l.append('e')

assert use_with(23) == 23
l.append('r')
s = ''.join(l)
print("Look: %r" % s)
assert s == "iwor"
"""),
    Case(
        name="continue_in_with",
        text_code=r"""
class NullContext(object):
    def __enter__(self):
        l.append('i')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        l.append('o')
        return False

l = []
for i in range(3):
    with NullContext():
        l.append('w')
        if i % 2:
           continue
        l.append('z')
    l.append('e')

l.append('r')
s = ''.join(l)
print("Look: %r" % s)
assert s == "iwzoeiwoiwzoer"
"""),
    Case(
        name="break_in_with",
        text_code=r"""
class NullContext(object):
    def __enter__(self):
        l.append('i')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        l.append('o')
        return False

l = []
for i in range(3):
    with NullContext():
        l.append('w')
        if i % 2:
           break
        l.append('z')
    l.append('e')

l.append('r')
s = ''.join(l)
print("Look: %r" % s)
assert s == "iwzoeiwor"
"""),
    Case(
        name="raise_in_with",
        text_code=r"""
class NullContext(object):
    def __enter__(self):
        l.append('i')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        l.append('o')
        return False

l = []
try:
    with NullContext():
        l.append('w')
        raise ValueError("oops")
        l.append('z')
    l.append('e')
except ValueError as e:
    assert str(e) == "oops"
    l.append('x')
l.append('r')
s = ''.join(l)
print("Look: %r" % s)
assert s == "iwoxr", "What!?"
"""),
    Case(
        name="at_context_manager_simplified",
        text_code=r"""
class GeneratorContextManager(object):
    def __init__(self, gen):
        self.gen = gen

    def __enter__(self):
        try:
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield")

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                next(self.gen)
            except StopIteration:
                return
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                value = type()
            try:
                self.gen.throw(type, value, traceback)
                raise RuntimeError(
                    "generator didn't stop after throw()"
                )
            except StopIteration as exc:
                return exc is not value
            except:
                if sys.exc_info()[1] is not value:
                    raise

def contextmanager(func):
    def helper(*args, **kwds):
        return GeneratorContextManager(func(*args, **kwds))
    return helper

@contextmanager
def my_context_manager(val):
    yield val

with my_context_manager(17) as x:
    assert x == 17
print("Assert test case for at_context_manager_simplified")
"""),
    Case(
        name="at_context_manager_complete",
        text_code=r"""
from _functools import partial

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)

def update_wrapper(wrapper,
                wrapped,
                assigned = WRAPPER_ASSIGNMENTS,
                updated = WRAPPER_UPDATES):
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Return the wrapper so this can be used as a decorator
    # via partial().
    return wrapper

def wraps(wrapped,
        assigned = WRAPPER_ASSIGNMENTS,
        updated = WRAPPER_UPDATES):
    return partial(update_wrapper, wrapped=wrapped,
                assigned=assigned, updated=updated)

class GeneratorContextManager(object):
    def __init__(self, gen):
        self.gen = gen

    def __enter__(self):
        try:
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield")

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                next(self.gen)
            except StopIteration:
                return
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                value = type()
            try:
                self.gen.throw(type, value, traceback)
                raise RuntimeError(
                    "generator didn't stop after throw()"
                )
            except StopIteration as exc:
                return exc is not value
            except:
                if sys.exc_info()[1] is not value:
                    raise

def contextmanager(func):
    @wraps(func)
    def helper(*args, **kwds):
        return GeneratorContextManager(func(*args, **kwds))
    return helper

@contextmanager
def my_context_manager(val):
    yield val

with my_context_manager(17) as x:
    assert x == 17
print("Assert test case for at_context_manager_complete")
"""),
    Case(
        name="generator_with_context_manager",
        text_code=r"""
from contextlib import contextmanager

def inner():
    yield "I'm inner!"

def foo():
    yield from inner()

    @contextmanager
    def cmgr():
        yield "Context Manager!"
    raise StopIteration(cmgr())

def main():
    with (yield from foo()) as x:
        print(x)

def run(fn, *args):
    x = fn(*args)
    while True:
        try:
            print(next(x))
        except StopIteration as e:
            return e.value
run(main)
""")
]

SMART_CASES = [

    #########################
    # Not Coverable
    # PRINT_EXPR (interactive mode only)
    # NOP (skipped by disassembler)
    #########################

    #########################
    # LOAD_CONST
    # RETURN_VALUE
    #########################

    Case(
        name="load_const",
        text_code=r"""

print("Empty string")
"""),

    #########################
    # STORE_NAME
    #########################

    Case(
        name="store_name",
        text_code=r"""
x = 1
print(x)
"""),

    #########################
    # MAKE_FUNCTION
    #########################

    Case(
        name="make_function",
        text_code=r"""
def foo():
    pass
print("Make function test case")
"""),

    #########################
    # CALL_FUNCTION
    #########################

    Case(
        name="call_function",
        text_code=r"""
print()
print("Print nothing test case")
"""),

    #########################
    # LOAD_NAME
    # POP_TOP
    #########################

    Case(
        name="load_name",
        text_code=r"""
int
print("Load name test case")
"""),

    #########################
    # POP_JUMP_IF_FALSE
    #########################

    Case(
        name="pop_jump_if_false",
        text_code=r"""
a = False
if a:
    print('Wrong')
else:
    pass
print("Test case for pop_jump_if_false")
"""),

    #########################
    # POP_JUMP_IF_TRUE
    # JUMP_FORWARD
    #########################

    Case(
        name="pop_jump_if_true",
        text_code=r"""
a = False
if not a:
    pass
else:
    print('Wrong')
print("Test case pop_jump_if_true")
"""),

    #########################
    # BINARY_AND
    #########################

    Case(
        name="binary_and",
        text_code=r"""
a = 0b1100
b = 0b1010
c = a & b
print(c)
assert(c == 0b1000)
"""),

    #########################
    # BINARY_INPLACE
    #########################

    Case(
        name="inplace_and",
        text_code=r"""
a = 0b1100
b = 0b1010
a &= b
print(a)
assert(a == 0b1000)
"""),

    #########################
    # BINARY_OR
    #########################

    Case(
        name="binary_or",
        text_code=r"""
a = 0b1100
b = 0b1010
c = a | b
print(c)
assert(c == 0b1110)
"""),

    #########################
    # INPLACE_OR
    #########################

    Case(
        name="inplace_or",
        text_code=r"""
a = 0b1100
b = 0b1010
a |= b
print(a)
assert(a == 0b1110)
"""),

    #########################
    # BINARY_XOR
    #########################

    Case(
        name="binary_xor",
        text_code=r"""
a = 0b1100
b = 0b1010
c = a ^ b
print(c)
assert(c == 0b0110)
"""),

    #########################
    # INPLACE_XOR
    #########################

    Case(
        name="inplace_xor",
        text_code=r"""
a = 0b1100
b = 0b1010
a ^= b
print(a)
assert(a == 0b0110)
"""),

    #########################
    # BINARY_LSHIFT
    #########################

    Case(
        name="binary_lshift",
        text_code=r"""
a = 0b1100
b = a << 1
print(b)
assert(b == 0b11000)
"""),

    #########################
    # INPLACE_LSHIFT
    #########################

    Case(
        name="inplace_lshift",
        text_code=r"""
a = 0b1100
a <<= 1
print(a)
assert(a == 0b11000)
"""),

    #########################
    # BINARY_RSHIFT
    #########################

    Case(
        name="binary_rshift",
        text_code=r"""
a = 0b1100
b = a >> 1
print(b)
assert(b == 0b110)
"""),

    #########################
    # INPLACE_RSHIFT
    #########################

    Case(
        name="inplace_rshift",
        text_code=r"""
a = 0b1100
a >>= 1
print(a)
assert(a == 0b110)
"""),

    #########################
    # BINARY_ADD
    #########################

    Case(
        name="binary_add",
        text_code=r"""
a = 10
b = a + 1
print(b)
assert(b == 11)
"""),

    #########################
    # INPLACE_ADD
    #########################

    Case(
        name="inplace_add",
        text_code=r"""
a = 10
a += 1
print(a)
assert(a == 11)
"""),

    #########################
    # BINARY_SUBTRACT
    #########################

    Case(
        name="binary_subtract",
        text_code=r"""
a = 10
b = a - 1
print(b)
assert(b == 9)
"""),

    #########################
    # INPLACE_SUBTRACT
    #########################

    Case(
        name="inplace_subtract",
        text_code=r"""
a = 10
a -= 1
print(a)
assert(a == 9)
"""),

    #########################
    # BINARY_MULTIPLY
    #########################

    Case(
        name="binary_multiply",
        text_code=r"""
a = 10
b = a * 2
print(b)
assert(b == 20)
"""),

    #########################
    # INPLACE_MULTIPLY
    #########################

    Case(
        name="inplace_multiply",
        text_code=r"""
a = 10
a *= 2
print(a)
assert(a == 20)
"""),

    #########################
    # BINARY_POWER
    #########################

    Case(
        name="binary_power",
        text_code=r"""
a = 10
b = a ** 2
print(b)
assert(b == 100)
"""),

    #########################
    # INPLACE_POWER
    #########################

    Case(
        name="inplace_power",
        text_code=r"""
a = 10
a **= 2
print(a)
assert(a == 100)
"""),

    #########################
    # BINARY_FLOOR_DIVIDE
    #########################

    Case(
        name="binary_floor_divide",
        text_code=r"""
a = 15
b = a // 2
print(b)
assert(b == 7)
"""),

    #########################
    # INPLACE_FLOOR_DIVIDE
    #########################

    Case(
        name="inplace_floor_divide",
        text_code=r"""
a = 15
a //= 2
print(a)
assert(a == 7)
"""),

    #########################
    # BINARY_TRUE_DIVIDE
    #########################

    Case(
        name="binary_true_divide",
        text_code=r"""
a = 15
b = a / 2
print(b)
assert(b == 7.5)
"""),

    #########################
    # INPLACE_TRUE_DIVIDE
    #########################

    Case(
        name="inplace_true_divide",
        text_code=r"""
a = 15
a /= 2
print(a)
assert(a == 7.5)
"""),

    #########################
    # BINARY_MODULO
    #########################

    Case(
        name="binary_module",
        text_code=r"""
a = 7
b = a % 2
print(b)
assert(b == 1)
"""),

    #########################
    # INPLACE_MODULO
    #########################

    Case(
        name="inplace_module",
        text_code=r"""
a = 7
a %= 2
print(a)
assert(a == 1)
"""),

    #########################
    # UNARY_POSITIVE
    #########################

    Case(
        name="unary_positive",
        text_code=r"""
a = 1
b = +a
print(b)
assert(b == 1)
"""),

    #########################
    # UNARY_NEGATIVE
    #########################

    Case(
        name="unary_negative",
        text_code=r"""
a = 1
b = -a
print(b)
assert(b == -1)
"""),

    #########################
    # UNARY_NOT
    #########################

    Case(
        name="unary_not",
        text_code=r"""
a = False
b = not a
print(b)
assert(b == True)
"""),

    #########################
    # UNARY_INVERT
    #########################

    Case(
        name="unary_invert",
        text_code=r"""
a = 0b1100
b = ~a
print(b)
assert(b == -0b1101)
"""),

    #########################
    # BINARY_SUBSCR
    #########################

    Case(
        name="binary_subscr",
        text_code=r"""
b = {'a': 3 }
c = b['a']
print(c)
assert(c == 3)
"""),

    #########################
    # STORE_SUBSCR
    #########################

    Case(
        name="store_subscr",
        text_code=r"""
b = {}
b['a'] = 3
print(b)
assert(b == {'a': 3})
"""),

    #########################
    # DELETE_SUBSCR
    #########################

    Case(
        name="delete_subscr",
        text_code=r"""
b = {'a': 3 }
del b['a']
print(b)
assert(b == {})
"""),

    #########################
    # BINARY_MATRIX_MULTIPLY
    #########################

    Case(
        name="binary_matrix_multiply",
        text_code=r"""
class A(object):
    def __init__(self, a):
        self.a = a
    def __matmul__(self, other):
        return self.__class__(self.a * other.a)
    def __eq__(self, other):
        return self.a == other.a
    def __repr__(self):
        return 'A(%s)' % self.a

a = A(2)
b = A(3)
c = a @ b
print(c)
assert(c == A(6))
"""),

    #########################
    # INPLACE_MATRIX_MULTIPLY
    #########################

    Case(
        name="inplace_matrix_multiply",
        text_code=r"""
class A(object):
    def __init__(self, a):
        self.a = a
    def __imatmul__(self, other):
        self.a = self.a * other.a
        return self
    def __eq__(self, other):
        return self.a == other.a
    def __repr__(self):
        return 'A(%s)' % self.a

a = A(2)
b = A(3)
a @= b
print(a)
assert(a == A(6))
"""),

    #########################
    # BUILD_CONST_KEY_MAP
    #########################

    Case(
        name="build_const_key_map",
        text_code=r"""
b = {3: 4, 5: 6}
print(sorted(b.items()))
assert(b == {3: 4, 5: 6})
"""),

    #########################
    # BUILD_LIST
    #########################

    Case(
        name="build_list",
        text_code=r"""
a = [1,2,3]
b = [1,2,3]
print(a)
print(b)
assert(a == b)
"""),

    #########################
    # BUILD_LIST_UNPACK
    #########################

    Case(
        name="build_list_unpack",
        text_code=r"""
a = [1, 2]
b = [3, 4]
c = [*a, *b]
print(c)
assert(c == [1, 2, 3, 4])
"""),

    #########################
    # BUILD_MAP
    #########################

    Case(
        name="build_map",
        text_code=r"""
x = 1
y = 2
a = {x: 2, y: 3}
print(sorted(a.items()))
assert(a == {1: 2, 2: 3})
"""),

    #########################
    # BUILD_MAP_UNPACK
    #########################

    Case(
        name="build_map_unpack",
        text_code=r"""
a = {1: 2, 2: 3}
b = {2: 4, 3: 5}
c = {**a, **b}
print(sorted(c.items()))
assert(c == {1: 2, 2: 4, 3: 5})
"""),

    #########################
    # BUILD_MAP_UNPACK_WITH_CALL
    #########################

    Case(
        name="build_map_unpack_with_call",
        text_code=r"""
def f(**kwargs):
    return kwargs

a = {"a": 2, "b": 3}
b = {"c": 5}
c = f(**a, **b)
print(sorted(c.items()))
assert(c == {"a": 2, "b": 3, "c": 5})
"""),

    #########################
    # BUILD_SET
    #########################

    Case(
        name="build_set",
        text_code=r"""
a = {1,2,2}
b = {1,1,2}
print(sorted(a))
print(sorted(b))
assert(a == b)
"""),

    #########################
    # BUILD_SET_UNPACK
    #########################

    Case(
        name="build_set_unpack",
        text_code=r"""
a = {1,2,2}
b = {1,1,2}
c = {*a, *b}
print(sorted(c))
assert(c == {1, 2})
"""),

    #########################
    # BUILD_SLICE
    #########################

    Case(
        name="build_slice",
        text_code=r"""
a = [1, 2, 3, 4, 5]
s = a[1:4:1]
print(s)
assert(s == [2, 3, 4])
"""),

    #########################
    # BUILD_STRING
    # BUILD_FORMAT
    #########################

    Case(
        name="build_string",
        text_code=r"""
a = "hello"
fa = f"{a} world"
print(fa)
assert(fa == "hello world")
"""),

    #########################
    # BUILD_TUPLE
    #########################

    Case(
        name="build_tuple",
        text_code=r"""
a = (1, 2, 3)
b = (1, 2, 3)
print(a)
print(b)
assert(a == b)
"""),

    #########################
    # BUILD_TUPLE_UNPACK
    #########################

    Case(
        name="build_tuple_unpack",
        text_code=r"""
a = (1,2)
b = (3,4)
c = (*a, *b)
print(c)
assert(c == (1, 2, 3, 4))
"""),

    #########################
    # BUILD_TUPLE_UNPACK_WITH_CALL
    #########################

    Case(
        name="build_tuple_unpack_with_call",
        text_code=r"""
def f(*args):
    return args
a = (1,2)
b = (3,4)
c = f(*a, *b)
print(c)
assert(c == (1, 2, 3, 4))
"""),

    #########################
    # IMPORT_FROM
    #########################

    Case(
        name="import_from",
        text_code=r"""
from io import SEEK_END
a = SEEK_END
print(a)
assert(a == 2)
"""),

    #########################
    # IMPORT_NAME
    #########################

    Case(
        name="import_name",
        text_code=r"""
import io
a = io.SEEK_END
print(a)
assert(a == 2)
"""),

    #########################
    # IMPORT_STAR
    #########################

    Case(
        name="import_star",
        text_code=r"""
from io import *
a = SEEK_END
print(a)
assert(SEEK_END == 2)
"""),

    #########################
    # COMPARE_OP
    #########################

    Case(
        name="compare_op_l",
        text_code=r"""
a = 1 < 2
print(a)
assert(a == True)
a = 1 > 2
print(a)
assert(a == False)
a = 1 <= 2
print(a)
assert(a == True)
a = 1 >= 2
print(a)
assert(a == False)
a = 1 == 2
print(a)
assert(a == False)
a = 1 != 2
print(a)
assert(a == True)
"""),

    #########################
    # LOAD_ATTR
    #########################

    Case(
        name="load_attr",
        text_code=r"""
a = (3).real
print(a)
assert(a == 3)
"""),

    #########################
    # STORE_ATTR
    #########################

    Case(
        name="store_attr",
        text_code=r"""
class A:
    pass
A.c = 3
print(A.c)
assert(A.c == 3)
"""),

    #########################
    # DELETE_ATTR
    #########################

    Case(
        name="delete_attr",
        text_code=r"""
class A:
    F = 1
del A.F
attr = getattr(A, 'F', None)
print(attr)
assert(attr == None)
"""),

    #########################
    # LOAD_FAST
    #########################

    Case(
        name="load_fast",
        text_code=r"""
def myfunc(alist):
    return len(alist)
m = myfunc([2])
print(m)
assert(m == 1)
"""),

    #########################
    # STORE_FAST
    #########################

    Case(
        name="store_fast",
        text_code=r"""
def myfunc(alist):
    a = len(alist)
m = myfunc([])
print(m)
assert(m == None)
"""),

    #########################
    # DELETE_FAST
    #########################

    Case(
        name="delete_fast",
        text_code=r"""
def myfunc(a):
    del a
d = 1
myfunc(d)
print(d)
assert(d == 1)
"""),

    #########################
    # GET_AWAITABLE
    #########################

    Case(
        name="get_awaitable",
        text_code=r"""
import asyncio
loop = asyncio.get_event_loop()

async def download(x):
    return x + 1

async def main():
    co = [download(x) for x in range(10)]
    completed, pending = await asyncio.gather(*co)
    results = sorted(i.result() for i in completed)
    print(results)
    assert(results == list(range(1,11)))

loop.run_until_complete(main())
"""),

    #########################
    # GET_AITER
    # GET_ANEXT
    #########################

    Case(
        name="get_awaitable_2",
        text_code=r"""
import asyncio

async def inc(i):
    await asyncio.sleep(0)
    return i + 1

class A:
    def __aiter__(self):
        self.data = (inc(i) for i in range(2))
        return self

    def __anext__(self):
        try:
            task = next(self.data)
        except StopIteration:
            raise StopAsyncIteration
        return task

results = []

async def main(tag):
    async for x in A():
        results.append((tag, x))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(main("A"), main("B"), main("C")))
s = sorted(results)

print(s)
assert(s == [('A', 1), ('A', 2), ('B', 1), ('B', 2), ('C', 1), ('C', 2)])
"""),

    #########################
    # BEFORE_ASYNC_WITH
    # SETUP_ASYNC_WITH
    #########################

    Case(
        name="get_awaitable_3",
        text_code=r"""
import asyncio

async def inc(i):
    await asyncio.sleep(0)
    return i + 1

async def dec(i):
    await asyncio.sleep(0)
    return i - 1

class A:
    def __init__(self, tag, i):
        self.tag = tag
        self.i = i

    async def __aenter__(self):
        self.i = await inc(self.i)
        print('enter')
        return ('enter', self.tag, self.i)

    async def __aexit__(self, exc_type, exc, tb):
        self.i = await dec(self.i)
        print('exit')

results = []

async def main(tag, i):
    async with A(tag, i) as f:
        results.append(f)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(main("A", 1), main("B", 2), main("C", 3)))
s = sorted(results)

print(s)
assert(s == [('enter', 'A', 2), ('enter', 'B', 3), ('enter', 'C', 4)])
"""),

    #########################
    # SETUP_ANNOTATIONS
    # STORE_ANNOTATION
    #########################

    Case(
        name="setup_annotations",
        text_code=r"""
import typing
a: list[int] = []
b: str
c = __annotations__
print(sorted(c.items()))
assert(c == {'a': list[int], 'b': str})
"""),

    #########################
    # LOAD_GLOBAL
    #########################

    Case(
        name="load_global",
        text_code=r"""
a = 3
def foo():
    return a
c = foo()
print(c)
assert(c == 3)
"""),

    #########################
    # STORE_GLOBAL
    #########################

    Case(
        name="store_global",
        text_code=r"""
a = 3
def foo():
    global a
    a = 5
foo()
print(a)
assert(a == 5)
"""),

    #########################
    # DELETE_GLOBAL
    #########################

    Case(
        name="delete_global",
        text_code=r"""
a = 3
def foo():
    global a
    del a
foo()
c = 'a' in dir()
print(c)
assert(c == False)
"""),

    #########################
    # LOAD_DEREF
    # STORE_DEREF
    #########################

    Case(
        name="load_deref",
        text_code=r"""
def foo():
    a = 4
    def bar():
        return a
    return bar()
c = foo()
print(c)
assert(c == 4)
"""),

    #########################
    # DELETE_DEREF
    #########################

    Case(
        name="delete_deref",
        text_code=r"""
def foo():
    a = 4
    def bar():
        return a
    bar()
    del a
    return 'a' in dir()
c = foo()
print(c)
assert(c == False)
"""),

    #########################
    # LOAD_CLASSDEREF
    #########################

    Case(
        name="classderef",
        text_code=r"""
def foo():
    x = 1
    class A:
        a = x
    f = A()
    return f.a
c = foo()
print(c)
assert(c == 1)
""")
]


EXCEPTIONS_CASES = [
    Case(
        name="catching_IndexError",
        text_code=r"""
try:
    [][1]
    print("Shouldn't be here...")
except IndexError:
    print("caught it!")
"""),
    Case(
        name="catching_by_parent",
        text_code=r"""
try:
    [][1]
    print("Shouldn't be here...")
except Exception:
    print("caught it!")
"""),
    Case(
        name="catching_all",
        text_code=r"""
try:
    [][1]
    print("Shouldn't be here...")
except:
    print("caught it!")
"""),
    Case(
        name="raise_exception",
        text_code=r"""
raise ValueError('oops')
"""),
    Case(
        name="raise_exception_class",
        text_code=r"""
raise ValueError
"""),
    Case(
        name="raise_and_catch_exception",
        text_code=r"""
try:
    raise ValueError("oops")
except ValueError as e:
    print("Caught: %s" % e)
print("All done")
"""),
    Case(
        name="raise_exception_from",
        text_code=r"""
raise ValueError from NameError
"""),
    Case(
        name="raise_and_catch_exception_in_function",
        text_code=r"""
def fn():
    raise ValueError("oops")

try:
    fn()
except ValueError as e:
    print("Caught: %s" % e)
print("done")
"""),
    Case(
        name="global_name_error",
        text_code=r"""
fooey
"""),
    Case(
        name="global_name_error_in_try",
        text_code=r"""
try:
    fooey
    print("Yes fooey?")
except NameError:
    print("No fooey")
"""),
    Case(
        name="local_name_error",
        text_code=r"""
def fn():
    fooey
fn()
"""),
    Case(
        name="catch_local_name_error",
        text_code=r"""
def fn():
    try:
        fooey
        print("Yes fooey?")
    except NameError:
        print("No fooey")
fn()
"""),
    Case(
        name="reraise",
        text_code=r"""
def fn():
    try:
        fooey
        print("Yes fooey?")
    except NameError:
        print("No fooey")
        raise
fn()
"""),
    Case(
        name="reraise_explicit_exception",
        text_code=r"""
def fn():
    try:
        raise ValueError("ouch")
    except ValueError as e:
        print("Caught %s" % e)
        raise
fn()
"""),
    Case(
        name="finally_while_throwing",
        text_code=r"""
def fn():
    try:
        print("About to..")
        raise ValueError("ouch")
    finally:
        print("Finally")
fn()
print("Done")
"""),
    Case(
        name="coverage_issue_92",
        text_code=r"""
l = []
for i in range(3):
    try:
        l.append(i)
    finally:
        l.append('f')
    l.append('e')
l.append('r')
print(l)
assert l == [0, 'f', 'e', 1, 'f', 'e', 2, 'f', 'e', 'r']
""")
]

STUDENT_CASES = [
    Case(
        name="unpacking",
        text_code=r"""
*a, b, c = [0, 1, 2, 3, 4]
print(a, b, c)
a, *b, c = [0, 1, 2, 3, 4]
print(a, b, c)
a, b, *c = [0, 1, 2, 3, 4]
print(a, b, c)
*a, b, c = [0, 1]
print(a, b, c)
a, *b, c = [0, 1]
print(a, b, c)
a, b, *c = [0, 1]
print(a, b, c)
"""),
    Case(
        name="nested_loops",
        text_code=r"""
for x in range(4):
    for y in range(4):
        if y == 3:
            break
        for z in range(4):
            if y == 2:
                break
            print(x, y, z)
"""),
    Case(
        name="comprehensions",
        text_code=r"""
print([i for i in {j for j in [k for k in range(5)] if j != 0}])
"""),
    Case(
        name="simple_function",
        text_code=r"""
def foo(x=[]):
    x.append(1)
    print(x)
foo()
foo()
"""),
    Case(
        name="big_function",
        text_code=r"""
def foo(x, y, a=1, b=2, c=3, *args, k, w=4, l, **kwargs):
    print(x)
    print(y)
    print(a)
    print(b)
    print(c)
    print(args)
    print(k)
    print(w)
    print(l)
    print([x for x in sorted(kwargs.items())])
# foo(-1, -2, *range(10,15), k=-3, l=-4, z=-5, zz=-6)
foo(-2, -1, *range(10,15), k=-3, l=-4, z=-5, w=99, zz=-6)
"""),
    Case(
        name="ackerman",
        text_code=r"""
def ackermann(m, n):
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))
for m in range(4):
    answers = []
    for n in range(5):
        answers.append(str(ackermann(m, n)))
    print(' '.join(answers))
"""),
    Case(
        name="small_closure",
        text_code=r"""
def dec(num):
    def wrapper(func):
        def new_func(*args, **kwargs):
            print(num)
            return func(*args, **kwargs)
        return new_func
    return wrapper
@dec(100)
def foo(x):
    print(x)
foo(200)
"""),
    Case(
        name="big_closure",
        text_code=r"""
def profiler(func):
    def wrapper(*args, **kwargs):
        if wrapper.snoop_dogg == 0:
            wrapper.level = 0
            wrapper.calls = 1
            wrapper.snoop_dogg = 1
        if wrapper.level != 0:
            wrapper.calls += 1
        wrapper.level += 1
        ret = func(*args, **kwargs)
        wrapper.level -= 1
        if wrapper.level == 0:
            wrapper.snoop_dogg = 0
        return ret
    wrapper.level = 0
    wrapper.calls = 0
    wrapper.snoop_dogg = 0
    return wrapper
@profiler
def foo(x):
    while x > 0:
        x -= 1
        foo(x)
    print('foo')
foo(0)
print(foo.calls)
foo(1)
print(foo.calls)
foo(2)
print(foo.calls)
""")
]

PYTHON_3_8_NEW_CASES = [
    Case(
        name="assignment_expression_if",
        text_code=r"""
a = [1, 2, 3]
if (n := len(a)) < 10:
    print(f"List is too short ({n} elements, expected >= 10)")
"""),
    Case(
        name="assignment_expression_while",
        text_code=r"""
a = [1, 2, 3]
i = 0
while (block := a[i]) != '':
    print(block)
    i += 1
    if i >= len(a):
        break
"""),
    Case(
        name="self_explained_fstring",
        text_code=r"""
name = "Eric"
surname = "Cartman"
string_var = f"Object: {name=}, {surname=} is <non-printable speech here>"
print(string_var)
""")
]

PYTHON_3_9_NEW_CASES = [
    Case(
        name="set_union",
        text_code=r"""
a = {1,2,2}
b = {1,1,2}
c = a | b
print(sorted(c))
assert(c == {1, 2})
"""),
    Case(
        name="dict_union",
        text_code=r"""
a = {'a': 1, 'b': 2}
b = {'b': 'set', 'c': 3}
c = a | b
print(c)
assert(c == {'a': 1, 'b': 'set', 'c': 3})
b |= a
print(b)
assert(b == {'a': 1, 'b': 2, 'c': 3})
"""),
    Case(
        name="new_typings_setup_annotations",
        text_code=r"""
a: list[int] = []
b: str
c = __annotations__
print(sorted(c.items()))
assert(c == {'a': list[int], 'b': str})
"""),
    Case(
        name="new_typings_features",
        text_code=r"""
import types
assert list[str] == list[str]
assert not (list[str] == list[int])
assert isinstance(list[str], types.GenericAlias)
l: list[str] = ['1', '2', '3']
t = list[str]('123')
print(l == t)
assert isinstance(l, list)
"""),
    Case(
        name="removeprefix_removesuffix",
        text_code=r"""
test_func_name = 'test_func_name'
print(test_func_name.removeprefix("test_"))
print(test_func_name.removesuffix("_name"))
"""),
]


PYTHON_3_10_NEW_CASES = [
    Case(
        name="parenthesized_context_managers",
        text_code=r"""
with (
    open('test.1', 'w') as example1,
    open('test.2', 'w') as example2,
    open('test.3', 'w') as example3,
):
    pass
"""),
    Case(
        name="structural_pattern_matching_simple",
        text_code=r"""
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case 500 | 501 | 502 | 505:
            return "Pyatysotim!"
        case _:
            return "Something's wrong with the Internet"

print(http_error(400))
print(http_error(418))
print(http_error(502))
print(http_error(100))
"""),
    Case(
        name="structural_pattern_matching_enum",
        text_code=r"""
from enum import Enum
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

color = Color.RED

match color:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")
"""),
    Case(
        name="structural_pattern_matching_complex",
        text_code=r"""
from dataclasses import dataclass

@dataclass
class Foo:
    x: int

def foo(x):
    match x:
        case [1]: return 1
        case {'a': 2}: return 2
        case Foo(3): return 3
        case _: return 'none'

print(foo([1]))
print(foo({'a': 2}))
print(foo(Foo(3)))
print(foo(123))
"""),
    Case(
        name="new_type_hints",
        text_code=r"""
def square(number: int | float) -> int | float:
    return number ** 2

print(square.__annotations__)

print(isinstance(1, int | str))
"""),
    Case(
        name="int_bits",
        text_code=r"""
a: int = 42

print(a.bit_count())
"""),
]


PYTHON_3_11_NEW_CASES = [
    Case(
        name="TypedDict_items_not_required",
        text_code=r"""
from typing import TypedDict, NotRequired

class Movie(TypedDict):
   title: str
   year: NotRequired[int]

m1: Movie = {"title": "Black Panther", "year": 2018}  # OK
m2: Movie = {"title": "Star Wars"}  # OK (year is not required)
m3: Movie = {"year": 2022}  # ERROR (missing required field title)
"""),
    Case(
        name="self_type",
        text_code=r"""
class MyClass:
    def get_me(self) -> Self:
        return self

class_obj = MyClass()
print(class_obj.__annotations__)
"""),
    Case(
        name="async_generator",
        text_code=r"""
import asyncio

async def foo():
    yield 1
    yield 2

async def main():
    g = foo()
    print(await anext(g))
    print(await anext(g))
    print(await anext(g))

asyncio.run(main())
"""),
    Case(
        name="exception_groups",
        text_code=r"""
def foo():
    raise ExceptionGroup("msg", [
        ValueError("foo"),
        TypeError("bar"),
        NameError("baz"),
    ])
try:
    try:
        foo()
    except* ValueError as eg:
        print(eg.exceptions)
        raise RuntimeError("wtf")
    except* TypeError as eg:
        print(eg.exceptions)
except ExceptionGroup as eg:
    print(eg.exceptions)
""")
]


TEST_CASES = \
    BASIC_UNSTRUCTURED_CASES + \
    FUNCTION_CASES + \
    GENERATOR_CASES + \
    PHILL_CASES + \
    WITH_CASES + \
    EXCEPTIONS_CASES + \
    STUDENT_CASES + \
    SMART_CASES + \
    PYTHON_3_8_NEW_CASES + \
    PYTHON_3_9_NEW_CASES + \
    PYTHON_3_10_NEW_CASES + \
    PYTHON_3_11_NEW_CASES
