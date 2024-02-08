#.................................................
#   ENTROPY.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the entropy of the fluid
#   given the pressure and the temperature
#.................................................
import mutationpp as mpp #useful library for thermodynamic computations
def entropy(settings,P,T): #we define the function entropy
    #.................................................
    #   This function returns the entropy of the fluid
    #   given the pressure and the temperature
    #.................................................
    #   INPUTS:
    #   settings: settings of the program, which contains the mixture name
    #   P: pressure
    #   T: temperature
    #   OUTPUTS:
    #   s: entropy
    #.................................................
    #we define some variables:
    mixture_name=settings.mixture_name #name of the mixture
    #we compute the entropy:
    mix=mpp.Mixture(mixture_name) #we create the mixture
    mix.equilibrate(T,P) #we equilibrate the mixture
    s=mix.mixtureSMass() #we compute the entropy
    return s #we return the entropy
#.................................................
#   Possible improvements:
#   - Check/add other mixture settings
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................