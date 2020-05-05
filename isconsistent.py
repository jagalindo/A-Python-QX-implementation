from pysat.formula import CNF
from pysat.solvers import Glucose3

import utils
import random
import sys
import time
import os
import time

def consistencyCheck(AC):
    g = Glucose3()
    for clause in AC: #AC es conjunto de conjuntos
        g.add_clause(clause)#añadimos la constraint
    sol=g.solve()
    return sol

requirements="./cnf/auto_fail.cnf"
model="./cnf/LargeAutomotive.dimacs"
modelCNF = CNF(from_file=model)
requirementsCNF = CNF(from_file=requirements)
res=consistencyCheck(modelCNF.clauses+requirementsCNF.clauses)
print(res)