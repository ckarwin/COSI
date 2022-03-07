#imports
import os

# Get path to Data_Challenge directory:
install_home = os.getcwd()
src_lib = os.path.join(install_home,"../Source_Library")

# Open master file:
master_file = os.path.join(src_lib,"master_source_list.txt")

# Specify full path to transmission probability file:
transmission_file = os.path.join(install_home,"../Input_Files/Transmission_Probability/TransmissionProbability_33000.dat")

# Construct source files with proper library paths:
f = open(master_file,"r")
this_master = eval(f.read())
f.close()

for i in range(0,len(this_master)):
    
    this_list = this_master[i]
    this_name = this_list[0]
    this_type = this_list[1]
    this_path = os.path.join(src_lib,this_name)
    this_file = os.path.join(this_path,this_name + ".source")
    this_spec = os.path.join(this_path,this_name + "_spec.dat")

    if this_type == "ps":
        
        this_l = this_list[2]
        this_b = this_list[3]
        this_flux = this_list[4]

        g = open(this_file,"w")
        g.write("DataChallenge.Source          %s\n" %this_name)
        g.write("%s.ParticleType               1\n" %this_name)
        g.write("%s.Beam                       FarFieldPointSource 0 0\n" %this_name)
        g.write("%s.Orientation                Galactic Fixed %s %s\n" %(this_name,this_l,this_b)) 
        g.write("%s.Spectrum                   File %s\n" %(this_name,this_spec))
        g.write("%s.Flux                       %s\n" %(this_name,this_flux))
        g.write("%s.FarFieldTransmissionProbability  %s" %(this_name,transmission_file))
        g.close()

    if this_type == "include":

        include_list = this_list[2]
        g = open(this_file,"w")
        for each in include_list:
            src_file = each + "/" + each + ".source"
            src_path = os.path.join(src_lib,src_file)
            g.write("#include %s\n" %each)
            g.write("Include %s\n\n" %src_path)
        g.close()
        
    if this_type == "LingBG":

        g = open(this_file,"w")
        g.write("DataChallenge.Source BGContinuum\n")
        g.write("DataChallenge.Source BGCosmic\n")
        g.write("DataChallenge.Source BGFive11\n\n")
        g.write("# Indicate the three .cosimadat files with NRLMSISE information:\n")
        g.write("BGContinuum.ParticleType 1\n")
        g.write("BGContinuum.Beam FarFieldNormalizedEnergyBeamFluxFunction %s/ling_continuum_33.500_km_00.cosimadat\n" %this_path)
        g.write("BGContinuum.Spectrum NormalizedEnergyBeamFluxFunction\n\n")
        g.write("BGCosmic.ParticleType 1\n")
        g.write("BGCosmic.Beam FarFieldNormalizedEnergyBeamFluxFunction %s/ling_cosmic_33.500_km_00.cosimadat\n" %this_path)
        g.write("BGCosmic.Spectrum NormalizedEnergyBeamFluxFunction\n\n")
        g.write("BGFive11.ParticleType 1\n")
        g.write("BGFive11.Beam FarFieldNormalizedEnergyBeamFluxFunction %s/ling_511_33.500_km_00.cosimadat\n" %this_path)
        g.write("BGFive11.Spectrum NormalizedEnergyBeamFluxFunction")
        g.close()

print()
print("setup successful!")
print()
