#.................................................
#   ENTHALPY.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the enthalpy of the fluid
#   given the pressure and the temperature
#.................................................
import mutationpp as mpp #Library for thermodynamic computations
def enthalpy(mixture_name, P, T): #we define the function enthalpy
    """This function returns the enthalpy of the fluid given the pressure and the temperature

    Args:
        mixture_name (str): the mixture of the case
        P (float): pressure
        T (float): temperature

    Returns:
        h (float): enthalpy
    """
    #.................................................
    #   This function returns the enthalpy of the fluid
    #   given the pressure and the temperature
    #.................................................
    #   INPUTS:
    #   mixture_name: the mixture of the case
    #   P: pressure
    #   T: temperature
    #   OUTPUTS:
    #   h: enthalpy
    #.................................................
    #we define some variables:
    h = None #enthalpy
    #we compute the enthalpy:
    mix = mpp.Mixture(mixture_name) #we create the mixture
    mix.equilibrate(T,P) #we equilibrate the mixture
    h = mix.mixtureHMass() #we compute the enthalpy
    return h #we return the enthalpy
#.................................................
#   Possible improvements:
#   -Implement h_shift
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................