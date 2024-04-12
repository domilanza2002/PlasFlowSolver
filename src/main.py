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
import os  # Standard library for system operations
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
import read_srun as read_srun_file  # Module to read a .srun file
import read_dataframe as read_dataframe_file  # Module to read a .xlsx file
import read_filerun as read_filerun_file  # Module to read a .in and .pfs file
import retrieve_data_srun as retrieve_data_srun_file  # Module to retrieve the data from a .srun file
import retrieve_data_xlsx as retrieve_data_xlsx_file  # Module to retrieve the data from a xlsx file
import retrieve_data_filerun as retrieve_data_filerun_file  # Module to retrieve the data a .in and .pfs file
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
#.................................................
# PROGRAM VARIABLES:
# I declare here all the variables I will use in this script
# Variables to manage the program mode:
program_mode = None  # Variable to store the program mode
bash_run = None  # Variable to store if a bashrun has to be executed
# Variables for the output file:
output_filename = None  # Name of the output file
# Dataframe variables:
n_lines = None  # Number of lines of the dataframe
check = None  # Variable to check if the line must be skipped
# Counter variables:
ncase = None  # Counter of the number of cases to be run
# Input variables read from the file:
comment = None  # Comment of the case
P = None  # Static pressure of the flow
P_stag = None  # Stagnation pressure ("Target" if the Barker's effect is considered) of the flow
q_target = None  # Target stagnation heat flux
mixture_name = None # Mixture name
warnings = None  # Warnings due to the input file
# Newton loop variables:
iter = None # Current number of iterations
has_converged = None # Boolean to check if the iteration has converged
res = None # Residuals array
cnv = None # Current convergence criteria
cnvref = None # Reference convergence criteria
jac = None # Jacobian matrix of the system
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
has_converged_out = None  # Variable to store if the iteration has converged
rho_out = None  # Edge density to be written on the output file
T_out = None  # Edge temperature to be written on the output file
h_out = None  # Edge enthalpy to be written on the output file
u_out = None  # Edge velocity to be written on the output file
a_out = None  # Edge sound speed to be written on the output file
M_out = None  # Edge Mach number to be written on the output file
h_t_out = None  # Total enthalpy to be written on the output file
P_t_out = None  # Total pressure to be written on the output file
T_t_out = None  # Total temperature to be written on the output file
Re_out = None  # Pitot Reynolds number to be written on the output file
warnings_out=None  # Warnings to be written on the output file
res_out = None  # Final convergence criteria to be written on the output file
# Variables to manage the heat flux computation:
exit_due_hf = None  # Variable to exit the Newton loop if an error occurs during the heat flux computation
hf_first_comp = None  # Variable to store if it is the first time that we compute the heat flux for the current case
#
#.................................................
# CLASS INSTANCES:
# I will create here the instances of the classes I will use in the program
inputs_object = classes_file.inputs_class()  # Object with the inputs for the current iteration
settings_object = classes_file.settings_class()  # Object with the settings for the current iteration
probes_object = classes_file.probes_class()  # Object with the probe properties for the current iteration
initials_object = classes_file.initials_class()  # Object with the initial conditions for the current iteration
df_object = classes_file.dataframe_class()  # Object to store the dataframe, independently from the program mode
#.................................................
#
#   Here the program starts
t1 = time.time()  # I store the time at the beginning of the program, to keep track of the execution time
presentation_file.presentation()  # I call the presentation module, to present the program to the user
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
# Now I read the inputs, depending on the program mode
if (program_mode == 1): #Single run
    print("Mode selected: Single run.")
    # In this case, I want to read a .srun file, with only 1 case
    try:
        df_object, output_filename = read_srun_file.read_srun(bash_run)
    except Exception as e:
        print("Error while reading the .srun file: "+str(e))
        print("Please check your .srun file format and try again.")
        print("The program will now terminate.")
        exit()
elif (program_mode == 2): #File run
    print("Excel run selected")
    #   In this case, I want to read the dataframe from a file
    try:
        df_object, output_filename = read_dataframe_file.read_dataframe(bash_run) #note: never edit this object
    except Exception as e:
        print("Error while reading the dataframe: "+str(e))
        print("Please check your excel file format and try again")
        print("The program will now terminate")
        exit()
elif (program_mode == 3): #File run
    print("File run selected")
    try:
        df_object, output_filename = read_filerun_file.read_filerun(bash_run) #note: never edit this object
    except Exception as e:
        print("Error while reading the .in and .pfs files: "+str(e))
        print("Please check your .in and .pfs file format and try again")
        print("The program will now terminate")
        exit()
else:
    print("ERROR: Invalid program mode. You should never see this message...")
    print("The program will now terminate")
    exit()
#.................................................
#   MAIN PROGRAM LOOP:
#   Here the main program loop starts
ncase = 0 #I initialize the number of cases counter
n_lines = df_object.n #I store the number of lines of the dataframe
print("Number of cases to be executed: "+str(n_lines))
#we inizialize the output vectors:
has_converged_out = []
rho_out = []
T_out = []
h_out = []
u_out = []
a_out = []
M_out = []
h_t_out = []
P_t_out = []
T_t_out = []
Re_out = []
warnings_out=[]
res_out = []
print("Starting main program loop...")
while(ncase<n_lines): #this is the main loop of the program. The loop will stop when the end of the dataframe is reached
    print("--------------------------------------------------")
    #   Now I extract the data from the dataframe:
    if (program_mode == 1): #Single run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_srun_file.retrieve_data(df_object)
        except Exception as e:
            print("Error while retrieving the data from the .srun file: "+str(e))
            print("The program will now terminate")
            exit()
    elif (program_mode == 2): #File run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_xlsx_file.retrieve_data(df_object, ncase)
        except Exception as e:
            print("Error while retrieving the data from the dataframe: "+str(e))
            print("We skip the case number "+str(ncase))
            has_converged_out.append("Error: invalid data")
            rho_out.append(-1)
            T_out.append(-1)
            h_out.append(-1)
            u_out.append(-1)
            a_out.append(-1)
            M_out.append(-1)
            h_t_out.append(-1)
            P_t_out.append(-1)
            T_t_out.append(-1)
            Re_out.append(-1)
            warnings_out.append("Error: invalid data")
            res_out.append(-1)
            ncase+=1 #we increase the number of cases
            continue
    elif (program_mode == 3): #File run
        try:
            inputs_object, initials_object, probes_object, settings_object, warnings = retrieve_data_filerun_file.retrieve_data(df_object, ncase)
        except Exception as e:
            print("Error while retrieving the data from the dataframe: "+str(e))
            print("We skip the case number "+str(ncase))
            has_converged_out.append("Error: invalid data")
            rho_out.append(-1)
            T_out.append(-1)
            h_out.append(-1)
            u_out.append(-1)
            a_out.append(-1)
            M_out.append(-1)
            h_t_out.append(-1)
            P_t_out.append(-1)
            T_t_out.append(-1)
            Re_out.append(-1)
            warnings_out.append("Error: invalid data")
            res_out.append(-1)
            ncase+=1 #we increase the number of cases
            continue
    else:
        print("ERROR: Invalid program mode. You should never see this message...")
        print("The program will now terminate")
        exit()
    ncase += 1 #we increase the number of cases
    print("Executing case number "+str(ncase)+"...")
    #We save the important variables in the variables we will use in the main loop
    comment = inputs_object.comment #we store the comment
    P = inputs_object.P #Static pressure at the edge
    P_stag = inputs_object.P_stag #Stagnation pressure
    q_target = inputs_object.q #Target heat flux
    mixture_name = inputs_object.plasma_gas #Mixture name
    #   Now we are going to check for the type of heat flux law:
    if (probes_object.hflaw != 0): #if we do not use the exact heat flux law
        print("Error: heat flux law not yet implemented") #we print an error message
        exit() #we exit the program
    #   Note: in the future we could add more implementations for the heat flux law
    #   From now on, we are going to compute the heat flux using the exact heat flux law
    #   Now we understand how many equations we have to solve:
    if (probes_object.barker == 0): #we check if we need to consider the barker effect
        n_eq = 3 #we do not consider the barker effect, so we need to solve 3 equations, since that P_t=P_stag
    else: #otherwise we need to consider the barker effect:
        n_eq = 4 #we do consider the barker effect, so we need to solve 4 equations, since that P_t!=P_stag
    #   Premilimary operation:
    if (probes_object.hflaw == 0 and settings_object.use_prev_ite == 1): #if we use the exact heat flux law
        #we want to store x,y,z in a file in order to use the previous results each time we compute the heat flux
        # for now, we want to inizialize the variable hf_first_comp, that stores 0 or 1:
        #   0: We have never computed the heat flux
        #   1: We have already computed the heat flux previously, so we have a x,y,z file
        hf_first_comp = np.array([0]) #we initialize the variable
        # now we want to store this variable in a file using numpy.savetxt
        np.savetxt("hf_first_comp.var", hf_first_comp, fmt="%1.1u") #we store the variable in a file
    # now we reset some variables useful for the upcoming loops:
    iter = 0 #we reset the iteration counter for the newton loop
    has_converged = False #we reset the convergence boolean for the newton loop
    # We need to inizialize the other thermo variables:
    T = initials_object.T_0 #T is the static temperature
    T_t = initials_object.Tt_0 #T_t is the total temperature
    u = initials_object.u_0 #u is the velocity
    P_t = initials_object.Pt_0 #P_t is the total pressure
    # The unknowns are: T_t,u,T,P_t. P is constant
    # Now we start the newton loop to obtain the flow parameters from the probes
    exit_due_hf = False #we reset the variable to exit
    max_newton_iter = settings_object.max_newton_iter #we set the maximum number of iterations for the newton loop
    newton_conv = settings_object.newton_conv #we set the convergence criteria for the newton loop
    print("Executing Newton loop...")
    mixture_object = mpp.Mixture(mixture_name) #we create the mixture object
    while(iter<max_newton_iter): #this is the Newton loop
        #   The loop has a stop condition for safety reason, but inside the loop there is also a convergence condition
        #   The loop will stop when the end newton computation converges or when the maximum number of iterations is reached
        iter=iter+1 #increase the iteration counter
        # In the most general case, with the Barker effect, we need to solve 4 equations in order to find T,u,T_t,P_t:  
        #   1)q: heat flux equation
        #       q(P_t,T_t,u)-q_target=0
        #   2)h: enthalpy equation:
        #       h_t(P_t,T_t)-[h(P,T)+0.5*u^2]=0
        #   3)s: entropy equation:
        #       s_t(P_t,T_t)-s(P,T)=0
        #   4)P_t: stagnation pressure equation
        #       P_pitot-P_stag=0
        #   where P_pitot=P_t+0.5*rho(P,T)*u^2*(Cp(P,T,u)-1)
        #   If no barker effect is considered, then the last equation is not needed, since that P_t=P_stag, so we have 3 unknowns: T,u,T_t
        #   while P=static pressure, P_stag=stagnation pressure read,q_target=heat flux read; are known
        # We start by computing the heat flux in order to solve the first equation:
        try:
            q = heat_flux_file.heat_flux(probes_object, settings_object, P_t, T_t, u, mixture_object) #we compute the heat flux
        except Exception as e:
            print("Error encountered during the heat flux computation: "+str(e))
            print("Skipping case...")
            exit_due_hf = True
            break
        # now we compute the enthalpy:
        h = enthalpy_file.enthalpy(mixture_object, P, T) #we compute the enthalpy at the edge
        h_t = enthalpy_file.enthalpy(mixture_object, P_t, T_t) #we compute the enthalpy at the stagnation point
        # now we compute the entropy:
        s = entropy_file.entropy(mixture_object,P,T) #we compute the entropy at the edge
        s_t = entropy_file.entropy(mixture_object,P_t,T_t) #we compute the entropy at the stagnation point
        # now we compute the barker effect:
        P_b, Re = barker_effect_file.barker_effect(probes_object, mixture_object, P_t, P, T, u) #we compute the barker pressure
        # Note: if barker==0 then P_b=P_stag, but the function can handle this case
        #.................................................
        #   We can now compute the residuals:
        res = [] #we initialize the residuals array
        res.append(-(q-q_target)) #residual 1
        res.append(-(h_t-(h+0.5*pow(u,2)))) #residual 2
        res.append(-(s_t-s)) #residual 3
        res.append(-(P_b-P_stag)) #residual 4
        cnv = 0 #we reset the convergence criteria
        for i in range(0, n_eq): #we compute the convergence criteria
            cnv += pow(res[i],2)
        #we use a normalized convergence criteria:
        if (iter == 1): #we check if this is the first iteration
            cnvref = math.sqrt(cnv) #we set the reference convergence criteria/normalize
            cnv = 1 #we set the convergence criteria to 1
        else:
            cnv = math.sqrt(cnv)/cnvref #we compute the convergence criteria
        #.................................................
        print("Case:"+str(ncase)+", Iteration "+str(iter)+", convergence criteria: "+str(cnv))
        #   We can now check if the iteration has converged:
        if (iter>max_newton_iter): #we check if we reached the maximum number of iterations. REDUNDANT
            break #we break the loop
        if( cnv<newton_conv): #we check if we reached the convergence criteria
            has_converged = True
            break
        #.................................................
        #   We can now compute the jacobian:
        try:
            jac = jacobian_matrix_file.jacobian_matrix(probes_object, settings_object, T, T_t, P, P_t, P_b, q, h, h_t, s, s_t, u, mixture_object) #we compute the jacobian matrix
        except Exception as e:
            print("Error encountered during the jacobian computation: "+str(e))
            exit_due_hf = True
            break
        #.................................................
        #   Now we finally solve the system
        try:
            dvar = system_solve_file.system_solve(n_eq,jac,res)
        except Exception as e:
            print("Error encountered during the system solve: "+str(e))
            exit_due_hf = True
            break
        T_star = T+dvar[0]
        u_star = u+dvar[1]
        T_t_star = T_t+dvar[2]
        if(probes_object.barker != 0):
            P_t_star = P_t+dvar[3]
        else:
            P_t_star = P_t
        #.................................................
        #   Now we perform the under-relaxation scheme:
        # This scheme avoids that T_star,Ustar, T_t_star and P_t_star
        # become negative or too high
        relax = 1.0 #we set the relaxation factor
        # we check if the new values are negative:
        while ( (T_star<settings_object.min_T_relax) or (u_star<0) or (T_t_star<settings_object.min_T_relax) or (P_t_star<0) or (T_t_star<probes_object.Tw) ): 
            relax = relax/2 #we decrease the relaxation factor
            # we relax the new values
            T_star = T+dvar[0]*relax
            u_star = u+dvar[1]*relax
            T_t_star = T_t+dvar[2]*relax
            if (probes_object.barker != 0):
                P_t_star = P_t+dvar[3]*relax
        # we check if the new values are too high:
        while ( (T_star>settings_object.max_T_relax) or (T_t_star>settings_object.max_T_relax)):
            relax = relax/2 #we decrease the relaxation factor
            # we relax the new values
            T_star = T+dvar[0]*relax
            u_star = u+dvar[1]*relax
            T_t_star = T_t+dvar[2]*relax
            if (probes_object.barker != 0):
                P_t_star = P_t+dvar[3]*relax
        #.................................................
        #  Now we update the variables:
        T = T_star
        u = u_star
        T_t = T_t_star
        if (probes_object.barker!=0):
            P_t = P_t_star
        else:
            P_t = P_stag
    #.................................................
    # Newton loop ends here
    if (exit_due_hf == True and program_mode!=1): #we check if we have skipped the case and if we are not in single run
        #we set -1 to the output vectors in order to keep the same number of lines in the output file
        print("The case number "+str(ncase)+" has encountered an error during the computation. The case will be skipped")
        has_converged_out.append("Error detected during the computation")
        rho_out.append(-1)
        T_out.append(-1)
        h_out.append(-1)
        u_out.append(-1)
        a_out.append(-1)
        M_out.append(-1)
        h_t_out.append(-1)
        P_t_out.append(-1)
        T_t_out.append(-1)
        Re_out.append(-1)
        warnings_out.append("Error detected during the computation")
        res_out.append(-1)
        continue
    if (exit_due_hf == True and program_mode==1): #we check if we have skipped the case and if we are in single run
        print("Error detected during the computation of the case. The program will now terminate")
        exit()
    print("Executing Newton loop...done")
    # Now we need to compute the flow properties useful for data rebuilding
    rhoe, ae, Me, h, h_t = out_properties_file.out_properties(mixture_object, T, P, u) #we compute the final properties
    # The Reynold number is taken from the barker effect computation in the loop
    # Now we append the results to the output vectors:
    if (has_converged ):
        has_converged_out.append("yes")
        print("Iteration has converged")
    else:
        has_converged_out.append("no")
        print("Iteration has not converged")
    rho_out.append(rhoe)
    T_out.append(T)
    h_out.append(h)
    u_out.append(u)
    a_out.append(ae)
    M_out.append(Me)
    h_t_out.append(h_t)
    P_t_out.append(P_t)
    T_t_out.append(T_t)
    Re_out.append(Re)
    warnings_out.append(warnings)
    res_out.append(cnv)
    print("Executing case number "+str(ncase)+"...done")
print("--------------------------------------------------")
print("Writing output file...")
if (program_mode == 1): #Single run
    write_output_srun_file.write_output_srun(output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,h_t_out,P_t_out,T_t_out,Re_out,warnings_out)
elif (program_mode == 2): #File run
    write_output_xlsx_file.write_output_xlsx(output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,h_t_out,P_t_out,T_t_out,Re_out,warnings_out)
elif (program_mode == 3): #File run
    write_output_filerun_file.write_output_filerun(df_object,output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,h_t_out,P_t_out,T_t_out,Re_out,res_out)
else:
    print("ERROR: Invalid program mode. You should never see this message...")
    print("The program will now terminate")
    exit()
print("Writing output file...done")
# We clean the temporary files:
try:
    os.remove("hf_first_comp.var") #we remove the temporary file
except:
    pass
try:
    os.remove("x.var") #we remove the temporary file
    os.remove("y.var") #we remove the temporary file
    os.remove("z.var") #we remove the temporary file
except:
    pass
print("Program terminated")
t2=time.time() #we store the time at the end of the program
print("Execution time: "+str(t2-t1)+" seconds")
