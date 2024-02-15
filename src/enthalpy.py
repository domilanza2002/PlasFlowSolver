#.................................................
#   ENTHALPY.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the enthalpy of the fluid
#   given the pressure and the temperature
#.................................................
import mutationpp as mpp #useful library for thermodynamic computations
def enthalpy(settings,P,T): #we define the function enthalpy
    #.................................................
    #   This function returns the enthalpy of the fluid
    #   given the pressure and the temperature
    #.................................................
    #   INPUTS:
    #   settings: settings of the program, which contains the mixture name
    #   P: pressure
    #   T: temperature
    #   OUTPUTS:
    #   h: enthalpy
    #.................................................
    #we define some variables:
    mixture_name=settings.mixture_name #name of the mixture
    h=None #enthalpy
    #h_shift=0 #enthalpy shift
    #we compute the enthalpy:
    mix=mpp.Mixture(mixture_name) #we create the mixture
    mix.equilibrate(T,P) #we equilibrate the mixture
    h=mix.mixtureHMass() #we compute the enthalpy
    #we compute the enthalpy shift:
    # mix.equilibrate(298.15,P) #we equilibrate the mixture at 298.15 K and P
    # h_shift=mix.mixtureHMinusH0Mass() #we compute the enthalpy shift
    # h=h+h_shift #we subtract the enthalpy shift
    return h #we return the enthalpy
#.................................................
#   Possible improvements:
#   - Check/add other mixture settings
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................