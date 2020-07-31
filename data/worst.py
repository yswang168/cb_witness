# -*- coding: UTF-8 -*-
import subprocess
from generate_theory import generate_theory
import os,sys
import random
import re
import math
from run import to_dimacs

TEMP_THEORY = ".TEMP_THEORY_WORST_"
TEMP_MODEL  = ".TEMP_MODEL_WORST_" 
OUT_PUT = "OUT_PUT_WORST_"
time_out = 1800

def checkMin_worstcase(n):
    clauses = []
    Yes = False
    for i in range(2,n+1):
        clauses.append((set([1]),set([i])))
        clauses.append((set([i]),set([1])))
    clauses.append((set([i for i in range(2,n+1)]),set()))
    model = set([i for i in range(1, n+1)])
    with open(TEMP_MODEL, 'w') as f:
        f.write(' '.join(str(atom) for atom in model))
    with open(TEMP_THEORY, 'w') as f:
        f.write(to_dimacs(clauses, n, n))
    out = subprocess.check_output(["python3.7", "check_min.py", "-TT_PYSAT",TEMP_THEORY, TEMP_MODEL]).decode("ascii")
    os.system("cp "+TEMP_THEORY +" " + TEMP_MODEL + " /tmp")
    
    if out.find("YES") != -1:
        Yes = True
    return (Yes, float(out.split("\n")[0]))

def cbwitness_worstcase(n):
    clauses = []
    Yes = False
    for i in range(2,n+1):
        clauses.append((set([1]),set([i])))
        clauses.append((set([i]),set([1])))
    clauses.append((set([i for i in range(2,n+1)]),set()))
    model = set([i for i in range(1, n+1)])
    with open(TEMP_MODEL, 'w') as f:
        f.write(' '.join(str(atom) for atom in model))
    with open(TEMP_THEORY, 'w') as f:
        f.write(to_dimacs(clauses, n, n))
    os.system("cp "+TEMP_THEORY +" " + TEMP_MODEL + " /tmp")
    try:
        #out = subprocess.check_output(["python3.7", "cb_witness.py", "-q", "-v4", "-TT_PYSAT", "-MUS_Solver=picomus", TEMP_THEORY, TEMP_MODEL], timeout=time_out).decode("ascii")
        out = subprocess.check_output(["python3.7", "cb_witness.py", "-q", "-v4", "-TT_PYSAT",  TEMP_THEORY, TEMP_MODEL], timeout=time_out).decode("ascii")
    except subprocess.TimeoutExpired as e:
        return -1
    if out.find("YES") != -1:
        Yes = True
    #print(out)
    return (Yes, float(out.split("\n")[2].split(" ")[1]))

if __name__ == "__main__": 

    mc = False
    if len(sys.argv) > 3 and sys.argv[3] == "mc": # minimal model checking
        mc =True

    if len(sys.argv) >= 3: 
        lower = int(sys.argv[1])
        upper = int(sys.argv[2])
        OUT_PUT = OUT_PUT +  sys.argv[1] + "_" + sys.argv[2] +"_"

    TEMP_THEORY += str(os.getpid())
    TEMP_MODEL  += str(os.getpid()) 
    OUT_PUT += str(os.getpid())

    os.system("echo n	time > " + OUT_PUT)
    for n in range(lower, upper+1, 10):
        if not mc:
            Yes, time = cbwitness_worstcase(n) 
            s = str(n) + "	" + str(round(time,6))
            os.system("echo " + s + str(Yes) + "  >> " + OUT_PUT )
            print("{0} {1:6f} {2}".format(n,time,str(Yes)))
        else:
            Yes, time = checkMin_worstcase(n)
            s = str(n) + "	" + str(round(time,6))
            os.system("echo " + s + str(Yes) + " >> " + OUT_PUT)
            print("{0} {1:6f} {2}".format(n, time, str(Yes)))

        os.remove(TEMP_THEORY)
        os.remove(TEMP_MODEL)

