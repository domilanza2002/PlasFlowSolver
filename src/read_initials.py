#.................................................
#   READ_INITIALS.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to read the
#   initial conditions of the program from the file 
#   "initials.ppb"
#.................................................
import classes as classes_file #import the classes file for the initials class
def read_initials():
    #.................................................
    #   This function reads the initial conditions from the file "initials.ppb"
    #   If the file is not found, the initials are set to default values
    #.................................................
    #   INPUTS:
    #   None.
    #.................................................
    #   OUTPUTS:
    #   initials: the initials object containing the initials
    #.................................................
    print("Reading initials...") #print the message to the user
    #VARIABLES:
    FILE_NAME = 'initials.ppb' #standard name of the initial file
    # variables to return
    initials=classes_file.initials_class() #object with the initials
    # variables to store:
    Tt_0=None #initial total temperature
    T_0=None #initial static temperature
    u_0=None #initial velocity
    Pt_0=None #initial total pressure
    file_opened=True #boolean to check if the file has been opened
    # start reading the file:
    try: #We try to open the file
        file = open(FILE_NAME, "r")
        # File has been opened successfully
        if file is None:
            file_opened=False
            Tt_0=7000.0
            T_0=7000.0
            u_0=900.0
            Pt_0=0.0
    except FileNotFoundError:
        file_opened=False
        Tt_0=7000.0
        T_0=7000.0
        u_0=900.0
        Pt_0=0.0
    if(file_opened==True):
        # now we skip 9 lines
        for i in range(9):
            file.readline()
        #there are 31 characters in the line before the data to read
        # reading the total temperature
        line = file.readline()
        try:
            Tt_0 = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
        except ValueError:
            raise Exception("Invalid total temperature")
        # reading the temperature
        line = file.readline()
        try:
            T_0 = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
        except ValueError:
            raise Exception("Invalid temperature")
        # reading the velocity
        line = file.readline()
        try:
            u_0 = float(line[31:].strip().replace('d', 'e')) # Replace 'd' with 'e' for exponent notation
        except ValueError:
            raise Exception("Invalid velocity")
        # reading the pressure
        line = file.readline()
        try:
            Pt_0 = float(line[31:].strip().replace('d', 'e'))  # Replace 'd' with 'e' for exponent notation
        except ValueError:
            raise Exception("Invalid pressure")
        # As we said before, we could check a little bit better, but for now it is ok
        # we close the file:
        file.close()
    if(file_opened==True):
        print("Initials read from file")
    else:
        print("Initials set to standard values")
    print("Reading initials...done")
    # now we update the iniitials object
    initials.Tt_0=Tt_0
    initials.T_0=T_0
    initials.u_0=u_0
    initials.Pt_0=Pt_0
    # now we return the initials object
    return initials
#.................................................
#   Possible improvements:
#   -Check for errors in the file
#   -Create a standard file if the file is not found
#   -Create a standard file if the file is not complete
#   -Check if the variables have valid values
#.................................................
# EXECUTION TIME: 3.814697265625e-05=0 seconds, acceptable.
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................