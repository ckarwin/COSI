############################################################
# 
# Written by Chris karwin; November 2021; Clemson University
#
# Purpose: Main script for generating simulation challenge.
# 
# Index of functions:
#
#   Run_Data_Challenge(superclass)
#       -define_sim()
#       -run_cosima(seed="none")
#       -run_revan(config_file="none")
#       -run_mimrec(save_dir, numbins, rad, config_file="none")
#
###########################################################

######################
#imports:
import os,sys,shutil 
import yaml
import pandas as pd
######################

#superclass:
class Run_Data_Challenge:
    
    """Main inputs are specified in inputs.yaml file"""

    def __init__(self,input_yaml):

        #get home directory:
        self.home = os.getcwd()
        
        #load main inputs from yaml file:
        with open(input_yaml,"r") as file:
            inputs = yaml.load(file,Loader=yaml.FullLoader)

        self.DC_dir = inputs["DC_dir"]
        self.geo_file = inputs["geometry_file"]
        self.name = inputs["name"]
        self.source_file = self.name + ".source"
        self.NTriggers = inputs["NTriggers"]
        self.src_list = inputs["src_list"]
        self.orientation_file = os.path.join(self.DC_dir,"Data_Challenge/Input_Files/GalacticScan.ori")
        self.master_src_list = os.path.join(self.DC_dir,"Data_Challenge/Source_Library/master_source_list.dat")
        
        #specify default geometry file:
        if self.geo_file == "default":
            this_file = "Data_Challenge/Input_Files/Geometry_Files/AMEGO_Geometry/AMEGO_Probe/AmegoBase.geo.setup"
            self.geo_file = os.path.join(self.DC_dir,this_file)
        
    def define_sim(self):

        """

         This function makes the main source file for the simulation. 

         The input source list is passed from inputs.yaml,
         and it must be a list of strings, where each string is from the available options.
    
         
        """

        #make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running define_sim...")
        print()

        ########################
        #unit testing:

        #verify that input sources are given as list:
        if isinstance(self.src_list,list) == False:
            raise TypeError("Input sources must be a list!")

        #check that input sources are included in library:
        df = pd.read_csv(self.master_src_list,delim_whitespace=True,names=["srcname"])
        masterlist = df["srcname"].tolist()
        for each in self.src_list:
            if each not in masterlist:
                print()
                print("ERROR: Input source is not defined!")
                print() 
                print("Sources must be selected from available list:")
                print(masterlist)
                print()
                sys.exit()
        
        ##########################   

        #print source list:      
        print()
        print("Simulation will include the following sources:")
        print(self.src_list)
        print()

        #write source file:
        f = open(self.source_file,"w")
        f.write("#Source file for data challenge, version 1\n")
        f.write("#The detector rotates in the Galactic coordiante system as given in the ori file.\n")
        f.write("#The point sources are fixed in Galactic coordinates.\n\n")
        f.write("#geometry file\n")
        f.write("Version         1\n")
        f.write("Geometry   %s\n\n" %self.geo_file)
        f.write("#Physics list\n")
        f.write("PhysicsListEM                        LivermorePol\n")
        f.write("PhysicsListEMActivateFluorescence    false\n\n")
        f.write("#Output formats\n")
        f.write("StoreCalibrated                      true\n")
        f.write("StoreSimulationInfo                  true\n")
        f.write("StoreSimulationInfoIonization        false\n")
        f.write("DiscretizeHits                       true\n\n")
        f.write("#Define run:\n")
        f.write("Run DataChallenge\n")
        f.write("DataChallenge.FileName               %s\n" %self.name)
        f.write("DataChallenge.NTriggers              %s\n" %self.NTriggers)
        f.write("DataChallenge.OrientationSky         Galactic File NoLoop %s\n\n" %self.orientation_file)

        #write sources:
        for each in self.src_list:
            this_file = os.path.join(each,each + ".source")
            this_path = os.path.join(self.DC_dir,"Data_Challenge/Source_Library/")
            this_src = os.path.join(this_path,this_file)
            f.write("#include %s\n" %each)
            f.write("Include %s\n\n" %this_src)
        
        #close file:
        f.close()
    
        return
    
    def run_cosima(self,seed="none"):

        """

         input definitions:
        
         seed: Optional input. Specify seed to be used in simulations for reproducing results.
        
        """

        #make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running run_cosima...")
        print()

        #make output image directory:
        if os.path.isdir("Output_Images") == True:
            shutil.rmtree("Output_Images")
        os.system("mkdir Output_Images")
        
        #make output data directory:
        if os.path.isdir("Output_Data") == True:
            shutil.rmtree("Output_Data")
        os.system("mkdir Output_Data")
        os.chdir("Output_Data")
    
        #copy source file to output directory:
        shutil.copy2(os.path.join(self.home,self.source_file),self.source_file)

        #run Cosima:
        if seed != "none":
            print("running with a seed...")
            os.system("cosima -s %s -z %s | tee cosima_terminal_output.txt" %(seed,self.source_file))
        if seed == "none":
            print("running with no seed...")
            os.system("cosima -z %s | tee cosima_terminal_output.txt" %(self.source_file))

        #return home:
        os.chdir(self.home)

        return

    def run_revan(self,config_file="none"):

        """
        
         input definitions:
        
         config_file: Optional input. 
            - Configuration file specifying selections for event reconstruction.
            - Needs to be in "Inputs" directory

        """

        #make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running run_revan...")
        print()

        #change to output directory:
        os.chdir("Output_Data")

        #define input sim file:
        sim_file = self.name + ".inc1.id1.sim.gz"

        #run revan:
        if config_file != "none":

            print("running with a configuration file...")
            os.system("revan -g %s -c %s -f %s -n -a | tee revan_terminal_output.txt" %(self.geo_file, config_file, sim_file))

        if config_file == "none":
            print("running without a configuration file...")
            os.system("revan -g %s -f %s -n -a | tee revan_terminal_output.txt" %(self.geo_file, sim_file))

        #go home:
        os.chdir(self.home)

        return

    def run_mimrec(self, config_file="none"):

        """
        
         input definitions:
        
         config_file: Optional input. Configuration file specifying selections for image reconstruction.


        """

        #make print statement:
        print()
        print("********** Run_Data_Challenge_Module ************")
        print("Running run_mimrec...")
        print()

        #change to output directory:
        os.chdir("Output_Data")

    
        #define tra file:
        tra_file = self.name + ".inc1.id1.tra.gz"
        
        #define outputs:
        output_events = "%s.inc1.id1.extracted.tra.gz" %self.name
        output_spec = "source_counts_spectrum.root"

        #run mimrec:
        if config_file != "none":
            
            print("running with a configuration file...")
           
            #extracted events:
            os.system("mimrec -g %s -f %s -x -o %s -n \
                    | tee mimrec_terminal_output.txt" %(self.geo_file, tra_file, output_events))
            
            #source spectrum:
            os.system("mimrec -g %s -c %s -f %s -s -o %s -n \
                    | tee mimrec_terminal_output.txt" %(self.geo_file, config_file, tra_file, output_spec))
             
        if config_file == "none":
            
            print("running without a configuration file...")
            
            #extracted events:
            os.system("mimrec -g %s -f %s -x -o %s -n \
                    | tee mimrec_terminal_output.txt" %(self.geo_file, tra_file, output_events))

            #source spectrum:
            os.system("mimrec -g %s -f %s -s -o %s -n \
                    | tee mimrec_terminal_output.txt" %(self.geo_file, tra_file, output_spec))
       
        #extract spectrum histogram:
        #os.system("root -q -b %s/ExtractSpectrum.cxx" %self.home)
        
        #go home:
        os.chdir(self.home)

        return

