#!/bin/python3
import os
import time

starttime = time.time()
cc=["16","8","4","2","1"]

for i in cc:
    modelPath="./cnf/bench/model_"+i+".cnf"
    for j in range(3):
        productPath="./cnf/bench/prod-"+i+"-"+str(j)+".prod"
        for solver in ["Sat4j","Glucose3"]:    
            for lmax in ["4","3","2","1","0"]:
                    for difficulty in ["0","50","100"]:
                        os.system("python3 ./qx.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " result.csv")
                        if not lmax == "0":
                            os.system("python3 ./qx_parallel_mp.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " result.csv")

reqtime = time.time() - starttime
print("GlucoseSat4j time: "+str(reqtime))

for i in cc:
    modelPath="./cnf/bench/model_"+i+".cnf"
    for j in range(3):
        productPath="./cnf/bench/prod-"+i+"-"+str(j)+".prod"
        for solver in ["Choco4"]:    
            for lmax in ["4","3","2","1","0"]:
                    for difficulty in ["0","50","100"]:
                        os.system("python3 ./qx.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " result_choco4.csv")
                        if not lmax == "0":
                            os.system("python3 ./qx_parallel_mp.py " + modelPath + " "+productPath+" "+lmax+" "+solver+" "+difficulty+" >>"+ " result_choco4.csv")

reqtime = time.time() - starttime
print("Choco4 time: "+(reqtime))
