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
def wal(m, n):
    if m == 0:
        return 1
    if m == 1:
        return 1 if n <= m // 2 - 1 else -1
    return wal(m//2, 2*n) * wal(m - 2*(m//2), n)

# computes Walsh transform coefficients F(m)=sum from 0 to N-1 of f(n) wal(m, n)
def wc(f, m, N):
    return sp.simplify(sum([f(n)*wal(m, n) for n in range(N)])/N)

# the input function! computes the diagonal entries of the operator which
# we desire to exponentiate
def f(n):
    return -n * sp.Symbol('t')

if __name__ == '__main__':
    N = 8
    print(wc(f, 0, N))
