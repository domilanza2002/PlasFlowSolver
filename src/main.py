#.................................................
#       PLASPROBES Project
#       main.py: main script
#       Version 2.0.0, Domenico Lanza
#.................................................
#   I will re-write in python the program "Plasprobes" written by  Benoit Bottin, March 1999, VKI Ar. Dpt.(v1.1)
#   The previous code used the libray PEGASE 4.5, but unfortunately I did not manage to find it anywhere, so I will use the library
#   MUTATION++, which follows the same purpose.
#   Starting date: 01/28/2024
#   In this version, I will not strictly follow the original code, but I will try to make it more readable and easy to upgrade
#.................................................
#
#    LIBRARY IMPORTS:
#   I will import here the useful libraries for the project
import math #useful library for math operations
import numpy as np  #useful library for math operations and to store x,y,z
import mutationpp as mpp #useful library for thermodynamic computations
import time #useful library for time operations
#       add more if needed...
#
#.................................................
#   PROJECT FILES IMPORTS:
#   I will import here the other files of the project: modules
#   The format of the import is "file" as "name_file"
import classes as classes_file #file with the classes of the program
import presentation as presentation_file #file with the presentation of the program
import read_settings as read_settings_file #file with the function to read the settings
import read_probes as read_probes_file #file with the function to read the probes properties
import read_initials as read_initials_file #file with the function to read the initial conditions
import prompt_input_file as prompt_input_file_file #file with the function to prompt the user to choose the input file
import heat_flux as heat_flux_file #file with the function to compute the heat flux
import enthalpy as enthalpy_file #file with the function to compute the enthalpy
import entropy as entropy_file #file with the function to compute the entropy
import barker_effect as barker_effect_file #file with the function to compute the barker effect
import jacobian_matrix as jacobian_matrix_file #file with the function to compute the jacobian matrix
import system_solve as system_solve_file #file with the function to solve the system
#   ....ADD THEM HERE....
#
#.................................................
#
#       GLOBAL VARIABLES:
#       In the future it could be a good idea to organize them better in different files/classes/modules
#       I will put here the global variables of the program
#   File name variables:
input_file_name=None #name of the input file
output_file_name=None #name of the output file
#   File variables:
input_file=None #input file variable
output_file=None #output file variable
#   Counter variables:
ncase=None #number of cases counter of the input file
n_eq=None #number of equations to solve
#   Loop variables read from input:
comment=None #comment of the line
Pe=None #static pressure at the edge. Read from input
Pdyn=None #dynamic pressure at the edge. Read from input
Pstag=None #total pressure at the edge. Computed from P_e and P_dyn
q_target=None #target heat flux. Read from input
# Inner loop variables:
iter=None #number of iterations
has_converged=None #boolean to check if the iteration has converged
res=None #residuals
cnv=None #convergence criteria
cnvref=None #reference convergence criteria
jac=None #jacobian matrix
#   Loop thermodynamic variables:
q=None #heat flux
Pt=None #total pressure
Pb=None #barker pressure
Te=None #static temperature
Tt=None #total temperature
ue=None #velocity
he=None #enthalpy at the edge
ht=None #enthalpy at the stagnation point
se=None #entropy at the edge
st=None #entropy at the stagnation point
Tstar=None #variable to store new temporary T value
ustar=None #variable to store new temporary u value
Ttstar=None #variable to store new temporary Tt value
Ptstar=None #variable to store new temporary Pt value
relax=None #relaxation factor
Re=None #reynolds number of the pitot probe
# final properties:
mix=None #mixture
rhoe=None #density at the edge
ae=None #sound speed at the edge
Me=None #mach number at the edge
Ht=None #total enthalpy at the edge
# variable for heat flux optimization:
q_first=None #variable to store 0 or 1. 0: we have never computed the heat flux. 1: we have already computed the heat flux previously, so we have a x,y,z file
#
#.................................................
#   INSTANCIATE OBJECTS:
#   I will create here the objects we will use
settings_object=classes_file.settings_class() #object with the settings of the program
probes_object=classes_file.probes_class() #object with the probes properties
initials_object=classes_file.initials_class() #object with the initial conditions
#   ....ADD THEM HERE....
#
#.................................................
#
#       PROGRAM START:
#       Here the program starts

#    First of all, we call the presentation module to print the presentation of the program:
presentation_file.presentation() # we call the presentation function
#   Now we are going to read the setting file and store it in the settings_object:
settings_object=read_settings_file.read_settings() #note: never edit this object
#   Now we are going to read the probes properties file:
probes_object=read_probes_file.read_probes() #note: never edit this object
#   Now we are going to check for the type of heat flux law:
if (probes_object.hflaw==0): #if we use the exact heat flux law
    print("Exact heat flux law computation detected") #we can go on, we have an implementation for this
else: #otherwise we do not have an implementation for this
    print("Error: heat flux law not yet implemented") #we print an error message
    exit() #we exit the program
#   note: in the future we could add more implementations for the heat flux law
#   SUPPOSING HFLAW==0:Now we are going to read the initial conditions file:
initials_object=read_initials_file.read_initials() #note: never edit this object
#   Now we are going to read the input/output file name:
input_file_name,output_file_name=prompt_input_file_file.prompt_input_file(settings_object) #note: never edit this variables
#   Now we understand how many equations we have to solve:
if(probes_object.barker==0): #we check if we need to consider the barker effect
    n_eq=3 #we do not consider the barker effect, so we need to solve 3 equations, since that Pt=Pstag
    print("Barker effect not considered") #we print a message to the user
else: #otherwise we need to consider the barker effect:
    n_eq=4 #we do consider the barker effect, so we need to solve 4 equations, since that Pt!=Pstag
    print("Barker effect considered") #we print a message to the user
#
#.................................................
#   MAIN PROGRAM LOOP:
#   Here the main program loop starts
#   Premilimary operation:
if(probes_object.hflaw==0): #if we use the exact heat flux law
    #we want to store x,y,z in a file in order to use the previous results each time we compute the heat flux
    # for now, we want to inizialize the variable q_first, that stores 0 or 1:
    #   0: We have never computed the heat flux
    #   1: We have already computed the heat flux previously, so we have a x,y,z file
    q_first=np.array([0]) #we initialize the variable
    # now we want to store this variable in a file using numpy.savetxt
    np.savetxt("q_first.var",q_first, fmt="%1.1u") #we store the variable in a file
print("Starting main program loop...") #we print a message to the user
ncase=0 #we initialize the number of cases counter
input_file=open(input_file_name,"r") #we open the input file
while(True): #this is the main loop of the program
    #   The loop does not have a stop conditions since that it is performed inside the loop.
    #   The loop will stop when the end of file is reached
    #we want to read one line of data from the input file. The format is:t
    #   a)20 characters of comment
    #   b)e20.8 static pressure value
    #   c)e20.8 dynamic pressure value(pitot reading)
    #   d)e20.8 heat flux probe measurament
    #now we read the first line of the input file:
    line=input_file.readline()
    #we check if we reached the end of file:
    if(line=="" or line=="\n"): 
        break #if we reached the end of the file, we break the loop. This is the stop condition
    print("--------------------------------------------------")
    print("Executing case number "+str(ncase+1)+"...")
    #now we need to extract the data from the line:
    comment=line[0:20] # The first 20 characters are the comment
    Pe=float(line[20:40].strip().replace("d","e")) # the next 20 characters are the static pressure
    Pdyn=float(line[40:60].strip().replace("d","e")) # the next 20 characters are the dynamic pressure
    q_target=float(line[60:80].strip().replace("d","e")) # the next 20 characters are the heat flux
    #now we convert them with the convertion factor from the probes file:
    Pe*=probes_object.psfactor #static pressure in Pa
    q_target*=probes_object.qfactor #heat flux in W/m^2
    Pstag=Pe+(Pdyn*probes_object.ptfactor) #total pressure in Pa
    ncase+=1 #we increase the number of cases
    print("Data read:") #we print the data read from the input file to the user
    print("Comment: "+comment)
    print("Static pressure: "+str(Pe)+" Pa")
    print("Dynamic pressure: "+str(Pdyn)+" Pa")
    print("Heat flux: "+str(q_target)+" W/m^2")
    print("Stagnation pressure: "+str(Pstag)+" Pa")
    # now we reset some variables useful for the upcoming loops:
    iter=0 #we reset the iteration counter for the newton loop
    has_converged=False #we reset the convergence boolean for the newton loop
    # if in the initial conditions file the total pressure is set to 0, we set it to the value computed from the edge(stagnation pressure):
    #   note: this is true is no barkers effect is considered
    if(initials_object.Pt_0==0): #P_t is the total pressure. Here we are setting an initial value for it
        Pt=Pstag
    else:
        Pt=initials_object.Pt_0
        if(probes_object.barker==0): #if no barker effect is considered
            print("Warning: if no barker effect is considered, then the stagnation pressure read from the input file is the total pressure")
            print("We are going to use the stagnation pressure read from the input file instead of the one read from the initial conditions file")
            Pt=Pstag #if no barker effect is considered, the total pressure is the stagnation pressure
    # We need to inizialize the other thermo variables:
    Te=initials_object.T_0 #T_e is the static temperature
    Tt=initials_object.Tt_0 #T_t is the total temperature
    ue=initials_object.u_0 #u_e is the velocity
    # The unknowns are: Tt,u,Te,Pt. Pe is constant
    # Now we start the newton loop to obtain the flow parameters from the probes.
    # This procedure is described in Bottin, Ph.D. Thesis, 136-137
    # we print the initials conditions to the user:
    # print("Initial conditions:")
    # print("Te: "+str(Te)+" K")
    # print("Tt: "+str(Tt)+" K")
    # print("Ue: "+str(ue)+" m/s")
    # print("Pt: "+str(Pt)+" Pa")
    print("Executing Newton loop...")
    while(True): #this is the Newton loop
        #   The loop does not have a stop conditions since that it is performed inside the loop.
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
        #print("------------------------------------")
        q=heat_flux_file.heat_flux(probes_object,settings_object,Pt,Tt,ue) #we compute the heat flux
        #print("Heat flux: "+str(q)+" W/m^2")
        # now we compute the enthalpy:
        he=enthalpy_file.enthalpy(settings_object,Pe,Te) #we compute the enthalpy at the edge
        #print("Enthalpy at the edge: "+str(he)+" J/kg")
        ht=enthalpy_file.enthalpy(settings_object,Pt,Tt) #we compute the enthalpy at the stagnation point
        #print ("Enthalpy at the stagnation point: "+str(ht)+" J/kg")
        # now we compute the entropy:
        se=entropy_file.entropy(settings_object,Pe,Te) #we compute the entropy at the edge
        #print("Entropy at the edge: "+str(se)+" J/kg K")
        st=entropy_file.entropy(settings_object,Pt,Tt) #we compute the entropy at the stagnation point
        #print("Entropy at the stagnation point: "+str(st)+" J/kg K")
        # now we compute the barker effect:
        if(probes_object.barker!=0): #we check if we need to compute the barker effect
            # we compute the barker effect:
            Pb,Re=barker_effect_file.barker_effect(probes_object,settings_object,Pt,Pe,Te,ue) #we compute the barker pressure
        else: # we do not need to compute the barker effect
            Pb=Pt #we set the barker pressure to the total pressure
            Re=0 #we set the reynolds number to 0
        #.................................................
        #   We can now compute the residuals:
        res=[] #we initialize the residuals array
        res.append(-(q-q_target)) #residual 1
        res.append(-(ht-(he+0.5*pow(ue,2)))) #residual 2
        res.append(-(st-se)) #residual 3
        res.append(-(Pb-Pstag)) #residual 4
        cnv=0 #we reset the convergence criteria
        for i in range(n_eq): #we compute the convergence criteria
            cnv+=pow(res[i],2)
        #we use a normalized convergence criteria:
        if(iter==1): #we check if this is the first iteration
            cnvref=math.sqrt(cnv) #we set the reference convergence criteria/normalize
            cnv=1 #we set the convergence criteria to 1
        else:
            cnv=math.sqrt(cnv)/cnvref #we compute the convergence criteria
        #.................................................
        #   We can now check if the iteration has converged:
        print("Case:"+str(ncase)+", Iteration "+str(iter)+", convergence criteria: "+str(cnv))
        if(iter>settings_object.iterlim): #we check if we reached the maximum number of iterations
            break #we break the loop
        if(cnv<settings_object.cnvlim): #we check if we reached the convergence criteria
            has_converged=True
            break
        #.................................................
        #   We can now compute the jacobian:
        jac=jacobian_matrix_file.jacobian_matrix(probes_object,settings_object,Te,Tt,Pe,Pt,Pb,q,he,ht,se,st,ue) #we compute the jacobian matrix
        #.................................................
        #   Now we finally solve the system
        dvar=system_solve_file.system_solve(n_eq,jac,res)
        Tstar=Te+dvar[0]
        ustar=ue+dvar[1]
        Ttstar=Tt+dvar[2]
        Ptstar=Pt+dvar[3]
        #.................................................
        #   Now we perform the under-relaxation scheme:
        # This scheme avoids that Tstar,Ustar, Ttstar and Ptstar
        # become negative or too high
        relax=1.0 #we set the relaxation factor
        # we check if the new values are negative:
        while( (Tstar<0) or (ustar<0) or (Ttstar<0) or (Ptstar<0) ): 
            relax=relax/2 #we decrease the relaxation factor
            print("Relaxing the solution...")
            # we relax the new values
            Tstar=Te+dvar[0]*relax
            ustar=ue+dvar[1]*relax
            Ttstar=Tt+dvar[2]*relax
            Ptstar=Pt+dvar[3]*relax
        # we check if the new values are too high:
        while( (Tstar>settings_object.max_value_T) or (Ttstar>settings_object.max_value_T)):
            relax=relax/2 #we decrease the relaxation factor
            print("Relaxing the solution...")
            # we relax the new values
            Tstar=Te+dvar[0]*relax
            ustar=ue+dvar[1]*relax
            Ttstar=Tt+dvar[2]*relax
            Ptstar=Pt+dvar[3]*relax
        #.................................................
        #  Now we update the variables:
        Te=Tstar
        #print("Static temperature: "+str(Te)+" K")
        ue=ustar
        Tt=Ttstar
        if(probes_object.barker!=0):
            Pt=Ptstar
        else:
            Pt=Pstag
    print("Executing Newton loop...done")
    # Now we need to compute the flow properties useful for data rebuilding
    mix=mpp.Mixture(settings_object.mixture_name) #we create the mixture
    mix.equilibrate(Te,Pe) #we equilibrate the mixture
    rhoe=mix.density() #we compute the density
    ae=mix.equilibriumSoundSpeed() #we compute the sound speed
    Me=ue/ae #we compute the mach number
    he=mix.mixtureHMass()#we compute the mixture enthalpy
    mix.equilibrate(298.15,Pe)
    #h_shift=mix.mixtureHMinusH0Mass() #we compute the enthalpy shift
    h_shift=mix.mixtureHMinusH0Mass() #we compute the enthalpy shift
    he=he+h_shift #we subtract the enthalpy shift
    ht=he+0.5*pow(ue,2) #we compute the total enthalpy
    # The Reynold number is taken from the barker effect computation in the loop
    # now we need to write on the output file:
    print("Writing on output file...")
    if(ncase==1): #if it is the first case, we need to check if the output file already exists
        try:
            output_file=open(output_file_name,"r") #we try to open the output file
            output_file.close() #we close the output file
            #if the file exits, we append the date and time in the file
            output_file=open(output_file_name,"a") #we open the output file in append mode
            # we retrieve date and time
            date=time.strftime("%d/%m/%Y")
            time=time.strftime("%H:%M:%S")
            # we write the date and time in the file
            output_file.write("----- Data appended at: "+time+" on "+date+" -----\n")
        except: #if the file does not exist, we just create it
            output_file=open(output_file_name,"w")
        # we write the header of the file
        output_file.write("comment                    pressure [Pa]     density [kg/m3]     temperature [K]     enthalpy [J/kg]      velocity [m/s]   sound speed [m/s]         Mach number  total enth. [J/kg] Pitot pressure [Pa] total pressure [Pa]    heat flux [W/m2]      Pitot Reynolds\n")
        output_file.close()
    # now we append the results
    output_file=open(output_file_name,"a")
    if(has_converged):
        # i want each data to occupy exactly 20 characters, in order to have a nice output file
        output_file.write(comment+'{:20.10e}'.format(Pe)+'{:20.10e}'.format(rhoe)+'{:20.10e}'.format(Te)+'{:20.10e}'.format(he)+'{:20.10e}'.format(ue)+'{:20.10e}'.format(ae)+'{:20.10e}'.format(Me)+'{:20.10e}'.format(ht)+'{:20.10e}'.format(Pstag)+'{:20.10e}'.format(Pt)+'{:20.10e}'.format(q)+'{:20.10e}'.format(Re)+"\n")
    else:
        output_file.write("WARNING: the next set of data has not converged: residual= "+str(cnv)+"\n")
        output_file.write(comment+'{:20.10e}'.format(Pe)+'{:20.10e}'.format(rhoe)+'{:20.10e}'.format(Te)+'{:20.10e}'.format(he)+'{:20.10e}'.format(ue)+'{:20.10e}'.format(ae)+'{:20.10e}'.format(Me)+'{:20.10e}'.format(ht)+'{:20.10e}'.format(Pstag)+'{:20.10e}'.format(Pt)+'{:20.10e}'.format(q)+'{:20.10e}'.format(Re)+"\n")
    print("Executing case number "+str(ncase)+"...done")
    #we close the output file:
    output_file.close()
print("--------------------------------------------------")
#we close the input file:
input_file.close()
print("Program terminated")