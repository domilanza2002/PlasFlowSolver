#.................................................
#   HEAT_FLUX_HFLAW0_EDGE.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to compute the 
#   flow edge properties in the heat flux model hflaw=0
#.................................................
import mutationpp as mpp #useful library for thermodynamic computations
def heat_flux_hflaw0_edge(Pe,Te,mixture): #we define the function
    #.................................................
    #   This function computes the flow edge properties
    #.................................................
    #   INPUTS:
    #   Pe: edge pressure
    #   Te: edge temperature
    #   mixture: mixture object
    #   OUTPUTS:
    #   rhoe: edge density
    #   cpe: edge specific heat
    #   mue: edge viscosity
    #.................................................
    # we declare the variables we need to return
    rhoe=None #density on the edge
    cpe=None #specific heat on the edge
    mue=None #viscosity on the edge
    # we start the computations
    #mixture=mpp.Mixture(settings.mixture_name) #we create the mixture object
    mixture.equilibrate(Te,Pe) #we equilibrate the mixture with the edge temperature and pressure
    rhoe=mixture.density() #we get the density on the edge
    cpe=mixture.mixtureEquilibriumCpMass() #we get the specific heat on the edge in J/(kg*K)
    mue=mixture.viscosity() #we get the viscosity on the edge
    return rhoe,cpe,mue #we return the variables
#.................................................
#   Possible improvements:
#   - Set the mixture better?
#.................................................
# EXECUTION TIME: 0.01839923858642578 s=0.02s, acceptable
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................