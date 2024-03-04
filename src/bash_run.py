#.................................................
#   BASH_RUN.PY, v3.0.0, February 2024, Domenico Lanza.
#.................................................
#   File to detect if a bashrun must be executed.
#.................................................

def bash_file_detected():
    """This function checks if the bash.pfs file is present in the current directory.

    Returns:
        bool: True if the file is present, False otherwise
    """
    #.................................................
    #   This function checks if the bash.pfs file
    #   is present in the current directory.
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   bool: True if the file is present, False otherwise
    #.................................................
    FILENAME = "bash.pfs"
    try:
        open(FILENAME, "r")
        return True
    except:
        return False

def program_mode():
    """This function returns the program mode.

    Raises:
        ValueError: If the program mode is invalid

    Returns:
        int: program_mode, the program mode
    """
    #.................................................
    #   This function returns the program mode.
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   int: program_mode, the program mode
    #.................................................
    # Variables:
    FILENAME = "bash.pfs"
    file = None
    line = None
    file = open(FILENAME, "r")
    line = file.readline()
    # we take the part after the : symbol and strip it
    program_mode = line.split(":")[1].strip()
    file.close()
    match program_mode:
        case "srun":
            return 1
        case "xlsx":
            return 2
        case "in":
            return 3
        case _:
            raise ValueError("Invalid program mode")
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