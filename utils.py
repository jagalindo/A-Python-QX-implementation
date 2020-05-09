from pysat.solvers import Glucose3
import pickle as pickle
import sys
import os
import tempfile
from pysat.formula import CNF
import time

def getHash(C,l): 
    C=sorted([i for i in C if i[0] >=l],key=lambda x: x[0])
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

def consistencyCheck(AC,solver,difficulty):
    if solver == "Sat4j":
        f = tempfile.NamedTemporaryFile()
        cnf = CNF()
        for clause in AC: #AC es conjunto de conjuntos
            cnf.append(clause[1])#añadimos la constraint
        cnf.to_file(f.name)
        starttime = time.time()
        out=os.popen("java -jar org.sat4j.core.jar "+f.name).read()
        f.close()
        reqtime = time.time() - starttime
        time.sleep(reqtime*difficulty)
        if "UNSATISFIABLE" in out:
            return False
        else:
            return True
        
    elif solver == "Glucose3":
        g = Glucose3()
        for clause in AC: #AC es conjunto de conjuntos
            g.add_clause(clause[1])#añadimos la constraint
        starttime = time.time()
        sol=g.solve()
        reqtime = time.time() - starttime
        time.sleep(reqtime*difficulty)
        return sol
    elif solver == "Choco":
        raise ValueError("Choco Solver not defined")
    else :
        raise ValueError("Solver not defined")
    
