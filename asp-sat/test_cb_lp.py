import sys
import copy
import os
import subprocess

def build_cb_lp(dirs):
# compute the minimal beta-witness for answer sets of logic programs
# in directory dirs
# the files are in the file SAT 
  cb_solver="/usr/local/bin/python3.7"
  rfile = "cb_lp.res"
  if not dirs.endswith("/"):
    dirs = dirs + "/"
  fp = open(dirs+"SAT", "r")
  files = [x.replace("\n","") for x in fp.readlines()]
  fp.close()
  rf = open(dirs+rfile,"w")
  for f in files:
    f = dirs + f 
    lp = f.replace(".m",".lp")
    sargs = " ".join([cb_solver, "cb_witness.py", "-v4", "-t 7200", "-TT_PYSAT", "-lp", "-q", lp, f])
    rf.write(sargs+"\n")
    print(sargs+"\n")
    sres = subprocess.check_output([cb_solver, "cb_witness.py", "-v4", "-t 7200", "-TT_PYSAT", "-lp", "-q", lp, f])
    #sres = subprocess.check_output(sargs)
    #sres = subprocess.check_output([cb_solver, "cb_witness.py", "-v4", "-t 7200", "-TT_PYSAT",\ "-lp", "-q", lp, f], stdout=rf) 
    rf.write(str(sres))
    print(str(sres))
  rf.close()

if __name__ == "__main__":
  if len(sys.argv) != 2:
    printf("Usage %s <Dir>"%sys.argv[1])
  build_cb_lp(sys.argv[1])


