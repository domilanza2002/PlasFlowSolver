#.................................................
#   HEAT_FLUX.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the heat flux
#   for different heat flux laws.
#.................................................

import heat_flux_hf_law0 as heat_flux_hf_law0_file  # Module to compute the heat flux with the exact heat flux law
import heat_flux_hf_law1 as heat_flux_hf_law1_file  # Module to compute the heat flux with the Fay-Riddell heat flux law

def heat_flux(probes, settings, P_t, T_t, u, mixture_object):
    """This function computes the stagnation
    heat flux of the flux with different heat flux laws.

    Args:
        probes (probes_class): the probes object containing the probe properties
        settings (settings_class): the settings object containing the program settings
        P_t (float): the total pressure at the stagnation point
        T_t (float): the total temperature at the stagnation point
        u (float): the freestream velocity of the flow
        mixture_object (mpp.Mixture): the Mutation++ mixture object

    Returns:
        q (float): the heat flux
    """
    # Variable to return:
    q = None
    bad_hf = None # Variable to store the bad heat flux law
    # Heat flux law to use:
    hf_law = probes.hf_law
    match(hf_law):
        case 0:  # Exact heat flux law
            q, bad_hf = heat_flux_hf_law0_file.heat_flux(probes, settings, P_t, T_t, u, mixture_object) 
        case 1:  # Fay-Riddell heat flux law
            q = heat_flux_hf_law1_file.heat_flux(probes, P_t, T_t, u, mixture_object)
            bad_hf = False
        case _:  # Heat flux law not implemented
            raise ValueError("The heat flux law is not valid (You shouldn't see this message, check retrieve_helper.py)")
    return q, bad_hf
#.................................................
#   Possible improvements:
#   -Implement other heat flux laws.
#.................................................
# EXECUTION TIME: Please refer to the specific heat flux law.
#.................................................
#   KNOW PROBLEMS: Please refer to the specific heat flux law.
#.................................................