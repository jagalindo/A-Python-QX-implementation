#!/bin/python3
import os
cc=["1","2","4","8","16"]
for i in cc:
    modelPath="./cnf/bench/model_"+i+".cnf"
    for j in range(10):
        productPath="./cnf/bench/prod-"+i+"-"+str(j)+".prod"
        for lmax in ["0","1","2"]:
            for solver in ["Glucose3","Sat4j","Choco4"]:
                for difficulty in ["0","300","400","500"]:
                    os.system("python3 ./qx.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " result.csv")
                    if not lmax == "0":
                        os.system("python3 ./qx_parallel_mp.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " result.csv")
