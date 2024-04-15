#.................................................
#   HEAT_FLUX_HF_LAW1.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the 
#   heat flux for the heat flux law hf_law=1,
#   the Fay-Riddell heat flux law, with Le=1
#.................................................
import math # Math library
import mutationpp as mpp  # Thermodynamic library
def heat_flux(probes, P_e, T_e, u, mixture_object):
    """This function computes the stagnation heat flux
    for the Fay-Riddell heat flux law, with Le=1.

    Args:
        probes (probes_class): the probes object containing the probe properties
        P_e (float): the static pressure at the edge
        T_e (float): the static temperature at the edge
        u (float): the freestream velocity of the flow
        mixture_object (mpp.Mixture): the Mutation++ mixture object

    Returns:
        q (float): the stagnation heat flux
    """
    # Variables:
    q = None  # Stagnation Heat flux
    Pr_w = None  # Prandtl number at the wall
    rho_e = None  # Density at the edge
    mu_e = None  # Dynamic viscosity at the edge
    rho_w = None  # Density at the wall
    mu_w = None  # Dynamic viscosity at the wall
    beta = None  # Velocity gradient
    h_e = None  # Enthalpy at the edge
    h_w = None  # Enthalpy at the wall
    C_p_w = None  # Specific heat at the wall
    lambda_eq_w = None  # Equilibrium thermal conductivity at the wall
    # Computation:
    mixture_object.equilibrate(T_e,P_e)
    rho_e = mixture_object.density()
    mu_e = mixture_object.viscosity()
    h_e = mixture_object.mixtureHMass()
    mixture_object.equilibrate(probes.T_w, P_e)
    rho_w = mixture_object.density()
    mu_w = mixture_object.viscosity()
    C_p_w = mixture_object.mixtureEquilibriumCpMass()
    lambda_eq_w = mixture_object.equilibriumThermalConductivity()
    h_w = mixture_object.mixtureHMass()
    Pr_w = mu_w * C_p_w / lambda_eq_w
    beta= probes.stag_var * u/probes.R_m
    q = 0.76* pow(Pr_w, -0.6) * pow(rho_e * mu_e, 0.4)* pow(rho_w * mu_w, 0.1) * math.sqrt(beta) * (h_e - h_w)
    return q
    
    