#.................................................
#   HEAT_FLUX_HF_LAW0_FLOW.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   flow properties inside the BL in the heat flux model with hf_law=0
#.................................................
import mutationpp as mpp  # Thermodynamic library

def heat_flux_hf_law0_flow(P, T, mixture):
    """This function computes the flow properties inside 
    the boundary layer.

    Args:
        P (float): Pressure
        T (float): Temperature
        mixture (mpp.Mixture): The mixture object

    Returns:
        rho (float): The density
        cp (float): The specific heat
        mu (float): The viscosity
        lambda_eq (float): The thermal conductivity
    """
    # Variable to return:
    rho = None  # Density of the flow at the current point
    cp = None  # Specific heat at constant pressure of the flow at the current point
    mu = None  # Viscosity of the flow at the current point
    lambda_eq = None  # Equilibrium thermal conductivity of the flow at the current point
    # I start the computation
    mixture.equilibrate(T, P)  # I equilibrate the mixture at the current point
    rho = mixture.density()  # I get the density of the flow at the current point, in kg/m^3
    cp = mixture.mixtureEquilibriumCpMass()  # I get the specific heat at constant pressure of the flow at the current point, in J/kg/K
    mu = mixture.viscosity()  # I get the viscosity of the flow at the current point, in Pa*s
    lambda_eq = mixture.equilibriumThermalConductivity()  # I get the equilibrium thermal conductivity of the flow at the current point, in W/m/K
    return rho, cp, mu, lambda_eq 
#.................................................
#   Possible improvements:
#   None.
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................