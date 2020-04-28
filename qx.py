from pysat.formula import CNF
from pysat.solvers import Glucose3
import sys
import time
modelCNFClauses=[]


#---------------------------------------------------------
def l2s(C):  
	return str(Diff(C,modelCNFClauses))

def isConsistent(AC):
	print(l2s(AC))
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
		return C 
		
	k=int(len(C)/2) 
	Ca=C[0:k]
	Cb=C[k:len(C)]
	A2=QX(Ca,B+Cb,Cb)
	A1=QX(Cb,B+A2,A2)
	return A1 + A2

def Diff(x, y): 
	li_dif = [item for item in x if item not in y]
	#li_dif = [i for i in x + y if i not in x or i not in y] 
	return li_dif 

#model=sys.argv[1]
#requirements=sys.argv[2]
#outFile=sys.argv[3]

model="./cnf/TS/QX33.cnf"
requirements="./cnf/TS/QX33_prod.cnf"
outFile="./out.txt"

modelCNF = CNF(from_file=model)
requirementsCNF = CNF(from_file=requirements)
modelCNFClauses=modelCNF.clauses
starttime = time.time()
result= quickXplain(requirementsCNF.clauses,modelCNF.clauses)
reqtime = time.time() - starttime
print(reqtime)

print(result)
