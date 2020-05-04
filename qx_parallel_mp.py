from pysat.formula import CNF
import multiprocessing as mp
import utils
import sys
import time
import os

#-------------------------------------------------------
#------------Auxiliary functions definition-------------
#-------------------------------------------------------
# Function to create a hash. 


def LookUpCC(C):
	global cache,count
	result=cache.get(utils.getHash(C,len(modelCNF.clauses)))
	if result.ready() :
		count=count+1
	return result.get()

def existConsistencyCheck(C):
	return (utils.getHash(C,len(modelCNF.clauses)) in cache)

#-------------------------------------------------------
#------------Auxiliary Parallel functions definition-------------
#-------------------------------------------------------

def callConsistencyCheck(AC):
	sol=utils.consistencyCheck(AC)
	time.sleep(sleepTime)
	return sol

def f(AC):
	res=0
	for C in AC:
		res=res+len(C)
	return res
#-------------------------------------------------------
#-----------------QX functions definition---------------
#-------------------------------------------------------

def inconsistent(C,B,Bd):
	if not existConsistencyCheck(B):
		QXGen([C],[Bd],[utils.Diff(B,Bd)],[Bd],0)
		time.sleep(lockTime)
	return (not LookUpCC(B)) #check the shared table
	
def quickXplain(C, B):

	if utils.consistencyCheck(C+B):
		return "No Conflict"
	elif len(C)==0:
		return []
	else :
		return QX(C,B,[])
		
	
def QX(C,B,Bo):
	if len(Bo)!=0 and inconsistent(C,B,Bo):
		return []
	
	if len(C) == 1:
		return C
		
	k=int(len(C)/2) 
	Ca=C[0:k]
	Cb=C[k:len(C)]
	A2=QX(Ca,B+Cb,Cb)
	A1=QX(Cb,B+A2,A2)
	return A1 + A2


def QXGen(C, Bd, B, d, l):
	if l< lmax :
		if f(d)>0 :
			u=utils.union(B,Bd)
			hash=utils.getHash(u,len(modelCNF.clauses))
			if (not (hash in cache)):#evito crear multiples hilos si ya esta en ejecución 
				future=pool.apply_async(callConsistencyCheck,args=([u]))
				cache.update({hash:future})
	
		if f(C)==1 and f(Bd)>0:
			QXGen(Bd,[],B+[C[0]],[C[0]],l+1)
		
		elif f(C)>1 :
			if(len(C)>1):
				k=int(len(C)/2) 
				Ca=C[0:k]
				Cb=C[k:len(C)]
			else :
				k=int(len(C[0])/2) 
				Ca=[C[0][0:k]]
				Cb=[C[0][k:len(C[0])]]
			QXGen(Ca,Cb + Bd,B,Cb,l+1)
		if f(Bd)>0 and f(d)>0  :
			QXGen([Bd[0]],utils.Diff(Bd,[Bd[0]]),B,[],l+1)



#-------------------------------------------------------
#--------------Gloval variable definition---------------
#-------------------------------------------------------
if __name__ == '__main__':
	lmax=1
	cache={}
	count=0
	
	sleepTime=0 #can be used to simulate harder problems
	lockTime=0 #can be used to simulate harder problems

	if len(sys.argv) > 1:
		model=sys.argv[1]
		requirements=sys.argv[2]
		lmax=int(sys.argv[3])
	else:
		requirements="../QX-Benchmark/cnf/betty/model-5000-50-1/model-5000-50-1-100-0.prod"
		model="../QX-Benchmark/cnf/betty/model-5000-50-1.cnf"
		requirements="./cnf/AutomotiveRQ.cnf"
		model="./cnf/LargeAutomotive.dimacs"
		#requirements="./cnf/bench/frb59-26-1.cnf_prod"
		#model="./cnf/bench/frb59-26-1.cnf"

	modelCNF = CNF(from_file=requirements)
	requirementsCNF = CNF(from_file=model)

	#Vamos a almacenar el id con la C
	B=sorted(enumerate(modelCNF.clauses,0), key=lambda x: x[0])
	C=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])

	pool = mp.Pool(mp.cpu_count()-1)
	starttime = time.time()
	result= quickXplain(C,B)
	reqtime = time.time() - starttime
	print(os.path.basename(requirements).replace(".prod","").replace("model-","").replace("-","|")+"|"+str(reqtime)+"|"+str(count+1)+"|"+str(len(cache)+1)+"|"+"qx_parallel_mp|"+str(lmax)+"|"+str(result))
	pool.close()
