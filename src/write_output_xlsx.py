#.................................................
#   WRITE_OUTPUT_XLSX.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file is needed to write the output file
#.................................................
import pandas as pd #we import the pandas library to write the output file
def write_output_xlsx(output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,ht_out,Pt_out,Tt_out,Re_out,warnings_out):
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
    #   OUTPUTS:
    #   None
    #.................................................
    #Variables:
    input_filename=None #name of the input file
    n_col=None #number of columns
    df=None #dataframe we edit)
    #we rebuild the input file name: the input file was "name".xlsx, the output file is "name_out.xlsx"
    input_filename=output_filename[:-9]+".xlsx" #we rebuild the input file name
    #we retrieve the dataframe from the input file
    df=pd.read_excel(input_filename, header=[0,1]) #we read the dataframe from the input file
    #we add the new columns to the dataframe
    # HAS CONVERGED
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","has converged"),has_converged_out,False) #we add the new column to the dataframe
    # DENSITY
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","density [kg/m^3]"),rho_out,False) #we add the new column to the dataframe
    # TEMPERATURE
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","temperature [K]"),T_out,False) #we add the new column to the dataframe
    # ENTHALPY
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","enthalpy [J/Kg]"),h_out,False) #we add the new column to the dataframe
    # VELOCITY
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","velocity [m/s]"),u_out,False) #we add the new column to the dataframe
    # SPEED OF SOUND
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","speed of sound [m/s]"),a_out,False) #we add the new column to the dataframe
    # MACH NUMBER
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","mach number"),M_out,False) #we add the new column to the dataframe
    # TOTAL ENTHALPY
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","total enthalpy [J/kg]"),ht_out,False) #we add the new column to the dataframe
    # TOTAL PRESSURE
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","total pressure [Pa]"),Pt_out,False) #we add the new column to the dataframe
    # TOTAL TEMPERATURE
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","total temperature [K]"),Tt_out,False) #we add the new column to the dataframe
    # REYNOLDS NUMBER
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","reynolds number"),Re_out,False) #we add the new column to the dataframe
    # WARNINGS
    n_col=len(df.columns) #we retrieve the number of columns
    df.insert(n_col,("Output","warnings"),warnings_out,False) #we add the new column to the dataframe
    #we write the dataframe to the output file
    with pd.ExcelWriter(output_filename,mode="w") as writer: #we open the output file
        df.to_excel(writer,sheet_name="Sheet1") #we write the dataframe to the output file