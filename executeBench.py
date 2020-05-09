#!/bin/python3
import os
cc=["1","2","4","8","16"]
for i in cc:
    modelPath="./cnf/bench/model_"+i+".cnf"
    for j in range(10):
        productPath="./cnf/bench/prod-"+i+"-"+str(j)+".prod"
        #create product in cnf
        for lmax in ["1","2"] :
            os.system("python3 ./qx.py " + modelPath + " "+productPath+" "+lmax+" >>"+ " result.csv")
            os.system("python3 ./qx_parallel_mp.py " + modelPath + " "+productPath+" "+lmax+" >>"+ " result.csv")
