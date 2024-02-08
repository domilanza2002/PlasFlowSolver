#.................................................
#   CLASSES.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This file contains the classes of the program.
#   There are currently 3 classes:
#   -settings_class: class to store all the settings of the program
#   -probes_class: class to store all the probes properties
#   -initials_class: class to store all the initial conditions
#   More classes may be added in the future.
#.................................................
class settings_class: #class to store all the settings of the program
    #.................................................
    #   This class contains the settings of the program, read from the settings.ppb file.
    #   At the moment we just have a basic contructor and all the variables public and set to None at the beginning.
    #   In the future, we may add new contructors, make the varibles private and add getters and setters.
    #   We could also include the read_settings() function in the class
    def __init__(self): #basic constructor
        mixture_name=None #name of the mixture
        default_input_file=None #name of the default input file
        p=None #Number of point for the boundary layer eta discretization(normal coordinate)
        max_ht_iter=None #maximum number of iterations for the heat transfer
        ht_conv=None #convergence criteria for the heat transfer
        cnvlim=None #convergence criteria for the newton solver
        iterlim=None #maximum number of iterations for the newton solver
        findiff=None #main newton jacobian finite difference epsilon
        max_value_T=None #maximum value for the temperature used for relaxation
        # We may add more variables in the future
#.................................................
class probes_class: #class to store all the probes properties
    #   This class contains the properties of the probe, read from the probes.ppb file.
    #   At the moment we just have a basic contructor and all the variables public and set to None at the beginning.
    #   In the future, we may add new contructors, make the varibles private and add getters and setters.
    #   We could also include the read_probes() function in the class
    def __init__(self): #basic constructor
        Tw=None #wall temperature
        Rp=None #pitot external radius
        Rm=None #flux probe external radius
        Rj=None #plasma jet radius
        stagtype=None #stagnation type, flat(for now)
        hflaw=None #heat flux law, 0=exact(for now)
        barker=None #Barker correct, 0=none, 1=homann
        psfactor=None #pressure scale factor
        ptfactor=None #pitot scale factor
        qfactor=None #heat flux scale factor
        stagvar=None #stagnation variable, Beta*R/U
        # We may add more variables in the future
#.................................................
class initials_class: #class to store all the initial conditions
    #   This class contains the initial conditions of the program, read from the initials.ppb file.
    #   At the moment we just have a basic contructor and all the variables public and set to None at the beginning.
    #   In the future, we may add new contructors, make the varibles private and add getters and setters.
    #   We could also include the read_initials() function in the class
    def __init__(self): #basic constructor
        Tt_0=None #initial total temperature
        T_0=None #initial static temperature
        u_0=None #initial velocity
        Pt_0=None #initial total pressure(useful only if the barker effect is considered)
        # we may add more variables in the future
#.................................................
#   Possible improvements:
#   -Add getters and setters and make all the variable private
#   -Add more constructors
#   -Include the read_settings(), read_probes() and read_initials() functions in the classes
#.................................................
# EXECUTION TIME: Not applicable.
#.................................................
#   KNOW PROBLEMS:
#   -None
#.................................................