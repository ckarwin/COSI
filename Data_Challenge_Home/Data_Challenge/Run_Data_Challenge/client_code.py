# Imports:
from run_data_challenge_module import RunDataChallenge

# Define instance with input parameter card::
instance = RunDataChallenge("inputs.yaml")

# Run help function:
#help(instance)

# Generate tra file for simulation challenge:
instance.define_sim()
instance.run_cosima(432020)
instance.run_revan()
instance.run_mimrec()


