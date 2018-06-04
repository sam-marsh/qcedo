import sympy as sp

# dynamic programming memoization tool for computing discrete walsh functions
def memoize(f):
    cache = {}

    def memoized_fn(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    memoized_fn.cache = cache
    return memoized_fn

# computes walsh function
@memoize
def wal(N, m, n):
    if m == 0:
        return 1
    if m == 1:
        return 1 if n <= N // 2 - 1 else -1
    return wal(N, m//2, (2*n) % N) * wal(N, m - 2*(m//2), n)

# computes Walsh transform coefficients F(m)=sum from 0 to N-1 of f(n)*wal(m, n)
def wc(f, m, N):
    return sp.simplify(sum([f(n)*wal(N, m, n) for n in range(N)])/N)

# the input function! computes the diagonal entries of the operator which
# we desire to exponentiate
def f(n):
    return -(2**n) * sp.Symbol('t')

def gray(x):
    return (x >> 1) ^ x

def msb(x):
    i = 0
    while (x > 1):
        x >>= 1
        i += 1
    return i

def generate_gates(n, fn):
    N = 2**n
    for i in range(n):
        print('\t\tqubit q%d' % (i))
    print('\n')
    for i in range(1, N):
        j = gray(i)
        z_rot = -2 * wc(fn, j, N)
        if z_rot != 0:
            q = msb(j)
            l = []
            for k in range(0, q):
                if (j >> k) & 1 == 1:
                    l.append(k)
            for k in reversed(l):
                print('\tcnot q%d,q%d' % (k, q))
            print('\trz(%s) q%d' % (z_rot, q))
            for k in l:
                print('\tcnot q%d,q%d' % (k, q))


if __name__ == '__main__':
    generate_gates(3, f)
