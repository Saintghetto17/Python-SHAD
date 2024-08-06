from libcpp.string cimport string

cdef extern from "concat.h":
    string cpp_concat(string l, string r) except +


def concat(str l, str r):
    cdef string res = cpp_concat(l.encode('utf-8'), r.encode('utf-8'))
    return res.decode('utf-8')

def concat_list(list args):
    if len(args) < 2:
        raise RuntimeError("Expected at least 2 arguments")

    cdef string res = args[0].encode('utf-8')
    for i in range(1, len(args)):
        res = cpp_concat(res, args[i].encode('utf-8'))
    return res.decode('utf-8')
