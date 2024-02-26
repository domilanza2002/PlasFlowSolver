#.................................................
#   JACOBIAN_MATRIX.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to compute the jacobian matrix of the system
#   in order to use the newton-raphson method
#.................................................
import enthalpy as enthalpy_file #we import the enthalpy file
import entropy as entropy_file #we import the entropy file
import barker_effect as barker_effect_file #we import the barker effect file
import heat_flux as heat_flux_file #we import the heat flux file
def jacobian_matrix(probes,settings,Te,Tt,Pe,Pt,Pb,q,he,ht,se,st,ue,mixture_object): #we define the function jacobian_matrix
    """This function returns the jacobian matrix of the system in order to use the newton-raphson method

    Args:
        probes (probes): probes of the system
        settings (settings): settings of the program
        Te (float): temperature at the exit
        Tt (float): temperature at the turbine
        Pe (float): pressure at the exit
        Pt (float): pressure at the turbine
        Pb (float): pressure at the barker
        q (float): heat flux
        he (float): enthalpy at the exit
        ht (float): enthalpy at the turbine
        se (float): entropy at the exit
        st (float): entropy at the turbine
        ue (float): velocity at the exit
        mixture_object (mpp.Mixture): mixture of the case

    Returns:
        jac (matrix float): jacobian matrix
    """
    #.................................................
    #   This function returns the jacobian matrix of the system
    #   in order to use the newton-raphson method
    #   In order to compute the partial derivatives, we use a 
    #   forward finite difference method
    #.................................................
    #   INPUTS:
    #   probes: probes of the system
    #   settings: settings of the program
    #   Te: temperature at the exit
    #   Tt: temperature at the turbine
    #   Pe: pressure at the exit
    #   Pt: pressure at the turbine
    #   Pb: pressure at the barker
    #   q: heat flux
    #   he: enthalpy at the exit
    #   ht: enthalpy at the turbine
    #   se: entropy at the exit
    #   st: entropy at the turbine
    #   ue: velocity at the exit
    #   mixture_object: mixture of the case
    #   OUTPUTS:
    #   jac: jacobian matrix
    #.................................................
    # we declare some variables:
    jac = None #variable to store the jacobian matrix
    delta = None #variable to store the delta for the finite difference
    Tstar = None #new temperature for the finite difference
    dhdte = None #derivative of h(Pe,Te) wrt Te
    dsdte = None #derivative of s(Pe,Te) wrt Te
    dbdte = None #derivative of Pb(Pt,Pe,Te,ue) wrt Te
    ustar = None #new velocity for the finite difference
    dqdu = None #derivative of q(Pt,Tt,ue) wrt ue
    dbdu = None #derivative of Pb(Pt,Pe,Te,ue) wrt ue
    Ttstar = None #new total temperature for the finite difference
    dqdtt = None #derivative of q(Pt,Tt,ue) wrt Tt
    dhtdtt = None #derivative of ht(Pt,Tt) wrt Tt
    dstdtt = None #derivative of st(Pt,Tt) wrt Tt
    Ptstar = None #new value for the total pressure for the finite difference
    dqdpt = None #derivative of q(Pt,Tt,ue) wrt Pt
    dhtdpt = None #derivative of ht(Pt,Tt) wrt Pt
    dstdpt = None #derivative of st(Pt,Tt) wrt Pt
    dbdpt = None #derivative of Pb(Pt,Pe,Te,ue) wrt Pt
    hstar = None #new value for the enthalpy
    htstar = None #new value for the total enthalpy
    sstar = None #new value for the entropy
    ststar = None #new value for the total entropy
    Pbstar = None #new value for the barker pressure
    qstar = None #new value for the heat flux
    # we retrieve some settings:
    jac_diff = settings.jac_diff #we get the finite difference epsilon
    barker = probes.barker #we get the barker correction
    # we start the computation of the jacobian matrix
    #.................................................
    # DERIVATIVE WRT Te:
    delta = Te*jac_diff #we compute the delta for the finite difference
    Tstar = Te+delta #we compute the new temperature
    # we compute the new enthalpy and entropy
    hstar = enthalpy_file.enthalpy(mixture_object, Pe, Tstar)
    sstar = entropy_file.entropy(mixture_object, Pe, Tstar)
    #We compute the barker pressure:
    Pbstar = barker_effect_file.barker_effect(probes, mixture_object, Pt, Pe, Tstar, ue)[0]
    # Now we compute the derivative using the forward finite difference method
    dhdte = (hstar-he)/delta #derivative of h(Pe,Te) wrt Te
    dsdte = (sstar-se)/delta #derivative of s(Pe,Te) wrt Te
    dbdte = (Pbstar-Pb)/delta #derivative of Pb(Pt,Pe,Te,ue) wrt Te
    #.................................................
    # DERIVATIVE WRT ue:
    delta = ue*jac_diff #we compute the delta for the finite difference
    ustar = ue+delta #we compute the new velocity
    # we compute the new heat flux
    qstar = heat_flux_file.heat_flux(probes,settings,Pt,Tt,ustar,mixture_object)
    #We compute the new barker pressure
    Pbstar=barker_effect_file.barker_effect(probes,mixture_object,Pt,Pe,Te,ustar)[0]
    # Now we compute the derivative using the forward finite difference method
    dqdu = (qstar-q)/delta #derivative of q(Pt,Tt,ue) wrt ue
    dbdu = (Pbstar-Pb)/delta #derivative of Pb(Pt,Pe,Te,ue) wrt ue
    #.................................................
    # DERIVATIVE WRT Tt:
    delta = Tt*jac_diff #we compute the delta for the finite difference
    Ttstar = Tt+delta #we compute the new temperature for the finite difference
    # we compute the new heat flux
    qstar = heat_flux_file.heat_flux(probes,settings,Pt,Ttstar,ue,mixture_object)
    # we compute the new total enthalpy and entropy
    htstar = enthalpy_file.enthalpy(mixture_object, Pt, Ttstar) #we compute the enthalpy at the start
    ststar = entropy_file.entropy(mixture_object, Pt, Ttstar) #we compute the entropy at the start
    # Now we compute the derivative using the forward finite difference method
    dqdtt = (qstar-q)/delta #derivative of q(Pt,Tt,ue) wrt Tt
    dhtdtt = (htstar-ht)/delta  #derivative of ht(Pt,Tt) wrt Tt
    dstdtt = (ststar-st)/delta  #derivative of st(Pt,Tt) wrt Tt
    #.................................................
    # DERIVATIVE WRT Pt: ONLY IF BARKER CORRECTION IS ENABLED
    if (barker != 0):
        delta = Pt*jac_diff
        Ptstar = Pt+delta
        # we compute the new heat flux:
        qstar = heat_flux_file.heat_flux(probes, settings, Ptstar, Tt, ue, mixture_object)
        # we copmute the new total enthalpy and entropy
        htstar = enthalpy_file.enthalpy(mixture_object, Ptstar, Tt)
        ststar = entropy_file.entropy(mixture_object, Ptstar, Tt)
        # we compute the new barker pressure
        Pbstar = barker_effect_file.barker_effect(probes, mixture_object, Ptstar, Pe, Te, ue)[0]
        # we compute the derivative using the forward finite difference method
        dqdpt = (qstar-q)/delta
        dhtdpt = (htstar-ht)/delta
        dstdpt = (ststar-st)/delta
        dbdpt = (Pbstar-Pb)/delta
    else:
        dqdpt = 0
        dhtdpt = 0
        dstdpt = 0
        dbdpt = 0
    #.................................................
    # we now create the jacobian matrix:
    # we inizialize a 4x4 matrix with zeros
    jac = [[0.0 for i in range(4)] for j in range(4)]
    # we fill the matrix with the derivatives according to the theory
    jac[0][0] = 0
    jac[0][1] = dqdu
    jac[0][2] = dqdtt
    jac[1][0] = -dhdte
    jac[1][1] = -ue
    jac[1][2] = dhtdtt
    jac[2][0] = -dsdte
    jac[2][1] = 0
    jac[2][2] = dstdtt
    jac[0][3] = dqdpt
    jac[1][3] = dhtdpt
    jac[2][3] = dstdpt
    jac[3][0] = dbdte 
    jac[3][1] = dbdu
    jac[3][2] = 0
    jac[3][3] = dbdpt
    return jac #we return the jacobian matrix
#.................................................
#   Possible improvements:
#   -Change to a central finite diffence method
#   -Improve order of the derivatives
#.................................................
# EXECUTION TIME: fast
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................