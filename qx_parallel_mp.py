from pysat.formula import CNF
from pysat.solvers import Glucose3
import multiprocessing as mp
import sys
import time

#-------------------------------------------------------
#------------Auxiliary functions definition-------------
#-------------------------------------------------------
# Function to create a hash. 
def l2s(C): 
	global modelCNFClauses
	clauses=Diff(C,modelCNFClauses)
	results= sorted(clauses, key=sub)
	return str(results)

def sub(C): return C[0]

def Diff(x, y): 
	li_dif = [item for item in x if item not in y]
	#li_dif = [i for i in x + y if i not in x or i not in y] 
	return li_dif 

def LookUpCC(C):
	global cache
	result=cache.get(l2s(C))
	return result.get()

def existConsistencyCheck(C):
	return (l2s(C) in cache)

#-------------------------------------------------------
#------------Auxiliary Parallel functions definition-------------
#-------------------------------------------------------

def consistencyCheck(AC):
	g = Glucose3()
	for clause in AC: #AC es conjunto de conjuntos
		g.add_clause(clause)
	return g.solve()



#def AddCC(result):
#	global cache
#	print(result)
#	cache.update(result)

#-------------------------------------------------------
#-----------------QX functions definition---------------
#-------------------------------------------------------

def inconsistent(C,B,Bo):
	if not existConsistencyCheck(B):
		QXGen(C,Bo,Diff(B,Bo),Bo,0)
	return ( not LookUpCC(B)) #check the shared table
	
def quickXplain(C, B):
	if consistencyCheck(B + C):
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

def QXGen(C, Bd, B, o, l):
	if l< lmax :
		if len(o)>0 :
			#launch mp of the consistency and store with a callback func
			#pool.apply_async(consistencyCheckParallel,args=([Bd+B]),callback=AddCC)
			global l2s
			union=Bd+B
			hash=l2s(union)
			future=pool.apply_async(consistencyCheck,args=([union]))
			cache.update({hash:future})
	if len(C)==1 and len(Bd)>0:
		QXGen(Bd,[],B+[C[0]],C[0],l+1)
		
	elif len(C)>1 :
		k=int(len(C)/2) 
		Ca=C[0:k]
		Cb=C[k:len(C)]
		QXGen(Ca,Cb + Bd,B,Cb,l+1)

	if len(Bd)>0 and len(o)>0  :
		QXGen([Bd[0]],Diff(Bd,[Bd[0]]),B,[],l+1)
		
#-------------------------------------------------------
#--------------Gloval variable definition---------------
#-------------------------------------------------------
lmax=1
cache={}

#model=sys.argv[1]
#requirements=sys.argv[2]
#outFile=sys.argv[3]

model="./cnf/TS/QX33.cnf"
requirements="./cnf/TS/QX33_prod.cnf"
outFile="./out.txt"


modelCNF = CNF(from_file=model)
requirementsCNF = CNF(from_file=requirements)
modelCNFClauses=modelCNF.clauses
pool = mp.Pool(mp.cpu_count()-1)
starttime = time.time()
result= quickXplain(requirementsCNF.clauses,modelCNF.clauses)
reqtime = time.time() - starttime

pool.close()
pool.join()
#time.sleep(10)
print(len(cache))
print (result)
print(reqtime)
