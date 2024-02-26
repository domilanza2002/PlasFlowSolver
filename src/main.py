#.................................................
#       PlasFlowSolver Program
#       main.py: main script
#       Version 3.0.0, Domenico Lanza
#.................................................
#   LIBRARY IMPORTS:
#   I import here the libraries I will use in the program
#   Standard library imports:
import math #Standard library for math operations
import time #Standard library for time trackingoperations
import os #Standard library for operating system operations
#   Third party library imports:
import numpy as np  #Third party library for numerical operations
import mutationpp as mpp #Third party library for thermodynamic computations
#   Project file imports:
#   I import here all the modules I will use in the program
#   The format for the import is: import filename as filename_file
import classes as classes_file #Module with the classes that I use in the program
import presentation as presentation_file #Module to print the presentation of the program
import prompt_program_mode as prompt_program_mode_file #Module to prompt the program mode to the user
import read_srun as read_srun_file #Module to read the .srun file
import read_dataframe as read_dataframe_file #Module to read the dataframe from the xlsx file
import read_filerun as read_filerun_file #Module to read the .in and .pfs files
import retrieve_data_srun as retrieve_data_srun_file #Module to retrieve the data from the .srun file
import retrieve_data_xlsx as retrieve_data_xlsx_file #Module to retrieve the data from the dataframe
import retrieve_data_filerun as retrieve_data_filerun_file #Module to retrieve the data from the .in and .pfs files
import heat_flux as heat_flux_file #Module to compute the heat flux
import enthalpy as enthalpy_file #Module to compute the enthalpy
import entropy as entropy_file #Module to compute the entropy
import barker_effect as barker_effect_file #Module to compute the barker effect
import jacobian_matrix as jacobian_matrix_file #Module to compute the jacobian matrix
import system_solve as system_solve_file #Module to solve the system
import out_properties as out_properties_file #Module to compute the final properties
import write_output_srun as write_output_srun_file #Module to write the output file
import write_output_xlsx as write_output_xlsx_file #Module to write the output file
import write_output_filerun as write_output_filerun_file #Module to write the output file
#.................................................
#       PROGRAM VARIABLES:
#   I declare here all the variables I will use in the program, in particular in the file main.py
#   Variables for the program mode:
program_mode = None #Variable to store the program mode
#   Variables for the output file:
output_filename = None #Name of the output file
#   Dataframe variables:
n_lines = None #Number of lines of the dataframe
check = None #Variable to check if the line must be skipped
#   Counter variables:
ncase = None #Number of cases counter of the input file
n_eq = None #Number of equations to solve
#   Loop variables read from input:
comment = None #Comment of the line
Pe = None #Static pressure at the edge. Read from input
Pstag = None #Stagnation pressure at the edge.
q_target = None #Target heat flux. Read from input
warnings = None #Warnings
mixture_name=None #Mixture name read from input
# Inner loop variables:
iter = None #Number of iterations
has_converged = None #Boolean to check if the iteration has converged
res = None #Residuals
cnv = None #Convergence criteria
cnvref = None #Reference convergence criteria
jac = None #Jacobian matrix
#   Loop thermodynamic variables:
mixture_object = None #Mixture object
q = None #Heat flux
Pt = None #Total pressure
Pb = None #Barker pressure
Te = None #Static temperature
Tt = None #Total temperature
ue = None #velocity
he = None #Enthalpy at the edge
ht = None #Enthalpy at the stagnation point
se = None #Entropy at the edge
st = None #Entropy at the stagnation point
Tstar = None #Variable to store new temporary T value
ustar = None #Variable to store new temporary u value
Ttstar = None #Variable to store new temporary Tt value
Ptstar = None #Variable to store new temporary Pt value
relax = None #Relaxation factor
Re = None #Reynolds number of the pitot probe
# Final properties:
has_converged_out = None #Variable to store "yes" or "no". 0: the iteration has not converged. 1: the iteration has converged
rho_out = None #Density to be written on the output file
T_out = None #Temperature to be written on the output file
h_out = None #Enthalpy to be written on the output file
u_out = None #Velocity to be written on the output file
a_out = None #Sound speed to be written on the output file
M_out = None #Mach number to be written on the output file
ht_out = None #Total enthalpy to be written on the output file
Pt_out = None #Total pressure to be written on the output file
Tt_out = None #Total temperature to be written on the output file
Re_out = None #Reynolds number to be written on the output file
warnings_out=None #Variable to store the warnings
# Variables for heat flux optimization:
to_exit = None #Variable to store the error of the heat flux
q_first = None #Variable to store 0 or 1. 0: we have never computed the heat flux. 1: we have already computed the heat flux previously, so we have a x,y,z file
#
#.................................................
#   INSTANCIATE OBJECTS:
#   I will create here the objects I will use
inputs_object = classes_file.inputs_class() #Object with the inputs of the program for the current iteration
settings_object = classes_file.settings_class() #Object with the settings of the program, for the current iteration
probes_object = classes_file.probes_class() #Object with the probes properties, for the current iteration
initials_object = classes_file.initials_class() #Object with the initial conditions, for the current iteration
df_object = classes_file.dataframe_xlsx_class() #Object with the dataframe variables from the xlsx file
#.................................................
#
#       PROGRAM START:
#       Here the program starts
t1 = time.time() #We store the time at the beginning of the program, to keep track of the execution time
presentation_file.presentation() #We call the presentation function, to present the program to the user
#   We prompt the user to select the program mode. 1: Single run. 2: File run
program_mode = prompt_program_mode_file.prompt_program_mode() #We prompt the program mode to the user
#   We read the data according to the program mode:
if (program_mode == 1): #Single run
    print("Single run selected")
    #   In this case, I want to read a .srun file, with only 1 case
    try:
        df_object, output_filename = read_srun_file.read_srun() #note: never edit this object
    except Exception as e:
        print("Error while reading the .srun file: "+str(e))
        print("Please check your .srun file format and try again")
        print("The program will now terminate")
        exit()
elif (program_mode == 2): #File run
    print("Excel run selected")
    #   In this case, I want to read the dataframe from a file
    try:
        df_object, output_filename = read_dataframe_file.read_dataframe() #note: never edit this object
    except Exception as e:
        print("Error while reading the dataframe: "+str(e))
        print("Please check your excel file format and try again")
        print("The program will now terminate")
        exit()
elif (program_mode == 3): #File run
    print("File run selected")
    try:
        df_object, output_filename = read_filerun_file.read_filerun() #note: never edit this object
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
ht_out = []
Pt_out = []
Tt_out = []
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
            ht_out.append(-1)
            Pt_out.append(-1)
            Tt_out.append(-1)
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
            ht_out.append(-1)
            Pt_out.append(-1)
            Tt_out.append(-1)
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
    Pe = inputs_object.P #Static pressure at the edge
    Pstag = inputs_object.Pstag #Stagnation pressure
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
        n_eq = 3 #we do not consider the barker effect, so we need to solve 3 equations, since that Pt=Pstag
    else: #otherwise we need to consider the barker effect:
        n_eq = 4 #we do consider the barker effect, so we need to solve 4 equations, since that Pt!=Pstag
    #   Premilimary operation:
    if (probes_object.hflaw == 0 and settings_object.use_prev_ite == 1): #if we use the exact heat flux law
        #we want to store x,y,z in a file in order to use the previous results each time we compute the heat flux
        # for now, we want to inizialize the variable q_first, that stores 0 or 1:
        #   0: We have never computed the heat flux
        #   1: We have already computed the heat flux previously, so we have a x,y,z file
        q_first = np.array([0]) #we initialize the variable
        # now we want to store this variable in a file using numpy.savetxt
        np.savetxt("q_first.var", q_first, fmt="%1.1u") #we store the variable in a file
    # now we reset some variables useful for the upcoming loops:
    iter = 0 #we reset the iteration counter for the newton loop
    has_converged = False #we reset the convergence boolean for the newton loop
    # We need to inizialize the other thermo variables:
    Te = initials_object.T_0 #T_e is the static temperature
    Tt = initials_object.Tt_0 #T_t is the total temperature
    ue = initials_object.u_0 #u_e is the velocity
    Pt = initials_object.Pt_0 #P_t is the total pressure
    # The unknowns are: Tt,u,Te,Pt. Pe is constant
    # Now we start the newton loop to obtain the flow parameters from the probes
    to_exit = False #we reset the variable to exit
    max_newton_iter = settings_object.max_newton_iter #we set the maximum number of iterations for the newton loop
    newton_conv = settings_object.newton_conv #we set the convergence criteria for the newton loop
    print("Executing Newton loop...")
    mixture_object = mpp.Mixture(mixture_name) #we create the mixture object
    while(iter<max_newton_iter): #this is the Newton loop
        #   The loop has a stop condition for safety reason, but inside the loop there is also a convergence condition
        #   The loop will stop when the end newton computation converges or when the maximum number of iterations is reached
        iter=iter+1 #increase the iteration counter
        # In the most general case, with the Barker effect, we need to solve 4 equations in order to find Te,ue,Tt,Pt:  
        #   1)q: heat flux equation
        #       q(Pt,Tt,ue)-q_target=0
        #   2)h: enthalpy equation:
        #       ht(Pt,Tt)-[h(Pe,Te)+0.5*ue^2]=0
        #   3)s: entropy equation:
        #       st(Pt,Tt)-s(Pe,Te)=0
        #   4)P_t: stagnation pressure equation
        #       P_pitot-Pstag=0
        #   where P_pitot=Pt+0.5*rho(Pe,Te)*ue^2*(Cp(Pe,Te,ue)-1)
        #   If no barker effect is considered, then the last equation is not needed, since that Pt=Pstag, so we have 3 unknowns: Te,ue,Tt
        #   while Pe=static pressure, Pstag=stagnation pressure read,q_target=heat flux read; are known
        # We start by computing the heat flux in order to solve the first equation:
        try:
            q = heat_flux_file.heat_flux(probes_object, settings_object, Pt, Tt, ue, mixture_object) #we compute the heat flux
        except Exception as e:
            print("Error encountered during the heat flux computation: "+str(e))
            print("Skipping case...")
            to_exit = True
            break
        # now we compute the enthalpy:
        he = enthalpy_file.enthalpy(mixture_object, Pe, Te) #we compute the enthalpy at the edge
        ht = enthalpy_file.enthalpy(mixture_object, Pt, Tt) #we compute the enthalpy at the stagnation point
        # now we compute the entropy:
        se = entropy_file.entropy(mixture_object,Pe,Te) #we compute the entropy at the edge
        st = entropy_file.entropy(mixture_object,Pt,Tt) #we compute the entropy at the stagnation point
        # now we compute the barker effect:
        Pb, Re = barker_effect_file.barker_effect(probes_object, mixture_object, Pt, Pe, Te, ue) #we compute the barker pressure
        # Note: if barker==0 then Pb=Pstag, but the function can handle this case
        #.................................................
        #   We can now compute the residuals:
        res = [] #we initialize the residuals array
        res.append(-(q-q_target)) #residual 1
        res.append(-(ht-(he+0.5*pow(ue,2)))) #residual 2
        res.append(-(st-se)) #residual 3
        res.append(-(Pb-Pstag)) #residual 4
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
            jac = jacobian_matrix_file.jacobian_matrix(probes_object, settings_object, Te, Tt, Pe, Pt, Pb, q, he, ht, se, st, ue, mixture_object) #we compute the jacobian matrix
        except Exception as e:
            print("Error encountered during the jacobian computation: "+str(e))
            to_exit = True
            break
        #.................................................
        #   Now we finally solve the system
        try:
            dvar = system_solve_file.system_solve(n_eq,jac,res)
        except Exception as e:
            print("Error encountered during the system solve: "+str(e))
            to_exit = True
            break
        Tstar = Te+dvar[0]
        ustar = ue+dvar[1]
        Ttstar = Tt+dvar[2]
        if(probes_object.barker != 0):
            Ptstar = Pt+dvar[3]
        else:
            Ptstar = Pt
        #.................................................
        #   Now we perform the under-relaxation scheme:
        # This scheme avoids that Tstar,Ustar, Ttstar and Ptstar
        # become negative or too high
        relax = 1.0 #we set the relaxation factor
        # we check if the new values are negative:
        while ( (Tstar<settings_object.min_T_relax) or (ustar<0) or (Ttstar<settings_object.min_T_relax) or (Ptstar<0) or (Ttstar<probes_object.Tw) ): 
            relax = relax/2 #we decrease the relaxation factor
            # we relax the new values
            Tstar = Te+dvar[0]*relax
            ustar = ue+dvar[1]*relax
            Ttstar = Tt+dvar[2]*relax
            if (probes_object.barker != 0):
                Ptstar = Pt+dvar[3]*relax
        # we check if the new values are too high:
        while ( (Tstar>settings_object.max_T_relax) or (Ttstar>settings_object.max_T_relax)):
            relax = relax/2 #we decrease the relaxation factor
            # we relax the new values
            Tstar = Te+dvar[0]*relax
            ustar = ue+dvar[1]*relax
            Ttstar = Tt+dvar[2]*relax
            if (probes_object.barker != 0):
                Ptstar = Pt+dvar[3]*relax
        #.................................................
        #  Now we update the variables:
        Te = Tstar
        ue = ustar
        Tt = Ttstar
        if (probes_object.barker!=0):
            Pt = Ptstar
        else:
            Pt = Pstag
    #.................................................
    # Newton loop ends here
    if (to_exit == True and program_mode!=1): #we check if we have skipped the case and if we are not in single run
        #we set -1 to the output vectors in order to keep the same number of lines in the output file
        print("The case number "+str(ncase)+" has encountered an error during the computation. The case will be skipped")
        has_converged_out.append("Error detected during the computation")
        rho_out.append(-1)
        T_out.append(-1)
        h_out.append(-1)
        u_out.append(-1)
        a_out.append(-1)
        M_out.append(-1)
        ht_out.append(-1)
        Pt_out.append(-1)
        Tt_out.append(-1)
        Re_out.append(-1)
        warnings_out.append("Error detected during the computation")
        res_out.append(-1)
        continue
    if (to_exit == True and program_mode==1): #we check if we have skipped the case and if we are in single run
        print("Error detected during the computation of the case. The program will now terminate")
        exit()
    print("Executing Newton loop...done")
    # Now we need to compute the flow properties useful for data rebuilding
    rhoe, ae, Me, he, ht = out_properties_file.out_properties(mixture_object, Te, Pe, ue) #we compute the final properties
    # The Reynold number is taken from the barker effect computation in the loop
    # Now we append the results to the output vectors:
    if (has_converged ):
        has_converged_out.append("yes")
        print("Iteration has converged")
    else:
        has_converged_out.append("no")
        print("Iteration has not converged")
    rho_out.append(rhoe)
    T_out.append(Te)
    h_out.append(he)
    u_out.append(ue)
    a_out.append(ae)
    M_out.append(Me)
    ht_out.append(ht)
    Pt_out.append(Pt)
    Tt_out.append(Tt)
    Re_out.append(Re)
    warnings_out.append(warnings)
    res_out.append(cnv)
    print("Executing case number "+str(ncase)+"...done")
print("--------------------------------------------------")
print("Writing output file...")
if (program_mode == 1): #Single run
    write_output_srun_file.write_output_srun(output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,ht_out,Pt_out,Tt_out,Re_out,warnings_out)
elif (program_mode == 2): #File run
    write_output_xlsx_file.write_output_xlsx(output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,ht_out,Pt_out,Tt_out,Re_out,warnings_out)
elif (program_mode == 3): #File run
    write_output_filerun_file.write_output_filerun(df_object,output_filename,has_converged_out,rho_out,T_out,h_out,u_out,a_out,M_out,ht_out,Pt_out,Tt_out,Re_out,res_out)
else:
    print("ERROR: Invalid program mode. You should never see this message...")
    print("The program will now terminate")
    exit()
print("Writing output file...done")
# We clean the temporary files:
try:
    os.remove("q_first.var") #we remove the temporary file
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
