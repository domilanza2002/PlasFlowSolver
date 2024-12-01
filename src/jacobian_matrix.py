#.................................................
#   JACOBIAN_MATRIX.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the Jacobian matrix of the system
#   in order to use the Newton-Raphson's method.
#.................................................
import enthalpy as enthalpy_file  # Module to compute the enthalpy
import entropy as entropy_file  # Module to compute the entropy
import barker_effect as barker_effect_file  # Module to compute the Barker's effect
import heat_flux as heat_flux_file  # Module to compute the heat flux
import math
def jacobian_matrix(probes, settings, T, T_t, P, P_t, eps, k,d,mixture_object,sigmas):
    """This function returns the Jacobian matrix of the system in order to use 
    the Newton-Raphson's method.

    Args:
        probes (probes_class): Probes of the system
        settings (settings_class): Settings of the program
        T (float): Flow temperature
        T_t (float): Flow total temperature
        P (float): Flow pressure
        P_t (float): Flow total pressure
        P_b (float): Barker's pressure
        q (float): Stagnation heat flux
        h (float): Flow enthalpy
        h_t (float): Flow total enthalpy
        s (float): Flow entropy 
        s_t (float): Flow total entropy 
        u (float): Flow velocity
        mixture_object (mpp.Mixture): mixture of the case

    Returns:
        jac (square matrix, float): The Jacobian matrix
    """
    # Variables:
    jac = None  # Variable to store the Jacobian matrix of the system
    delta = None  # Variable to store the delta for the finite difference
    T_star = None  # New temperature for the finite difference
    dh_dt = None  # Derivative of h(P, T) w.r.t. T
    ds_dt = None  # Derivative of s(P, T) w.r.t. T
    db_dt = None  # Derivative of P_b(P_t, P, T, u) w.r.t. T
    u_star = None  # New velocity for the finite difference
    dq_du = None  # Derivative of q(P_t, T_t, u) w.r.t. u
    db_du = None  # Derivative of P_b(P_t, P, T, u) w.r.t. u
    T_t_star = None  # New total temperature for the finite difference
    dq_dtt = None  # Derivative of q(P_t, T_t, u) w.r.t. T_t
    dht_dtt = None  # Derivative of h_t(P_t, T_t) w.r.t. T_t
    dst_dtt = None # derivative of s_t(P_t,T_t) w.r.t. T_t
    P_t_star = None  # New total pressure for the finite difference
    dq_dpt = None  # Derivative of q(P_t, T_t, u) w.r.t. P_t
    dht_dpt = None  # Derivative of h_t(P_t, T_t) w.r.t. P_t
    dst_dpt = None  # Derivative of s_t(P_t, T_t) w.r.t. P_t
    db_dpt = None  # Derivative of P_b(P_t, P, T, u) w.r.t. P_t
    h_star = None  # New value for the enthalpy
    h_t_star = None  # New value for the total enthalpy
    s_star = None  # New value for the entropy
    s_t_star = None  # New value for the total entropy
    P_b_star = None  # New value for the barker pressure
    q_star = None  # New value for the heat flux
    # I retrieve some settings from the settings object
    jac_diff = settings.jac_diff  # I get the finite difference epsilon for the Jacobian matrix
    barker_type = probes.barker_type  # Type of Barker's correction
    #.................................................
    M = d/(1+k*math.exp(-eps))  # Mach number
    # DERIVATIVE WRT T:
    delta = T*jac_diff  # Temperature increment for the finite difference
    T_star_1 = T + delta  # New temperature for the finite difference
    T_star_2 = T - delta  # New temperature for the finite difference
    h_star_1 = enthalpy_file.enthalpy(mixture_object, P, T_star_1)
    h_star_2 = enthalpy_file.enthalpy(mixture_object, P, T_star_2)
    s_star_1 = entropy_file.entropy(mixture_object, P, T_star_1)
    s_star_2 = entropy_file.entropy(mixture_object, P, T_star_2)
    mixture_object.equilibrate(T_star_1, P)
    a_star_1 = mixture_object.equilibriumSoundSpeed()
    u_star_1 = M*a_star_1  # Velocity
    mixture_object.equilibrate(T_star_2, P)
    a_star_2 = mixture_object.equilibriumSoundSpeed()
    u_star_2 = M*a_star_2  # Velocity
    P_b_star_1 = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T_star_1, u_star_1)[0]  # I retrieve only the pressure
    P_b_star_2 = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T_star_2, u_star_2)[0]  # I retrieve only the pressure
    q_star_1 = heat_flux_file.heat_flux(probes, settings, P_t, T_t, u_star_1, mixture_object)[0]
    q_star_2 = heat_flux_file.heat_flux(probes, settings, P_t, T_t, u_star_2, mixture_object)[0]
    # Derivatives:
    #dh_dt = (h_star-h)/delta  # Derivative of h(P, T) w.r.t. T
    dh_dt = (h_star_1-h_star_2)/(2*delta)  # Derivative of h(P, T) w.r.t. T
    #ds_dt = (s_star-s)/delta  # Derivative of s(P, T) w.r.t. T
    ds_dt = (s_star_1-s_star_2)/(2*delta)  # Derivative of s(P, T) w.r.t. T
    #db_dt = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. T
    db_dt = (P_b_star_1-P_b_star_2)/(2*delta)  # Derivative of P_b(P_t, P, T, u) w.r.t. T
    #dq_dt = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. T
    dq_dt = (q_star_1-q_star_2)/(2*delta)  # Derivative of q(P_t, T_t, u) w.r.t. T
    # Derivative of a wrt T
    da_dt = (a_star_1-a_star_2)/(2*delta)
    #.................................................
    # DERIVATIVE WRT xi:
    delta = M*jac_diff  # Velocity increment for the finite difference
    M_star_1 = M + delta  # New velocity for the finite difference
    M_star_2 = M - delta  # New velocity for the finite difference
    mixture_object.equilibrate(T, P)
    a = mixture_object.equilibriumSoundSpeed()
    u_star_1 = M_star_1*a  # New velocity
    u_star_2 = M_star_2*a  # New velocity
    q_star_1 = heat_flux_file.heat_flux(probes, settings, P_t, T_t, u_star_1, mixture_object)[0]
    q_star_2 = heat_flux_file.heat_flux(probes, settings, P_t, T_t, u_star_2, mixture_object)[0]
    P_b_star_1 = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T, u_star_1)[0]
    P_b_star_2 = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T, u_star_2)[0]
    # Derivatives:
    #dq_dM = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. u
    dq_dM = (q_star_1-q_star_2)/(2*delta)  # Derivative of q(P_t, T_t, u) w.r.t. u
    dq_dxi = dq_dM*M*(d-M)  # Derivative of q(P_t, T_t, u) w.r.t. xi
    #db_dM = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. u
    db_dM = (P_b_star_1-P_b_star_2)/(2*delta)  # Derivative of P_b(P_t, P, T, u) w.r.t. u
    db_dxi = db_dM*M*(d-M)  # Derivative of P_b(P_t, P, T, u) w.r.t. xi
    #.................................................
    # DERIVATIVE WRT T_t:
    delta = T_t*jac_diff  # Total temperature increment for the finite difference
    T_t_star_1 = T_t + delta  # New total temperature for the finite difference
    T_t_star_2 = T_t - delta  # New total temperature for the finite difference
    mixture_object.equilibrate(T, P)
    a = mixture_object.equilibriumSoundSpeed()
    u = M*a  # Velocity
    q_star_1 = heat_flux_file.heat_flux(probes, settings, P_t, T_t_star_1, u, mixture_object)[0]
    q_star_2 = heat_flux_file.heat_flux(probes, settings, P_t, T_t_star_2, u, mixture_object)[0]
    h_t_star_1 = enthalpy_file.enthalpy(mixture_object, P_t, T_t_star_1)
    h_t_star_2 = enthalpy_file.enthalpy(mixture_object, P_t, T_t_star_2)
    s_t_star_1 = entropy_file.entropy(mixture_object, P_t, T_t_star_1)
    s_t_star_2 = entropy_file.entropy(mixture_object, P_t, T_t_star_2)
    # Derivatives:
    #dq_dtt = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. T_t
    dq_dtt = (q_star_1-q_star_2)/(2*delta)  # Derivative of q(P_t, T_t, u) w.r.t. T_t
    #dht_dtt = (h_t_star-h_t)/delta  # Derivative of h_t(P_t, T_t) w.r.t. T_t
    dht_dtt = (h_t_star_1-h_t_star_2)/(2*delta)  # Derivative of h_t(P_t, T_t) w.r.t. T_t
    #dst_dtt = (s_t_star-s_t)/delta  # Derivative of s_t(P_t, T_t) w.r.t. T_t
    dst_dtt = (s_t_star_1-s_t_star_2)/(2*delta)  # Derivative of s_t(P_t, T_t) w.r.t. T_t
    #.................................................
    # DERIVATIVE WRT P_t: ONLY IF BARKER CORRECTION IS ENABLED
    if (barker_type != 0):
        delta = P_t*jac_diff  # Total pressure increment for the finite difference
        P_t_star_1 = P_t + delta  # New total pressure for the finite difference
        P_t_star_2 = P_t - delta  # New total pressure for the finite difference
        q_star_1 = heat_flux_file.heat_flux(probes, settings, P_t_star_1, T_t, u, mixture_object)[0]
        q_star_2 = heat_flux_file.heat_flux(probes, settings, P_t_star_2, T_t, u, mixture_object)[0]
        h_t_star_1 = enthalpy_file.enthalpy(mixture_object, P_t_star_1, T_t)
        h_t_star_2 = enthalpy_file.enthalpy(mixture_object, P_t_star_2, T_t)
        s_t_star_1 = entropy_file.entropy(mixture_object, P_t_star_1, T_t)
        s_t_star_2 = entropy_file.entropy(mixture_object, P_t_star_2, T_t)
        P_b_star_1 = barker_effect_file.barker_effect(probes, mixture_object, P_t_star_1, P, T, u)[0]  # I retrieve only the pressure
        P_b_star_2 = barker_effect_file.barker_effect(probes, mixture_object, P_t_star_2, P, T, u)[0]  # I retrieve only the pressure
        # Derivatives:
        #dq_dpt = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. P_t
        dq_dpt = (q_star_1-q_star_2)/(2*delta)  # Derivative of q(P_t, T_t, u) w.r.t. P_t
        #dht_dpt = (h_t_star-h_t)/delta  # Derivative of h_t(P_t, T_t) w.r.t. P_t
        dht_dpt = (h_t_star_1-h_t_star_2)/(2*delta)  # Derivative of h_t(P_t, T_t) w.r.t. P_t
        #dst_dpt = (s_t_star-s_t)/delta  # Derivative of s_t(P_t, T_t) w.r.t. P_t
        dst_dpt = (s_t_star_1-s_t_star_2)/(2*delta)  # Derivative of s_t(P_t, T_t) w.r.t. P_t
        #db_dpt = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. P_t
        db_dpt = (P_b_star_1-P_b_star_2)/(2*delta)  # Derivative of P_b(P_t, P, T, u) w.r.t. P_t
    else:
        dq_dpt = 0
        dht_dpt = 0
        dst_dpt = 0
        db_dpt = 0
    #.................................................
    # JACOBIAN MATRIX:
    jac = [[0.0 for i in range(4)] for j in range(4)]  # Initialize the Jacobian matrix
    # According to the system of equations:
    jac[0][0] = dq_dt
    jac[0][1] = dq_dxi
    jac[0][2] = dq_dtt
    jac[1][0] = -dh_dt-0.5*M**2*2*a*da_dt
    jac[1][1] = -0.5*a**2*2*M*M*(d-M)
    jac[1][2] = dht_dtt
    jac[2][0] = -ds_dt
    jac[2][1] = 0
    jac[2][2] = dst_dtt
    jac[0][3] = dq_dpt
    jac[1][3] = dht_dpt
    jac[2][3] = dst_dpt
    jac[3][0] = db_dt 
    jac[3][1] = db_dxi
    jac[3][2] = 0
    jac[3][3] = db_dpt
    #row 1 divided by sigmas[0]
    jac[0][0] = jac[0][0]/sigmas[0]
    jac[0][1] = jac[0][1]/sigmas[0]
    jac[0][2] = jac[0][2]/sigmas[0]
    jac[0][3] = jac[0][3]/sigmas[0]
    #row 2 divided by sigmas[1]
    jac[1][0] = jac[1][0]/sigmas[1]
    jac[1][1] = jac[1][1]/sigmas[1]
    jac[1][2] = jac[1][2]/sigmas[1]
    jac[1][3] = jac[1][3]/sigmas[1]
    #row 3 divided by sigmas[2]
    jac[2][0] = jac[2][0]/sigmas[2]
    jac[2][1] = jac[2][1]/sigmas[2]
    jac[2][2] = jac[2][2]/sigmas[2]
    jac[2][3] = jac[2][3]/sigmas[2]
    #row 4 divided by sigmas[3]
    jac[3][0] = jac[3][0]/sigmas[3]
    jac[3][1] = jac[3][1]/sigmas[3]
    jac[3][2] = jac[3][2]/sigmas[3]
    jac[3][3] = jac[3][3]/sigmas[3]
    #.................................................
    return jac
#.................................................
#   Possible improvements:
#   -Change to a central finite diffence method
#   -Improve order of the derivatives
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................