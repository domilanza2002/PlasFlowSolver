#.................................................
#   WRITE_OUTPUT_SRUN.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to write the output file
#.................................................
def write_output_srun(output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,ht_out,Pt_out,Tt_out,Re_out,warnings_out):
    #.................................................
    #   This function writes the output file
    #.................................................
    #   INPUTS:
    #   output_file_name: the name of the output file
    #   has_converged_out: the convergence status
    #   rho_out: the density
    #   T_out: the temperature
    #   h_out: the enthalpy
    #   u_out: the velocity
    #   a_out: the speed of sound
    #   M_out: the mach number
    #   ht_out: the total enthalpy
    #   Pt_out: the total pressure
    #   Tt_out: the total temperature
    #   Re_out: the Reynolds number
    #   warnings_out: the warnings
    #.................................................
    file = open(output_filename, "w")
    file.write("has_converged_out: "+str(has_converged_out[0])+"\n")
    file.write("rho_out: "+str(rho_out[0])+" Kg/m^3\n")
    file.write("T_out: "+str(T_out[0])+" K\n")
    file.write("h_out: "+str(h_out[0])+" J/Kg\n")
    file.write("u_out: "+str(u_out[0])+" m/s\n")
    file.write("a_out: "+str(a_out[0])+" m/s\n")
    file.write("M_out: "+str(M_out[0])+"\n")
    file.write("ht_out: "+str(ht_out[0])+" J/Kg\n")
    file.write("Pt_out: "+str(Pt_out[0])+" Pa\n")
    file.write("Tt_out: "+str(Tt_out[0])+" K\n")
    file.write("Re_out: "+str(Re_out[0])+"\n")
    file.write("warnings_out: "+str(warnings_out[0])+"\n")
    file.close()