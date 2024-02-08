#.................................................
#   HEAT_FLUX_HFLAW0_WALL.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to compute the 
#   flow wall properties in the heat flux model hflaw=0
#.................................................
import mutationpp as mpp #useful library for thermodynamic computations
def heat_flux_hflaw0_wall(Pw,Tw,mixture): #we define the function
    #.................................................
    #   This function computes the wall edge properties
    #.................................................
    #   INPUTS:
    #   Pw: Wall pressure
    #   Tw: Wall temperature
    #   mixture: mixture object
    #   OUTPUTS:
    #   rhow: wall density
    #   kwt: wall thermal conductivity
    #.................................................
    # we declare the variables we need to return
    rhow=None #density on the edge
    kwt=None #thermal conductivity on the wall
    # we start the computations
    #mixture=mpp.Mixture(settings.mixture_name) #we create the mixture object
    mixture.equilibrate(Tw,Pw) #we equilibrate the mixture
    rhow=mixture.density() #we get the density on the edge
    kwt=mixture.equilibriumThermalConductivity() #we get the thermal conductivity on the wall
    return rhow,kwt #we return the variables
#.................................................
#   Possible improvements:
#   - Set the mixture better?
#.................................................
# EXECUTION TIME: 0.025792837142944336 s=0.03s, acceptable
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................