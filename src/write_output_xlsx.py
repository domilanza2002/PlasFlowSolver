#.................................................
#   WRITE_OUTPUT_XLSX.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to write the output file
#   in xlsx format.
#.................................................
import pandas as pd  # Library to write the xlsx file
def write_output_xlsx(output_filename, has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, h_t_out, P_t_out, Re_out, warnings_out, res_out):
    """This function writes the output file in xlsx format.

    Args:
        output_filename (str): the name of the output file
        has_converged_out (bool): the convergence status
        rho_out (float): the density
        T_out (float): the temperature
        h_out (float): the enthalpy
        u_out (float): the velocity
        a_out (float): the speed of sound
        M_out (float): the mach number
        T_t_out (float): the total temperature
        h_t_out (float): the total enthalpy
        P_t_out (float): the total pressure
        Re_out (float): the Reynolds number
        warnings_out (str): the warnings
        res_out (float): the residual
    """
    #Variables:
    input_filename = None  # Input filename
    n_col = None  # Number of columns
    df = None  # Dataframe to edit
    # I rebuild the input file name:
    input_filename=output_filename[:-9]+".xlsx"
    df=pd.read_excel(input_filename, header=[0,1])  #I read the dataframe from the input file
    # Scale the output data:
    for i in range(0, len(rho_out)):
        rho_out[i] = rho_out[i]*1000
        h_out[i] = h_out[i]/1000
        h_t_out[i] = h_t_out[i]/1000
    # I add the new columns to the dataframe
    # HAS CONVERGED
    n_col = len(df.columns)
    df.insert(n_col, ("Output","has converged"), has_converged_out, False) 
    # DENSITY
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","density [g/m^3]"), rho_out, False) 
    # TEMPERATURE
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","temperature [K]"), T_out, False) 
    # ENTHALPY
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","enthalpy [kJ/Kg]"), h_out, False) 
    # VELOCITY
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","velocity [m/s]"), u_out, False)
    # SPEED OF SOUND
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","speed of sound [m/s]"), a_out, False)
    # MACH NUMBER
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","mach number"), M_out, False)
    # TOTAL TEMPERATURE
    n_col = len(df.columns)
    df.insert(n_col, ("Output","total temperature [K]"), T_t_out, False) 
    # TOTAL ENTHALPY
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","total enthalpy [kJ/kg]"), h_t_out, False)
    # TOTAL PRESSURE
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","total pressure [Pa]"), P_t_out, False) 
    # REYNOLDS NUMBER
    n_col = len(df.columns)
    df.insert(n_col, ("Output","reynolds number"), Re_out, False) 
    # WARNINGS
    n_col = len(df.columns) 
    df.insert(n_col, ("Output","warnings"), warnings_out, False) 
    # RESIDUAL
    n_col = len(df.columns)
    df.insert(n_col, ("Output","residual"), res_out, False)
    # I write the dataframe to the output file
    with pd.ExcelWriter(output_filename, mode="w") as writer:  # I open the output file
        df.to_excel(writer, sheet_name="Results") 
#.................................................
#   Possible improvements:
#   None.
#.................................................
# Execution time: Not relevant.
#.................................................
#   Known problems:
#   None.
#.................................................