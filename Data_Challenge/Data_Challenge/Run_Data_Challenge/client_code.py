#imports:
from Run_Data_Challenge_module import Run_Data_Challenge

#define instance with input parameter card::
instance = Run_Data_Challenge("inputs.yaml")

#run help function:
#help(instance)

#Generate tra file for simulation challenge:
instance.define_sim()
instance.run_cosima(432020)
instance.run_revan()
instance.run_mimrec()


