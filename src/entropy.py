#.................................................
#   ENTROPY.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the entropy of the fluid
#   given the pressure and the temperature.
#.................................................
import mutationpp as mpp  # Thermodynamic library

def entropy(mixture_object, P, T): 
    """This function returns the entropy of the fluid 
    given the pressure and the temperature.

    Args:
        mixture_object (mpp.Mixture): the mixture of the case
        P (float): pressure
        T (float): temperature
    Returns:
        s (float): entropy
    """
    # Variable to return:
    s = None 
    # Compute the entropy:
    mixture_object.equilibrate(T, P)  # I equilibrate the mixture
    s = mixture_object.mixtureSMass()  # I compute the entropy
    return s 
#.................................................
#   Possible improvements:
#   None
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................