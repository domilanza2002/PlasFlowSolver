#.................................................
#   OUT_PROPERTIES.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the final
#   properties of the gas
#.................................................
import mutationpp as mpp #library to compute the final properties of the gas
def out_properties(mixture_object,Te,Pe,ue):
    """Computes the final properties of the gas

    Args:
        mixture_object (mpp.Mixture): the mixture object
        Te (float): temperature
        Pe (float): pressure
        ue (float): velocity
    Returns:
        rhoe (float): density
        ae (float): sound speed
        Me (float): mach number
        he (float): enthalpy
        ht (float): total enthalpy
    """
    #.................................................
    #   This function computes the final properties of the gas
    #.................................................
    #   INPUTS:
    #   mixture_object: the mixture object
    #   Te: temperature
    #   Pe: pressure
    #   ue: velocity
    #   OUTPUTS:
    #   rhoe: density
    #   ae: sound speed
    #   Me: mach number
    #   he: enthalpy
    #   ht: total enthalpy
    #.................................................
    #Variables
    rhoe = None #density
    ae = None #sound speed
    Me = None #mach number
    he = None #enthalpy
    ht = None #total enthalpy
    #Compute the final properties of the gas
    mixture_object.equilibrate(Te,Pe) #we equilibrate the mixture
    rhoe = mixture_object.density() #we compute the density
    ae = mixture_object.equilibriumSoundSpeed() #we compute the sound speed
    Me = ue/ae #we compute the mach number
    he = mixture_object.mixtureHMass()#we compute the mixture enthalpy
    mixture_object.equilibrate(298.15,Pe)
    h_shift = mixture_object.mixtureHMinusH0Mass() #we compute the enthalpy shift
    he = he+h_shift #we subtract the enthalpy shift
    ht = he+0.5*pow(ue,2) #we compute the total enthalpy
    return rhoe,ae,Me,he,ht