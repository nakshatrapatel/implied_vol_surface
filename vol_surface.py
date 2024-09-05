#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 21:33:36 2024

@author: nakshatrapatel
"""

import pandas as pd
import numpy as np

path = '/Users/nakshatrapatel/project/vol_surface/BTC-30AUG24-export.csv'
data = pd.read_csv(path)
data = data.set_index('Instrument')

## preprocessing data -- getting everything sorted in the dataframe

'''
cols_na = [col for col in data.columns if data[col].isnull().any()]

for col in cols_na:
    data[col] = data[col].replace('-', np.NAN)
'''

# data = data.drop(['ExtValue', 'NDelta'], axis='columns')

# data['IV Bid'] = data['IV Bid'].replace('-', np.NAN)

# data = data.dropna(axis='index')



## SPLITTING DATA INTO 2 DATAFRAMES: CALLS AND PUTS

def split(lst_of_indices):
    '''
    Parameters
    ----------
    lst_of_indices : list
       list of the pandas dataframe indices

    Returns
    -------
    lst_call : list
        list of all the call options
    lst_put : TYPE
        list of all the put options
    '''
    lst_call = []
    lst_put = []
    for index in lst_of_indices:
        if index[-1] == 'C':
            lst_call.append(index)
        elif index[-1] == 'P':
            lst_put.append(index) 
    return lst_call, lst_put

lst_call, lst_put = split(data.index)
call_options = data.loc[lst_call]
put_options = data.loc[lst_put]


## FIGURING OUT WHICH OPTIONS TO TAKE FROM EACH DATAFRAME

underlying_value = 58000                # spot -- pull current price of BTC

# For every strike less than spot use puts and every strike greater 
# than spot use call 

def get_strikes_maturity(lst_of_indices):
    '''
    
    Parameters
    ----------
    lst_of_indices : list
        list of indices from the call/put options dataframe

    Returns
    -------
    lst_of_strikes : list
        list of strike dates
    maturity : str -- date
        the maturity -- DDMMMYY

    '''
    lst_of_strikes = []
    for index in lst_of_indices:
        temp_lst = index.split('-')
        lst_of_strikes.append(temp_lst[2])
    maturity = lst_of_indices[0].split('-')[1]
    
    return lst_of_strikes, maturity

strikes, maturity = get_strikes_maturity(call_options.index)

strikes_call = []
strikes_put = []

for strike in strikes:
    if int(strike) <= int(underlying_value):
        strikes_put.append(strike)
    else:
        strikes_call.append(strike)
        

## GETTING THE RELEVANT IMPLIED VOLATILITIES


print(str(data.loc[['BTC-30AUG24-44000-P'], ['IV Bid']]))

IV_call = []

# for istrike, strike in enumerate(strikes_call):
#     print(data.loc[[f'BTC-{maturity}-{strike}-P'], ['IV Bid']])
#     IV_call.append()


















































