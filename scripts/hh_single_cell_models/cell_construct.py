"""
This file construct the equations for brian2
"""
from __future__ import print_function
import numpy as np
import brian2
    
from brian2 import *
from .cell_library import get_neuron_params


import sys
sys.path.append('../')
from hh_synapses_and_connectivity.syn_and_connec_library import get_connectivity_and_synapses_matrix


def get_membrane_equation(neuron_params, synaptic_array,\
                          return_equations=False):

    # ---- Default tau_max handling ----
    if 'tau_max' not in neuron_params:
        neuron_params['tau_max'] = 400.  # default in ms
    
    # added El and VT to equations

    eqs = """
        dV/dt = (%(Gl)f*nS*(El - V) 
            - %(GNa)f*nS*(m*m*m)*h*(V-%(ENa)f*mV) 
            - %(GK)f*nS*(n*n*n*n)*(V - %(EK)f*mV) 
            - %(GM)f*nS*p*(V - %(EK)f*mV) 
            + I)/(%(Cm)f*pF) : volt
        dm/dt = 0.32*(mV**-1)*(13.*mV-V+VT)/
            (exp((13.*mV-V+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(V-VT-40.*mV)/
            (exp((V-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
        dn/dt = 0.032*(mV**-1)*(15.*mV-V+VT)/
            (exp((15.*mV-V+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-V+VT)/(40.*mV))/ms*n : 1
        dh/dt = 0.128*exp((17.*mV-V+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-V+VT)/(5.*mV)))/ms*h : 1
        dp/dt=((1./
            (exp(-(35.*mV+V)/(10.*mV))+1.))-p)/((%(tau_max)f*ms)/(3.3*( exp((35.*mV+V)/(20.*mV)) )+1.*(exp(-(35.*mV+V)/(20.*mV))) )) :1
        El : volt
        VT : volt
        """% neuron_params
    
        




    ## synaptic currents, 1) adding all synaptic currents to the membrane equation via the I variable
    eqs += """
        I = I0 """
    for synapse in synaptic_array:
        # loop over each presynaptic element onto this target
        Gsyn = 'G'+synapse['name']
        eqs += '+'+Gsyn+'*(%(Erev)f*mV - V)' % synapse
    eqs += ' : amp'
    
    ## synaptic currents, 2) constructing the temporal dynamics of the synaptic conductances
    ## N.B. VALID ONLY FOR EXPONENTIAL SYNAPSES UNTIL NOW !!!!
    for synapse in synaptic_array:
        # loop over each presynaptic element onto this target
        Gsyn = 'G'+synapse['name']
        eqs += """
        """+'d'+Gsyn+'/dt = -'+Gsyn+'*(1./(%(Tsyn)f*ms)) : siemens' % synapse
    eqs += """
        I0 : amp """
    # adexp, pratical detection threshold Vthre+5*delta_v


    # changed spike detection to V>0 mV

    neurons = brian2.NeuronGroup(neuron_params['N'], model=eqs,\
                                 threshold='V > 0*mV', # changed from -40
                                 refractory='V > 0*mV', # changed from -40
                                 method='exponential_euler')





    #print(eqs)
    if return_equations:
        return neurons, eqs
    else:
        return neurons


if __name__=='__main__':

    print(__doc__)
    
    # starting from an example

# starting from an example


    NTWK='CONFIG1'
    M = get_connectivity_and_synapses_matrix(NTWK, number=2)
    NRN_exc='HH_RS'
    
    # number of neurons
    Ne, Ni= int(M[0,0]['Ntot']*(1-M[0,0]['gei'])), int(M[0,0]['Ntot']*M[0,0]['gei'])
    print("EEEE",NRN_exc)
    exc_neurons, eqs = get_membrane_equation(get_neuron_params(NRN_exc, number=Ne), M[:,0], return_equations=True)
    
    neuron = NeuronGroup(1, eqs,threshold='V > -40*mV',refractory='V > -40*mV',method='exponential_euler')
    
    neuron.V = -65.
    neuron.p  = '.2'
    neuron.m  = '.2'
    neuron.h  = '.2'
    neuron.n  = '.2'
    
    mon = StateMonitor(neuron, ['V', 'n'], record=True)
    neuron.I0 = 50700*pA
    run_time = 200*ms
    run(run_time)
    
    
    #plt.plot(mon.t/ms, mon.V[0]/mV)
    #plt.show()
    
    
    
    ivect=np.arange(240,800,10)
    
    ivect=np.arange(240,800,100)
    
    frvect=[]
    for i in range(len(ivect)):
        
        
        neuron.V = -65.
        neuron.p  = '.2'
        neuron.m  = '.2'
        neuron.h  = '.2'
        neuron.n  = '.2'
        mon = StateMonitor(neuron, ['V', 'n'], record=True)
        neuron.I0 = ivect[i]*pA
        #neuron.I0 = 300*pA
        run_time = 2000*ms
        if(ivect[i]<400):
            run_time = 10000*ms
            run_time = 200*ms
        run(run_time)
        vv=mon.V[0]/mV
        tt=mon.t/ms
        cc=0
        for j in range(10,len(vv)-1):
            if(vv[j]<20 and vv[j+1]>20):
                cc+=1
    
        print("eee",cc,tt[-1]-tt[0],ivect[i])
        #plt.plot(tt,vv)
        #plt.show()


        frvect.append(1000*cc/(tt[-1]-tt[0]))


#plt.plot(ivect,frvect,'o')
#plt.show()

#np.save('hh_fi_4',[ivect,frvect])