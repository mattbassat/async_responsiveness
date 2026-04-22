"""
Some configuration of neuronal properties so that we pick up
within this file
"""
from __future__ import print_function
from math import pi

def get_neuron_params(NAME, name='', number=1, SI_units=False):

    if NAME=='HH_FS':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':0.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':30.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}
        
    # new version of above with GM equal to zero
    elif NAME=='HH_RS_GM0':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':0.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}



    elif NAME=='HH_RS_DB':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':30.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS_A':
        params = {'name':name, 'N':number,\
            'Gl':10.,'GNa':20000.,'GK':6000,'GM':30.,  'Cm':50.,'Trefrac':5.,\
            'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}

    elif NAME=='HH_RS_noAd':
        params = {'name':name, 'N':number,\
                'Gl':20.,'GNa':20000.,'GK':6000,'GM':0.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS1':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':80.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS2':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':15.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}
        
    # Add other HH variants with neurons from Pospischil et al. 2008

    elif NAME=='HH_RSpospischil':
        params = {'name':name, 'N':number,\
                'Gl':1.90,'GNa':50000.,'GK':4800,'GM':130.,  'Cm':100.,\
                'El':-65.,'EK':-90.,'ENa':50., 'VT':-61.5,'hhtype':1,\
                'tau_max': 1123.5}
        
    elif NAME=='HH_FSpospischil':
        params = {'name':name, 'N':number,\
                'Gl':8.21,'GNa':46000.,'GK':5100,'GM':70.,  'Cm':100.,\
                'El':-65.,'EK':-90.,'ENa':50., 'VT':-61.84,'hhtype':1,\
                'tau_max': 824.5}
        
    # # Add other HH variants with neurons from Giannari and Astolfi 2022

    # elif NAME=='HH_RS_GA':
    #     params = {'name':name, 'N':number,\
    #             'Gl':1.90,'GNa':56000.,'GK':6000,'GM':75.,  'Cm':100.,\
    #             'El':-70.3,'EK':-90.,'ENa':56., 'VT':-56.2,'hhtype':1,\
    #             'tau_max': 1123.5}
        
    # elif NAME=='HH_FS_GA':
    #     params = {'name':name, 'N':number,\
    #             'Gl':8.21,'GNa':56000.,'GK':10000,'GM':0.,  'Cm':50.,\
    #             'El':-70.,'EK':-90.,'ENa':50., 'VT':-56.2,'hhtype':1,\
    #             'tau_max': 824.5}
        
    # Add hybrid HH variants with as many parameters as possible taken from AdEx, and others taken from Pospischil et al. 2008
    # Justify - different transfer functions for RS and FS cells integral to responsiveness peak - not captured in Carlu

    elif NAME=='HH_FS_hybrid':
        params = {'name':name, 'N':number,\
                'Gl':10., 'Cm':200., 'El':-65., 'VT':-50, 'Trefrac':5.,\
                'GNa':46000.,'GK':5100,'GM':70., 'EK':-90.,'ENa':50., 'tau_max': 824.5,\
                'Vthre':-40., 'Vreset':-60., 'delta_v':0.,'hhtype':1,'hhtype':1, 'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS_hybrid':
        params = {'name':name, 'N':number,\
                'Gl':10., 'Cm':200., 'El':-65., 'VT':-50, 'Trefrac':5.,\
                'GNa':50000.,'GK':4800,'GM':130., 'EK':-90.,'ENa':50., 'tau_max': 1123.5,\
                'Vthre':-40., 'Vreset':-60., 'delta_v':0.,'hhtype':1, 'a':0., 'b': 0., 'tauw':1e9}

    # New version of Pospischil cells from figures (figure 2a for RS and figure 4 for FS)
    # Values adjusted to cell size
    # CHECK MATHS!!!

    elif NAME=='HH_RS_pospischil_clean':

        L = 61.4 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 61.4 * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 2.05*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008\
            'GNa': 0.056*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.006*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GM': 7.5*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Cm': 1.0*1.e6 * membrane_size, # in pF/cm^2, from Pospischil et al. 2008
            'El': -70.3, # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -56.2, # in mV, from Pospischil et al. 2008
            'tau_max': 608., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }
    elif NAME=='HH_FS_pospischil_clean':

        L = 56.9 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 56.9 * 1.e-4 # in cm, from Pospischil et al. 2008\
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 3.8*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GNa': 0.058*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.0039*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GM': 7.87*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Cm': 1.0*1.e6 * membrane_size, # in pF/cm^2, from Pospischil et al. 2008
            'El': -70.4, # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -57.9, # in mV, from Pospischil et al. 2008
            'tau_max': 502., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }

    elif NAME=='HH_RS_pospischil_clean_alt':

        L = 61.4 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 61.4 * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 2.05*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008\
            'GNa': 0.056*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.006*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            # 'GM': 7.5*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GM': 0. * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Cm': 1.0*1.e6 * membrane_size, # in pF/cm^2, from Pospischil et al. 2008
            'El': -70.3, # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -56.2, # in mV, from Pospischil et al. 2008
            'tau_max': 608., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }
    
    elif NAME=='HH_FS_pospischil_clean_alt':

        # L = 56.9 * 1.e-4 # in cm, from Pospischil et al. 2008
        # d = 56.9 * 1.e-4 # in cm, from Pospischil et al. 2008
        L = 56.9 * (2/3) * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 56.9 * (2/3) * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 3.8*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GNa': 0.058*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.0039*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            # 'GM': 7.87*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GM': 0. * membrane_size, # changed
            'Cm': 1.0*1.e6 * membrane_size, # in pF/cm^2, from Pospischil et al. 2008
            'El': -70.4, # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -57.9, # in mV, from Pospischil et al. 2008
            'tau_max': 502., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }

    elif NAME=='HH_RS_pospischil_clean_alt2':

        L = 61.4 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 61.4 * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 2.05*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008\
            'GNa': 0.056*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.006*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            # 'GM': 7.5*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GM': 0. * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Cm': 1.0*1.e6 * membrane_size, # in pF/cm^2, from Pospischil et al. 2008
            'El': -70.3, # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -56.2, # in mV, from Pospischil et al. 2008
            'tau_max': 608., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }
    
    elif NAME=='HH_FS_pospischil_clean_alt2':

        # L = 56.9 * (2/3) * 1.e-4 # in cm, from Pospischil et al. 2008
        # d = 56.9 * (2/3) * 1.e-4 # in cm, from Pospischil et al. 2008
        L = 61.4 * (1/2) * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 61.4 * (1/2) * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 3.8*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GNa': 0.058*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.0039*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            # 'GM': 7.87*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GM': 0. * membrane_size, # changed
            'Cm': 1.0*1.e6 * membrane_size, # in pF/cm^2, from Pospischil et al. 2008
            'El': -70.4, # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -57.9, # in mV, from Pospischil et al. 2008
            'tau_max': 502., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }

    elif NAME=='HH_RS_pospischil_ferret':

        L = 96 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 96 * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 1.0*1.e5 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GNa': 0.05*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.005*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008 
            'GM': 7*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Cm': 1.0*1.e6 * membrane_size, # CHECK THIS
            'El': -70., # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -60, # EXPLORE
            'tau_max': 4000., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }
    
    elif NAME=='HH_FS_pospischil_ferret':

        L = 67 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 67 * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 1.5*1.e5 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GNa': 0.05*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.01*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008 
            'GM': 0 * membrane_size,
            'Cm': 1.0*1.e6 * membrane_size, # CHECK THIS
            'El': -70., # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -60, # EXPLORE
            'tau_max': 4000., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }

    elif NAME=='HH_RS_pospischil_ferret_alt':

        # L = 96 * 1.e-4 # in cm, from Pospischil et al. 2008
        # d = 96 * 1.e-4 # in cm, from Pospischil et al. 2008
        L = 64 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 64 * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            # 'Gl': 1.0*1.e5 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Gl': 1.0*1.e5 * membrane_size, # changed
            'GNa': 0.05*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.005*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008 
            'GM': 7*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            # 'Cm': 1.0*1.e6 * membrane_size, # CHECK THIS
            'Cm': 1.0*1.e6 * membrane_size, # changed
            'El': -70., # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -60, # EXPLORE
            # 'tau_max': 4000., # in ms, from Pospischil et al. 2008
            'tau_max': 4000., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }
    
    elif NAME=='HH_FS_pospischil_ferret_alt':

        # L = 67 * 1.e-4 # in cm, from Pospischil et al. 2008
        # d = 67 * 1.e-4 # in cm, from Pospischil et al. 2008
        L = 36 * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 36 * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 1.5*1.e5 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GNa': 0.05*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.01*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008 
            'GM': 0 * membrane_size,
            # 'Cm': 1.0*1.e6 * membrane_size, # CHECK THIS
            'Cm': 1.0*1.e6 * membrane_size, # changed
            'El': -70., # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -60, # EXPLORE
            'tau_max': 4000., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }

    elif NAME=='HH_RS_pospischil_ferret_alt2':

        # L = 96 * 1.e-4 # in cm, from Pospischil et al. 2008
        # d = 96 * 1.e-4 # in cm, from Pospischil et al. 2008
        L = 96*(5/6) * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 96*(5/6) * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            # 'Gl': 1.0*1.e5 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Gl': 1.0*1.e5 * membrane_size, # changed - explore
            'GNa': 0.05*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.005*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008 
            # 'GM': 7*1.e4 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GM': 0 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'Cm': 1.0*1.e6 * membrane_size, # CHECK THIS
            'El': -70., # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -60, # EXPLORE
            'tau_max': 4000., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }
    
    elif NAME=='HH_FS_pospischil_ferret_alt2':

        # L = 67 * 1.e-4 # in cm, from Pospischil et al. 2008
        # d = 67 * 1.e-4 # in cm, from Pospischil et al. 2008
        L = 67*(5/6) * 1.e-4 # in cm, from Pospischil et al. 2008
        d = 67*(5/6) * 1.e-4 # in cm, from Pospischil et al. 2008
        membrane_size = pi * L * d # in cm^2, from Pospischil et al. 2008

        params = {
            'name':name, 'N':number,\
            'Gl': 1.5*1.e5 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GNa': 0.05*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008
            'GK': 0.01*1.e9 * membrane_size, # in nS/cm^2, from Pospischil et al. 2008 
            'GM': 0 * membrane_size,
            # 'Cm': 1.0*1.e6 * membrane_size, # CHECK THIS
            'Cm': 1.0*1.e6 * membrane_size, # CHECK THIS
            'El': -70., # in mV, from Pospischil et al. 2008
            'EK': -90.,
            'ENa': 50.,
            'VT': -60, # EXPLORE
            'tau_max': 4000., # in ms, from Pospischil et al. 2008
            'hhtype': 1
        }

    # New HH variants matching AdEx passive membrane properties (from grid search)
    
    elif NAME=='HH_RS_grid':
        
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
    

    # Add new HH variants from Destexhe, Contreras and Steriade 1998, with parameters taken from Table 1
    elif NAME=='HH_RS_DCS':
        membrane_size = 29000 * 1.e-8 # in cm^2, from Destexhe et al. 1998, Table 1

        params = {
            'name':name, 'N':number,\
            'Gl': 1.0*1.e6 * membrane_size, # in nS/cm^2, from Destexhe et al. 1998, Table 1
            'GNa': 50*1.e6 * membrane_size, # in nS/cm^2, from Destexhe et al. 1998, Table 1
            'GK': 5*1.e6 * membrane_size, # in nS/cm^2, from Destexhe et al. 1998, Table 1
            'GM': 0.07*1.e6 * membrane_size, # in nS/cm^2, from Destexhe et al. 1998, Table 1
            'Cm': 118.,
            'El': -70., # in mV, from Destexhe et al. 1998, Table 1
            'EK': -90.,
            'ENa': 50.,
            'VT': -56.2,
            'tau_max': 608.,
            'hhtype': 1
        }
    elif NAME=='HH_FS_DCS':
        membrane_size = 14000 * 1.e-8 # in cm^2, from Destexhe et al. 1998, Table 1
        params = {
            'name':name, 'N':number,\
            'Gl': 0.15*1.e6 * membrane_size, # in nS/cm^2, from Destexhe et al. 1998, Table 1
            'GNa': 50*1.e6 * membrane_size, # in nS/cm^2, from Destexhe et al. 1998, Table 1
            'GK': 10*1.e6 * membrane_size, # in nS/cm^2, from Destexhe et al. 1998, Table 1
            'GM': 0., 
            'Cm': 102.,
            'El': -70.,
            'EK': -90.,
            'ENa': 50.,
            'VT': -57.9,
            'tau_max': 502.,
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
