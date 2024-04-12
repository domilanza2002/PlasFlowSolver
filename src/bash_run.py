#.................................................
#   BASH_RUN.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is used to detect if a bashrun 
#   must be executed.
#.................................................

def bash_file_detected():
    """This function checks if a bash.pfs file is present 
    in the current directory.

    Returns:
        bool: True if the file is present, False otherwise
    """
    FILENAME = "bash.pfs"  # Default filename for the bash file
    file = None  # Temporary file variable
    # I check if the file exists
    try:
        file = open(FILENAME, "r")
        file.close()
        return True
    except:
        return False

def retrieve_program_mode():
    """This function retrieve the program mode
    from the bash.pfs file.

    Raises:
        ValueError: If the program mode is invalid
        FileError: If the bash.pfs cannot be read

    Returns:
        program_mode (int): the program mode
    """
    # Variables:
    FILENAME = "bash.pfs"  # Default filename for the bash file
    file = None  # File variable
    line = None  # Line variable
    
    try:  # I try to open the file
        file = open(FILENAME, "r")
    except:
        raise Exception("FileError: The bash.pfs file cannot be read.")
    line = file.readline()
    program_mode = line.split(":")[1].strip().lower()  # I take the part of the string after the ":", I strip it and I convert it to lowercase
    file.close() 
    match program_mode:  # I check if the program mode is valid, and I return the corresponding integer
        case "srun":
            return 1
        case "xlsx":
            return 2
        case "in":
            return 3
        case _:
            raise ValueError("Invalid program mode.")

def retrieve_filename():
    """This function retrieves the filename from the bash.pfs file.

    Returns:
        str: filename, the filename
    """
    #.................................................
    #   This function retrieves the filename from
    #   the bash.pfs file.
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   str: filename, the filename
    #.................................................
    # Variables:
    FILENAME = "bash.pfs"
    file = None
    filename = None
    line = None
    file = open(FILENAME, "r")
    line = file.readline() # we skip the first line
    line = file.readline()
    # we take the part after the : symbol and strip it
    filename = line.split(":")[1].strip()
    file.close()
    return filename
def retrieve_settings():
    """This function retrieves the settings filename from the bash.pfs file.

    Returns:
        str: settings_filename, the settings filename
    """
    #.................................................
    #   This function retrieves the settings filename from
    #   the bash.pfs file.
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   str: settings_filename, the settings filename
    #.................................................
    # Variables:
    FILENAME = "bash.pfs"
    file = None
    settings_filename = None
    line = None
    file = open(FILENAME, "r")
    line = file.readline() # we skip the first line
    line = file.readline() # we skip the second line
    line = file.readline()
    # we take the part after the : symbol and strip it
    settings_filename = line.split(":")[1].strip()
    file.close()
    return settings_filename