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
	global count
	count=count+1
	for _ in range(lmax):
		utils.getHash(AC,len(modelCNF.clauses))
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
	A2=QX(Ca,(B+Cb),Cb)
	A1=QX(Cb,(B+A2),A2)
	return (A1 + A2)

if __name__ == '__main__':

	if len(sys.argv) > 1:
		model=sys.argv[1]
		requirements=sys.argv[2]
		lmax=int(sys.argv[3])

	else :
		lmax=int(0)
		#requirements="../QX-Benchmark/cnf/betty/5000_30_0/16-50-4.prod"
		#model="../QX-Benchmark/cnf/betty/5000_30_0.cnf"
		#requirements="./cnf/AutomotiveRQ.cnf"		
		#requirements="./cnf/auto_fail.cnf"
		#model="./cnf/LargeAutomotive.dimacs"
		requirements="./cnf/bench/prod-2-3.prod"
		model="./cnf/bench/model_2.cnf"
		#requirements="./cnf/ecos-icse11.dimacs_prod"
		#model="./cnf/ecos-icse11.dimacs"
		#requirements="./cnf/TS/QX11_prod.cnf"
		#model="./cnf/TS/QX11.cnf"

	modelCNF = CNF(from_file=model)
	requirementsCNF = CNF(from_file=requirements)
	
	sleepTime=0 #can be used to simulate harder problems
	lockTime=0 #can be used to simulate harder problems
	
	M_C=sorted(enumerate(modelCNF.clauses), key=lambda x: x[0])
	RQ_C=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])
	#random.shuffle(RQ_C)
	starttime = time.time()
	result= quickXplain(RQ_C,M_C)
	reqtime = time.time() - starttime
	print(os.path.dirname(requirements)+"|"+os.path.basename(requirements)+"|"+str(reqtime)+"|"+str(count)+"|"+str(count)+"|"+str(lmax)+"|qx|"+str(result))
