#.................................................
#   BARKER_EFFECT.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the Barker's effect.
#.................................................
import mutationpp as mpp  # Thermodynamic library
import math  # Math library
def barker_effect(probes, mixture_object, P_t, P, T, u):
    """This function returns the barker pressure given the total pressure, the pressure, the temperature and the velocity

    Args:
        probes (probes_class): probe properties
        mixture_object (mpp.Mixture): the mixture of the case
        P_t (float): total pressure
        P (float): pressure
        T (float): temperature
        u (float): velocity
    Returns:
        P_b (float): barker pressure
        Re (float): reynolds number
    """
    # Variables:
    barker_type = probes.barker_type  # Barker's correction type
    R_p = probes.R_p  # Pitot external radius
    rho = None  # Flow density
    mu = None  # Flow viscosity
    C_p = None  # Barker's correction C_p
    P_b = None  # Barker's stagnation pressure read
    Re = None  # Reynolds number on the pitot probe
    mixture_object.equilibrate(T, P)  # I equilibrate the mixture
    rho = mixture_object.density()  # I get the density
    mu = mixture_object.viscosity()  # I get the viscosity
    Re = rho*u*(2*R_p)/mu  # Barker's Reynolds number
    match (barker_type):
        case 0:  # No barker effect
            C_p = 0
        case 1:  # Homann's correction
            C_p = 6/(Re+0.455*math.sqrt(Re))
        case 2:  # Carleton's correction
            C_p = 1 + 8/(Re+0.5576*math.sqrt(Re))
        case _:
            print("Error: Barker's correction not yet implemented. But you should not be there... check retrieve_helper.py")
            exit()
    # Barker's pressure (stagnation pressure read instead of the total pressure)
    P_b = P_t + 0.5*rho*pow(u, 2)*C_p
    return P_b, Re
#.................................................
#   Possible improvements:
#   - Add other barker computations
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................