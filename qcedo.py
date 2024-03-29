import sympy as sp
import random
import itertools
from functools import lru_cache

# computes walsh function
@lru_cache(maxsize=None)
def wal(N, m, n):
    if m == 0:
        return 1
    if m == 1:
        return 1 if n <= N // 2 - 1 else -1
    return wal(N, m//2, (2*n) % N) * wal(N, m - 2*(m//2), n)

# computes Walsh transform coefficients F(m)=sum from 0 to N-1 of f(n)*wal(m, n)
def wc(f, m, N):
    return sp.simplify(sum([f(n)*wal(N, m, n) for n in range(N)])/N)

def gray(x):
    return (x >> 1) ^ x

def msb(x):
    i = 0
    while (x > 1):
        x >>= 1
        i += 1
    return i

def only_uniques(group):
    for x in group:
        if group.count(x) == 1:
            yield x

def break_list(seq):
    group = []
    for num in seq:
        if num[0] == 'R':
            u = list(only_uniques(group))
            if u:
                yield u
                group = []
            if num[1] != 0:
                yield [num]
        else:
            group.append(num)

def gates(n, fn):
    N = 2**n
    ops = []
    for i in range(1, N):
        j = gray(i)
        z_rot = -2 * wc(fn, j, N)
        q = msb(j)
        l = []
        for k in reversed(range(0, q)):
            if (j >> k) & 1 == 1:
                l.append(('CNOT', k, q))
        ops += l
        ops.append(('R', z_rot, q))
        ops += reversed(l)
    return list(itertools.chain.from_iterable(break_list(ops)))

def print_qasm(n, gates):
    qubits = ['qubit\tq%d' % (i) for i in range(n)]
    defs = []
    ops = []
    for gate in gates:
        if gate[0] == 'CNOT':
            ops.append('cnot\tq%d,q%d' % (gate[1], gate[2]))
        elif gate[0] == 'R':
            def_name = 'QCEDO-%d' % (len(defs))
            defs.append('def\t%s,0,\'R\\left(%s\\right)\'' % (def_name, sp.latex(gate[1])))
            ops.append('%s\tq%d' % (def_name, gate[2]))
    print('\n\t\t'.join(['# AUTOGENERATED'] + defs + qubits + ops))

if __name__ == '__main__':
    n = 4
    arr = [random.randint(0, 3) for x in range(2**n)]
    f = lambda n : -arr[n] * sp.Symbol('t')
    #f = lambda n : -(2**n) * sp.Symbol('t')
    print('\n'.join(str(g) for g in gates(n, f)))
