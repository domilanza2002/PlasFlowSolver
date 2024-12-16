#.................................................
#       PlasFlowSolver Program
#       main.py: main script
#       Version 2.0.0, Domenico Lanza
#.................................................
# LIBRARY IMPORTS:
# Standard library imports:
import math  # Standard library for math operations
import time  # Standard library for time tracking operations
# Third party library imports:
import numpy as np  # Third party library for math operations
import mutationpp as mpp  # Third party library for thermodynamic computations
# Project file imports:
# The format for the import is: "import filename as filename_file"
import presentation as presentation_file  # Module to print the presentation of the program
import prompt_program_mode as prompt_program_mode_file  # Module to prompt the program mode to the user
import script_run as script_run_file  # Module to execute a scripted run from a bash.pfs file
import read_data as read_data_file  # Module to read the data from the input file
import retrieve_data as retrieve_data_file  # Module to retrieve the data from the dataframe
import heat_flux as heat_flux_file  # Module to compute the stagnation heat flux
import thermodyn as thermodyn_file  # Module to compute the flow enthalpy
import barker_effect as barker_effect_file  # Module to compute the Barker effect
import jacobian_matrix as jacobian_matrix_file  # Module to compute the Jacobian matrix of the system of equations
import newton_operations as newton_operations_file  # Module to perform the Newton-Raphson's method
import system_solve as system_solve_file  # Module to solve the system of equations
import out_properties as out_properties_file  # Module to compute the output properties
import write_output as write_output  # Module to write the output file
import database_manager as database_manager_file  # Module to manage the database
from exit_program import exit_program, clean_files  # Module to kill the program and kill the temporary files
from mpp_memory_fixer import fix_mpp_memory_leak  # Module to fix Mutation++ memory leak (if any, due to Python wrapper)
#.................................................
# PROGRAM CONSTANTS: %TO REVIEW
USE_PREV_ITE_FILENAME = "hf_first_comp.var"  # File to store the flag for the use_prev_ite option
#.................................................
#   PROGRAM START:
# Preliminary operations:
t1 = time.time()  # I store the time at the beginning of the program to keep track of the execution time
presentation_file.presentation()  # I write the presentation of the program
fix_mpp_memory_leak()  # Fix the memory leak in the MPP library:
# Program scripting check:
script_run = script_run_file.script_file_detected()  # Check if a scripted run has to be executed
if (script_run == False):  # If the program is in manual mode
    print("No valid script.pfs file detected, the program will run in manual mode.")
    program_mode = prompt_program_mode_file.prompt_program_mode()  # Prompt the user for the program mode
else:  # The program is in bash mode
    print("A valid script.pfs file detected, the program will run in scripted mode.")
    try:
        program_mode = script_run_file.retrieve_program_mode()  # Trying to retrieve the program mode
    except Exception as e:
        print("Invalid program mode: " + str(e))
        print("The program will continue in manual mode.")
        program_mode = prompt_program_mode_file.prompt_program_mode()  # Prompt the program mode to the user
        script_run = False
# Check if a database must be used and retrieve its settings:
db_settings = database_manager_file.init_database()  # The initial operations for the database are performed
if (db_settings is None):
    db_used = False  # Flag to check if the database is used
    print("No valid database_settings.pfs file detected, the program will not use a database.")
else:
    db_used = True
    print("Valid database_settings.pfs file detected, the program will use the database.")
    # The initial operations for the database inputs are performed
    db_inputs = database_manager_file.db_inputs_init()  
# Now I read the data:
try:
    df_object, output_filename = read_data_file.read_data(program_mode, script_run)
except Exception as e:
    print("Error while reading the data: " + str(e))
    print("The program will now terminate.")
    exit_program()
#.................................................
#   MAIN PROGRAM LOOP:
n_case = 0  # Case counter
n_lines = df_object.n  # I store the number of cases to be executed = number of lines in the dataframe object
print("Number of cases to be executed: " + str(n_lines) + ".")
# I initialize the output vectors
(
    has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, 
    h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out, 
    species_names_out, species_Y_out, run_time_vect
) = out_properties_file.initialize_output_vectors()
print("Starting main program loop...")
while (n_case < n_lines):  # Loop through all the cases
    print("--------------------------------------------------")
    # Now I retrieve the data for the current case
    try:
        (
            inputs_object, initials_object, probes_object, 
            settings_object, warnings
        ) = retrieve_data_file.retrieve_data(df_object, program_mode, n_case)
    except Exception as e:
        if (program_mode == 1):
            print("Error while retrieving the data from the .srun file: " + str(e))
            print("The program will now terminate.")
            exit_program()
        elif (program_mode == 2 or program_mode == 3):
            (
                has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
                h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out
            ) = out_properties_file.append_error_case(
                has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
                h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out, 0
            )
            n_case += 1  # Since these are usually assigned after n_case is increased, I increase it here
            species_names_out[n_case] = None
            species_Y_out[n_case] = None
            if (db_used):
                db_inputs = database_manager_file.db_inputs_append_null_line(db_inputs)
                run_time_vect.append(-1)
            continue
    n_case += 1 # Increase counter
    print("Executing case number "+str(n_case) + "...")
    # I store the data from the inputs object
    comment = inputs_object.comment
    P = inputs_object.P
    P_stag = inputs_object.P_stag
    q_target = inputs_object.q_target
    mixture_name = inputs_object.mixture_name
    # Print the data for the current case
    print("Comment: " + comment)
    print("Static pressure: " + str(P) + " Pa")
    print("Stagnation pressure: " + str(P_stag) + " Pa")
    print("Target heat flux: " + str(q_target) + " W/m^2")
    print("Mixture name: " + mixture_name)
    # Premilimary operation:
    if (probes_object.barker_type == 0):
        n_eq = 3 
    else:
        n_eq = 4  # If the Barker effect is considered, 4 equations must be solved
    # Manage the use_prev_ite flag:
    if (probes_object.hf_law == 0 and settings_object.use_prev_ite == 1):
        # Flag that indicates if the heat flux has been previously computed
        # in this case (and if it has converged)
        hf_first_comp = np.array([0])
        # Store this variable in a file
        np.savetxt(USE_PREV_ITE_FILENAME, hf_first_comp, fmt="%1.1u")
    # Initial conditions:
    T = initials_object.T_0
    T_t = initials_object.T_t_0
    u = initials_object.u_0
    P_t = initials_object.P_t_0
    # Reset variables useful for the upcoming Newton loop:
    bad_hf = False  # Variable to store if the heat flux did not converge
    iter = 0  # Counter for the Newton loop
    has_converged = False  # Convergence flag
    exit_due_error = False  # Flag to exit the Newton loop if an error occurs during the computation
    max_newton_iter = settings_object.max_newton_iter  # Maximum number of iterations for the Newton loop
    newton_conv = settings_object.newton_conv  # Conv. criteria for the Newton loop
    mixture_object = mpp.Mixture(mixture_name) # Mixture object for the current case
    print("Executing Newton loop...")
    # Database operation:
    if(db_used):
        db_inputs = database_manager_file.db_inputs_append(db_inputs, inputs_object, probes_object)
        t_start_case = time.time()  # I store the time at the beginning of the case
    # NEWTON-RAPHSON LOOP:
    while (iter < max_newton_iter):
        iter += 1
        # Compute the heat flux
        try:
            q, bad_hf = heat_flux_file.heat_flux(probes_object, settings_object, P_t, T_t, u, mixture_object)
        except Exception as e:
            print("Error encountered during the heat flux computation: "+str(e))
            print("Skipping case...")
            exit_due_error = True
            break
        # Compute the enthalpy:
        h = thermodyn_file.enthalpy(mixture_object, P, T)  # Free stream enthalpy
        h_t = thermodyn_file.enthalpy(mixture_object, P_t, T_t)  # Total enthalpy
        # Compute the entropy:
        s = thermodyn_file.entropy(mixture_object,P,T)  # Free stream entropy
        s_t = thermodyn_file.entropy(mixture_object,P_t,T_t)  # Total entropy
        # Compute the Barker effect:
        P_b, Re = barker_effect_file.barker_effect(probes_object, mixture_object, P_t, P, T, u)
        # NOTE: if barker_type==0 then P_b=P_stag, and the function will return P_stag
        #.................................................
        # I can now compute the residuals:
        res = []
        res.append(-(q-q_target))  # Heat flux residual
        res.append(-(h_t-(h+0.5*pow(u,2))))  # Enthalpy residual
        res.append(-(s_t-s))  # Entropy residual
        res.append(-(P_b-P_stag))  # Barker effect residual
        # Convergence criteria: Normalized residual
        cnv = 0 
        for i in range(0, n_eq):
            cnv += pow(res[i],2)
        if (iter == 1):  # Create reference convergence criteria for the first iteration
            cnv_ref = math.sqrt(cnv)
            cnv = 1
            cnv_old = 1
        else:
            cnv = math.sqrt(cnv)/cnv_ref
            try:
                (
                    cnv, res, settings_object, T, u, T_t, P_t, 
                    h, h_t, s, s_t, P_b
                ) = newton_operations_file.dynamic_jacobian_diff(
                    cnv, cnv_old, cnv_ref, res, settings_object, probes_object, T, u, T_t, P_t, P,
                    q_target, P_stag, mixture_object, h, h_t, s, s_t, P_b
                )
            except Exception as e:
                print("Error encountered during the dynamic Jacobian computation: " + str(e))
                print("Operation cancelled.")
            cnv_old = cnv
        #.................................................
        print("Case:" + str(n_case) + ", Iteration " + str(iter) + ", convergence criteria: " + str(cnv))
        # Check for convergence:
        # If the maximum number of iterations is reached, the loop is broken
        if (iter > max_newton_iter):  
            break 
        # If the method converged, the loop is broken
        if (cnv < newton_conv): 
            has_converged = True
            break
        # If the method did not converge, the loop is continued
        # Compute the Jacobian matrix:
        try:
            jac = jacobian_matrix_file.jacobian_matrix(
                probes_object, settings_object, T, T_t, P, P_t, P_b, 
                q, h, h_t, s, s_t, u, mixture_object
                )
        except Exception as e:
            print("Error encountered during the jacobian computation: " + str(e))
            exit_due_error = True
            break
        # The linear system is solved:
        try:
            d_vars = system_solve_file.system_solve(n_eq, jac, res)
        except Exception as e:
            print("Error encountered while solving the system: " + str(e))
            exit_due_error = True
            break
        # Variables update:
        T_star = T + d_vars[0] 
        u_star = u + d_vars[1]
        T_t_star = T_t + d_vars[2]
        if (probes_object.barker_type != 0):
            P_t_star = P_t + d_vars[3]
        else:
            P_t_star = P_t
        #.................................................
        # Under-relaxation scheme:
        T_star, u_star, T_t_star, P_t_star = newton_operations_file.under_relaxation(
            settings_object, probes_object, T_star, u_star, T_t_star, P_t_star, T, u, T_t, P_t, d_vars
        )
        #.................................................
        # New variables' values:
        T = T_star
        u = u_star
        T_t = T_t_star
        if (probes_object.barker_type != 0):
            P_t = P_t_star
    # END OF NEWTON LOOP
    #.................................................
    # Database operation:
    if (db_used):
        t_end_case = time.time()  # Store the time at the end of the case
        run_time_vect.append(t_end_case - t_start_case)  # Store the run time
    # Check if the heat flux converged in the last iteration:
    if (bad_hf):
        print("The heat flux did not converge in the last iteration. The case did not converge.")
        has_converged = False
    # Check if an error occurred during the computation:
    if (exit_due_error == True and program_mode != 1):  # If we are not in single run
        # The case will be skipped
        print("Case number " + str(n_case) + " has encountered an error during computation.")
        print("The case will be skipped.")
        (
                has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
                h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out
            ) = out_properties_file.append_error_case(
                has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out,
                h_t_out, P_t_out, Re_out, Kn_out, warnings_out, res_out, 1
        )
        species_names_out[n_case] = None
        species_Y_out[n_case] = None
        continue  # We go to the next case
    if (exit_due_error == True and program_mode==1):  # If we have skipped the case and we are in single run
        print("Error detected during the computation of the case. The program will now terminate.")
        exit_program()
    print("Executing Newton loop...done")
    # Output properties computation:
    rho, a, M, h, h_t, mfp = out_properties_file.out_properties(mixture_object, T, P, u)
    species_names, species_Y = out_properties_file.mass_fraction_composition(mixture_object, T, P)
    Kn = mfp/(probes_object.R_j)  # Knudsen number
    # NOTE: The sensible enthalpy is shifted to 0 K
    if (has_converged):
        has_converged_out.append("yes")
        print("Iteration has converged.")
    else:
        has_converged_out.append("no")
        print("Iteration has not converged.")
    (
        rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, h_t_out, P_t_out,
        Re_out, Kn_out, warnings_out, res_out
    ) = out_properties_file.append_output_case(
        rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, h_t_out, P_t_out,
        Re_out, Kn_out, warnings_out, res_out, rho, T, h, u, a, M, T_t, h_t, P_t, Re, Kn, warnings, cnv
    )
    species_names_out[n_case] = species_names
    species_Y_out[n_case] = species_Y
    print("Executing case number "+str(n_case)+"...done")
print("--------------------------------------------------")
print("End of main program loop...")
# END OF MAIN PROGRAM LOOP
# Output file writing:
print("Writing output file...")
# Packing the output data:
out_object = out_properties_file.return_out_object(
    has_converged_out, rho_out, T_out, h_out, u_out, a_out, M_out, T_t_out, h_t_out, P_t_out,
    Re_out, Kn_out, warnings_out, res_out, species_names_out, species_Y_out
)
# Writing the output file:
write_output.write_output(output_filename, out_object, program_mode, df_object)
print("Writing output file...done")
# Database operations:
if (db_used):
    print("Generating database...")
    database_manager_file.update_database(db_settings, db_inputs, out_object, run_time_vect)
    print("Generating database...done")
# Clean temporary files:
clean_files()
print("Program terminated.")
t2 = time.time()
print("Execution time: " + str(t2 - t1) + " seconds.")
