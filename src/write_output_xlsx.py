#.................................................
#   WRITE_OUTPUT_XLSX.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to write the output file
#   in xlsx format.
#.................................................
import pandas as pd  # Library to write the xlsx file
def write_output_xlsx(output_filename, out_obj):
    """This function writes the output file in xlsx format.

    Args:
        output_filename (str): the name of the output file
        out_obj (out_properties_class): the object containing all the output properties
    """
    #Variables:
    input_filename = None  # Input filename
    n_col = None  # Number of columns
    df = None  # Dataframe to edit
    n_cases = None  # Number of cases
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
    warnings_out = out_obj.warnings_out  # Warnings
    res_out = out_obj.res_out  # Final convergence criteria
    species_names_out = out_obj.species_names_out  # Names of the species (dictionary)
    species_Y_out = out_obj.species_Y_out  # Mass fractions of the species (dictionary)
    # I rebuild the input file name:
    input_filename=output_filename[:-9]+".xlsx"
    df = pd.read_excel(input_filename, header=[0,1])  #I read the dataframe from the input file
    # Scale the output data:
    for i in range(0, len(rho_out)):
        rho_out[i] = rho_out[i]*1000  # From kg/m^3 to g/m^3
        h_out[i] = h_out[i]/1000  # From J/kg to kJ/kg
        h_t_out[i] = h_t_out[i]/1000  # From J/kg to kJ/kg
        P_t_out[i] = P_t_out[i]/1000  # From Pa to kPa
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
    df.insert(n_col, ("Output","total pressure [kPa]"), P_t_out, False) 
    # REYNOLDS NUMBER
    n_col = len(df.columns)
    df.insert(n_col, ("Output","reynolds number"), Re_out, False) 
    # SPECIES NAMES AND MASS FRACTIONS
    n_cases = len(species_names_out)
    if(len(species_Y_out) != n_cases):
        raise ValueError("The number of cases in the species names and mass fractions dictionaries is different. This should not be possible.")
    for i in range(1,n_cases+1):  # From 1 to n_cases included
        c_species_names = species_names_out[i]  # I extract the current species names
        c_species_Y = species_Y_out[i]  # I extract the current species mass fractions
        if ((c_species_names is None) or (c_species_Y is None)):
            continue
        for j in range(len(c_species_names)):
            c_species_name = c_species_names[j]
            #print(df.columns)
            if ("Output",c_species_name) not in df.columns:
                n_col = len(df.columns)
                df.insert(n_col, ("Output",c_species_name), None, False)
        for j in range(len(c_species_names)):
            c_species_name = c_species_names[j]
            c_species_Y_value = c_species_Y[j]
            df.loc[i-1,("Output",c_species_name)] = c_species_Y_value
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