#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

import numpy as np

def getinputdict():
    inputdict = {}

    inputdict['paramssdict'] = {'GAMMA': 1, 'RHO': 0.05, 'ETA': 2, 'MU': 100, 'SIGMA': 6, 'PHI_pi': 1.5, 'RHO_A': 0.9, 'Abar': 1, 'Pistar': 1}

    # adding A just to get code to run (since I need at least one state for my code to work)
    inputdict['states'] = ['A']
    inputdict['controls'] = ['X', 'Pi', 'I']
    inputdict['irfshocks'] = []

    # equations:{{{
    inputdict['equations'] = [
    'X_dot = 1 / GAMMA * (I - Pi)'
    ,
    'Pi_dot = RHO * Pi - SIGMA * MC_ss / MU * (GAMMA + ETA) * X'
    ,
    'I = PHI_pi * Pi'
    ,
    'A_dot = (RHO_A - 1) * A'
    ]
    # equations:}}}

    # same steady state as the model with labor
    # steady state:{{{
    p = inputdict['paramssdict']

    p['A'] = p['Abar']
    p['Pi'] = p['Pistar']
    p['I'] = np.exp(p['RHO'] + np.log(p['Pi']))
    p['MC'] = (p['SIGMA'] - 1) / p['SIGMA'] + p['RHO'] * p['MU'] / p['SIGMA'] * np.log(p['Pi'])
    p['W'] = p['MC'] * p['A']
    p['L'] = p['W'] ** (1 / (p['GAMMA'] + p['ETA']))
    p['C'] = p['L']
    p['Y'] = p['C']

    # adding X just to get code to run
    p['X'] = 1
    p['MC_ss'] = p['MC']
    # steady state:}}}

    inputdict['loglineareqs'] = True

    return(inputdict)



def dsgefull():
    inputdict = getinputdict()

    sys.path.append(str(__projectdir__ / Path('submodules/dsge-perturbation/')))
    from dsge_continuous_func import continuouslineardsgefull
    continuouslineardsgefull(inputdict)


# Run:{{{1
dsgefull()
