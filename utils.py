from pysat.solvers import Glucose3
import pickle as pickle
import sys
import os
import tempfile
from pysat.formula import CNF
import time
def getHash(C,l): 
    #print(str(C))
    #smallList=list(filter(lambda x: x[0] > l, C))
    C=sorted([i for i in C if i[0] >=l],key=lambda x: x[0])
    #C=sorted(C,key=lambda x: x[0])
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

#def consistencyCheck(AC):
#    g = Glucose3()
#    for clause in AC: #AC es conjunto de conjuntos
#        g.add_clause(clause[1])#añadimos la constraint
#    sol=g.solve()
#    return sol

def consistencyCheck(AC):
    f = tempfile.NamedTemporaryFile()
    cnf = CNF()
    for clause in AC: #AC es conjunto de conjuntos
        cnf.append(clause[1])#añadimos la constraint
    cnf.to_file(f.name)
    starttime = time.time()
    out=os.popen("java -jar org.sat4j.core.jar "+f.name).read()
    f.close()
    reqtime = time.time() - starttime
    #print(str(reqtime*10))
    time.sleep(reqtime*10)
    if "UNSATISFIABLE" in out:
        return False
    else:
        return True
    
