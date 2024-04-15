#.................................................
#   WRITE_OUTPUT_SRUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This Module is needed to write the output file.
#.................................................
def write_output_srun(output_filename, has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, h_t_out, P_t_out, Re_out, warnings_out, res_out):
    """This function writes the output file for the srun mode of the program.

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
    # Variables:
    file = None # File object
    # Writing the output file:
    file = open(output_filename, "w")
    file.write("has_converged_out: " + str(has_converged_out[0]) + "\n")
    file.write("rho_out: " + str(rho_out[0]*1000) + " g/m^3\n")
    file.write("T_out: " + str(T_out[0]) + " K\n")
    file.write("h_out: " + str(h_out[0]/1000) + " kJ/Kg\n")
    file.write("u_out: " + str(u_out[0]) + " m/s\n")
    file.write("a_out: " + str(a_out[0]) + " m/s\n")
    file.write("M_out: " + str(M_out[0]) + "\n")
    file.write("T_t_out: " + str(T_t_out[0]) + " K\n")
    file.write("h_t_out: " + str(h_t_out[0]/1000) + " kJ/Kg\n")
    file.write("P_t_out: " + str(P_t_out[0]) + " Pa\n")
    file.write("Re_out: " + str(Re_out[0]) + "\n")
    file.write("warnings_out: " + str(warnings_out[0]) + "\n")
    file.write("res_out: " + str(res_out[0]) + "\n")
    file.close()
#.................................................
#   Possible improvements:
#   None.
#.................................................
# Execution time: Not relevant.
#.................................................
#   Known problems:
#   None.
#.................................................