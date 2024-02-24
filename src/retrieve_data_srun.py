#.................................................
#   RETRIEVE_DATA_SRUN.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This project file is needed to retrieve the needed
#   data from the dataframe object for the srun case
#.................................................
import classes as classes_file # Module with the classes
def retrieve_data(df):
    #.................................................
    #   This function retrieves the needed data
    #   from the dataframe object for the srun case
    #.................................................
    #   INPUTS:
    #   df: dataframe object
    #   OUTPUTS:
    #   inputs_object: inputs object
    #   initials_object: initials object
    #   probes_object: probes object
    #   settings_object: settings object
    #   warnings: warnings
    #.................................................
    # we define some variables:
    inputs_object = None # variable to store the inputs object
    initials_object = None # variable to store the initials object
    probes_object = None # variable to store the probes object
    settings_object = None # variable to store the settings object
    warnings = None # variable to store the warnings
    stagvar = None # variable to store the stagvar
    # we create the objects
    inputs_object = classes_file.inputs_class() # we create the inputs object
    initials_object = classes_file.initials_class() # we create the initials object
    probes_object = classes_file.probes_class() # we create the probes object
    settings_object = classes_file.settings_class() # we create the settings object
    warnings = "None"
    # we retrieve the data
    inputs_object.comment = df.comment
    inputs_object.P = df.P
    inputs_object.Pdyn = df.Pdyn
    inputs_object.Pstag = df.Pstag
    inputs_object.q = df.q
    inputs_object.plasma_gas = df.plasma_gas
    inputs_object.P_CF = df.P_CF
    inputs_object.PD_CF = df.PD_CF
    inputs_object.PS_CF = df.PS_CF
    inputs_object.Q_CF = df.Q_CF
    initials_object.T_0 = df.T_0
    initials_object.Tt_0 = df.Tt_0
    initials_object.u_0 = df.u_0
    initials_object.Pt_0 = df.Pt_0
    probes_object.Tw = df.Tw
    probes_object.Rp = df.Rp
    probes_object.Rm = df.Rm
    probes_object.Rj = df.Rj
    probes_object.stagtype = df.stagtype
    probes_object.hflaw = df.hflaw
    probes_object.barker = df.barker
    match probes_object.stagtype:
        case 0:
            l=probes_object.Rm/probes_object.Rj
            if(l<=1):
                den=2-l-1.68*pow((l-1),2)-1.28*pow((l-1),3)
                stagvar=1/den
            else:
                stagvar=1
        case _:
            raise ValueError("Error: Check the code, you should not be here")
    probes_object.stagvar = stagvar
    settings_object.p = df.p
    settings_object.max_hf_iter = df.max_hf_iter
    settings_object.hf_conv = df.hf_conv
    settings_object.use_prev_ite = df.use_prev_ite
    settings_object.newton_conv = df.newton_conv
    settings_object.max_newton_iter = df.max_newton_iter
    settings_object.jac_diff = df.jac_diff
    settings_object.max_T_relax = df.max_T_relax
    settings_object.min_T_relax = df.min_T_relax
    # we return the result
    return inputs_object, initials_object, probes_object, settings_object, warnings