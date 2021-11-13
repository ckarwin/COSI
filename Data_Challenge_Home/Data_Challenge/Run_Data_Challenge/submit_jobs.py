import os, sys
import time

for i in range(0,1):

    f = open('multiple_batch_submission.pbs','w')

    f.write("#PBS -N AMEGO\n")
    f.write("#PBS -l select=1:ncpus=1:mem=5gb:interconnect=1g,walltime=10:00:00\n\n")
    f.write("#the MEGAlib environment first needs to be sourced:\n")
    f.write("cd /zfs/astrohe/Software\n")
    f.write("source MEGAlibX.sh\n\n")
    f.write("#change to working directory and run job\n")
    f.write("cd /zfs/astrohe/ckarwin/AMEGO_X/TXS_0506_056/First_Flare/Run_6\n")
    f.write("python client_code.py")
    f.close()

    os.system("qsub multiple_batch_submission.pbs")
    time.sleep(3)