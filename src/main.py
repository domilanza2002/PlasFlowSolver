#.................................................
#       PlasFlowSolver Program
#       main.py: main script
#       Version 1.0.0, Domenico Lanza
#.................................................
# LIBRARY IMPORTS:
# I import here the libraries I will use in the program
# Standard library imports:
import math  # Standard library for math operations
import time  # Standard library for time tracking operations
#   Third party library imports:
import numpy as np  # Third party library for math operations
import mutationpp as mpp  # Third party library for thermodynamic computations
# Project file imports:
# I import here all the modules I will use in the program
# The format for the import is: "import filename as filename_file"
import classes as classes_file  # Module with all the classes that I will use in the program
import presentation as presentation_file  # Module to print the presentation of the program
import prompt_program_mode as prompt_program_mode_file  # Module to prompt the program mode to the user
import bash_run as bash_run_file  # Module to execute a bashrun
import read_data as read_data_file  # Module to read the data from the input file
import retrieve_data as retrieve_data_file  # Module to retrieve the data from the dataframe
import heat_flux as heat_flux_file  # Module to compute the stagnation heat flux
import enthalpy as enthalpy_file  # Module to compute the flow enthalpy
import entropy as entropy_file  # Module to compute the flow entropy
import barker_effect as barker_effect_file  # Module to compute the Barker's effect
import jacobian_matrix as jacobian_matrix_file  # Module to compute the Jacobian matrix of the system of equations
import system_solve as system_solve_file  # Module to solve the system of equations
import out_properties as out_properties_file  # Module to compute the output properties
import write_output_srun as write_output_srun_file  # Module to write the output file in a .srun run
import write_output_xlsx as write_output_xlsx_file  # Module to write the output file in a .xlsx run
import write_output_filerun as write_output_filerun_file  # Module to write the output file in a .in run
import database_manager as database_manager_file  # Module to manage the database
from exit_program import exit_program, clean_files  # Module to kill and clean the program
from mpp_memory_fixer import fix_mpp_memory_leak  # Module to fix the memory leak
#.................................................
# PROGRAM VARIABLES:
# I declare here all the variables I will use in this script
# Variables to manage the program mode:
program_mode = None  # Variable to store the program mode
bash_run = None  # Variable to store if a bashrun has to be executed
t1 = None  # Variable to store the time at the beginning of the program
t2 = None  # Variable to store the time at the end of the program
# Variables for the output file:
output_filename = None  # Name of the output file
# Dataframe variables:
n_lines = None  # Number of lines of the dataframe
check = None  # Variable to check if the line must be skipped
# Counter variables:
n_case = None  # Counter of the number of cases to be run
# Input variables read from the file:
comment = None  # Comment of the case
P = None  # Static pressure of the flow
P_stag = None  # Stagnation pressure ("Target" if the Barker's effect is considered) of the flow
q_target = None  # Target stagnation heat flux
mixture_name = None # Mixture name
warnings = None  # Warnings due to the input file
# Newton loop variables:
iter = None  # Current number of iterations
max_newton_iter = None  # Maximum number of iterations for the Newton loop
has_converged = None  # Boolean to check if the iteration has converged
res = None  # Residuals array
cnv = None  # Current convergence criteria
cnv_ref = None  # Reference convergence criteria
jac = None  # Jacobian matrix of the system
d_vars = None  # Variable to store the variable increments
n_eq = None  # Number of equations to solve
relax = None  # Relaxation factor
# Newton loop thermodynamic variables:
mixture_object = None  #Mixture object from Mutation++ library
q = None  # Current stagnation heat flux
P_t = None  # Current total pressure of the flow
P_b = None  # Current Barker's effect pressure (Current stagnation pressure) (P_b = P_t+0.5*rho*pow(u,2)*Cp)
T = None  # Current static temperature of the flow
T_t = None  # Current total temperature of the flow
u = None  # Current flow speed
h = None  # Current flow enthalpy
h_t = None  # Current flow stagnation enthalpy
s = None  # Current flow entropy
s_t = None  # Current flow stagnation entropy
T_star = None  # Variable to store the new T value, before the relaxation
u_star = None  # Variable to store the new u value, before the relaxation
T_t_star = None  # Variable to store the new T_t value, before the relaxation
P_t_star = None  # Variable to store the new P_t value, before the relaxation
Re = None  # Pitot Reynolds number for the Barker's effect
# Output properties:
rho = None  # Final density of the flow
a = None  # Final sound speed of the flow
M = None  # Final Mach number of the flow
species_names = None  # Names of the species
species_Y = None  # Mass fractions of the species
has_converged_out = None  # Variable to store if the iteration has converged
rho_out = None  # Edge density to be written on the output file
T_out = None  # Edge temperature to be written on the output file
h_out = None  # Edge enthalpy to be written on the output file
u_out = None  # Edge velocity to be written on the output file
a_out = None  # Edge sound speed to be written on the output file
M_out = None  # Edge Mach number to be written on the output file
T_t_out = None  # Total temperature to be written on the output file
h_t_out = None  # Total enthalpy to be written on the output file
P_t_out = None  # Total pressure to be written on the output file
Re_out = None  # Pitot Reynolds number to be written on the output file
warnings_out=None  # Warnings to be written on the output file
res_out = None  # Final convergence criteria to be written on the output file
species_names_out = None  # Names of the species
species_Y_out = None  # Mass fractions of the species
# Variables to manage the heat flux computation:
exit_due_error = None  # Variable to exit the Newton loop if an error occurs during the computation
hf_first_comp = None  # Variable to store if it is the first time that we compute the heat flux for the current case
# Variable to manage the database
db_settings = None  # Database settings object
db_used = None  # Flag to indicate if the database is used
t_start_case = None  # Variable to store the time at the beginning of the case
t_end_case = None  # Variable to store the time at the end of the case
run_time_vect = None  # Vector to store the run time of each case
db_inputs = None  # Database inputs
#
#.................................................
# CLASS INSTANCES:
# I will create here the instances of the classes I will use in the program
inputs_object = classes_file.inputs_class()  # Object with the inputs for the current iteration
settings_object = classes_file.settings_class()  # Object with the settings for the current iteration
probes_object = classes_file.probes_class()  # Object with the probe properties for the current iteration
initials_object = classes_file.initials_class()  # Object with the initial conditions for the current iteration
df_object = classes_file.dataframe_class()  # Object to store the dataframe, independently from the program mode
out_object = classes_file.out_properties_class()  # Object to store the output properties
db_settings = classes_file.database_settings_class()  # Object to store the database settings
db_inputs = classes_file.database_inputs_class()  # Object to store the database inputs
#.................................................
#
#   Here the program starts
t1 = time.time()  # I store the time at the beginning of the program, to keep track of the execution time
presentation_file.presentation()  # I call the presentation module, to present the program to the user
# Fix the memory leak in the MPP library:
fix_mpp_memory_leak()
# Bashrun check:
bash_run = bash_run_file.bash_file_detected()  # I check if a bashrun has to be executed
if (bash_run == False):  # If the program is in manual mode
    print("No valid bash.pfs file detected, the program will run in manual mode.")
    program_mode = prompt_program_mode_file.prompt_program_mode()  # I prompt the user for the program mode
else:  # If the program is in bash mode
    print("A valid bash.pfs file detected, the program will run in bash mode.")
    try:
        program_mode = bash_run_file.retrieve_program_mode()  # I retrieve the program mode from the bashrun file
    except Exception as e:
        print("Invalid program mode: "+str(e))
        print("The program will continue in normal mode")
        program_mode = prompt_program_mode_file.prompt_program_mode()  # I prompt the program mode to the user
        bash_run = False  # I set the program to manual mode
# Database check:
db_settings = database_manager_file.init_database()  # The initial operations for the database are performed
if (db_settings is None):
    db_used = False
    print("No valid database_settings.pfs file detected, the program will not use the database.")
else:
    db_used = True
    print("A valid database_settings.pfs file detected, the program will use the database.")
    db_inputs = database_manager_file.db_inputs_init()  # The initial operations for the database inputs are performed
# Now I read the data:
try:
    df_object, output_filename = read_data_file.read_data(program_mode, bash_run)
except Exception as e:
    print(e)
    print("The program will now terminate.")
    exit_program()
    
#.................................................
#   MAIN PROGRAM LOOP:
#   Here the main program loop starts.
n_case = 0
n_lines = df_object.n  # I store the number of cases to be executed
print("Number of cases to be executed: "+str(n_lines)+".")
# I initialize the output vectors
run_time_vect = []
has_converged_out = []
rho_out = []
T_out = []
h_out = []
u_out = []
a_out = []
M_out = []
T_t_out = []
h_t_out = []
P_t_out = []
Re_out = []
warnings_out=[]
res_out = []
species_names_out = {}  # Dictionary to store the names of the species
species_Y_out = {}  # Dictionary to store the mass fractions of the species
print("Starting main program loop...")
while (n_case < n_lines):  # I loop through all the cases
    print("--------------------------------------------------")
    # Now I retrieve the data
    try:
        inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_file.retrieve_data(df_object, program_mode, n_case)
    except Exception as e:
        if (program_mode == 1):
            print("Error while retrieving the data from the .srun file: " + str(e))
            print("The program will now terminate.")
            exit_program()
        elif (program_mode == 2 or program_mode == 3):
            has_converged_out.append("Error: invalid data")
            rho_out.append(-1)
            T_out.append(-1)
            h_out.append(-1)
            u_out.append(-1)
            a_out.append(-1)
            M_out.append(-1)
            T_t_out.append(-1)
            h_t_out.append(-1)
            P_t_out.append(-1)
            Re_out.append(-1)
            warnings_out.append("Error: invalid data")
            res_out.append(-1)
            n_case += 1
            species_names_out[n_case] = None
            species_Y_out[n_case] = None
            if (db_used):
                db_inputs = database_manager_file.db_inputs_append_null_line(db_inputs)
                run_time_vect.append(-1)
            continue
    n_case += 1 #we increase the number of cases
    print("Executing case number "+str(n_case)+"...")
    # I store the data from the inputs object
    comment = inputs_object.comment
    P = inputs_object.P
    P_stag = inputs_object.P_stag
    q_target = inputs_object.q_target
    mixture_name = inputs_object.mixture_name
    # print inputs
    print("Comment: "+comment)
    print("Static pressure: "+str(P)+" Pa")
    print("Stagnation pressure: "+str(P_stag)+" Pa")
    print("Target heat flux: "+str(q_target)+" W/m^2")
    print("Mixture name: "+mixture_name)
    if (probes_object.barker_type == 0): 
        n_eq = 3  # If we do not consider the barker effect, we need to solve 3 equations
    else:
        n_eq = 4  # If we consider the barker effect, we need to solve 4 equations
    #   Premilimary operation:
    if (probes_object.hf_law == 0 and settings_object.use_prev_ite == 1):
        # If we use the "exact" heat flux law and we want to use the previous iteration, we need to create
        # a file to understand if we have already computed the heat flux for the current case
        # For now, we want to inizialize the variable hf_first_comp, that stores 0 or 1:
        #   0: We have never computed the heat flux
        #   1: We have already computed the heat flux previously, so we have a x,y,z file (with the previous result)
        hf_first_comp = np.array([0])
        # We store this variable in a file using numpy.savetxt
        np.savetxt("hf_first_comp.var", hf_first_comp, fmt="%1.1u")
    # I reset some variables useful for the upcoming loops:
    iter = 0  # I reset the iteration counter
    has_converged = False  # I reset the convergence boolean
    # I initialize the variables for the Newton loop:
    T = initials_object.T_0
    T_t = initials_object.T_t_0
    u = initials_object.u_0
    P_t = initials_object.P_t_0
    # We start the Newton-Raphson loop to obtain the flow parameters from the probes
    exit_due_error = False  # Variable to exit the Newton loop if an error occurs during the computation
    max_newton_iter = settings_object.max_newton_iter  # I retrieve the maximum number of iterations for the Newton loop
    newton_conv = settings_object.newton_conv  # I retrieve the convergence criteria for the Newton loop
    print("Executing Newton loop...")
    mixture_object = mpp.Mixture(mixture_name) # I create the mixture object
    # Database operation:
    if(db_used):
        db_inputs = database_manager_file.db_inputs_append(db_inputs, inputs_object, probes_object)
        t_start_case = time.time()  # I store the time at the beginning of the case
    # NEWTON-RAPHSON LOOP:
    while (iter < max_newton_iter):
        # The loop has a stop condition for safety reason, but inside the loop there is also a convergence condition.
        # The loop will stop when the end newton computation converges or when the maximum number of iterations is reached.
        iter += 1
        # I compute the heat flux:
        try:
            q = heat_flux_file.heat_flux(probes_object, settings_object, P_t, T_t, u, mixture_object)
        except Exception as e:
            print("Error encountered during the heat flux computation: "+str(e))
            print("Skipping case...")
            exit_due_error = True
            break
        # Now I compute the enthalpy:
        h = enthalpy_file.enthalpy(mixture_object, P, T)  # I compute the free stream enthalpy
        h_t = enthalpy_file.enthalpy(mixture_object, P_t, T_t)  # I compute the stagnation enthalpy
        # Now I compute the entropy:
        s = entropy_file.entropy(mixture_object,P,T)  # I compute the entropy at the free stream
        s_t = entropy_file.entropy(mixture_object,P_t,T_t)  # I compute the entropy at the stagnation point
        # I compute the Barker's effect pressure:
        P_b, Re = barker_effect_file.barker_effect(probes_object, mixture_object, P_t, P, T, u)
        # Note: if barker_type==0 then P_b=P_stag, and the function will return P_stag
        #.................................................
        # I can now compute the residuals:
        res = []
        res.append(-(q-q_target))  # Heat flux residual
        res.append(-(h_t-(h+0.5*pow(u,2))))  # Enthalpy residual
        res.append(-(s_t-s))  # Entropy residual
        res.append(-(P_b-P_stag))  # Barker's effect residual
        # Convergence criteria: Normalized residual
        cnv = 0 
        for i in range(0, n_eq):
            cnv += pow(res[i],2)
        if (iter == 1):  # I create the reference convergence criteria if it is the first iteration
            cnv_ref = math.sqrt(cnv)
            cnv = 1
        else:
            cnv = math.sqrt(cnv)/cnv_ref
        #.................................................
        print("Case:"+str(n_case)+", Iteration "+str(iter)+", convergence criteria: "+str(cnv))
        # I check for the convergence:
        if (iter>max_newton_iter):  # If the maximum number of iterations is reached we break the loop
            break 
        if (cnv<newton_conv):  # If the convergence criteria is reached we break the loop
            has_converged = True
            break
        #.................................................
        # If I did not converge, I compute the Jacobian matrix:
        try:
            jac = jacobian_matrix_file.jacobian_matrix(probes_object, settings_object, T, T_t, P, P_t, P_b, q, h, h_t, s, s_t, u, mixture_object)
        except Exception as e:
            print("Error encountered during the jacobian computation: "+str(e))
            exit_due_error = True
            break
        #.................................................
        # Now I finally solve the system
        try:
            d_vars = system_solve_file.system_solve(n_eq, jac, res)
        except Exception as e:
            print("Error encountered during the system solve: "+str(e))
            exit_due_error = True
            break
        # I update the variables:
        T_star = T + d_vars[0] 
        u_star = u + d_vars[1]
        T_t_star = T_t + d_vars[2]
        if (probes_object.barker_type != 0):
            P_t_star = P_t + d_vars[3]
        else:
            P_t_star = P_t
        #.................................................
        # UNDER-RELAXATION SCHEME:
        # This scheme avoids that T_star, u_star, T_t_star and P_t_star
        # become negative or too high
        relax = 1.0  # Reset the relaxation factor
        # If the new valus are too low, we relax them:
        while ( (T_star < settings_object.min_T_relax) or (u_star < 0) or (T_t_star < settings_object.min_T_relax) or (P_t_star < 0) or (T_t_star < probes_object.T_w) ): 
            relax = relax/2  # We halve the relaxation factor
            # New values:
            T_star = T + d_vars[0]*relax
            u_star = u + d_vars[1]*relax
            T_t_star = T_t + d_vars[2]*relax
            if (probes_object.barker_type != 0):
                P_t_star = P_t + d_vars[3]*relax
        # If the new values are too high, we relax them:
        while ( (T_star > settings_object.max_T_relax) or (T_t_star > settings_object.max_T_relax)):
            relax = relax/2  # We halve the relaxation factor
            # New values:
            T_star = T + d_vars[0]*relax
            u_star = u + d_vars[1]*relax
            T_t_star = T_t + d_vars[2]*relax
            if (probes_object.barker_type != 0):
                P_t_star = P_t + d_vars[3]*relax
        #.................................................
        # New values are now accepted:
        T = T_star
        u = u_star
        T_t = T_t_star
        if (probes_object.barker_type != 0):
            P_t = P_t_star
    #.................................................
    # The Newton's loop has ended
    # Database operation:
    if (db_used):
        t_end_case = time.time()  # I store the time at the end of the case
        run_time_vect.append(t_end_case-t_start_case)  # I store the run time
    # I check if the case has converged or not
    if (exit_due_error == True and program_mode != 1):  # If we have skipped the case and we are not in single run
        # We only skip the case, but we do not exit the program
        print("The case number "+str(n_case)+" has encountered an error during the computation. The case will be skipped.")
        has_converged_out.append("Error detected during the computation.")
        rho_out.append(-1)
        T_out.append(-1)
        h_out.append(-1)
        u_out.append(-1)
        a_out.append(-1)
        M_out.append(-1)
        T_t_out.append(-1)
        h_t_out.append(-1)
        P_t_out.append(-1)
        Re_out.append(-1)
        warnings_out.append("Error detected during the computation.")
        res_out.append(-1)
        species_names_out[n_case] = None
        species_Y_out[n_case] = None
        continue
    if (exit_due_error == True and program_mode==1):  # If we have skipped the case and we are in single run
        print("Error detected during the computation of the case. The program will now terminate.")
        exit_program()
    print("Executing Newton loop...done")
    # Flow properties to output:
    rho, a, M, h, h_t = out_properties_file.out_properties(mixture_object, T, P, u)
    species_names, species_Y = out_properties_file.mass_fraction_composition(mixture_object, T, P)
    # P.S. The enthalpy is shifted to 0 K
    # Now we append the results to the output vectors:
    if (has_converged):
        has_converged_out.append("yes")
        print("Iteration has converged.")
    else:
        has_converged_out.append("no")
        print("Iteration has not converged.")
    rho_out.append(rho)
    T_out.append(T)
    h_out.append(h)
    u_out.append(u)
    a_out.append(a)
    M_out.append(M)
    h_t_out.append(h_t)
    P_t_out.append(P_t)
    T_t_out.append(T_t)
    Re_out.append(Re)
    warnings_out.append(warnings)
    res_out.append(cnv)
    species_names_out[n_case] = species_names
    species_Y_out[n_case] = species_Y
    print("Executing case number "+str(n_case)+"...done")
print("--------------------------------------------------")
print("Writing output file...")
# Packing the output data:
out_object.has_converged_out = has_converged_out
out_object.rho_out = rho_out
out_object.T_out = T_out
out_object.h_out = h_out
out_object.u_out = u_out
out_object.a_out = a_out
out_object.M_out = M_out
out_object.T_t_out = T_t_out
out_object.h_t_out = h_t_out
out_object.P_t_out = P_t_out
out_object.Re_out = Re_out
out_object.warnings_out = warnings_out
out_object.res_out = res_out
out_object.species_names_out = species_names_out
out_object.species_Y_out = species_Y_out
# Writing the output file:
if program_mode == 1:  # Single run
    write_output_srun_file.write_output_srun(output_filename, out_object)
elif program_mode == 2:  # xlsx run
    write_output_xlsx_file.write_output_xlsx(output_filename, out_object)
elif program_mode == 3:  # File run
    write_output_filerun_file.write_output_filerun(df_object, output_filename, out_object)
else:
    print("ERROR: Invalid program mode. You should never see this message...")
    print("The program will now terminate.")
    exit_program()
print("Writing output file...done")
# Database operation:
if (db_used):
    print("Generating database...")
    database_manager_file.update_database(db_settings, db_inputs, out_object, run_time_vect)
    print("Generating database...done")
# We clean the temporary files for use_prev_ite:
clean_files()
print("Program terminated.")
t2=time.time()
print("Execution time: "+str(t2-t1)+" seconds.")
