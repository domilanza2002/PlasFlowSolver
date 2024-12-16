#.................................................
#   JACOBIAN_MATRIX.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to compute the Jacobian matrix of the system
#   in order to use the Newton-Raphson's method.
#.................................................
import thermodyn as thermodyn_file  # Module to compute the enthalpy
import barker_effect as barker_effect_file  # Module to compute the Barker's effect
import heat_flux as heat_flux_file  # Module to compute the heat flux
def jacobian_matrix(probes, settings, T, T_t, P, P_t, P_b, q, h, h_t, s, s_t, u, mixture_object):
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
    # DERIVATIVE WRT T:
    delta = T*jac_diff  # Temperature increment for the finite difference
    T_star = T + delta  # New temperature for the finite difference
    h_star = thermodyn_file.enthalpy(mixture_object, P, T_star)
    s_star = thermodyn_file.entropy(mixture_object, P, T_star)
    P_b_star = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T_star, u)[0]  # I retrieve only the pressure
    # Derivatives:
    dh_dt = (h_star-h)/delta  # Derivative of h(P, T) w.r.t. T
    ds_dt = (s_star-s)/delta  # Derivative of s(P, T) w.r.t. T
    db_dt = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. T
    #.................................................
    # DERIVATIVE WRT u:
    delta = u*jac_diff  # Velocity increment for the finite difference
    u_star = u + delta  # New velocity for the finite difference
    q_star = heat_flux_file.heat_flux(probes, settings, P_t, T_t, u_star, mixture_object)[0]
    P_b_star = barker_effect_file.barker_effect(probes, mixture_object, P_t, P, T, u_star)[0]
    # Derivatives:
    dq_du = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. u
    db_du = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. u
    #.................................................
    # DERIVATIVE WRT T_t:
    delta = T_t*jac_diff  # Total temperature increment for the finite difference
    T_t_star = T_t + delta  # New total temperature for the finite difference
    q_star = heat_flux_file.heat_flux(probes, settings, P_t, T_t_star, u, mixture_object)[0]
    h_t_star = thermodyn_file.enthalpy(mixture_object, P_t, T_t_star)
    s_t_star = thermodyn_file.entropy(mixture_object, P_t, T_t_star)
    # Derivatives:
    dq_dtt = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. T_t
    dht_dtt = (h_t_star-h_t)/delta  # Derivative of h_t(P_t, T_t) w.r.t. T_t
    dst_dtt = (s_t_star-s_t)/delta  # Derivative of s_t(P_t, T_t) w.r.t. T_t
    #.................................................
    # DERIVATIVE WRT P_t: ONLY IF BARKER CORRECTION IS ENABLED
    if (barker_type != 0):
        delta = P_t*jac_diff  # Total pressure increment for the finite difference
        P_t_star = P_t + delta  # New total pressure for the finite difference
        q_star = heat_flux_file.heat_flux(probes, settings, P_t_star, T_t, u, mixture_object)[0]
        h_t_star = thermodyn_file.enthalpy(mixture_object, P_t_star, T_t)
        s_t_star = thermodyn_file.entropy(mixture_object, P_t_star, T_t)
        P_b_star = barker_effect_file.barker_effect(probes, mixture_object, P_t_star, P, T, u)[0]  # I retrieve only the pressure
        # Derivatives:
        dq_dpt = (q_star-q)/delta  # Derivative of q(P_t, T_t, u) w.r.t. P_t
        dht_dpt = (h_t_star-h_t)/delta  # Derivative of h_t(P_t, T_t) w.r.t. P_t
        dst_dpt = (s_t_star-s_t)/delta  # Derivative of s_t(P_t, T_t) w.r.t. P_t
        db_dpt = (P_b_star-P_b)/delta  # Derivative of P_b(P_t, P, T, u) w.r.t. P_t
    else:
        dq_dpt = 0
        dht_dpt = 0
        dst_dpt = 0
        db_dpt = 0
    #.................................................
    # JACOBIAN MATRIX:
    jac = [[0.0 for i in range(4)] for j in range(4)]  # Initialize the Jacobian matrix
    # According to the system of equations:
    jac[0][0] = 0
    jac[0][1] = dq_du
    jac[0][2] = dq_dtt
    jac[1][0] = -dh_dt
    jac[1][1] = -u
    jac[1][2] = dht_dtt
    jac[2][0] = -ds_dt
    jac[2][1] = 0
    jac[2][2] = dst_dtt
    jac[0][3] = dq_dpt
    jac[1][3] = dht_dpt
    jac[2][3] = dst_dpt
    jac[3][0] = db_dt 
    jac[3][1] = db_du
    jac[3][2] = 0
    jac[3][3] = db_dpt
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