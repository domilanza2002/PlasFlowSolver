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
    #we compute the enthalpy:
    mix=mpp.Mixture(mixture_name) #we create the mixture
    mix.equilibrate(T,P) #we equilibrate the mixture
    h=mix.mixtureHMass() #we compute the enthalpy
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