#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 00:22:07 2024

@author: nakshatrapatel
"""
from implied_vol_project import deribit_options, Option
from datetime import datetime
import numpy as np
from scipy.stats import norm

my_instruments = deribit_options()


TICKER = 'BTC-28MAR25-80000-C'
info = my_instruments.get_order_book_1(TICKER)


# data, data_call, data_put = my_instruments.data(num_options=50)

# maturities_strikes_call, maturities_strikes_put, array_call, array_put = my_instruments.plotting_axes(data_call,
#                                                                                 data_put)


def vega(s:float, t:float, k:float, r:float, sigma:float):
    '''
    

    Parameters
    ----------
    s : float
        Current price of underlying
    t : float
        time to maturity
    k : float
        strike
    r : float
        interest rate
    sigma : float
        volatility

    Returns
    -------
    float
        vega (dv/dsigma)

    '''
    add = (np.log(s / k) + (r + (sigma**2 / 2)) * t) / (sigma * np.sqrt(t))
    return norm.pdf(add) * s * np.sqrt(t)
    
    
    
def black_scholes_e_call(s:float, t:float, k:float, r:float, sigma:float):
    '''
    

    Parameters
    ----------
    s : float
        Current price of underlying
    t : float
        time to maturity
    k : float
        strike
    r : float
        interest rate
    sigma : float
        volatility

    Returns
    -------
    current_value : float
        value of option

    '''
    

    add = (np.log(s / k) + (r + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
    
    sub = add - (sigma * np.sqrt(t))
    current_value = (s * norm.cdf(add)) - ((k * np.exp(-r * t)) * norm.cdf(sub))
    return current_value


def implied_vol_Newton(P:float, s:float, t:float, k:float, r:float, iterations:int):
    
    for i in range(iterations):
        sigma = 200
        
        price_diff = black_scholes_e_call(s, t, k, r, sigma) - P
        
        if abs(price_diff) < 0.001:
            break
        
        sigma = sigma - (price_diff / vega(s, t, k, r, sigma))
    
    return sigma


instr_name = TICKER
maturity = '28MAR25'
strike = 80000

datetime_obj = datetime.strptime(maturity, '%d%b%y')
date_delta = datetime_obj - datetime.today()

underlying_s = info['underlying_price']
P = info['mark_price'] * info['mark_price']

time_to_maturity_t = date_delta.days / 365

strike_k = strike
interest_r = info['interest_rate']

# sigma = implied_vol_Newton(P, underlying_s, time_to_maturity_t, strike_k, interest_r, 100)
iv = (info['mark_iv'] / 100)

calc_price = black_scholes_e_call(underlying_s, time_to_maturity_t, strike_k, interest_r, iv)

vega_calc = vega(underlying_s, time_to_maturity_t, strike_k, interest_r, iv)

vega = info['greeks']['vega']

print((underlying_s,
       P,
       calc_price,
       time_to_maturity_t,
       strike_k,
       interest_r,
       iv, 
       vega_calc,
       vega))
    

plotting_data = []
'''
for maturity in maturities_strikes_call.keys():
    for strike in maturities_strikes_call[f'{maturity}']:
        
        instr_name = f'BTC-{maturity}-{strike}-C'
        
        datetime_obj = datetime.strptime(maturity, '%d%b%y')
        date_delta = datetime_obj - datetime.today()
        
        underlying_s = data.loc[instr_name, 'underlying_price']
        P = data.loc[instr_name, 'mark_price'] * data.loc[instr_name, 'index_price']
        # time_to_maturity_t = date_delta.days
        time_to_maturity_t = 100
        strike_k = strike
        # interest_r = data.loc[instr_name, 'interest_rate']
        interest_r = 0.05
        sigma = implied_vol_Newton(P, underlying_s, time_to_maturity_t, strike_k, interest_r, 100)
        iv = data.loc[instr_name, 'mark_iv']
        calc_price = black_scholes_e_call(underlying_s, time_to_maturity_t, strike_k, interest_r, iv/100)
        
        print((underlying_s,
               P,
               calc_price,
               time_to_maturity_t,
               strike_k,
               interest_r,
               sigma,
               iv))

        print('..........................')'''



    
    




# option = Option(TICKER)

# print(option.instr_name)
# print(option.maturity)
# print(option.strike)

# pulling_data = pull_data()

# info = pulling_data.get_order_book_1(TICKER)

# print(info)




    