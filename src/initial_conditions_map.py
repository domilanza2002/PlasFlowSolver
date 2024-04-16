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
    
    

def interp_ic_db(ic_db, P, P_dyn, q_target, multiplication_factor):
    
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

    