#.................................................
#   WRITE_OUTPUT_FILERUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to write the output file
#   when the program is file run mode.
#.................................................
import time # Module to retrieve the current date and time
def write_output_filerun(df, output_filename, has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, h_t_out, P_t_out, Re_out, res_out):
    """This function writes the output file when the program is in file run mode.

    Args:
        df (pandas.DataFrame): dataframe containing the input data.
        output_filename (str): name of the output file.
        has_converged_out (list): list containing the convergence status of the solution.
        rho_out (list): list containing the density of the flow.
        T_out (list): list containing the temperature of the flow.
        h_out (list): list containing the enthalpy of the flow.
        u_out (list): list containing the velocity of the flow.
        a_out (list): list containing the speed of sound of the flow.
        M_out (list): list containing the Mach number of the flow.
        T_t_out (list): list containing the total temperature of the flow.
        h_t_out (list): list containing the total enthalpy of the flow.
        P_t_out (list): list containing the total pressure of the flow.
        Re_out (list): list containing the Pitot Reynolds number of the flow.
        res_out (list): list containing the residuals of the solution.
    """
    # Variables:
    comment = None  # Comment (string)
    P = None  # Pressure (float)
    P_dyn = None  # Dynamic pressure (float)
    q_target = None  # Target heat flux (float)
    # Conversion factors:
    P_CF = None  # Static pressure conversion factor (float)
    P_dyn_CF = None  # Dynamic pressure conversion factor (float)
    q_CF = None  # Heat flux conversion factor (float)
    output_file = None  # Output file (file)
    c_date = None  # Current date (string)
    c_time = None  # Current time (string)
    # Retrieve the data from the dataframe:
    comment = df.comment
    P = df.P
    P_dyn = df.P_dyn
    q_target = df.q_target
    P_CF = df.P_CF
    P_dyn_CF = df.P_dyn_CF
    q_CF = df.q_CF
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
    output_file.write("comment                    pressure [Pa]   dyn pressure [Pa]   heat flux [W/m^2]     density [g/m^3]     temperature [K]     enthalpy [kJ/kg]     velocity [m/s]   sound speed [m/s]         Mach number      Total Temp [K] total enth. [kJ/kg] Total pressure [Pa]      Pitot Reynolds\n")
    output_file.close()
    # Write the data in the file:
    output_file = open(output_filename, "a")
    for i in range(len(has_converged_out)):
        while (len(comment[i])<20):  # I want each comment to occupy exactly 20 characters
            comment[i] = comment[i] + " "
        if (rho_out[i] != -1):  # If the case crashed, we just write -1
            P[i] = float(P[i])*P_CF
            P_dyn[i] = float(P_dyn[i])*P_dyn_CF
            q_target[i] = float(q_target[i])*q_CF
        else:
            P[i] = -1
            P_dyn[i] = -1
            q_target[i] = -1
        if (has_converged_out[i] == "yes"):
            # I want each data to occupy exactly 20 characters, in order to have a nice output file
            output_file.write(comment[i]+'{:20.10e}'.format(P[i])+'{:20.10e}'.format(P_dyn[i])+'{:20.10e}'.format(q_target[i])+'{:20.10e}'.format(rho_out[i]*1000)+'{:20.10e}'.format(T_out[i])+'{:20.10e}'.format(h_out[i]/1000)+'{:20.10e}'.format(u_out[i])+'{:20.10e}'.format(a_out[i])+'{:20.10e}'.format(M_out[i])+'{:20.10e}'.format(T_t_out[i])+'{:20.10e}'.format(h_t_out[i]/1000)+'{:20.10e}'.format(P_t_out[i])+'{:20.10e}'.format(Re_out[i])+"\n")
        elif (has_converged_out[i] == "no"):
            output_file.write("WARNING: the next set of data has not converged: residual= " + str(res_out[i] ) +"\n")
            output_file.write(comment[i]+'{:20.10e}'.format(P[i])+'{:20.10e}'.format(P_dyn[i])+'{:20.10e}'.format(q_target[i])+'{:20.10e}'.format(rho_out[i]*1000)+'{:20.10e}'.format(T_out[i])+'{:20.10e}'.format(h_out[i]/1000)+'{:20.10e}'.format(u_out[i])+'{:20.10e}'.format(a_out[i])+'{:20.10e}'.format(M_out[i])+'{:20.10e}'.format(T_t_out[i])+'{:20.10e}'.format(h_t_out[i]/1000)+'{:20.10e}'.format(P_t_out[i])+'{:20.10e}'.format(Re_out[i])+"\n")
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