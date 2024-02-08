#.................................................
#   READ_PROBES.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to read the
#   probes properties from the file 
#   "probes.ppb"
#.................................................
import classes as classes_file #import the classes file for the probes class
def read_probes():
    #.................................................
    #   This function reads the probes properties from the file "probes.ppb"
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   probes: the probes object containing the probes properties
    #.................................................
    print("Reading probes...") #print the message to the user
    #VARIABLES:
    FILE_NAME = 'probes.ppb' #standard name of the probes file
    probes=classes_file.probes_class() #create the probes object
    # variables to store:
    Tw=None
    Rp=None
    Rm=None
    Rj=None
    stagtype=None
    hflaw=None
    barker=None
    psfactor=None
    ptfactor=None
    qfactor=None
    stagvar=None
    # start reading the file:
    try: #check for errors
        file = open(FILE_NAME, "r")
        # File has been opened successfully
        if file is None:
            raise Exception("Failed to open file")
    except FileNotFoundError:
        raise Exception("File not found")
    # now we skip 9 lines
    for i in range(9):
        file.readline()
    #there are 31 characters in the line before the data to read
    # reading the wall temperature
    line = file.readline()
    try:
        Tw = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
    except ValueError:
        raise Exception("Invalid wall temperature")
    # reading the pitot external radius
    line = file.readline()
    try:
        Rp = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
    except ValueError:
        raise Exception("Invalid pitot external radius")
    # reading the flux probe external radius
    line = file.readline()
    try:
        Rm = float(line[31:].strip().replace('d', 'e')) # Replace 'd' with 'e' for exponent notation
    except ValueError:
        raise Exception("Invalid flux probe external radius")
    # reading the plasma jet radius
    line = file.readline()
    try:
        Rj = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
    except ValueError:
        raise Exception("Invalid plasma jet radius")
    # reading the stagnation type, flat(for now)
    line = file.readline()
    line_to_analyse= line[31:].strip()
    match line_to_analyse:
        case "flat":
            stagtype=0
        case _:
            raise Exception("Invalid stagnation type")
    # reading the heat flux law, exact(for now)
    line = file.readline()
    line_to_analyse= line[31:].strip()
    match line_to_analyse:
        case "exact":
            hflaw=0
        case _:
            raise Exception("Invalid heat flux law")
    # reading the barker correction type, none or homann(for now)
    line = file.readline()
    line_to_analyse= line[31:].strip()
    match line_to_analyse:
        case "none":
            barker=0
        case "homann":
            barker=1
        case _:
            raise Exception("Invalid barker correction type")
    # reading the static pressure unit factor:
    line = file.readline()
    try:
        psfactor = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
    except ValueError:
        raise Exception("Invalid static pressure unit factor")
    # reading the pitot reading unit factor:
    line = file.readline()
    try:
        ptfactor = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
    except ValueError:
        raise Exception("Invalid pitot reading unit factor")
    # reading the heat flux unit factor:
    line = file.readline()
    try:
        qfactor = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
    except ValueError:
        raise Exception("Invalid heat flux unit factor")
    file.close()
    # calculating the stagnation variable: beta*R/U
    # for now, we implment just the flat plate case
    match stagtype:
        case 0:
            l=Rm/Rj
            if(l<=1):
                den=2-l-1.68*pow((l-1),2)-1.28*pow((l-1),3)
                stagvar=1/den
            else:
                stagvar=1
        case _:
            raise Exception("Option not yet implemented")
    # returning all the variables:
    probes.Tw=Tw
    probes.Rp=Rp
    probes.Rm=Rm
    probes.Rj=Rj
    probes.stagtype=stagtype
    probes.hflaw=hflaw
    probes.barker=barker
    probes.psfactor=psfactor
    probes.ptfactor=ptfactor
    probes.qfactor=qfactor
    probes.stagvar=stagvar
    print("Reading probes...done")
    return probes
#.................................................
#   Possible improvements:
#   -Check for errors in the file
#   -Create a standard file if the file is not found
#   -Create a standard file if the file is not complete
#   -Check if the variables have valid values
#   -Add more variables to customize the probes more
#   -Add more stagnation types computations
#.................................................
# EXECUTION TIME: 0.00011086463928222656=0 seconds, acceptable.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................