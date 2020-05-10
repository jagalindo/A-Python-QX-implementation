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


def LookUpCC(hash):
	global cache,count
	result=cache.get(hash)
	#print("Pido: "+str(hash))
	if result.ready() :
		count=count+1
	return result.get()

def existConsistencyCheck(hash):
	return (hash in cache)

#-------------------------------------------------------
#------------Auxiliary Parallel functions definition-------------
#-------------------------------------------------------

def callConsistencyCheck(AC):
	global solver, difficulty
	sol=utils.consistencyCheck(AC,solver,difficulty)
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
	global genhash
	genhash=hashB=utils.getHash(B,len(modelCNF.clauses))
	if not existConsistencyCheck(hashB):
		QXGen([C],[Bd],[utils.Diff(B,Bd)],[Bd],0)
	return (not LookUpCC(hashB)) #check the shared table
	
def quickXplain(C, B):
	global solver, difficulty
	if utils.consistencyCheck(C+B,solver, difficulty):
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
	global genhash
	if l< lmax :
		if f(d)>0 :
			u=utils.union(B,Bd)
			if(genhash == ""):
				hash=utils.getHash(u,len(modelCNF.clauses))
			else:
				hash=genhash
				genhash=""

			if (not (hash in cache)):#evito crear multiples hilos si ya esta en ejecución 
				future=pool.apply_async(callConsistencyCheck,args=([u]))
				cache.update({hash:future})
				#print("Genero: "+str(hash))
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
	lmax=2
	cache={}
	count=0
	genhash=""

	if len(sys.argv) > 1:
		model=sys.argv[1]
		requirements=sys.argv[2]
		lmax=int(sys.argv[3])
		solver=sys.argv[4]
		difficulty=sys.argv[5]
		difficulty=int(sys.argv[5])
	else:
		lmax=int(0)
		requirements="./cnf/bench/prod-2-3.prod"
		model="./cnf/bench/model_2.cnf"
		solver="Sat4j"
		difficulty=int(0)

	modelCNF = CNF(from_file=model)
	requirementsCNF = CNF(from_file=requirements)

	#Vamos a almacenar el id con la C
	B=sorted(enumerate(modelCNF.clauses,0), key=lambda x: x[0])
	C=sorted(enumerate(requirementsCNF.clauses,len(modelCNF.clauses)), key=lambda x: x[0])

	pool = mp.Pool(mp.cpu_count())
	starttime = time.time()
	result= quickXplain(C,B)
	reqtime = time.time() - starttime
	print(model+"|"+requirements+"|"+str(reqtime)+"|"+str(count+1)+"|"+str(len(cache))+"|"+str(lmax)+"|pqx|"+solver+"|"+str(difficulty)+"|"+str(result))
	pool.close()
	pool.terminate()