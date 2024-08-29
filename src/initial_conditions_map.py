#.................................................
#   INITIAL_CONDITIONS_MAP.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to manage the initial
#   conditions database map.
#.................................................
import h5py  # Library to manage the database files
import numpy as np  # Library to manage arrays
import scipy.interpolate as scipy_int  # Library to interpolate data
import classes as classes_file  # Module with the classes

def verify_db(db_name):
    """This function verifies if the database specified
    by the user exists and it is accessible.

    Args:
        db_name (string): the name of the database
        
    Returns:
        bool: True if the database exists and it is accessible, False otherwise
    """
    # Variables:
    tmp = None  # Temporary variable
    try:
        with h5py.File(db_name, 'r') as f:
            tmp = f['points'][:]
            tmp = f['values'][:]
        return True
    except:
        return False
    
def load_ic_db(db_name):
    """This function loads the initial conditions database
    from the file specified by the user.

    Args:
        db_name (string): the name of the database

    Returns:
        ic_db (initial_conditions_db_class): the initial conditions database object
    """
    # Variables:
    ic_db = None  # Initial conditions database
    points = None  # Points of the database
    values = None  # Values of the database
    
    # I create the object
    ic_db = classes_file.initial_conditions_db_class()
    with h5py.File(db_name, 'r') as f:
        points = f['points'][:]
        values = f['values'][:]
    
    ic_db.db_inputs = points
    ic_db.db_outputs = values
    
    return ic_db

def depack_db_to_ic_obj(db_obj):
    """This function depacks the database object(dataframe) to the initial conditions variables
    needed for the ic map.

    Args:
        db_obj (dataframe): the database object
    """
    # Variables:
    P = None  # Static pressure
    P_dyn = None  # Dynamic pressure
    q_target = None  # Target heat flux
    T = None  # Initial static temperature
    T_t = None  # Initial total temperature
    u = None  # Initial flow velocity
    # I extract the data
    P = db_obj["P"].tolist()
    P_dyn = db_obj["P_dyn"].tolist()
    q_target = db_obj["q_target"].tolist()
    T = db_obj["T"].tolist()
    T_t = db_obj["T_t"].tolist()
    u = db_obj["u"].tolist()
    return P, P_dyn, q_target, T, T_t, u
    
    
def create_ic_db_from_p_and_v(filename, points, values):
    """This function creates the initial conditions database
    file.

    Args:
        filename (string): the name of the ic map file
        points (numpy array): the points of the database
        values (numpy array): the values of the database
    """
    # Variables:
    f = None  # File object
    # I create the ic map file
    f = h5py.File(filename, 'w')
    f.create_dataset('points', data=points)
    f.create_dataset('values', data=values)
    f.close()
    
def create_ic_db(filename, db_obj):
    """This function creates the initial conditions database
    file.

    Args:
        filename (string): the name of the ic map file
        points (numpy array): the points of the database
        values (numpy array): the values of the database
    """
    # Variables:
    f = None  # File object
    points = None  # Points of the database
    values = None  # Values of the database
    P = None  # Static pressure
    P_dyn = None  # Dynamic pressure
    q_target = None  # Target heat flux
    T_0 = None  # Initial static temperature
    T_t_0 = None  # Initial total temperature
    u_0 = None  # Initial flow velocity
    # I extract the data
    P, P_dyn, q_target, T_0, T_t_0, u_0 = depack_db_to_ic_obj(db_obj)
    # I create the arrays
    P = np.array(P).flatten()
    P_dyn = np.array(P_dyn).flatten()
    q_target = np.array(q_target).flatten()
    T_0 = np.array(T_0).flatten()
    T_t_0 = np.array(T_t_0).flatten()
    u_0 = np.array(u_0).flatten()
    # I create the points and values arrays
    points = np.array([P, P_dyn, q_target]).T
    values = np.array([T_0, T_t_0, u_0]).T
    # I create the ic map file
    create_ic_db_from_p_and_v(filename, points, values)

def concatenate_ic_db(db_obj1, db_obj2):
    """This function concatenates two initial conditions
    database objects.

    Args:
        db_obj1 (initial_conditions_db_class): the first initial conditions database object
        db_obj2 (initial_conditions_db_class): the second initial conditions database object

    Returns:
        ic_db (initial_conditions_db_class): the initial conditions database object
    """
    # Constants:
    N = 3  # Number of decimal digits
    # Variables:
    ic_db = None  # Initial conditions database
    points = None  # Points of the database
    values = None  # Values of the database
    
    # I create the object
    ic_db = classes_file.initial_conditions_db_class()
    # I concatenate the data
    points = np.concatenate((db_obj1.db_inputs, db_obj2.db_inputs), axis=0)
    values = np.concatenate((db_obj1.db_outputs, db_obj2.db_outputs), axis=0)
    # I delete the duplicates rows with the same points
    points, indices = np.unique(np.round(points, N), axis=0, return_index=True)
    values = values[indices]
    # I assign the data
    ic_db.db_inputs = points
    ic_db.db_outputs = values
    # I return the object
    return ic_db

def update_ic_db(ic_obj, db_obj):
    """This function updates the initial conditions database with a new db object.

    Args:
        db_obj (_type_): _description_
        ic_obj (_type_): _description_
    """
    # Variables:
    new_ic_db = None  # New initial conditions database
    P = None  # Static pressure
    P_dyn = None  # Dynamic pressure
    q_target = None  # Target heat flux
    T = None  # Initial static temperature
    T_t = None  # Initial total temperature
    u = None  # Initial flow velocity
    # I initialize the new database
    new_ic_db = classes_file.initial_conditions_db_class()
    # I extract the data
    P, P_dyn, q_target, T, T_t, u = depack_db_to_ic_obj(db_obj)
    # I create the new arrays
    P = np.array(P).flatten()
    P_dyn = np.array(P_dyn).flatten()
    q_target = np.array(q_target).flatten()
    T = np.array(T).flatten()
    T_t = np.array(T_t).flatten()
    u = np.array(u).flatten()
    # I create the new points and values arrays
    new_ic_db.db_inputs = np.array([P, P_dyn, q_target]).T
    new_ic_db.db_outputs = np.array([T, T_t, u]).T
    # I concatenate the data
    new_ic_db = concatenate_ic_db(ic_obj, new_ic_db)
    # I return the new database
    return new_ic_db
    
    

def interp_ic_db(ic_db, P, P_dyn, q_target, multiplication_factor):
    """This function interpolates the initial conditions
    database to retrieve the initial conditions for the
    current case.

    Args:
        ic_db (initial_conditions_db_class): the initial conditions database object
        P (float): the static pressure
        P_dyn (float): the dynamic pressure
        q_target (float): the target heat flux
        multiplication_factor (float): the multiplication factor for the initial conditions

    Returns:
        initial_conditions (initials_class): the initial conditions object
        warnings (string): the warnings
    """
    # Variables:
    initial_conditions = None  # Initial conditions object
    int_point = None  # Interpolation point
    points = None  # Points of the database
    values = None  # Values of the database
    T_0 = None  # Initial static temperature
    T_t_0 = None  # Initial total temperature
    u_0 = None  # Initial flow velocity
    warnings = None  # Warnings
    
    initial_conditions = classes_file.initials_class()
    int_point = [P, P_dyn, q_target]
    points = ic_db.db_inputs
    values = ic_db.db_outputs
    T_0 = scipy_int.griddata(points, values[:,0], int_point, method='linear', fill_value=-1.0)
    T_t_0 = scipy_int.griddata(points, values[:,1], int_point, method='linear', fill_value=-1.0)
    u_0 = scipy_int.griddata(points, values[:,2], int_point, method='linear', fill_value=-1.0)
    
    if (T_0 == -1.0 or T_t_0 == -1.0 or u_0 == -1.0):  # If the linear interpolation fails, I use the nearest interpolation
        T_0 = scipy_int.griddata(points, values[:,0], int_point, method='nearest')
        T_t_0 = scipy_int.griddata(points, values[:,1], int_point, method='nearest')
        u_0 = scipy_int.griddata(points, values[:,2], int_point, method='nearest')
        warnings = "Linear interpolation failed, nearest interpolation used.|"
    # I create the object
    initial_conditions.T_0 = T_0[0]*multiplication_factor
    initial_conditions.T_t_0 = T_t_0[0]*multiplication_factor
    initial_conditions.u_0 = u_0[0]*multiplication_factor
    initial_conditions.P_t_0 = P + P_dyn
    # I return the object
    return initial_conditions, warnings

    