from pysat.formula import CNF
from pysat.solvers import Glucose3
import sys

#-------------------------------------------------------

def Diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 
	
def isConsistent(AC):
	g = Glucose3()
	for clause in AC:
		g.add_clause(clause)
	return g.solve()

def inconsistent(C,B,Bo):

	if not existConsistencyCheck(b):
	
		QXGen(C,Bo,Diff(B,Bo),Bo,0)
	
	return (not LookUp(B)) //check the shared table
	
def QXGen(C, Bo, B, o, l):

	if l< lmax :
		AddCC(Bd + B)//asincronous call to ask for that consistency check
		
	if len(C)==1 and len(Bo)>0:
		QXGen(Bo,[],B+C[0],C[0],l+1)
		
	elif len(C)>1 :
		k=int(len(C)/2) 
		Ca=C[0:k]
		Cb=C[k:len(C)]
		QXGen(Ca,Cb + B[0],B,Cb,l+1)

	if len(Bo>0) and len(o)>0  :
		QXGen(Bo[0],Diff(Bo,Bo[0]),[],l+1)
		
#-------------------------------------------------------

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
