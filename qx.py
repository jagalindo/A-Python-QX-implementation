from pysat.formula import CNF
import utils

import sys
import time
import os
import time
count=0

#---------------------------------------------------------

def callConsistencyCheck(AC):
	global count
	count=count+1
	sol=utils.consistencyCheck(AC)
	time.sleep(sleepTime)
	return sol


def quickXplain(C, B):
	if callConsistencyCheck(B + C):
		return "No Conflict"
	elif len(C)==0:
		return []
	else :
		return QX(C,B,[])
		
	
def QX(C,B,Bo):
	time.sleep(lockTime)
	if len(Bo)!=0 and not callConsistencyCheck(B):
		return []
	
	if len(C) == 1:
		return C 
		
	k=int(len(C)/2) 
	Ca=C[0:k]
	Cb=C[k:len(C)]
	A2=QX(Ca,B+Cb,Cb)
	A1=QX(Cb,B+A2,A2)
	return A1 + A2

if __name__ == '__main__':

	if len(sys.argv) > 1:
		model=sys.argv[1]
		requirements=sys.argv[2]

	else :
		requirements="../QX-Benchmark/cnf/betty/model-5000-50-1/model-5000-50-1-100-0.prod"
		model="../QX-Benchmark/cnf/betty/model-5000-50-1.cnf"
		#requirements="./cnf/AutomotiveRQ.cnf"
		#model="./cnf/LargeAutomotive.dimacs"
		#requirements="./cnf/bench/frb59-26-1.cnf_prod"
		#model="./cnf/bench/frb59-26-1.cnf"
		#requirements="./cnf/ecos-icse11.dimacs_prod"
		#model="./cnf/ecos-icse11.dimacs"
		#requirements="./cnf/bench/frb40-19-1.cnf_prod"
		#model="./cnf/bench/frb40-19-1.cnf"

	modelCNF = CNF(from_file=model)
	requirementsCNF = CNF(from_file=requirements)
	
	sleepTime=0 #can be used to simulate harder problems
	lockTime=0 #can be used to simulate harder problems
	
	M_C=sorted(enumerate(modelCNF.clauses), key=lambda x: x[0])
	RQ_C=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])
	starttime = time.time()
	result= quickXplain(RQ_C,M_C)
	reqtime = time.time() - starttime
	print(os.path.basename(requirements).replace(".prod","").replace("model-","").replace("-","|")+"|"+str(reqtime)+"|"+str(count)+"|"+str(count)+"|"+"qx|0|"+str(result))
