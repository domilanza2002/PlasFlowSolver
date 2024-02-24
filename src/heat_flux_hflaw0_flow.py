#.................................................
#   HEAT_FLUX_HFLAW0_FLOW.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to compute the 
#   flow properties inside the BL in the heat flux model hflaw=0
#.................................................
import mutationpp as mpp #Library for thermodynamic computations
def heat_flux_hflaw0_flow(P,T,mixture):  #we define the function
    """This function computes the flow properties inside the boundary layer

    Args:
        P (float): Pressure
        T (float): Temperature
        mixture (mpp.Mixture): The mixture object

    Returns:
        rho (float): The density
        cp (float): The specific heat
        mu (float): The viscosity
        k (float): The thermal conductivity
    """
    #.................................................
    #   This function computes the flow properties
    #   inside the boundary layer
    #.................................................
    #   INPUTS:
    #   P: Pressure
    #   T: Temperature
    #   mixture: mixture object
    #   OUTPUTS:
    #   rho: density
    #   cp: specific heat
    #   mu: viscosity
    #   k: thermal conductivity
    #.................................................
    # we declare the variables we need to return
    rho = None #density of the flow at the current point
    cp = None #specific heat of the flow at the current point
    mu = None #viscosity of the flow at the current point
    k = None #thermal conductivity of the flow at the current point
    # we start the computations
    mixture.equilibrate(T,P) #we equilibrate the mixture
    rho = mixture.density() #we get the density of the flow at the current point
    cp = mixture.mixtureEquilibriumCpMass() #we get the specific heat of the flow at the current point
    mu = mixture.viscosity() #we get the viscosity of the flow at the current point
    k = mixture.equilibriumThermalConductivity() #we get the thermal conductivity of the flow at the current point
    return rho, cp, mu, k #we return the values
#.................................................
#   Possible improvements:
#   None.
#.................................................
# EXECUTION TIME: Very fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................