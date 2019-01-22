"""
1.1
In traditional recursion, the typical model is that you perform your recursive
calls first, and then you take the return value of the recursive call and
calculate the result. In this manner, you don't get the result of your
calculation until you have returned from every recursive call.

In tail recursion, you perform your calculations first, and then you execute 
the recursive call, passing the results of your current step to the next 
recursive step. This results in the last statement being in the form of 
(return (recursive-function params)). 

Basically, the return value of any given recursive step is the same as the 
return value of the next recursive call.
"""
def sum_iter(term, lower, successor, upper):
    def iter(lower, result):
        if (lower > upper):
            return result
        else:
            return iter(successor(lower), result+term(lower))
    return iter(lower, 0)


"""
1.2
"""
def product_iter(term, lower, successor, upper):
    def iter(lower, result):
        if (lower > upper):
            return result
        else:
            return iter(successor(lower), result*term(lower))
    return iter(lower, 1)


def factorial(number):
    return product_iter(lambda n:n, 1, lambda n:n+1, number)


# Extra
def wallis(n):
    a = lambda s: (((4*(s**2))-1)/(4*(s**2)))
    b = lambda s: s+1
    wallis = product_iter(a, 1, b, n)
    pi = 2*(1/wallis)
    return pi


"""
1.3
"""
def accumulate(combiner, null, term, lower, succ, upper):
    pass


def accumulate_iter(combiner, null, term, lower, succ, upper):
    pass


"""
1.4
"""
def foldl(f, f0, data):
    def foldl_iter(data):
        if not data:
            return f0
        else:
            last = data[-1]
            data.remove(data[-1])
            return f(foldl_iter(data), last)
    return foldl_iter(data)


def foldr(f, f0, data):
    def foldl_iter(data):
        if not data:
            return f0
        else:
            first = data[0]
            data.remove(data[0])
            return f(first, foldl_iter(data))
    return foldl_iter(data)


def my_map(f, seq):
    g = lambda m,n: [n, m]
    return foldr(g, 0, seq)


def reverse_r(seq):
    pass

#print(my_map(lambda m,n:m+n, [1,2,3]))


"""
1.5

F: f(x) --> f^n(x)
"""
def repeat(f, n):
    if n == 0:
        return lambda n: 1
    def iter(n, result):
        if n == 1:
            return f
        else:
            return iter(n-1, f)
    return iter(n, f)

#print(repeat(lambda n:n*n, 0)(3))


def compose(f, g):
    return lambda x: f(g(x))

#print(compose(lambda n: n+1, lambda m: m*m)(2))


def repeated_application():
    pass


"""
1.6

Write a procedure smooth that takes f as input, and returns the smoothed 
version of f with dx=0.01.
"""
def smooth(f, dx):
    pass

"""
Write a procedure n fold smooth that takes f and n ≥ 0 as inputs and, 
using your repeat function, returns the n-fold smoothed version of f.
"""
def n_fold_smooth(f, n):
    pass


