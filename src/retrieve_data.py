#.................................................
#   RETRIEVE_DATA.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to retrieve the needed
#   data from the dataframe object for the current loop.
#.................................................
from exit_program import exit_program  # Function to exit the program
import retrieve_data_srun as retrieve_data_srun_file  # Module to retrieve the data from the .srun file
import retrieve_data_xlsx as retrieve_data_xlsx_file  # Module to retrieve the data from the .xlsx file
import retrieve_data_filerun as retrieve_data_filerun_file  # Module to retrieve the data from the .in and .pfs files

def retrieve_data(df_object, program_mode, n_case):
    # Variables:
    inputs_object = None  # Inputs object
    initials_object = None  # Initials object
    probes_object = None  # Probes object
    settings_object = None  # Settings object
    warnings = None  # Warnings for the reading process (string)
    
    if (program_mode == 1):  # .srun run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_srun_file.retrieve_data(df_object)
        except Exception as e:
            raise Exception(e)
    elif (program_mode == 2):  # .xlsx run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_xlsx_file.retrieve_data(df_object, n_case)
        except Exception as e:
            print("Error while retrieving the data from the dataframe: "+str(e))
            print("The case number " + str(n_case+1) + " will be skipped.")
            raise Exception(e)
    elif (program_mode == 3):  # File run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_filerun_file.retrieve_data(df_object, n_case)
        except Exception as e:
            print("Error while retrieving the data from the dataframe: "+str(e))
            print("The case number " + str(n_case+1) + " will be skipped.")
            raise Exception(e)
    else:
        print("ERROR: Invalid program mode. You should never see this message...")
        print("The program will now terminate")
        exit_program()
    
    return inputs_object, initials_object, probes_object, settings_object, warnings  # Return the inputs, initials, probes, settings and warnings