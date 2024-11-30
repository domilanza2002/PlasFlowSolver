#.................................................
#   HEAT_FLUX_HF_LAW0_EDGE.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   flow edge properties in the heat flux model with hf_law=0
#.................................................
import mutationpp as mpp  # Thermodynamic library

def heat_flux_hf_law0_edge(P_e,T_e,mixture):
    """This function computes the flow edge 
    properties for the mixture.

    Args:
        P_e (float): The edge pressure
        T_e (float): The edge temperature
        mixture (mpp.Mixture): The mixture object

    Returns:
        rho_e (float): The edge density
        mu_e (float): The edge viscosity
    """
    
    # I declare the variables I need to return
    rho_e = None  # Density on the edge
    mu_e = None  # Viscosity on the edge
    # I start the computations
    mixture.equilibrate(T_e, P_e)  # I equilibrate the mixture
    rho_e = mixture.density() # I get the density on the edge, Kg/m^3
    mu_e = mixture.viscosity()  # I get the viscosity on the edge, Pa s
    return rho_e, mu_e
#.................................................
#   Possible improvements:
#   None.
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................