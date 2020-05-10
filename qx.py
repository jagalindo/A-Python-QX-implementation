from pysat.formula import CNF
import utils
import random
import sys
import time
import os
import time
count=0

#---------------------------------------------------------

def callConsistencyCheck(AC):
	global count,solver,difficulty
	count=count+1
	for _ in range(lmax):
		utils.getHash(AC,len(modelCNF.clauses))
	sol=utils.consistencyCheck(AC,solver,difficulty)
	return sol


def quickXplain(C, B):
	if callConsistencyCheck(B + C):
		return "No Conflict"
	elif len(C)==0:
		return []
	else :
		return QX(C,B,[])
		
	
def QX(C,B,Bo):
	if len(Bo)!=0 and not callConsistencyCheck(B):
		return []
	
	if len(C) == 1:
		return C 
		
	k=int(len(C)/2) 
	Ca=C[0:k]
	Cb=C[k:len(C)]
	A2=QX(Ca,(B+Cb),Cb)
	A1=QX(Cb,(B+A2),A2)
	return (A1 + A2)

if __name__ == '__main__':

	if len(sys.argv) > 1:
		model=sys.argv[1]
		requirements=sys.argv[2]
		lmax=int(sys.argv[3])
		solver=sys.argv[4]
		difficulty=int(sys.argv[5])

	else : #Default values
		lmax=int(0)
		requirements="./cnf/bench/prod-2-3.prod"
		model="./cnf/bench/model_2.cnf"
		solver="Sat4j"
		difficulty=int(0)

	modelCNF = CNF(from_file=model)
	requirementsCNF = CNF(from_file=requirements)
	
	M_C=sorted(enumerate(modelCNF.clauses), key=lambda x: x[0])
	RQ_C=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])
	starttime = time.time()
	result= quickXplain(RQ_C,M_C)
	reqtime = time.time() - starttime
	print(model+"|"+requirements+"|"+str(reqtime)+"|"+str(count)+"|"+str(count)+"|"+str(lmax)+"|qx|"+solver+"|"+str(difficulty)+"|"+str(result))
