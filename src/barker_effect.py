#.................................................
#   BARKER_EFFECT.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the barker effect
#   given the total pressure, the pressure, the temperature and the velocity
#.................................................
import mutationpp as mpp #useful library for thermodynamic computations
import math #useful library for math operations
def barker_effect(probe,settings,Pt,P,T,u):
    #.................................................
    #   This function returns the barker pressure
    #   given the total pressure, the pressure, the temperature and the velocity
    #.................................................
    #   INPUTS:
    #   probe: probe object
    #   settings: settings of the program, which contains the mixture name
    #   Pt: total pressure
    #   P: pressure
    #   T: temperature
    #   u: velocity
    #   OUTPUTS:
    #   Pb: barker pressure
    #   Re: reynolds number
    #.................................................
    #we define the variables:
    mixture_name=settings.mixture_name #name of the mixture
    barker=probe.barker #barker effect
    Rp=probe.Rp #pitot external radius
    rho=None #density
    mu=None #viscosity
    Cp=None #barker cp
    Pb=None #barker pressure
    Re=None #reynolds number
    #we set the mixture:
    mix=mpp.Mixture(mixture_name) #we create the mixture
    mix.equilibrate(T,P) #we equilibrate the mixture
    #we get the density:
    rho=mix.density() #we compute the density
    #we get the viscosity:
    mu=mix.viscosity() #we compute the viscosity
    #we compute the reynolds number:
    Re=rho*u*(2*Rp)/mu #we compute the reynolds number
    match(barker): #we check which barker effect to use
        case 0: #no barker effect
            Cp=0 #we set the barker pressure to 0
        case 1: #homann barker effect
            Cp=6/(Re+0.455*math.sqrt(Re))
        case _:
            print("Error: barker effect not yet implemented. But you should not be there... check read_probes.py")
            exit()
    #we compute the barker pressure:
    Pb=Pt+0.5*rho*pow(u,2)*Cp
    return Pb,Re #we return the barker pressure and the reynolds number
#.................................................
#   Possible improvements:
#   - Check/add other mixture settings
#   - Add other barker computations
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................