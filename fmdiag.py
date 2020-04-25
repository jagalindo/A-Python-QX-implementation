from pysat.formula import CNF
from pysat.solvers import Glucose3
import sys
def isConsistent(AC):
	g = Glucose3()
	for clause in AC:
		g.add_clause(clause)
	return g.solve()

def fmdiag(S, AC):
	print(S)
	print(AC)
	if len(S)==0 or not isConsistent(Diff(AC,S)):
		return []
	else:
		return diag([],S,AC)
	
def diag(D, S, AC):
	if len(D)!=0 and isConsistent(AC):
		return []
		
	if len(S)==1:
		return S
		
	k=int(len(S)/2)
	S1=S[0:k]
	S2=S[k:len(S)]
	A1=diag(S2,S1,Diff(AC,S2))
	A2=diag(A1,S2,Diff(AC,A1))
	return A1 + A2

def Diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 

model=sys.argv[1]
requirements=sys.argv[2]
outFile=sys.argv[3]

modelCNF = CNF(from_file=model)
requirementsCNF = CNF(from_file=requirements)

result= fmdiag(requirementsCNF.clauses, modelCNF.clauses + requirementsCNF.clauses)
resCNF= CNF()
for c in result:
	resCNF.append(c)
resCNF.to_file(outFile)
