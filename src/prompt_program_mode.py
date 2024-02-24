#.................................................
#   PROMPT_PROGRAM_MODE.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   This file contains the prompt_program_mode() function.
#   This function prompts the user to select the program mode.
#   The user can choose between the following modes:
#   -single run: the program runs once
#   -file run: the program reads the input from a file
#.................................................
def is_int(s):
    try:
        int(s)
        return True
    except:
        return False
def prompt_program_mode():
    """This function prompt the user to choose the program mode.

    Returns:
        int: program_mode, the program mode
    """
    #.................................................
    #   This function prompt the user to choose
    #   the program mode.
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   program_mode: integer, the program mode
    #.................................................
    # Variables:
    program_mode=None #integer, the program mode
    
    # We prompt the user to select the program mode
    print("Please select the program mode:")
    print("1: Single run")
    print("2: File run")
    program_mode=input("Please enter your choice: ")
    # We check if the input is valid
    while ( (is_int(program_mode) == False) or (int(program_mode)!=1 and int(program_mode)!=2)):
        print("Invalid choice. Please enter 1 or 2.")
        program_mode=input("Please enter your choice: ")
    # We return the program mode
    program_mode=int(program_mode)
    return program_mode
#.................................................
#   Possible improvements:
#   None.
#.................................................
#   EXECUTION TIME: Not relevant.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................