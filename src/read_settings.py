#.................................................
#   READ_SETTINGS.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to read the
#   settings of the program from the file 
#   "settings.ppb"
#.................................................
import classes as classes_file #import the classes file for the settings class
def read_settings(): #function to read the settings from the file "settings.ppb"
    #.................................................
    #   This function reads the settings from the file "settings.ppb"
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   settings: the settings object containing the settings
    #.................................................
    print("Reading settings...") #print the message to the user
    #VARIABLES:
    FILE_NAME = 'settings.ppb' #standard name of the settings file
    settings=classes_file.settings_class() #create the settings object
    # variables to read:
    mixture_name=None #name of the mixture
    default_input_file=None #name of the default input file
    p=None #Number of point for the boundary layer eta discretization
    max_ht_iter=None #maximum number of iterations for the heat transfer
    ht_conv=None #convergence criteria for the heat transfer
    cnvlim=None #convergence criteria for the newton solver
    iterlim=None #maximum number of iterations for the newton solver
    findiff=None #main newton jabobian finite difference epsilon
    max_value_T=None #maximum value for the temperature used for relaxation
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
    #now we read the data
    #there are 31 characters in the line before the data to read
    # MIXTURE NAME: the name of the mixture to use
    line=file.readline()
    mixture_name=line[31:].strip()
    # DEFAULT INPUT FILE: the name of the default input file
    line=file.readline()
    default_input_file=line[31:].strip()
    # P: number of points for the boundary layer eta discretization
    line=file.readline()
    p=int(line[31:].strip())
    # MAX_HT_ITER: maximum number of iterations for the heat transfer
    line=file.readline()
    max_ht_iter=int(line[31:].strip())
    # HT_CONV: convergence criteria for the heat transfer
    line=file.readline()
    ht_conv=float(line[31:].strip().replace('d', 'e'))
    # CNVLIM: convergence criteria for the newton solver
    line=file.readline()
    cnvlim=float(line[31:].strip().replace('d', 'e'))
    # ITERLIM: maximum number of iterations for the newton solver
    line=file.readline()
    iterlim=int(line[31:].strip())
    # FINDIFF: main newton jabobian finite difference epsilon
    line=file.readline()
    findiff=float(line[31:].strip().replace('d', 'e'))
    # MAX_VALUE_T: maximum value for the temperature used for relaxation
    line=file.readline()
    max_value_T=float(line[31:].strip().replace('d', 'e'))
    #.....
    #.....
    #now we change the settings object
    settings.mixture_name=mixture_name
    settings.default_input_file=default_input_file
    settings.p=p
    settings.max_ht_iter=max_ht_iter
    settings.ht_conv=ht_conv
    settings.cnvlim=cnvlim
    settings.iterlim=iterlim
    settings.findiff=findiff
    settings.max_value_T=max_value_T
    #now we close the file
    file.close()
    print("Reading settings...done")
    #now we return the settings object
    return settings
#.................................................
#   Possible improvements:
#   -Check for errors in the file
#   -Create a standard file if the file is not found
#   -Create a standard file if the file is not complete
#   -Check if the variables have valid values
#   -Add more variables to customize the program more
#.................................................
# EXECUTION TIME: 0.00010895729064941406=0 seconds, accepable.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................