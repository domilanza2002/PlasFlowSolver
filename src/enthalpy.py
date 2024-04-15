#.................................................
#   ENTHALPY.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the enthalpy of the fluid
#   given the pressure and the temperature.
#.................................................
import mutationpp as mpp  # Thermodynamic library

def enthalpy(mixture_object, P, T):
    """This function returns the enthalpy of the fluid 
    given the pressure and the temperature.

    Args:
        mixture_object (mpp.Mixture): the mixture of the case
        P (float): pressure
        T (float): temperature

    Returns:
        h (float): enthalpy
    """
    # Variable to return:
    h = None
    # Compute the enthalpy:
    mixture_object.equilibrate(T, P)  # I equilibrate the mixture
    h = mixture_object.mixtureHMass() # I compute the enthalpy
    return h
#.................................................
#   Possible improvements:
#   None.
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................