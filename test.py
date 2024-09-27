#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 00:22:07 2024

@author: nakshatrapatel
"""
from implied_vol_project import deribit_options
from datetime import datetime
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from matplotlib import cm
import plotly.graph_objs as go
import plotly.io as pio

my_instruments = deribit_options()


TICKER = 'BTC-28MAR25-60000-P'
info = my_instruments.get_order_book_1(TICKER)


data, data_call, data_put = my_instruments.data(num_option=200)

# data = data[200:500]
# data_call = data_call[200:500]
# data_put = data_put[200:500]

maturities_strikes_call, maturities_strikes_put, array_call, array_put = my_instruments.plotting_axes(data_call,
                                                                                data_put)


def black_scholes_vega(s:float, t:float, k:float, r:float, sigma:float):
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
    
    
    
def black_scholes_e(s:float, t:float, k:float, r:float, sigma:float, opt:str):
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
    opt : string
        'C' for call 
        'P' for put

    Returns
    -------
    current_value : float
        value of option

    '''
    
    if opt == 'C':
        if t == 0:
            current_value = max(0, s - k)

        d1 = (np.log(s / k) + (r + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
        d2 = d1 - (sigma * np.sqrt(t))
        current_value = (s * norm.cdf(d1)) - ((k * np.exp(-r * t)) * norm.cdf(d2))
        
    elif opt == 'P':
        if t == 0:
            current_value = max(0, k-s)
        
        d1 = (np.log(s / k) + (r + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
        d2 = d1 - (sigma * np.sqrt(t))
        
        current_value = ((k * np.exp(-r * t)) * norm.cdf(-d2)) - (s * norm.cdf(-d1))
        
    return current_value


def implied_vol_Newton(P:float, s:float, t:float, k:float, r:float, opt:str, iterations:int):
    
    for i in range(iterations):
        sigma = 1
        
        price_diff = black_scholes_e(s, t, k, r, sigma, opt) - P
        # print((price_diff, black_scholes_vega(s, t, k, r, sigma)))
        
        if abs(price_diff) < 0.01:
            break
        
        sigma = sigma - (price_diff / black_scholes_vega(s, t, k, r, sigma))
    
    return sigma

'''
instr_name = TICKER
maturity = '28MAR25'
strike = 60000

datetime_obj = datetime.strptime(maturity, '%d%b%y')
date_delta = datetime_obj - datetime.today()

underlying_s = info['index_price']
P = info['mark_price'] * info['index_price']

time_to_maturity_t = date_delta.days / 365

strike_k = strike
interest_r = info['interest_rate']

# sigma = implied_vol_Newton(P, underlying_s, time_to_maturity_t, strike_k, interest_r, 100)
iv = (info['mark_iv'] / 100) 

calc_price = black_scholes_e(underlying_s, time_to_maturity_t, strike_k, interest_r, iv, 'P')

vega_calc = black_scholes_vega(underlying_s, time_to_maturity_t, strike_k, interest_r, iv)

vega = info['greeks']['vega'] * 100

implied_vol = implied_vol_Newton(P,underlying_s, time_to_maturity_t, strike_k, interest_r, 'P', 500)
print((underlying_s,
       P,
       calc_price,
       time_to_maturity_t,
       strike_k,
       interest_r,
       iv,
       implied_vol,
       vega_calc,
       vega))

'''
plotting_data = []

for maturity in maturities_strikes_call.keys():
    for strike in maturities_strikes_call[f'{maturity}']:
        
        instr_name = f'BTC-{maturity}-{strike}-C'
        
        datetime_obj = datetime.strptime(maturity, '%d%b%y')
        date_delta = datetime_obj - datetime.today()
        
        underlying_s = data.loc[instr_name, 'index_price']
        P = data.loc[instr_name, 'mark_price'] * data.loc[instr_name, 'index_price']
        time_to_maturity_t = date_delta.total_seconds() / (365 * 24 * 3600)
        strike_k = strike
        interest_r = data.loc[instr_name, 'interest_rate']
        iv = data.loc[instr_name, 'mark_iv'] / 100
        calc_price = black_scholes_e(underlying_s, time_to_maturity_t, strike_k, interest_r, iv, 'C')
        sigma = implied_vol_Newton(P, underlying_s, time_to_maturity_t, strike_k, interest_r, 'C', 500)
        delta = data.loc[instr_name, 'greeks']['delta']
        
        # print((underlying_s,
        #        P,
        #        calc_price,
        #        time_to_maturity_t,
        #        strike_k,
        #        interest_r,
        #        iv,
        #        sigma
        #        ))
        
        plotting_data.append([time_to_maturity_t, strike_k, sigma, delta])
        
for maturity in maturities_strikes_put.keys():
    for strike in maturities_strikes_put[f'{maturity}']:
        
        instr_name = f'BTC-{maturity}-{strike}-P'
        
        datetime_obj = datetime.strptime(maturity, '%d%b%y')
        date_delta = datetime_obj - datetime.today()
        
        underlying_s = data.loc[instr_name, 'index_price']
        P = data.loc[instr_name, 'mark_price'] * data.loc[instr_name, 'index_price']
        time_to_maturity_t = date_delta.total_seconds() / (365 * 24 * 3600)
        strike_k = strike
        interest_r = data.loc[instr_name, 'interest_rate']
        iv = data.loc[instr_name, 'mark_iv'] / 100
        calc_price = black_scholes_e(underlying_s, time_to_maturity_t, strike_k, interest_r, iv, 'P')
        sigma = implied_vol_Newton(P, underlying_s, time_to_maturity_t, strike_k, interest_r, 'P', 500)
        delta = data.loc[instr_name, 'greeks']['delta']
        
        # print((underlying_s,
        #        P,
        #        calc_price,
        #        time_to_maturity_t,
        #        strike_k,
        #        interest_r,
        #        iv,
        #        sigma
        #        ))
        
        plotting_data.append([time_to_maturity_t, strike_k, sigma, delta])
x_axis = []
y_axis = []
z_axis = []

for i, coord in enumerate(plotting_data):
    if 0.05 <= abs(coord[3]) <= 0.95 and 0 < coord[2] < 1 and 60000 < coord[1] < 70000: 
        print(coord)
        y_axis.append(coord[1])
        x_axis.append(coord[0] * 365)
        z_axis.append(coord[2])


print(x_axis)
print(y_axis)

xi = np.linspace(min(x_axis), max(x_axis), 100)
yi = np.linspace(min(y_axis), max(y_axis), 100)

xi, yi = np.meshgrid(xi, yi)

zi = griddata((x_axis, y_axis), z_axis, (xi, yi), method='cubic')

z_min, z_max = 0 , 1

zi_clipped = np.clip(zi, z_min, z_max)

# fig = plt.figure(figsize=(10, 10))


# ax = fig.add_subplot(111, projection='3d')


# ax.plot_surface(xi, yi, zi, cmap=cm.coolwarm)

# ax.set_ylabel('Strike (USD)')
# ax.set_xlabel('Time to Maturity (Days)')
# ax.set_zlabel('Implied Volatility')

# plt.title('Volatility Surface')

# plt.show()

surface = go.Surface(z=zi_clipped, x=xi, y=yi)
layout = go.Layout(
    title='Implied Volatility',
    scene=dict(
        xaxis_title='Time to Maturity (Days)',
        yaxis_title='Strike (USD)',
        zaxis_title='Implied Volatility'
    )
)

fig = go.Figure(data=[surface], layout=layout)

pio.renderers.default = 'browser'

pio.show(fig)















    