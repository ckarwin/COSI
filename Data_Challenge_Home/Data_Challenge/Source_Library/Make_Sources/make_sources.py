# Imports:
import numpy as np
from SpectralModels import Band
from scipy.interpolate import interp1d
from scipy import integrate
import pandas as pd
import os
import matplotlib.pyplot as plt

# Source energy range (100 keV - 10 MeV):
# Note: COSI range: 0.2 - 5 MeV 
# Include padding above and below to account for energy dispersion
energy_range = np.logspace(2,4,40) #keV

#function to make spectrum files:
def make_spec_file(src_name, src_energy, src_flux, intg):
    
    # Setup directory and file:
    this_name = src_name
    this_dir = "../%s" %this_name
    this_spec = os.path.join(this_dir,this_name + "_spec.dat")
    if os.path.isdir(this_dir) == False:
        os.system("mkdir %s" %this_dir)

    # Write spectrum file:
    f = open(this_spec,"w")
    f.write("#Format: <DP> <Energy in keV> <Spectrum in ph cm^-2 s^-1 keV^-1>\n")
    f.write("#flux (%s - %s keV): %s ph/cm^2/s\n" %(str(min(src_energy)),str(max(src_energy)),str(intg)))
    f.write("\n\nIP LINLIN\n\n")
    d = {"name":["DP"]*len(src_energy),"energy[keV]":src_energy,"photons[ph/cm^2/s/keV]":src_flux}
    df = pd.DataFrame(data=d, columns=["name","energy[keV]","photons[ph/cm^2/s/keV]"])
    df.to_csv(f,index=False, float_format='%10.5e',sep="\t",header=False)

    f.close()

    return

# Define sources below:

##################
#crab:
this_name = "crab"

#spectrum:
band = Band(amplitude=7.52e-4,E_peak=5.31,alpha=-1.99,beta=-2.32) #note: E_0 = 531 keV, which is the break energy, E_0 = E_peak/(2-alpha)
crab_energy,crab_photons = band.PhotonSpectrum(Energy=energy_range)
crab_func = interp1d(crab_energy,crab_photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#sanity checks on integrated flux:
crab_intg1 = integrate.quad(crab_func,325,480)
crab_intg2 = integrate.quad(crab_func,298.5984,515.978)
print()
print("Crab flux between 325 - 480 keV [ph/cm^2/s]: " + str(crab_intg1[0]))
print("Crab flux between 298.5984 - 515.978 keV [ph/cm^2/s]: " + str(crab_intg2[0]))
print()

#integrated flux for source file:
intg = integrate.quad(crab_func,1e2,1e4)[0]
intg = float("{:.6f}".format(intg))
print()
print("Crab flux between 100 keV - 10 MeV [ph/cm^2/s]: " + str(intg))
print()

make_spec_file(this_name, energy_range, crab_photons, intg)
##################

##################
#cen A
this_name = "cenA"

#spectrum:
df = pd.read_csv("cenA.txt",delim_whitespace=True)
energy = df["energy[eV]"]*(1.0/1000.0) #keV
flux = df["flux[erg/cm^2/s]"] #erg/cm^2/s
flux = flux*6.242e8 #keV/cm^2/s
photons = flux/(energy**2)
func = interp1d(energy,photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#integrated flux for source file:
intg = integrate.quad(func,1e2,1e4)[0]
intg = float("{:.6f}".format(intg))
print()
print("cenA flux between 100 keV - 10 MeV [ph/cm^2/s]: " + str(intg))
print()

#plot for sanity check:
#plt.loglog(df["energy[eV]"],df["flux[erg/cm^2/s]"])
#plt.show()

make_spec_file(this_name, energy_range, func(energy_range), intg)
##################

##################
#vela
this_name = "vela"

#spectrum:
df = pd.read_csv("vela.txt",delim_whitespace=True)
energy = df["energy[eV]"]*(1.0/1000.0) #keV
flux = df["flux[erg/cm^2/s]"] #erg/cm^2/s
flux = flux*6.242e8 #keV/cm^2/s
photons = flux/(energy**2)
func = interp1d(energy,photons,kind="linear",bounds_error=False,fill_value="extrapolate")

#integrated flux for source file:
intg = integrate.quad(func,1e2,1e4)[0]
intg = float("{:.6f}".format(intg))
print()
print("vela flux between 100 keV - 10 MeV [ph/cm^2/s]: " + str(intg))
print()

#plot for sanity check:
#plt.loglog(df["energy[eV]"],df["flux[erg/cm^2/s]"])
#plt.show()

make_spec_file(this_name, energy_range, func(energy_range), intg)
##################

