# Signed connected bipartite weights n_{a,b} (unordered parts, labeled k-set)
# from the two-sort EGF: log(e^x + e^y - 1).  n_{a,b} = C(a+b,a)*c2s_{a,b} (/2 if a==b).
import sympy as sp
from math import comb
x,y=sp.symbols('x y')
D=sp.exp(x)+sp.exp(y)-1
L=sp.log(D)
ser=sp.series(sp.series(L,x,0,11).removeO(),y,0,11).removeO().expand()
def c2s(a,b):
    c=ser.coeff(x,a).coeff(y,b)
    return int(sp.factorial(a)*sp.factorial(b)*c)
def n_ab(a,b):
    k=a+b
    v=comb(k,a)*c2s(a,b)
    return v//2 if a==b else v
if __name__=="__main__":
    print("n_{1,1} (edge) =", n_ab(1,1), "(expect -1)")
    for (a,b) in [(1,2),(2,2),(1,3),(2,3),(3,3),(3,4),(2,5),(3,5),(4,4),(4,5),(5,5),(1,7),(2,6),(2,7),(3,6),(3,7)]:
        print(f"n_{{{a},{b}}} =", n_ab(a,b))
