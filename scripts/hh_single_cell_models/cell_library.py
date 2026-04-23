"""
Some configuration of neuronal properties so that we pick up
within this file
"""
from __future__ import print_function
from math import pi

def get_neuron_params(NAME, name='', number=1, SI_units=False):

    # New HH variants matching AdEx passive membrane properties (from grid search)
    
    if NAME=='HH_RS_grid':
        
        membrane_size = 200e-6  # cm²
        
        # Excitatory (RS) - matching AdEx with b=0, gL=10nS, EL=-70mV
        params = {
            'name':name, 'N':number,\
            'Cm': 1.0*1.e6 * membrane_size,          # = 200 pF
            'Gl': 0.05*1.e6 * membrane_size,         # = 10 nS (matches AdEx gL)
            'GNa': 90*1.e-3 * 1.e9 * membrane_size,    # from grid search
            'GK': 3.0*1.e-3 * 1.e9 * membrane_size,  # from grid search
            'GM':  0.,                              # b=0 -> no adaptation
            'El': -70.,   # mV
            'EK': -90.,
            'ENa': 50.,
            'VT': -53,   # from grid search
            'tau_max': 4000., # irrelevant as no adaptation
            'hhtype': 1
        }

    elif NAME=='HH_FS_grid':

        membrane_size = 200e-6  # cm²

        # Inhibitory (FS) - matching AdEx with gL=10nS, EL=-70mV
        params = {
            'name':name, 'N':number,\
            'Cm': 1.0e6 * membrane_size,          # = 200 pF
            'Gl': 0.05e6 * membrane_size,         # = 10 nS
            'GNa': 110*1.e-3 * 1.e9 * membrane_size,    # from grid search
            'GK': 5.0*1.e-3 * 1.e9 * membrane_size,  # from grid search
            'GM':  0,                              # FS has no M-current
            'El': -70.,
            'EK': -90.,
            'ENa': 50.,
            'VT': -55,   # from grid search
            'tau_max': 4000., # irrelevant as no adaptation
            'hhtype': 1
        }

    else:
        print('====================================================')
        print('------------ CELL NOT RECOGNIZED !! ---------------')
        print('====================================================')


    if SI_units:
        print('cell parameters in SI units')
        # mV to V
        params['El'], params['Vthre'], params['Vreset'], params['delta_v'] =\
            1e-3*params['El'], 1e-3*params['Vthre'], 1e-3*params['Vreset'], 1e-3*params['delta_v']
        # ms to s
        params['Trefrac'], params['tauw'] = 1e-3*params['Trefrac'], 1e-3*params['tauw']
        # nS to S
        #params['a'], params['Gl'],params['GNa'],params['GK'] = 1e-9*params['a'], 1e-9*params['Gl'],1e-9*params['GNa'],1e-9*params['GK']
        params['a'], params['Gl']= 1e-9*params['a'], 1e-9*params['Gl']
        # pF to F and pA to A
        params['Cm'], params['b'] = 1e-12*params['Cm'], 1e-12*params['b']

        if(params['hhtype']>0):
            params['GNa'],params['GK'],params['GM'] = 1e-9*params['GNa'],1e-9*params['GK'],1e-9*params['GM']
            params['VT'],params['ENa'],params['EK'] =1e-3*params['VT'],1e-3*params['ENa'],1e-3*params['EK']
    else:
        print('cell parameters --NOT-- in SI units')
        
    return params.copy()

if __name__=='__main__':

    print(__doc__)
