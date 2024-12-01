#.................................................
#   OUT_PROPERTIES.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the final
#   flow properties to output.
#.................................................
import mutationpp as mpp  # Thermodinamic library

def enthalpy_shift(mixture_object, P):
    """This function computes the enthalpy shift.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        P (float): pressure

    Returns:
        h0 (float): enthalpy shift
    """
    h0 = None  # Enthalpy shift
    T0 = 298.15  # Reference temperature
    mixture_object.equilibrate(T0, P)
    h0 = mixture_object.mixtureHMinusH0Mass()
    return h0

def out_properties(mixture_object, T, P, u):
    """This function computes the final properties of the gas.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        T (float): temperature
        P (float): pressure
        u (float): velocity
    Returns:
        rho (float): density
        a (float): sound speed
        M (float): mach number
        h (float): enthalpy
        h_t (float): total enthalpy
        mfp (float): mean free path
    """
    #Variables
    rho = None  # Density
    a = None  # Sound speed
    M = None  # Mach number
    h = None  # Enthalpy
    h_t = None  # Total enthalpy
    mfp = None  # Mean free path
    #h0 = enthalpy_shift(mixture_object, P)  # Enthalpy shift
    # Computation:
    mixture_object.equilibrate(T, P) 
    rho = mixture_object.density() 
    a = mixture_object.equilibriumSoundSpeed() 
    M = u/a 
    #h = mixture_object.mixtureHMass() + h0
    h=mixture_object.mixtureHMinusH0Mass()
    h_t = h + 0.5*pow(u,2)
    mfp = mixture_object.meanFreePath()
    return rho, a, M, h, h_t, mfp

def mass_fraction_composition(mixture_object, T, P):
    """This function computes the mass fraction composition of the gas.

    Args:
        mixture_object (mpp.Mixture): the mixture object
        T (float): temperature
        P (float): pressure

    Returns:
        species_names (list): list of species names 
        species_Y (list): list of mass fractions
    """
    # Variables:
    species_names = None  # Species names
    species_Y = None  # Mass fraction composition
    n_species = None  # Number of species
    # Init:
    species_names = []
    species_Y = []
    # Computation:
    mixture_object.equilibrate(T, P)  # Equilibrate the mixture
    n_species = mixture_object.nSpecies()  # Number of species
    for i in range(n_species):
        species_names.append(mixture_object.speciesName(i))  # Append species name
    species_Y = mixture_object.Y()  # Retrieve mass fractions
    # Return:
    return species_names, species_Y
