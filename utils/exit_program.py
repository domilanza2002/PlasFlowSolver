#.................................................
#   EXIT_PROGRAM.PY, v2.0.0, December 2024, Domenico Lanza.
#.................................................
#   This module is needed to clean the temporary
#   files generated by the program.
#.................................................
import os
from utils.mpp_memory_fixer import delete_mixture_file  # Function to delete the mixture file
from utils.classes import ProgramConstants

def clean_files():
    """This function is used to clean the temporary files.
    """
    # Constants
    program_constants = ProgramConstants()
    MIXTURE_NAME = program_constants.TemporaryFiles.TEMP_MIXTURE_NAME
    USE_PREV_ITE_FILENAME = program_constants.TemporaryFiles.USE_PREV_ITE_FILENAME
    X_VAR_FILENAME = program_constants.TemporaryFiles.X_VAR_FILENAME
    Y_VAR_FILENAME = program_constants.TemporaryFiles.Y_VAR_FILENAME
    Z_VAR_FILENAME = program_constants.TemporaryFiles.Z_VAR_FILENAME
    try:
        os.remove(USE_PREV_ITE_FILENAME) 
    except:
        pass
    try: 
        os.remove(X_VAR_FILENAME) 
        os.remove(Y_VAR_FILENAME) 
        os.remove(Z_VAR_FILENAME) 
    except:
        pass
    delete_mixture_file(MIXTURE_NAME)
    return

def exit_program():
    """This function is used to kill the program.
    """
    clean_files()
    print("The program has been killed. Please see the previous errors for more information.")
    exit()

#.................................................
#   Possible improvements:
#   -None
#.................................................
#   KNOW PROBLEMS:
#   None
#.................................................