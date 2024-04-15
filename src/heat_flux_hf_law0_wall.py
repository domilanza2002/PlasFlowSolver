#.................................................
#   HEAT_FLUX_HF_LAW0_WALL.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   flow wall properties in the heat flux model with hf_law=0.
#.................................................
import mutationpp as mpp  # Thermodinamic library

def heat_flux_hf_law0_wall(P_w, T_w, mixture):
    """This function computes the flow wall 
    properties for the mixture.

    Args:
        P_w (float): The wall pressure
        T_w (float): The wall temperature
        mixture (mpp.Mixture): The mixture object

    Returns:
        rho_w (float): The wall density
        lambda_eq_wall (float): The wall thermal conductivity
    """
    # I declare the variables I need to return
    rho_w = None  # Density on the wall
    lambda_eq_wall = None  # Equilibrium thermal conductivity on the wall
    # I start the computations
    mixture.equilibrate(T_w, P_w)  # I equilibrate the mixture
    rho_w = mixture.density()  # I get the density on the wall, Kg/m^3
    lambda_eq_wall = mixture.equilibriumThermalConductivity()  # I get the equilibrium thermal conductivity on the wall, W/m/K
    return rho_w, lambda_eq_wall 
#.................................................
#   Possible improvements:
#   None.
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................