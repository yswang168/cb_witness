# -*- coding: UTF-8 -*-
import subprocess
from generate_theory import generate_theory
import os,sys
import random
import re
import math
 
from min_model_a import get_min_model

latex = []
TEMP_THEORY = ".TEMP_THEORY_"
TEMP_MODEL  = ".TEMP_MODEL_"
TEMP_MIN_MODEL = ".TEMP_MIN_MODEL_"
TEMP_DLV = ".TEMP_DLV_"
TEMP_CLASP = ".TEMP_CLASP_"
SAT_INPUT = ".TEMP_SAT_INPUT_"
OUT_PUT = "OUT_PUT_"
OUT_PUT_MIN = "OUT_PUT_MIN_"
ATOM_PRE = "p_"
steps = list()
time_out = 1800
COMPUT_MINIMAL_MODEL=False #True

### Yisong
def generate_clasp_maps(a:'int'):
    to_dlv_map = {}
    from_dlv_map = {}
    for i in range(1, a+1):
        s = ATOM_PRE + str(i)
        to_dlv_map[i] = s
        from_dlv_map[s] = i
    return (to_dlv_map, from_dlv_map)

def to_clasp(clauses, to_clasp_map):
    strings = []
    for head, body in clauses:
        strings.append(" | ".join(to_clasp_map[atom] for atom in head))
        if len(body) > 0:
            strings.append(" :- ")
            strings.append(" , ".join(to_clasp_map[atom] for atom in body))
        strings.append(".\n")
    return ''.join(strings)

def get_clasp_minmodel(clauses, ATOMS):
    to_clasp_map, from_clasp_map = generate_clasp_maps(ATOMS)
    clasp = to_clasp(clauses, to_clasp_map)
    with open(TEMP_CLASP, 'w') as f:
        f.write(clasp)
        f.close()
    line = None 
     
    try:
       line = subprocess.check_output(["clingo", "--models=1", "--verbose=0", "--quiet=1", "--warn=no-atom-undefined", TEMP_CLASP],timeout=None).decode("ascii") 
    except subprocess.TimeoutExpired as e: 
        return None
    except subprocess.CalledProcessError as e:
        line = str(e.output)
        if line.find("UNSATISFIABLE") != -1: return None
        line = line.strip("b'").split("\\")[0] 
    if line == "" or line == None :
        return None ## no answer set
    else: 
        return [from_clasp_map[x.strip(" ")] for x in filter(None, line.split(" "))]
        #return [from_clasp_map[x.strip(" ")] for x in filter(None, line.strip("}{\n\r").split(","))]
### ----------------------

def generate_dlv_maps(a):
    to_dlv_map = {}
    from_dlv_map = {}
    for i in range(1, a+1):
        x = i
        s = ""
        while x > 0:
            s += chr(x%26 + ord('a'))
            x//=26
        to_dlv_map[i] = s
        from_dlv_map[s] = i
    return (to_dlv_map, from_dlv_map)

def to_dlv(clauses, to_dlv_map):
    strings = []
    for head, body in clauses:
        strings.append(" v ".join(to_dlv_map[atom] for atom in head))
        strings.append(" :- ")
        strings.append(" , ".join(to_dlv_map[atom] for atom in body))
        strings.append(".\n")
    return ''.join(strings)

def to_dimacs(clauses, ATOMS, CLAUSES):
    strings = []
    strings.append("c average clause length: {0}".format(sum(len(x[0])+len(x[1]) for x in clauses) / len(clauses)))
    strings.append("\n")
    strings.append("c average head length: {0}".format(sum(len(x[0]) for x in clauses) / len(clauses)))
    strings.append("\n")
    strings.append("p cnf {0} {1}".format(ATOMS, CLAUSES))
    strings.append("\n")

    for head, body in clauses:
        for atom in head:
            strings.append(str(atom))
            strings.append(" ")
        for atom in body:
            strings.append(str(-atom))
            strings.append(" ")
        strings.append("0\n")
    return ''.join(strings)

def generate_sat_input(clauses, ATOMS, CLAUSES, minmodels=None):
    satinput = [to_dimacs(clauses, ATOMS, CLAUSES)]
    all_atoms = set([x for x in range(1, ATOMS+1)])
    i = 0
    if minmodels == None:
        minmodels = []
    for model in minmodels:
        satinput.append(' '.join([str(-atom) for atom in model]))
        satinput.append(' ')
        leftatoms = all_atoms.difference(set(model))
        satinput.append(' '.join([str(atom) for atom in leftatoms]))
        satinput.append(' 0\n')
        i += 1
    satinput[0] = re.sub("p cnf .*\n", "p cnf {0} {1}\n".format(ATOMS, CLAUSES+i), satinput[0])
    return ''.join(satinput)

def calcminmodels(clauses, ATOMS):
    to_dlv_map, from_dlv_map = generate_dlv_maps(ATOMS)
    dlv = to_dlv(clauses, to_dlv_map)
    with open(TEMP_DLV, 'w') as f:
        f.write(dlv)
    dlvout = subprocess.check_output(["dlv", "-silent", TEMP_DLV]).decode("ascii")
    minmodels = []
    for line in dlvout.strip().split("\n"):
        if line == "":
            break
        minmodels.append([from_dlv_map[x.strip(" ")] for x in filter(None, line.strip("}{\n\r").split(","))])
        if len(minmodels) == 0:
            continue
    return minmodels

def generate_tempmodel(satinput):
    with open(SAT_INPUT, 'w') as f:
            f.write(''.join(satinput))
    try:
        # weird exit status
        subprocess.check_output(["minisat", SAT_INPUT, TEMP_MODEL],timeout=time_out)
    except subprocess.CalledProcessError as e:
        pass
    except subprocess.TimeoutExpired as t:
        return None
    with open(TEMP_MODEL, 'r') as f:
        model = f.read().replace('\n', '')
        #print(model)
    if "UNSAT" in model:
        # we want theories with models that do not have minimal models            
        return "UNSAT"
    model = model.replace("SAT", "")
    model = [int(x) for x in model.split() if int(x) > 0]
    with open(TEMP_MODEL, 'w') as f:
        f.write(' '.join(str(atom) for atom in model))
    return model

def checkMin_worstcase(n):
    clauses = []
    for i in range(1,n):
        clauses.append((set([i]),set([i+1])))
    clauses.append((set([n]), set([1])))
    model = set([i for i in range(1, n+1)])
    with open(TEMP_MODEL, 'w') as f:
        f.write(' '.join(str(atom) for atom in model))
    with open(TEMP_THEORY, 'w') as f:
        f.write(to_dimacs(clauses, n, n))
    out = subprocess.check_output(["python3", "check_min.py", TEMP_THEORY, TEMP_MODEL]).decode("ascii")
    return float(out.split("\n")[0])

def cbwitness_worstcase(n):
    clauses = []
    for i in range(2,n+1):
        clauses.append((set([1]),set([i])))
        clauses.append((set([i]),set([1])))
    clauses.append((set([i for i in range(2,n+1)]),set()))
    model = set([i for i in range(1, n+1)])
    with open(TEMP_MODEL, 'w') as f:
        f.write(' '.join(str(atom) for atom in model))
    with open(TEMP_THEORY, 'w') as f:
        f.write(to_dimacs(clauses, n, n))
    out = subprocess.check_output(["python3", "cb_witness.py", "-v2", TEMP_THEORY, TEMP_MODEL]).decode("ascii")
    #print(out)
    return float(out.split("\n")[0])
    
def get_random_minmodel(clauses, ATOMS):
    to_dlv_map, from_dlv_map = generate_dlv_maps(ATOMS)
    dlv = to_dlv(clauses, to_dlv_map)
    with open(TEMP_DLV, 'w') as f:
        f.write(dlv)
    try:
        dlvout = subprocess.check_output(["dlv", "-n=1", "-silent", TEMP_DLV],timeout=None).decode("ascii") ### Yisong, change for linux
    except subprocess.TimeoutExpired as e:
        return None

    line = dlvout
    if line == "": ## no answer set
        return None
    else:
        return [from_dlv_map[x.strip(" ")] for x in filter(None, line.strip("}{\n\r").split(","))]

# add a test for computing minimal model for comparison
# minimal, dlv, clingo

def test_v4(CLAUSES, ATOMS, CLAUSE_LENGTH, HEAD_PROPORTION, fixclauselen = False, MIN_MODEL=0, MIN_CHECK=False):
    # MIN_MODEL = 0 : cadical
    # MIN_MODEL = 1 : clasp
    # MIN_MODEL = 2 : dlv
    # MIN_CHECK: do minimal model checking or nor
    sum_time1 = 0.0 
    sum_time2 = 0.0
    NON_MIN_MODEL = 0
    sum_minmodlen = 0
    t = 20
    tinitial = t
    out_of_times = 0 ### Yisong
    sat_dlv_out_of_times = 0
    if COMPUT_MINIMAL_MODEL:
        check_mm = 20
    else:
        check_mm = 0

    head_2 = 0.0 
    ration =  round(CLAUSES / ATOMS,1)
    while t > 0:   
        clauses = generate_theory(CLAUSES, ATOMS, CLAUSE_LENGTH, HEAD_PROPORTION, cl_std_derivation=0)
        minmodels = []
        satinput = generate_sat_input(clauses, ATOMS, CLAUSES, minmodels)
        '''
        if MIN_MODEL == 1 or MIN_MODEL == 2:
            model = generate_tempmodel(satinput)
            if model == "UNSAT": continue
            if model == None: 
                t -= 1
                sat_dlv_out_of_times += 1
                continue
            if MIN_MODEL == 1:
                rand_minmodel = get_clasp_minmodel(clauses, ATOMS)  # by clingo
            else:
                rand_minmodel = get_random_minmodel(clauses, ATOMS) # by dlv
            if rand_minmodel == None: 
                t -= 1
                sat_dlv_out_of_times += 1
                continue
            '''
        if MIN_MODEL == 1:
            rand_minmodel = get_clasp_minmodel(clauses, ATOMS)  # by clingo
        elif MIN_MODEL == 2:
            rand_minmodel = get_random_minmodel(clauses, ATOMS) # by dlv
        elif MIN_MODEL == 0: # cadical
            T_File = ".TEMP_SAT_FILE_" + str(os.getpid())
            with open(T_File,"w") as f:
                f.write(satinput)
                f.close()
            rand_minmodel = get_min_model(T_File) #,SAT_SOLVER="minimal")  # by cadical in default
            os.remove(T_File)
        if rand_minmodel == None: 
            sat_dlv_out_of_times += 1
            continue
        sum_minmodlen += len(rand_minmodel)

        if COMPUT_MINIMAL_MODEL: 
                t -= 1
                continue
         
        with open(TEMP_MIN_MODEL, 'w') as f:
            f.write(" ".join(str(atom) for atom in rand_minmodel))
        with open(TEMP_THEORY, 'w') as f:
            f.write(to_dimacs(clauses, ATOMS, CLAUSES))

        out = subprocess.check_output(["python3", "cb_witness.py", "-v4", "-TT_PYSAT", "-q", "-MUS_Solver=picomus", TEMP_THEORY, TEMP_MIN_MODEL], timeout = time_out).decode("ascii")
        '''
        The output looks like the below:
        YES
        1 clauses have head size >=2
        Time: 0.066 (s)
        Memory: 16.539 (M)
        '''
        if not "Out of time." in out:
            out = out.split("\n") #[2].split(" ")
            sum_time1 += float(out[2].split(" ")[1])  
            
            #if (int(out[len(out)-2]) > 0): # keep this theory and its minimal model
                # os.system("cp "+TEMP_THEORY + " " + TEMP_MIN_MODEL + " /tmp")
                ## just for fun to keep those interesting examples
            head_2 += int(out[1].split(" ")[0]) # the number of clauses with head size >= 2.
                #print("got! {0}".format(head_2))
            check_mm += 1 ### checked minimal models
        else:
            out_of_times += 1
        ## For minimal model checking
        if MIN_CHECK:            
            out = subprocess.check_output(["python3", "check_min.py",  "-TT_PYSAT", TEMP_THEORY, TEMP_MIN_MODEL]).decode("ascii")
            out = out.split("\n")
            sum_time2 += float(out[0]) 
            if out[1].find("NO") != -1:
                NON_MIN_MODEL += 1
        t -= 1 

    #w_str_mc = str(k) + " " + str(ration) + " " + str(round(sum_time2/20,6)) + " " + str(NON_MIN_MODEL)
    #os.system("echo "+w_str_mc + " >> " + OUT_PUT_MIN)
    ## latex.append((k, sum_time1/(tinitial-out_of_times), 0, out_of_times)) 
    w_str = str(k) + " " + str(ration) + " " + str(round(sum_time1/check_mm,6)) + " "+ str(sat_dlv_out_of_times) + " " + str(out_of_times) + " " + str(round(head_2/check_mm,3))
    os.system("echo " + w_str + " >> " + OUT_PUT)
 
    if check_mm > 0:
        print("{0} {1} {2:6f} {3} {4} {5:2f}".format(k, ration, round(sum_time1/check_mm,6),  sat_dlv_out_of_times, out_of_times, round(head_2/check_mm,3)))
    else:
        print("{0}  {1:2f} {2} {3} {4} {5:2f}".format(k, ration, 0, sat_dlv_out_of_times, out_of_times,round(head_2/check_mm,3)))


def test(CLAUSES, ATOMS, CLAUSE_LENGTH, HEAD_PROPORTION, cb, minmod, k, useminmodels, fixclauselen = False):
    sum_time1 = 0
    sum_time2 = 0
    sum_time3 = 0
    sum_modlen = 0
    sum_minmodlen = 0
    t = 20
    tinitial = t
    out_of_times = 0 ### Yisong
    while t>0:   
        # get random theory
        if fixclauselen:
            clauses = generate_theory(CLAUSES, ATOMS, CLAUSE_LENGTH, HEAD_PROPORTION, cl_std_derivation=0)
        else:
            clauses = generate_theory(CLAUSES, ATOMS, CLAUSE_LENGTH, HEAD_PROPORTION)
        
        # generate all minimal models
        minmodels = []
        if useminmodels:
            minmodels = calcminmodels(clauses, ATOMS)
        
        satinput = generate_sat_input(clauses, ATOMS, CLAUSES, minmodels)
        model = generate_tempmodel(satinput)
        if model == "UNSAT":
            continue
        sum_modlen += len(model)
        if minmod or minmod=="BOTH":
            rand_minmodel = get_random_minmodel(clauses, ATOMS)
            sum_minmodlen += len(rand_minmodel)
            with open(TEMP_MIN_MODEL, 'w') as f:
                f.write(" ".join(str(atom) for atom in rand_minmodel))
        with open(TEMP_THEORY, 'w') as f:
            f.write(to_dimacs(clauses, ATOMS, CLAUSES))
 

        #print(' '.join(map(str, filter(lambda x: x>0, atoms))))
        if cb and minmod in (True, "BOTH"):
            out = subprocess.check_output(["python3", "cb_witness.py", "-v2", "-TT_OLD", "-REDUCE",  TEMP_THEORY, TEMP_MIN_MODEL]).decode("ascii")
            sum_time1 += float(out.split("\n")[0])
            #print(out)
            assert(out.split("\n")[1] == "YES")
            out = subprocess.check_output(["python3", "cb_witness.py", "-v2", "-TT_OLD", TEMP_THEORY, TEMP_MIN_MODEL]).decode("ascii")
            #print(out)
            sum_time2 += float(out.split("\n")[0])

        if not cb and minmod in (True, "BOTH"):
            out = subprocess.check_output(["python3", "check_min.py", TEMP_THEORY, TEMP_MIN_MODEL]).decode("ascii")
            sum_time1 += float(out.split("\n")[0])
            #print(out.split("\n")[1], end=" ")
        if cb and minmod in (False, "BOTH"):
            out = subprocess.check_output(["python3", "cb_witness.py", "-orig", TEMP_THEORY, TEMP_MODEL]).decode("ascii")
            #print(out)
            assert(out.split("\n")[1] == "NO")
            

            sum_time1 += float(out.split("\n")[0])
            #out = subprocess.check_output(["python3", "cb_witness.py", "-v2", TEMP_THEORY, TEMP_MODEL]).decode("ascii")
            #sum_time2 += float(out.split("\n")[0])
        if not cb and minmod in (False, "BOTH"):
            out = subprocess.check_output(["python3", "check_min.py", TEMP_THEORY, TEMP_MODEL]).decode("ascii")      
            sum_time2 += float(out.split("\n")[0])
        
        '''if k <= 40:
            out = subprocess.check_output(["python3", "is_min_model.py", TEMP_THEORY, TEMP_MODEL]).decode("ascii")
            sum_time3 += float(out.split("\n")[0])'''
        t-=1
       
    latex.append((k, sum_time1/tinitial, sum_time2/tinitial))
    if sum_modlen > 0:
        print("modlen: ", sum_modlen/tinitial)
    if sum_minmodlen > 0:
        print("minmodlen: ", sum_minmodlen/tinitial)
    print(k, sum_time1/tinitial, sum_time2/tinitial)

def testsatcomp(file):
    with open(file, "r") as f:
        content = f.read()
    with open(TEMP_THEORY, "w") as f:
        f.write(content)

    try:
        # weird exit status
        subprocess.check_output(["minisat", TEMP_THEORY, TEMP_MODEL])
    except:
        pass
    with open(TEMP_MODEL, 'r') as f:
        model = f.read().replace('\n', '')
    model = model.replace("SAT", "")
    model = [int(x) for x in model.split() if int(x) > 0]
    with open(TEMP_MODEL, 'w') as f:
        f.write(' '.join(str(atom) for atom in model))
    print(len(model))
    try:
        out = subprocess.check_output(["python3", "check_min.py", TEMP_THEORY, TEMP_MODEL], timeout=120).decode("ascii")     
    except Exception as e:
        print(e)
        return
    print(out)

if __name__ == "__main__": 
    k = 2   
    CLAUSES = 50
    ATOMS = 2*math.sqrt(2*k)
    CLAUSE_LENGTH = math.sqrt(2*k)
    HEAD_PROPORTION = 0.8

    t = 10
    time_out = 1800
    TEMP_THEORY += str(os.getpid())
    TEMP_MODEL  += str(os.getpid())
    TEMP_MIN_MODEL += str(os.getpid())
    TEMP_DLV += str(os.getpid())
    TEMP_CLASP += str(os.getpid())
    SAT_INPUT += str(os.getpid())
  
    
    #testsatcomp("test_data/testcases/satcomp/planning/logistics.a.cnf")
    '''for i in range(7, 10):
        print(str(i) + "," + str(cbwitness_worstcase(i)))'''
    lower = 0
    upper = 0
    MIN_MODEL = 0
    MIN_CHECK = False
    if len(sys.argv) >= 3:
        # usage [<lower> <upper>] 
        lower = int(sys.argv[1])
        upper = int(sys.argv[2])
        OUT_PUT = OUT_PUT +  sys.argv[1] + "_" + sys.argv[2] +"_"
        if len(sys.argv) >= 4:
            MIN_MODEL = int(sys.argv[3]) # determine which minimal model solver is used
        if len(sys.argv) == 5 and sys.argv[4] == "mc":
            OUT_PUT_MIN = OUT_PUT_MIN + str(lower) +"_"+str(upper) + "_"+ str(os.getpid())
            MIN_CHECK = True # whether do minimal check
    OUT_PUT += str(os.getpid())
    step = 0.1 
    y=3.0    
    while (y <= 5.0):
        steps.append(y)
        y = round(y + 0.1,1) 
    os.system("echo k ration time sat_dlv_out wt_out len_2 >" + OUT_PUT)
    for k in range(lower,upper+1,10): ### yisong
        for c in steps:
            test_v4(CLAUSES = int(c*k), ###  5*k, due to the phase transition of 3-SAT whose cirtical point is about 4.2
                ATOMS=k, 
                CLAUSE_LENGTH=3, 
                HEAD_PROPORTION="UNIFORM", 
                #cb=True, 
                #minmod=True, 
                #k=k, 
                #useminmodels=False,
                fixclauselen=True,
                MIN_MODEL=MIN_MODEL, 
                MIN_CHECK = MIN_CHECK)
    '''for i in range(2, 21):
        print(str(i) + "," + str(checkMin_worstcase(i)))'''
    '''
    for (k,t1,t2,out_times) in latex: ### Yisong 
        if t1 == 0:
            print("{0}, {1:.6f}, {2}".format(k, t2, out_times))
        elif t2 == 0:
            print("{0}, {1:.6f}, {2}".format(k, t1, out_times))
        else:
            print("{0}, {1:.6f}, {2:.6f}, {3}".format(k, t1, t2, out_times))
    '''
    try:
        os.remove(TEMP_DLV)
        os.remove(SAT_INPUT)
        os.remove(TEMP_THEORY)
        os.remove(TEMP_MODEL)
        os.remove(TEMP_MIN_MODEL)
        os.remove(TEMP_CLASP)
        #os.remove(OUT_PUT)
    except:
        pass 
