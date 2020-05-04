from pysat.formula import CNF
from random import randint
from pysat.solvers import Glucose3

model="./cnf/bench/frb59-26-1.cnf"
modelCNF = CNF(from_file=model)
numberOfRequirements=10
hasSolution = True

def isConsistent(AC):
    g = Glucose3()
    for clause in AC:
        g.add_clause(clause)
    return g.solve()


while hasSolution:
    requirementsCNF = CNF()
    #for i in range(int(0.02*modelCNF.nv)):
    for i in range(numberOfRequirements):
        value = randint(1, modelCNF.nv)
        if(not (value in requirementsCNF)):
            requirementsCNF.append([value])	
    hasSolution= isConsistent(requirementsCNF.clauses + modelCNF.clauses)

requirementsCNF.to_file('./cnf/bench/frb59-26-1.cnf_prod')
