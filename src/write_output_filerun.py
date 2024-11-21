#.................................................
#   WRITE_OUTPUT_FILERUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to write the output file
#   when the program is file run mode.
#.................................................
import time # Module to retrieve the current date and time
def write_output_filerun(df, output_filename, out_obj):
    """This function writes the output file when the program is in file run mode.

    Args:
        df (pandas.DataFrame): dataframe containing the input data.
        output_filename (str): name of the output file.
        out_obj (out_properties_class): object containing all the output properties.
    """
    # Variables:
    comment = None  # Comment (string)
    P = None  # Pressure (float)
    P_dyn = None  # Dynamic pressure (float)
    q_target = None  # Target heat flux (float)
    output_file = None  # Output file (file)
    c_date = None  # Current date (string)
    c_time = None  # Current time (string)
    # Extracting the output properties:
    has_converged_out = out_obj.has_converged_out  # Has converged flag
    rho_out = out_obj.rho_out  # Density
    T_out = out_obj.T_out  # Static temperature
    h_out = out_obj.h_out  # Static enthalpy
    u_out = out_obj.u_out  # Flow velocity
    a_out = out_obj.a_out  # Speed of sound
    M_out = out_obj.M_out  # Mach number
    T_t_out = out_obj.T_t_out  # Total temperature
    h_t_out = out_obj.h_t_out  # Total enthalpy
    P_t_out = out_obj.P_t_out  # Total pressure
    Re_out = out_obj.Re_out  # Reynolds number
    Kn_out = out_obj.Kn_out  # Knudsen number
    warnings_out = out_obj.warnings_out  # Warnings
    res_out = out_obj.res_out  # Final convergence criteria
    # Retrieve the data from the dataframe:
    comment = df.comment
    P = df.P  # Already in kPa
    P_dyn = df.P_dyn  # Already in kPa
    q_target = df.q_target  # Already in W/cm^2
    # If the file exists, we append the date and time in the file:
    try:
        output_file = open(output_filename, "r")
        output_file.close() 
        # The file exists, we open it in append mode:
        output_file = open(output_filename, "a")
        c_date = time.strftime("%d/%m/%Y")
        c_time = time.strftime("%H:%M:%S")
        output_file.write("----- Data appended at: " + c_time + " on " + c_date + " -----\n")
    except:  # If the file does not exist, I create it
        output_file = open(output_filename, "w")
    # Header:
    output_file.write("comment                    pressure [kPa]  dyn pressure [kPa]  heat flux [W/cm^2]     density [g/m^3]     temperature [K]     enthalpy [kJ/kg]     velocity [m/s]   sound speed [m/s]         Mach number      Total Temp [K] total enth. [kJ/kg] Total pressure [kPa]     Pitot Reynolds     Warnings:\n")
    output_file.close()
    # OSS: Reynold and Kn not written in the output file
    # Write the data in the file:
    output_file = open(output_filename, "a")
    for i in range(len(has_converged_out)):
        while (len(comment[i])<20):  # I want each comment to occupy exactly 20 characters
            comment[i] = comment[i] + " "
        if (rho_out[i] != -1):  # If the case crashed, we just write -1
            P[i] = float(P[i])
            P_dyn[i] = float(P_dyn[i])
            q_target[i] = float(q_target[i])
        else:
            P[i] = -1
            P_dyn[i] = -1
            q_target[i] = -1
        if (has_converged_out[i] == "yes"):
            # I want each data to occupy exactly 20 characters, in order to have a nice output file
            output_file.write(comment[i]+'{:20.10e}'.format(P[i])+'{:20.10e}'.format(P_dyn[i])+'{:20.10e}'.format(q_target[i])+'{:20.10e}'.format(rho_out[i]*1000)+'{:20.10e}'.format(T_out[i])+'{:20.10e}'.format(h_out[i]/1000)+'{:20.10e}'.format(u_out[i])+'{:20.10e}'.format(a_out[i])+'{:20.10e}'.format(M_out[i])+'{:20.10e}'.format(T_t_out[i])+'{:20.10e}'.format(h_t_out[i]/1000)+'{:20.10e}'.format(P_t_out[i]/1000)+'{:20.10e}'.format(Re_out[i])+"     "+warnings_out[i]+"\n")
        elif (has_converged_out[i] == "no"):
            output_file.write("WARNING: the next set of data has not converged: residual= " + str(res_out[i] ) +"\n")
            output_file.write(comment[i]+'{:20.10e}'.format(P[i])+'{:20.10e}'.format(P_dyn[i])+'{:20.10e}'.format(q_target[i])+'{:20.10e}'.format(rho_out[i]*1000)+'{:20.10e}'.format(T_out[i])+'{:20.10e}'.format(h_out[i]/1000)+'{:20.10e}'.format(u_out[i])+'{:20.10e}'.format(a_out[i])+'{:20.10e}'.format(M_out[i])+'{:20.10e}'.format(T_t_out[i])+'{:20.10e}'.format(h_t_out[i]/1000)+'{:20.10e}'.format(P_t_out[i]/1000)+'{:20.10e}'.format(Re_out[i])+"     "+warnings_out[i]+"\n")
        else:  # Invalid data:
            output_file.write("WARNING: the next set of data is invalid:\n")
            output_file.write(comment[i] + ": Invalid input data detected.\n")
    output_file.close()
#.................................................
#   Possible improvements:
#   None.
#.................................................
# Execution time: Not relevant.
#.................................................
#   Known problems:
#   None.
#.................................................