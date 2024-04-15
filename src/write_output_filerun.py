#.................................................
#   WRITE_OUTPUT_FILERUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to write the output file
#   when the program is file run mode.
#.................................................
import time
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
    comment = df.comment
    P = df.P
    Pdyn = df.Pdyn
    q = df.q
    try:
        output_file=open(output_filename,"r") #we try to open the output file
        output_file.close() #we close the output file
        #if the file exits, we append the date and time in the file
        output_file=open(output_filename,"a") #we open the output file in append mode
        # we retrieve date and time
        c_date = time.strftime("%d/%m/%Y")
        c_time = time.strftime("%H:%M:%S")
        # we write the date and time in the file
        output_file.write("----- Data appended at: "+c_time+" on "+c_date+" -----\n")
    except: #if the file does not exist, we just create it
        output_file=open(output_filename,"w")
    # we write the header of the file
    output_file.write("comment                    pressure [Pa]   dyn pressure [Pa]   heat flux [W/m^2]     density [kg/m3]     temperature [K]     enthalpy [J/kg]      velocity [m/s]   sound speed [m/s]         Mach number  total enth. [J/kg] Total pressure [Pa]      Total Temp [K]      Pitot Reynolds\n")
    output_file.close()

    output_file=open(output_filename,"a")
    for i in range(len(has_converged_out)):
        while (len(comment[i])<20):
            comment[i]=comment[i]+" "
        if (rho_out[i] != -1):
            P[i]=float(P[i])*df.P_CF
            Pdyn[i]=float(Pdyn[i])*df.PD_CF
            q[i]=float(q[i])*df.Q_CF
        else:
            P[i] = -1
            Pdyn[i] = -1
            q[i] = -1
        if (has_converged_out[i] == "yes"):
            # i want each data to occupy exactly 20 characters, in order to have a nice output file
            output_file.write(comment[i]+'{:20.10e}'.format(P[i])+'{:20.10e}'.format(Pdyn[i])+'{:20.10e}'.format(q[i])+'{:20.10e}'.format(rho_out[i])+'{:20.10e}'.format(T_out[i])+'{:20.10e}'.format(h_out[i])+'{:20.10e}'.format(u_out[i])+'{:20.10e}'.format(a_out[i])+'{:20.10e}'.format(M_out[i])+'{:20.10e}'.format(h_t_out[i])+'{:20.10e}'.format(P_t_out[i])+'{:20.10e}'.format(T_t_out[i])+'{:20.10e}'.format(Re_out[i])+"\n")
        elif (has_converged_out[i] == "no"):
            output_file.write("WARNING: the next set of data has not converged: residual= "+str(res_out[i])+"\n")
            output_file.write(comment[i]+'{:20.10e}'.format(P[i])+'{:20.10e}'.format(Pdyn[i])+'{:20.10e}'.format(q[i])+'{:20.10e}'.format(rho_out[i])+'{:20.10e}'.format(T_out[i])+'{:20.10e}'.format(h_out[i])+'{:20.10e}'.format(u_out[i])+'{:20.10e}'.format(a_out[i])+'{:20.10e}'.format(M_out[i])+'{:20.10e}'.format(h_t_out[i])+'{:20.10e}'.format(P_t_out[i])+'{:20.10e}'.format(T_t_out[i])+'{:20.10e}'.format(Re_out[i])+"\n")
        else: #invalid data
            output_file.write("WARNING: the next set of data is invalid:\n")
            output_file.write(comment[i]+": Invalid input data detected\n")