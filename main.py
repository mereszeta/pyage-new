import os
import sys

emas = [ False]
mutation_prob = [0.1, 0.15, 0.2]
mutation_func = [0, 1]

generate = False
filename = ""

proc_base = "python2.7 -m pyage.core.bootstrap pyage.satcnf.sat_conf ERROR "

# Main routine

if __name__ == "__main__":
    filename = sys.argv[1]
    for e in emas:
        for pr in mutation_prob:
            for m in mutation_func:
                args = ('1' if e else '0') + " " + str(pr) + " " + str(m) + " " + filename
                print("Executing: " + proc_base + args + "...")
                os.system(proc_base + args)