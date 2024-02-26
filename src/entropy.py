#.................................................
#   ENTROPY.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the entropy of the fluid
#   given the pressure and the temperature
#.................................................
import mutationpp as mpp #useful library for thermodynamic computations
def entropy(mixture_object, P, T): #we define the function entropy
    """This function returns the entropy of the fluid given the pressure and the temperature

    Args:
        mixture_object (mpp.Mixture): the mixture of the case
        P (float): pressure
        T (float): temperature
    Returns:
        s (float): entropy
    """
    #.................................................
    #   This function returns the entropy of the fluid
    #   given the pressure and the temperature
    #.................................................
    #   INPUTS:
    #   mixture_object: the mixture of the case
    #   P: pressure
    #   T: temperature
    #   OUTPUTS:
    #   s: entropy
    #.................................................
    #we define some variables:
    s = None #entropy
    #we compute the entropy:
    mixture_object.equilibrate(T, P) #we equilibrate the mixture
    s = mixture_object.mixtureSMass() #we compute the entropy
    return s #we return the entropy
#.................................................
#   Possible improvements:
#   None
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................