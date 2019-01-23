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
def product(term, lower, succ, upper):
    if lower > upper:
        return 1
    else:
        return term(lower) *\
            product(term, succ(lower), succ, upper)

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
    if lower > upper:
        return null
    else:
        return combiner(term(lower), accumulate(combiner, null, term, succ(lower), succ, upper))


def accumulate_iter(combiner, null, term, lower, succ, upper):
    def iter(lower, res):
        if lower > upper:
            return res
        else:
            return iter(succ(lower), combiner(res, term(lower)))
    return iter(lower, null)

def acc_sum(lower, upper):
    return accumulate_iter(lambda x,y:x+y, 0, lambda x:x, lower, lambda x:x+1, upper)

def acc_prod(lower, upper):
    return accumulate_iter(lambda x,y:x*y, 1, lambda x:x, lower, lambda x:x+1, upper)
"""
c)
Natural numbers
The combiner can not have diffrent answers in order of execution

Example below:
print (accumulate_iter(lambda x,y:x-y, 0, lambda x:x, 1, lambda x:x+1, 3), '\n')
print (accumulate(lambda x,y:x-y, 0, lambda x:x, 1, lambda x:x+1, 3), '\n')
"""



"""
1.4
"""
def foldl(f, f0, data):
    def foldl_iter(data):
        if not data:
            return f0
        else:
            return f(foldl_iter(data[:-1]), data[-1])
    return foldl_iter(data)


def foldr(f, f0, data):
    def foldl_iter(data):
        if not data:
            return f0
        else:
            return f(data[0], foldl_iter(data[1:]))
    return foldl_iter(data)


def my_map(f, seq):
    return foldl( lambda x,y:x+[f(y)], [], seq )

def reverse_r(seq):
    return foldr( lambda x,y:y+[x], [], seq)

def reverse_l(seq):
    return foldl( lambda x,y:[y]+x, [], seq)


"""
1.5
"""
def rep(f, n):
    if n > 0:
        return lambda x: f(rep(f,n-1)(x))
    else:
        return lambda x:x
#print(rep(lambda x:x*x, 2)(5))


def compose(f, g):
    return lambda x: f(g(x))
#print(compose(lambda n: n+3, lambda m: m*m)(2))

"""
b) Def(f) = Val(f) 
"""

def repeated_application(f, n):
    return accumulate(compose, lambda x:x, lambda x:f, 1, lambda x:x+1, n)
#print(repeated_application(lambda n:n**n, 2)(5))


"""
1.6
"""
def smooth(f):
    dx = 0.01
    return lambda x: (f(x-dx)+f(x)+f(x+dx))/3
#print(smooth(lambda x:x*x)(4))


def n_fold_smooth(f, n):
    return rep(smooth, n)(f)
#print(n_fold_smooth(lambda x:x*x, 5)(4))


"""
2.1
Applicative-order language all the arguments procedures are evaluated when 
the procedure is applied. In contrast, normal-order languages delay evaluation 
of procedure arguments until the actual argument values are needed.
Read more.
"""

"""
2.2
"""
x = 10
def f():
    print("In f: ", x)
def g(x):
    print("In g: ", x)
    f()
def keep_val(value):
    def f():
        print("--- x={0}, value={1}\n".format(x, value))
    return f
"""
a)
print_mess = keep_val("Stored")
value = "New and updated."
print_mess()
g(5000)
x = 0
g(5000)

b)
???

c)
Lexical scoping, (static scoping) --> Reach variabler declared in same block. 
Dynamic scoping --> Reach variables outside block, e.g. f reaches g´s scope.
Output:
--- x=10, value=New and Updated
('In g: ', 5000)
('In f: ', 5000)
('In g: ', 5000)
('In f: ', 5000)
"""


"""
2.3
"""


