from pysat.solvers import Glucose3
import pickle as pickle
import sys


def getHash(C,l): 
    #print(str(C))
    #smallList=list(filter(lambda x: x[0] > l, C))
    C=sorted([i for i in C if i[0] >=l],key=lambda x: x[0])
    #p = pickle.dumps([i for i in C if i[0] >=l], -1)
    #return hash(p)
    return str(C)

def union(A,B):
    res=[]
    for X in A:
        res.extend(X)
    for X in B:
        res.extend(X)
    return res
    
def Diff(x, y): 
    li_dif = [item for item in x if item not in y]
    return li_dif

def consistencyCheck(AC):
    g = Glucose3()
    for clause in AC: #AC es conjunto de conjuntos
        g.add_clause(clause[1])#añadimos la constraint
    sol=g.solve()
    return sol

