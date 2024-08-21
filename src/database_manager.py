#.................................................
#   DATABASE_MANAGER.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to database creation, update and management.
#.................................................
import pandas as pd

from classes import database_settings_class
from classes import database_class

def db_inputs_init():
    """Function to initialize the database inputs.

    Returns:
        object: the database inputs
    """
    db_inputs = database_class()
    db_inputs.P = []  # Pressure
    db_inputs.P_dyn = []  # Dynamic pressure
    db_inputs.q_target = []  # Target heat flux
    db_inputs.mixture_name = []  # Mixture name
    db_inputs.T_w = []  # Wall temperature
    db_inputs.R_p = []  # Pitot external radius
    db_inputs.R_m = []  # External radius of the heat flux probe
    db_inputs.R_j = []  # Plasma jet radius
    db_inputs.barker_type = []  # Barker's correction type 
    db_inputs.stag_type = []  # Stagnation type
    return db_inputs

def db_inputs_append(db_inputs, inputs_object, probes_object):
    """Function to append the current case inputs to the database inputs.

    Args:
        db_inputs (list): the database inputs
        inputs_object (object): the inputs object
        probes_object (object): the probes object
    """
    # Depackaging the inputs and repackaging them
    db_inputs.P.append(inputs_object.P)
    db_inputs.P_dyn.append(inputs_object.P_dyn)
    db_inputs.q_target.append(inputs_object.q_target)
    db_inputs.mixture_name.append(inputs_object.mixture_name)
    db_inputs.T_w.append(probes_object.T_w)
    db_inputs.R_p.append(probes_object.R_p)
    db_inputs.R_m.append(probes_object.R_m)
    db_inputs.R_j.append(probes_object.R_j)
    db_inputs.barker_type.append(probes_object.barker_type)
    db_inputs.stag_type.append(probes_object.stag_type)
    return db_inputs
def db_inputs_append_null_line(db_inputs):
    """Function to append a line when the data are not valid.

    Args:
        db_inputs (list): the database inputs
    """
    # Depackaging the inputs and repackaging them
    db_inputs.P.append(-1)
    db_inputs.P_dyn.append(-1)
    db_inputs.q_target.append(-1)
    db_inputs.mixture_name.append(-1)
    db_inputs.T_w.append(-1)
    db_inputs.R_p.append(-1)
    db_inputs.R_m.append(-1)
    db_inputs.R_j.append(-1)
    db_inputs.barker_type.append(-1)
    db_inputs.stag_type.append(-1)
    return db_inputs

def pfs_file_detected():
    """This function checks if a database_settings.pfs file is present 
    in the current directory.

    Returns:
        bool: True if the file is present, False otherwise
    """
    FILENAME = "database_settings.pfs"  # Default filename for the database settings file
    file = None  # Temporary file variable
    # I check if the file exists
    try:
        file = open(FILENAME, "r")
        file.close()
        return True
    except:
        return False
    
def read_pfs_file():
    # Variables:
    file = None  # Temporary file variable
    db_settings = database_settings_class()
    if(pfs_file_detected==False):
        raise Exception("FileError: The database_settings.pfs file cannot be read. This should not happen. Check the code.")
    # I open the file
    file = open("database_settings.pfs", "r")
    # I read the file
    # DB name
    line = file.readline()
    db_settings.db_name = line.split(":")[1].strip()  # I take the part of the string after the ":", I strip it
    # CREATE DB FLAG
    line = file.readline()
    db_settings.create_db_flag = line.split(":")[1].strip().lower()  # I take the part of the string after the ":", I strip it
    match db_settings.create_db_flag:  # I check if the flag is valid
        case "true":
            db_settings.create_db_flag = True
        case "1":
            db_settings.create_db_flag = True
        case "false":
            db_settings.create_db_flag = False
        case "0":
            db_settings.create_db_flag = False
        case _:
            return None
    # LOWER TIME FLAG
    line = file.readline()
    db_settings.lower_time_flag = line.split(":")[1].strip().lower()  # I take the part of the string after the ":", I strip it
    match db_settings.lower_time_flag:  # I check if the flag is valid
        case "true":
            db_settings.lower_time_flag = True
        case "1":
            db_settings.lower_time_flag = True
        case "false":
            db_settings.lower_time_flag = False
        case "0":
            db_settings.lower_time_flag = False
        case _:
            return None
    # GENERATE IC FLAG
    line = file.readline()
    db_settings.generate_ic_flag = line.split(":")[1].strip().lower()  # I take the part of the string after the ":", I strip it
    match db_settings.generate_ic_flag:  # I check if the flag is valid
        case "true":
            db_settings.generate_ic_flag = True
        case "1":
            db_settings.generate_ic_flag = True
        case "false":
            db_settings.generate_ic_flag = False
        case "0":
            db_settings.generate_ic_flag = False
        case _:
            return None
    file.close()  # I close the file
    return db_settings

def init_database():
    """Functin to perform the initial operations for the database.

    Returns:
        db_settings (database_settings_class): the database settings
    """
    if (pfs_file_detected()==False):
        return None  # I return None if the file is not present. The database will not be used in this run.
    db_settings = read_pfs_file()  # I read the database settings. If the file is not in the correct format, none is returned.
    return db_settings  

def verify_database(db_name):
    """ Function to verify if a database exists and it is valid.

    Args:
        db_name (str): the name of the database to verify
    """
    # The database is a csv file
    try:
        db = pd.read_csv(db_name)
    except:
        return False
    # The database has the correct columns
    columns = db.columns
    if (columns[0] != "P" or columns[1] != "P_dyn" or columns[2] != "q_target" or columns[3] != "mixture_name" or columns[4] != "T_w" or columns[5] != "R_p"
        or columns[6] != "R_m" or columns[7] != "R_j" or columns[8] != "barker_type" or columns[9] != "stag_type" or columns[10] != "T"
        or columns[11] != "T_t" or columns[12] != "u" or columns[13] != "P_t" or columns[14] != "run_time"):
        return False
    else:
        return True         

def create_database(db_name):
    """ Function to create the database if it does not exist.

    Args:
        db_name (str): the name of the database to create
    """
    # Variables for the columns
    P = []  # Pressure
    P_dyn = []  # Dynamic pressure
    q_target = []  # Target heat flux
    mixture_name = []  # Mixture name
    T_w = []  # Wall temperature
    R_p = []  # Pitot external radius
    R_m = []  # External radius of the heat flux probe
    R_j = []  # Plasma jet radius
    barker_type = []  # Barker's correction type 
    stag_type = []  # Stagnation type
    T = []  # Temperature
    T_t = []  # Total temperature
    u = []  # Velocity
    P_t = []  # Total pressure
    run_time = []  # Run time
    # I create the dictionary
    data = {"P": P, "P_dyn": P_dyn, "q_target": q_target, "mixture_name": mixture_name, "T_w": T_w, "R_p": R_p, "R_m": R_m, "R_j": R_j,
            "barker_type": barker_type, "stag_type": stag_type, "T": T, "T_t": T_t, "u": u, "P_t": P_t, "run_time": run_time}
    # I create the dataframe
    db = pd.DataFrame(data)
    # I save the dataframe
    db.to_csv(db_name, index=False)
    
def database_updater(db_name, db, lower_time_flag):
    """Function to update the database with the new data.

    Args:
        db_name (str): The name of the database
        db (dataframe): The new data to append
        lower_time_flag (bool): The flag to update the run time only if it is lower

    Raises:
        Exception: DatabaseError: The database could not be read. This should not happen. Check the code

    Returns:
        dataframe: The updated database
    """
    # Variables:
    current_db = None  # Dataframe to store the current database
    # I read the current database
    try:
        current_db = pd.read_csv(db_name)
    except:
        raise Exception("DatabaseError: The database could not be read. This should not happen. Check the code.")
    # I concatenate the two dataframes
    if(current_db.empty):
        current_db = db
    else:
        current_db = pd.concat([current_db, db], ignore_index=True)
    # I drop the duplicates
    current_db = current_db.drop_duplicates()
    # I update the run time if needed
    if (lower_time_flag == True):
        current_db = current_db.sort_values(by="run_time", ascending=True)
        current_db = current_db.drop_duplicates(subset=["P", "P_dyn", "q_target", "mixture_name", "T_w", "R_p", "R_m", "R_j", "barker_type", "stag_type"], keep="first")
    # I return the updated database
    return current_db

def generate_ic_map(): #TO DO
    print("To be implemented.")

def update_database(db_settings, db_inputs, out_vars, run_time):
    """This function update the database at the end of the program.
    
    Args:
        db_settings (database_settings_class): Object containing the database settings
        db_inputs (object): Object containing the database inputs
        out_vars (object): Object containing the outputs of the program
        run_time (float): The run times of the simulation
    """
    # Variables:
    db_data = database_class()
    data = None  # Dictionary to store the data
    db = None  # Dataframe to store the data
    updated_db = None  # Dataframe to store the updated database
    # Depackaging the database settings
    db_name = db_settings.db_name
    create_db_flag = db_settings.create_db_flag
    lower_time_flag = db_settings.lower_time_flag
    generate_ic_flag = db_settings.generate_ic_flag
    # Validate the database
    if (verify_database(db_name) == False and create_db_flag == False):
        print("DatabaseError: The database is not valid and the create_db_flag is set to False. The database will not be generated.")
        return
    if (verify_database(db_name) == False and create_db_flag == True):
        create_database(db_name)  # I create the database
        print("The database has been created.")
    # Now we need to update the database
    # Packing all the data
    db_data.P = db_inputs.P
    db_data.P_dyn = db_inputs.P_dyn
    db_data.q_target = db_inputs.q_target
    db_data.mixture_name = db_inputs.mixture_name
    db_data.T_w = db_inputs.T_w
    db_data.R_p = db_inputs.R_p
    db_data.R_m = db_inputs.R_m
    db_data.R_j = db_inputs.R_j
    db_data.barker_type = db_inputs.barker_type
    db_data.stag_type = db_inputs.stag_type
    db_data.T = out_vars.T_out
    db_data.T_t = out_vars.T_t_out
    db_data.u = out_vars.u_out
    db_data.P_t = out_vars.P_t_out
    db_data.has_converged = out_vars.has_converged_out
    db_data.run_time = run_time
    # I create the dictionary
    data = {"P": db_data.P, "P_dyn": db_data.P_dyn, "q_target": db_data.q_target, "mixture_name": db_data.mixture_name, "T_w": db_data.T_w, "R_p": db_data.R_p, "R_m": db_data.R_m, "R_j": db_data.R_j,
            "barker_type": db_data.barker_type, "stag_type": db_data.stag_type, "T": db_data.T, "T_t": db_data.T_t, "u": db_data.u, "P_t": db_data.P_t, "run_time": db_data.run_time, "has_converged": db_data.has_converged}
    # I create the dataframe
    db = pd.DataFrame(data)
    # I delete the rows which did not converge
    db = db[db["has_converged"] == "yes"]
    # I drop the has_converged column
    db = db.drop(columns=["has_converged"])
    # I update the database
    updated_db = database_updater(db_name, db, lower_time_flag)
    # I save the updated database
    updated_db.to_csv(db_name, index=False)
    print("The database has been updated.")
    # If needed, we generate the IC map
    if (generate_ic_flag == True):
        generate_ic_map()
        print("The IC map has been generated.")
    