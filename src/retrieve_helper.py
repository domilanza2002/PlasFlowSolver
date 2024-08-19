#.................................................
#   RETRIEVE_HELPER.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the some 
#   of the data from the dataframe object, in 
#   order to provide an easy customization
#   for the user.
#.................................................
import mutationpp as mpp
import initial_conditions_map as ic_map_file  # Module with the initial conditions map functions
from classes import CF_constants as CF_constants_class  # Class with the conversion factors

def pressure_consistency_check(P, P_dyn, P_stag):
    """This function checks the consistency of the pressures.

    Args:
        P (float): the pressure
        P_dyn (float): the dynamic pressure
        P_stag (float): the stagnation pressure

    Returns:
        bool: True if the pressures are consistent, False otherwise
    """
    # Variables:
    P_TOL = 1e-3  # Tolerance for the pressure difference, P_stag = P + P_dyn
    if (abs(P_stag - P - P_dyn) > P_TOL):
        return False
    else:
        return True

def retrieve_mixture_name(plasma_gas):
    """This function retrieves the mixture name from the plasma gas.

    Args:
        plasma_gas (string): the plasma gas

    Raises:
        ValueError: when an invalid plasma gas is found

    Returns:
        mixture_name (string): the mixture name
    """
    mixture_name = None  # Variable to store the mixture name
    mix_temp = None  # Variable to store the temporary mixture
    match plasma_gas:
        case "n2":
            mixture_name = "nitrogen2"
        case "N2":
            mixture_name = "nitrogen2"
        case "nitrogen2":
            mixture_name = "nitrogen2"
        case "air_13":
            mixture_name = "air_13"
        case "air_11":
            mixture_name = "air_11"
        case _:
            try:
                mix_temp = mpp.Mixture(plasma_gas)
                mixture_name = plasma_gas
            except:
                raise ValueError("Error: Invalid plasma gas. Check the input file.")
    return mixture_name
#...................................................
def retrieve_ic(db_name, P, P_dyn, q_target):
    """This function retrieves the initial conditions from the database.

    Args:
        db_name (string): the database name
        P (float): the pressure
        P_dyn (float): the dynamic pressure
        q_target (float): the target heat flux

    Returns:
        ic_db (initial_conditions_db_class): the initial conditions database object
    """
    # Variables:
    initials_object = None  # Variable to store the initials object
    ic_db = None  # Variable to store the initial conditions database object
    MULTIPLICATION_FACTOR = 1.15  # Multiplication factor for the interpolation
    warnings = None  # Variable to store the warnings
    try:
        ic_db = ic_map_file.load_ic_db(db_name)
    except Exception as e:
        raise ValueError("Error: Cannot read the initial conditions database: " + str(e) + ".")
    try:
        initials_object, warnings = ic_map_file.interp_ic_db(ic_db, P, P_dyn, q_target, MULTIPLICATION_FACTOR)
    except Exception as e:
        raise ValueError("Error: Interpolation failed: " + str(e) + ".")
    
    return initials_object, warnings
#...................................................
def retrieve_stag_type(stag_type_string):
    """This function retrieves the stagnation type.

    Args:
        stag_type_string (string): the stagnation type

    Raises:
        ValueError: when an invalid stagnation type is found

    Returns:
        stag_type (int): the stagnation type
    """
    stag_type = None  # Variable to store the stagtype
    match stag_type_string:
        case "flat":
            stag_type = 0
        case _:
            raise ValueError("Error: Invalid stagnation type. Check the input file.")
    return stag_type
#...................................................

def retrieve_hf_law(hf_law_string):
    """This function retrieves the heat flux law.

    Args:
        hf_law_string (string): the heat flux law

    Raises:
        ValueError: when an invalid heat flux law is found

    Returns:
        hf_law (int): the heat flux law
    """
    hf_law = None  # Variable to store the heat flux law
    match hf_law_string:
            case "exact":
                hf_law = 0
            case "fay_riddell":
                hf_law = 1
            case _:
                raise ValueError("Error: Invalid heat flux law. Check the input file.")
    return hf_law

def retrieve_barker_type(barker_type_string):
    """This function retrieves the Barker's correction type.

    Args:
        barker_type_string (string): the Barker's correction type

    Raises:
        ValueError: when an invalid Barker's correction type is found

    Returns:
        barker_type (int): the Barker's correction type
    """
    barker_type = None  # Variable to store the barker type
    match barker_type_string:
        case "none":
            barker_type = 0
        case "homann":
            barker_type = 1
        case "carleton":
            barker_type = 2
        case _:
            raise ValueError("Error: Invalid Barker's correction type. Check the input file.")
    return barker_type
#...................................................

def retrieve_stag_var(stag_type, R_m, R_j):
    """This function retrieves the stagnation variable.

    Args:
        stag_type (int): the stagnation type
        df (dataframe_class): the dataframe object

    Raises:
        ValueError: when an invalid stagvar is found

    Returns:
        stag_var (float): the stagvar
    """
    stag_var = None  # Variable to store the stagvar
    ratio_L = None  # Variable to store the ratio of the lengths
    den_sv = None  # Variable to store the denominator for the stagvar
    match stag_type:
        case 0:
            ratio_L = R_m/R_j
            if (ratio_L <= 1):
                den_sv= 2 - ratio_L - 1.68 * pow ((ratio_L-1), 2) - 1.28 * pow((ratio_L-1), 3)
                stag_var = 1/den_sv
            else:
                stag_var=ratio_L
        case _:
            raise ValueError("Error: Check the code, you should not be here")
    return stag_var

def retrieve_use_prev_ite(use_prev_ite_string):
    """This function retrieves the use_prev_ite.

    Args:
        use_prev_ite_string (string): the use_prev_ite

    Raises:
        ValueError: when an invalid use_prev_ite is found

    Returns:
        use_prev_ite (int): the use_prev_ite
    """
    use_prev_ite = None  # Variable to store the use_prev_ite
    match use_prev_ite_string:
        case "yes":
            use_prev_ite = 1
        case "no":
            use_prev_ite = 0
        case _:
            raise ValueError("Error: Invalid use_prev_ite. Check the input file.")
    return use_prev_ite

def retrieve_log_warning_hf(log_warning_hf_string):
    """This function retrieves the log_warning_hf.

    Args:
        log_warning_hf_string (string): the log_warning_hf

    Raises:
        ValueError: when an invalid log_warning_hf is found

    Returns:
        log_warning_hf (int): the log_warning_hf
    """
    log_warning_hf = None  # Variable to store the log_warning_hf
    match log_warning_hf_string:
        case "yes":
            log_warning_hf = 1
        case "no":
            log_warning_hf = 0
        case _:
            raise ValueError("Error: Invalid log_warning_hf. Check the input file.")
    return log_warning_hf

def retrieve_converted_inputs(inputs_object, initials_object, probes_object):
    """This function retrieves the converted inputs.
    
    Args:
        inputs_object (inputs_class): the inputs object
        initials_object (initials_class): the initials object
        probes_object (probes_class): the probes object
        
    Returns:
        inputs_object (inputs_class): the converted inputs object
        initials_object (initials_class): the converted initials object
        probes_object (probes_class): the converted probes object
    """
    CF_CONSTANTS = CF_constants_class()  # Object with the conversion factors
    # Conversion of the inputs:
    inputs_object.P *= CF_CONSTANTS.P_CF
    inputs_object.P_dyn *= CF_CONSTANTS.P_CF
    inputs_object.P_stag *= CF_CONSTANTS.P_CF
    inputs_object.q_target *= CF_CONSTANTS.Q_CF
    # Conversion of the initials:
    initials_object.P_t_0 *= CF_CONSTANTS.P_CF
    # Conversion of the probes:
    probes_object.R_p *= CF_CONSTANTS.L_CF
    probes_object.R_m *= CF_CONSTANTS.L_CF
    probes_object.R_j *= CF_CONSTANTS.L_CF
    # Return the objects:
    return inputs_object, initials_object, probes_object