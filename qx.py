from pysat.formula import CNF
from pysat.solvers import Glucose3
import sys


#---------------------------------------------------------

def isConsistent(AC):
	g = Glucose3()
	for clause in AC:
		g.add_clause(clause)
	return g.solve()


def quickXplain(C, B):
	if isConsistent(B + C):
		return "No Conflict"
	elif len(C)==0:
		return []
	else :
		return QX(C,B,[])
		
	
def QX(C,B,Bo):
	if len(Bo)!=0 and not isConsistent(B):
		return []
	
	if len(C) == 1:
		return C[0] //Devuelvo el primer elemento
		
	k=int(len(C)/2) 
	Ca=C[0:k]
	Cb=C[k:len(C)]
	A2=QX(Ca,B+Cb,Cb)
	A1=QX(Cb,B+A2,A2)
	return A1 + A2

def Diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 

model=sys.argv[1]
requirements=sys.argv[2]
outFile=sys.argv[3]

modelCNF = CNF(from_file=model)
requirementsCNF = CNF(from_file=requirements)

result= quickXplain(modelCNF.clauses, requirementsCNF.clauses)
resCNF= CNF()
for c in result:
	resCNF.append(c)
resCNF.to_file(outFile)
