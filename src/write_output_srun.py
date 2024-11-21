#.................................................
#   WRITE_OUTPUT_SRUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This Module is needed to write the output file.
#.................................................
from classes import CF_constants as CF_constants_class  # Class with the conversion factors
def write_output_srun(output_filename, out_obj):
    """This function writes the output file for the srun mode of the program.

    Args:
        output_filename (str): the name of the output file
        out_obj (out_properties_class): the object containing all the output properties
    """
    # Constants:
    P_CF = CF_constants_class().P_CF  # Conversion factor for the pressure
    # Variables:
    file = None # File object
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
    species_names_out = out_obj.species_names_out[1]  # Names of the species, only 1 element
    species_Y_out = out_obj.species_Y_out[1]  # Mass fractions of the species, only 1 element
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
    file.write("P_t_out: " + str(P_t_out[0]/P_CF) + " kPa\n")  # From Pa to kPa
    file.write("Re_out: " + str(Re_out[0]) + "\n")
    file.write("Kn_out: " + str(Kn_out[0]) + "\n")
    file.write("Species mass fraction composition:\n")
    for i in range(len(species_names_out)):
        file.write(species_names_out[i] + ": " + str(species_Y_out[i]) + "\n")
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