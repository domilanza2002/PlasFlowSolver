#.................................................
#   OUT_PROPERTIES.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the final
#   flow properties to output.
#.................................................
import mutationpp as mpp  # Thermodinamic library

def enthalpy_shift(mixture_object, P):
    """This function computes the enthalpy shift.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        P (float): pressure

    Returns:
        h0 (float): enthalpy shift
    """
    h0 = None  # Enthalpy shift
    T0 = 298.15  # Reference temperature
    mixture_object.equilibrate(T0, P)
    h0 = mixture_object.mixtureHMinusH0Mass()
    return h0

def out_properties(mixture_object, T, P, u):
    """This function computes the final properties of the gas.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        T (float): temperature
        P (float): pressure
        u (float): velocity
    Returns:
        rho (float): density
        a (float): sound speed
        M (float): mach number
        h (float): enthalpy
        h_t (float): total enthalpy
    """
    #Variables
    rho = None  # Density
    a = None  # Sound speed
    M = None  # Mach number
    h = None  # Enthalpy
    h_t = None  # Total enthalpy
    h0 = enthalpy_shift(mixture_object, P)  # Enthalpy shift
    # Computation:
    mixture_object.equilibrate(T, P) 
    rho = mixture_object.density() 
    a = mixture_object.equilibriumSoundSpeed() 
    M = u/a 
    h = mixture_object.mixtureHMass() + h0
    h_t = h + 0.5*pow(u,2)
    return rho, a, M, h, h_t