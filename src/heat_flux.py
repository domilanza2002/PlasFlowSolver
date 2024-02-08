#.................................................
#   HEAT_FLUX.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to compute the heat flux
#   of the flux with different heat flux laws.
#   At the moment, only the exact heat flux law is implemented.
#.................................................
import heat_flux_hflaw0 as heat_flux_hflaw0_file #file with the function to compute the heat flux with hflaw=0
def heat_flux(probes,settings,Pt,Tt,ue): #function to compute the heat flux
    #.................................................
    #   This function computes the heat flux of the flux with different heat flux laws.
    #   At the moment, only the exact heat flux law is implemented.
    #   In the future other heat flux laws will be implemented.
    #.................................................
    #   INPUTS:
    #   probes: the probes object containing the probes properties
    #   settings: the settings object containing the settings properties
    #   Pt: the total pressure at the stagnation point
    #   Tt: the total temperature at the stagnation point
    #   ue: the velocity of the flow
    #.................................................
    #   OUTPUTS:
    #   q: the heat flux
    #.................................................
    # we define the variable to return
    q=None #variable to store the heat flux
    # we retrive the heat flux law to use
    hflaw=probes.hflaw #heat flux law to use
    match(hflaw): # we check which heat flux law to use
        case 0: #exact heat flux law
            q=heat_flux_hflaw0_file.heat_flux_hflaw0(probes,settings,Pt,Tt,ue) #we compute the heat flow for hflaw=0
            return q #we return the heat flux
        case _: #heat flux law not implemented
            print("Error: heat flux law not implemented")
            exit()
#.................................................
#   Possible improvements:
#   -Implement other heat flux laws.
#.................................................
# EXECUTION TIME: Please refer to the specific heat flux law.
#.................................................
#   KNOW PROBLEMS:
#   None
#   Please refer to the specific heat flux law.
#.................................................