#.................................................
#   HEAT_FLUX_HFLAW0.PY, v2.0.0, January 2024, Domenico Lanza.
#.................................................
#   This project file is needed to compute the 
#   heat flux for the exact heat flux law, hflaw=0
#.................................................
import heat_flux_hflaw0_edge as heat_flux_hflaw0_edge_file #file with the function to compute the edge properties of the flow for hflaw=0
import heat_flux_hflaw0_wall as heat_flux_hflaw0_wall_file #file with the function to compute the wall properties of the flow for hflaw=0
import heat_flux_hflaw0_flow as heat_flux_hflaw0_flow_file #file with the function to compute the flow properties of the flow for hflaw=0
import continuity as continuity_file #file with the function to solve the continuity equation to compute the heat flux
import first_deriv as first_deriv_file #file with the function to compute the first derivative of a function
import tridiag_inv as tridiag_inv_file #file with the function to solve a tridiagonal system
import math #math library for the sqrt function
import time #library to compute the execution time
import mutationpp as mpp #useful library for thermodynamic computations
import numpy as np #we use this library to save the public variables x,y,z
def heat_flux_hflaw0(probes,settings,Pt,Tt,ue): #function to compute the heat flux for the hflaw=0 case
    #.................................................
    #   This function computes the heat flux for the hflaw=0 case
    #.................................................
    #   INPUTS:
    #   probes: the probes object containing the probes
    #   settings: the settings object containing the settings
    #   Pt: the total pressure
    #   Tt: the total temperature
    #   ue: the edge velocity
    #.................................................
    #   OUTPUTS:
    #   q: the heat flux
    #.................................................
    # we now define some new variables:
    ###### TIMER:INITIALIZATION ######
    ORDER=4 #order for the central,backward and forward finite difference method for the derivatives.
    max_iter=settings.max_ht_iter #maximum number of iterations for the heat flux computations
    ht_conv=settings.ht_conv #convergence criteria for the heat transfer computations
    Pe=Pt # To compute the heat flux at the stagnation point, we use the total pressure(measured OUTSIDE the boundary layer)
    Te=Tt # To compute the heat flux at the stagnation point, we use the total temperature(measured OUTSIDE the boundary layer)
    ue=ue # To compute the heat flux at the stagnation point, we use the edge velocity(measured OUTSIDE the boundary layer)
    Tw=probes.Tw # To compute the heat flux at the stagnation point, we use the wall temperature(constant)
    p=settings.p # Number of points for the boundary layer eta discretization
    q=None #variable to store the heat flux
    eta=None #variable to store the eta_i-th value
    f_i=None #variable to store the f'_i-th value
    g_i=None #variable to store the g_i-th value
    deta=None #variable to store the step of eta
    x=[] #array to store the eta values=eta of the boundary layer(normal)
    y=[] #array to store the f' values of the boundary layer
    z=[] #array to store the g values of the boundary layer
    T=None #variable to store the current loop temperature
    iter=None #variable to store the number of iterations
    # edge properties:
    rhoe=None #density on the edge
    cpe=None #specific heat on the edge
    mue=None #viscosity on the edge
    # wall properties:
    rhow=None #density on the wall
    kwt=None #thermal conductivity on the wall
    # flow properties:
    rho=None #density on the current point
    cp=None #specific heat on the current point
    mu=None #viscosity on the current point
    k=None #thermal conductivity on the current point
    # loop variables:
    khi=None #vector to store the khi values. khi=rho*mu/(rhoe*mue)
    rr=None #vector to store the rr values. rr=rhoe/rho
    kpr=None #vector to store the kpr values. kpr=k/(mue*cp*rr)
    c=None #vector to store the c values. c=cp/cpe
    e=None #vector to store the e values. e=ue^2/(cpe*Te)
    aa=None #vector to store the aa values: coefficients for the continuity equation
    bb=None #vector to store the bb values: coefficients for the quadratic equation
    cc=None #vector to store the cc values: coefficients for the quadratic equation
    dd=None #vector to store the dd values: coefficients for the quadratic equation
    dkhi=None #vector to store the dkhi values: derivative of khi with respect to eta
    V=None #vector to store the V values: solution of the continuity equation
    f1=None #variable to solve the tridiag system
    g1=None #variable to solve the tridiag system
    h1=None #variable to solve the tridiag system
    we=None #variable to solve the tridiag system
    newf=None #variable to solve the tridiag system, new f
    q_first=None #variable to understand if the heat flux has been computed previously
    #START OF THE CODE:
    # Now we define the eta array used to distretize eta:
    # we go from eta=0 to eta=6(we should go to infinity, but we stop at 6. It is a good approximation)
    deta=6/(p-1) #step of eta. We use p-1 because we need p points, not p+1(we start from 0 and we end at 6)
    # now we check if the x,y,z exist, so if the heat flux has been computed previously
    # we need to read the q_first variable from the q_first.var file using numpy
    q_first=np.loadtxt('q_first.var',dtype=int) # we read the q_first variable from the file
    if(q_first==0): #we have never computed the heat flux
        # we now create the x array, which starts from 0, steps of deta, of p points and we initialize f' and g arrays.
        # The x array contains the eta values
        for i in range(p):
            eta=i*deta # we compute the eta value
            x.append(eta) # we append the eta value to the array
            f_i=0.007005*pow(eta,3)-0.114439*pow(eta,2)+0.598555*eta # we compute the f' starting value/guess(formula from previous code)
            y.append(f_i) # we append the f' value to the array
            g_i=min(1,f_i+Tw/Te*(6-eta)/6) # we compute the g starting value/guess(formula from previous code)
            z.append(g_i) # we append the g value to the array
    else: # we have already computed the heat flux
        # we need to read the x,y,z arrays from the x.var,y.var and z.var files using numpy
        x=np.loadtxt('x.var')
        y=np.loadtxt('y.var')
        z=np.loadtxt('z.var')
        x=x.tolist() # we convert the array to a list
        y=y.tolist() # we convert the array to a list
        z=z.tolist() # we convert the array to a list
    ###### TIMER_END:INITIALIZATION ###### 0.00019288063049316406 s, very good
    # we print the vectors x,y,z to the user
    # print("x:")
    # print(x)   
    # print("y:")
    # print(y)
    # print("z:")
    # print(z)    
    mixture=mpp.Mixture(settings.mixture_name) #we create the mixture object
    #we print Te, Pe, Tw, ue
    # print("Te: "+str(Te))
    # print("Pe: "+str(Pe))
    # print("Tw: "+str(Tw))
    # print("ue: "+str(ue))
    # now we need to compute the flow properties at the edge
    ###### TIMER:FLOW_EDGE_PROPERTIES ######
    rhoe,cpe,mue=heat_flux_hflaw0_edge_file.heat_flux_hflaw0_edge(Pe,Te,mixture)
    # we print the edge properties to the user
    # print("Edge properties:")
    # print("rhoe: "+str(rhoe))
    # print("cpe: "+str(cpe))
    # print("mue: "+str(mue))
    ###### TIMER_END:FLOW_EDGE_PROPERTIES ###### 0.01839923858642578 s,acceptable
    # now we need to compute the flow properties at wall:
    ###### TIMER:FLOW_WALL_PROPERTIES ######
    rhow,kwt=heat_flux_hflaw0_wall_file.heat_flux_hflaw0_wall(Pe,Tw,mixture)
    # we print the wall properties to the user
    # print("Wall properties:")
    # print("rhow: "+str(rhow))
    # print("kwt: "+str(kwt))
    ###### TIMER_END:FLOW_WALL_PROPERTIES ###### 0.025792837142944336 s, acceptable
    # now we can start the convergence loop to find the solution
    iter=0 # we initialize the iteration counter
    # we create the mixture object in advace to save time(A LOT!)
    while(True): # we start the convergence loop
        #There is no stopping condition since that we check it inside the loop(if convergence is reached or the max number of iterations is reached)
        iter+=1 # we increase the iteration counter
        #print("Iteration number: "+str(iter))
        #print("Iteration number: "+str(iter))
        # we start by getting the properties across the BL grid
        # we reset some vectors:
        khi=[] # we reset the khi array
        rr=[] # we reset the rr array
        kpr=[] # we reset the kpr array
        c=[]    # we reset the c array
        e=[]    # we reset the e array
        ###### TIMER:FLOW_PROPERTIES_ACROSS_GRID ######
        for i in range(0,p):
            T=Te*z[i] # we compute the temperature. This is because g=z=T/Te
            #print("T: "+str(T))
            if(T<=0): #this should never happen, but we check it anyway
                print("ERROR: T<=0") # it does not make sense to have a negative temperature
                # print("T: "+str(T)) # we print the temperature
                exit() # we exit the program
                # T=abs(T) # we set the temperature to the absolute value, temporary solution
                # z[i]=T/Te # we set the g value to the new value
            # now we retrive the flow properties:
            ###### TIMER:FLOW_PROPERTIES ######
            rho,cp,mu,k=heat_flux_hflaw0_flow_file.heat_flux_hflaw0_flow(Pe,T,mixture)
            ###### TIMER_END:FLOW_PROPERTIES ###### 
            khi_i=rho*mu/(rhoe*mue) # we compute the khi value
            khi.append(khi_i)   # we append the khi value to the array
            rr_i=rhoe/rho   # we compute the rr value
            rr.append(rr_i)  # we append the rr value to the array
            kpr_i=k/(mue*cp*rr_i) # we compute the kpr value
            kpr.append(kpr_i)   # we append the kpr value to the array
            c_i=cp/cpe # we compute the c value
            c.append(c_i)  # we append the c value to the array
            e_i=pow(ue,2)/(cpe*Te) # we compute the e value
            e.append(e_i) # we append the e value to the array
        ###### TIMER_END:FLOW_PROPERTIES_ACROSS_GRID ###### 0.01 FAST!
        # if(iter==4):
        #     exit()  
        #since that the code is fast, we stop documenting the time here
        # now we need to solve the continuity equation to find V
        # we compute the aa vector. This is because dV/deta=-f'=y
        aa=[] # we initialize the aa array
        for i in range(0,p):
            aa.append(-y[i]) # we append the value to the array
        V=continuity_file.continuity(deta,aa) # we solve the continuity equation
        # now we need to solve the momentum equation for y=f'
        #firstly, we need to compute the dkhi vector, that is the derivative of khi with respect to eta
        dkhi=first_deriv_file.first_deriv_array(khi,deta,ORDER) # we compute the dkhi vector
        # we reset the aa,bb,cc and dd vectors
        aa=[] # we initialize the aa array
        bb=[] # we initialize the bb array
        cc=[] # we initialize the cc array 
        dd=[] # we initialize the dd array
        # we set the coefficients of the linear equation to solve
        for i in range(0,p):
            aa.append(khi[i]/pow(deta,2))
            bb.append((dkhi[i]-V[i])/deta) 
            cc.append(0)
            dd.append(0.5*(pow(y[i],2)-rr[i]))
        f1=0
        g1=1
        h1=0
        we=1
        # we solve the tridiagonal system
        newf=tridiag_inv_file.tridiag_inv(we,f1,g1,h1,aa,bb,cc,dd) # we solve it with the tridiag module
        newf.append(we) # we append the we value to the array
        # now we need to solve the energy equation for z=g
        # we computed the needed derivatives
        dkpr=first_deriv_file.first_deriv_array(kpr,deta,ORDER)
        dc=first_deriv_file.first_deriv_array(c,deta,ORDER)
        dy=first_deriv_file.first_deriv_array(y,deta,ORDER)
        # we reset the aa,bb,cc and dd vectors
        aa=[] # we initialize the aa array
        bb=[] # we initialize the bb array
        cc=[] # we initialize the cc array
        dd=[] # we initialize the dd array
        # we set the coefficients of the linear equation to solve
        for i in range(0,p):
            aa.append(kpr[i]/pow(deta,2))
            bb.append((dkpr[i]+kpr[i]/c[i]*dc[i]-V[i])/deta)
            cc.append(0)
            dd.append(e[i]/c[i]*(0.5*rr[i]*y[i]-khi[i]*pow(dy[i],2)))
        f1=0
        g1=1
        h1=Tw/Te
        we=1
        newg=tridiag_inv_file.tridiag_inv(we,f1,g1,h1,aa,bb,cc,dd)
        newg.append(we)
        # now we need to check the convergence to exit the loop
        stop=True # we initialize the stop variable to True
        # we check the convergence for each point of the grid, using the succesive iteration convergence criteria
        # If for each point of the grid, the following iteration criteria is reached, we stop the loop
        for i in range(0,p):
            if(abs(newf[i]-y[i])>ht_conv or abs(newg[i]-z[i])>ht_conv): # if the convergence is not reached
                stop=False # we set the stop variable to False, we do not stop
        # we also stop the loop if the max number of iterations is reached
        if(stop or iter>max_iter): # if the convergence is reached or the max number of iterations is reached
            break # we exit the loop
        # If we do not stop, now we need to update the f and g arrays
        for i in range(0,p):
            y[i]=newf[i]
            z[i]=newg[i]
        #print(".....")
        #print(y)
        #print(".....")
        #print(z)
    # now we need to compute the heat flux
    #we find the derivative of g=z with respect to eta
    dg_v=first_deriv_file.first_deriv_array(z,deta,ORDER) # we compute the derivative of g with respect to eta
    #we take the value on the wall,eta=0
    dg=dg_v[0] #we take the value on the wall,eta=0
    q=math.sqrt(2/(rhoe*mue))*dg*Te*rhow*kwt # we compute the heat flux
    # we multiply by the stagnation variable
    q=q*math.sqrt(probes.stagvar*ue/probes.Rm) #we multiply by the stagnation variable
    # we save the new x,y,z arrays to the x.var,y.var and z.var files using numpy
    np.savetxt('x.var',x) # we save the x array to the file
    np.savetxt('y.var',y) # we save the y array to the file
    np.savetxt('z.var',z) # we save the z array to the file
    if(q_first==0):
        #we update q_first to 1
        q_first=np.array([1])
        #q_first=np.array([0])
        # we save the q_first variable to the q_first.var file using numpy
        np.savetxt("q_first.var",q_first, fmt="%1.1u") # we save the q_first variable to the file
    return q
#.................................................
#   Possible improvements:
#   -Make the central finite derivative order variable
#   -Understand with eta stops at 6 and if it is a good approximation/improvable
#   -Understand if we need to keep the x,y,z arrays to the files
#.................................................
# EXECUTION TIME: TBD
#.................................................
#   KNOW PROBLEMS:
#   None.
#.................................................