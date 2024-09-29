#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 00:22:07 2024

@author: nakshatrapatel
"""
from deribit_batch_api import deribit_options
from datetime import datetime
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import plotly.graph_objs as go
import plotly.io as pio
from scipy.optimize import curve_fit

my_instruments = deribit_options()


TICKER = 'BTC-29NOV24-60000-C'
info = my_instruments.get_order_book_1(TICKER)


data, data_call, data_put = my_instruments.data()

max_iv = data['mark_iv'].max() / 100
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

def implied_vol_Newton(P:float, s:float, t:float, k:float, r:float, opt:str, iterations:int, max_iv=max_iv):
    '''
    

    Parameters
    ----------
    P : float
        premium
    s : float
        underlying price
    t : float
        time to maturity
    k : float
        strike
    r : float
        interest rate
    opt : str
        call or put
    iterations : int
        number of iterations for Newton Raphson

    Returns
    -------
    sigma : float
        implied volatility

    '''
    
    for i in range(iterations):
        sigma = max_iv
        
        price_diff = black_scholes_e(s, t, k, r, sigma, opt) - P
        
        if abs(price_diff) < 0.01:
            break
        
        sigma = sigma - (price_diff / black_scholes_vega(s, t, k, r, sigma))
    
    return sigma

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
        sigma = implied_vol_Newton(P, underlying_s, time_to_maturity_t, strike_k, interest_r, 'C', 5000)
        delta = data.loc[instr_name, 'greeks']['delta']
        plotting_data.append([time_to_maturity_t, strike_k / underlying_s, sigma, delta])
        
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
        sigma = implied_vol_Newton(P, underlying_s, time_to_maturity_t, strike_k, interest_r, 'P', 5000)
        delta = data.loc[instr_name, 'greeks']['delta']
        plotting_data.append([time_to_maturity_t, strike_k / underlying_s, sigma, delta])
        
x_axis = []
y_axis = []
z_axis = []

for i, coord in enumerate(plotting_data):
    if abs(coord[3]) >= 0 and 0 < coord[2] < 1:
        print(coord)
        y_axis.append(coord[1])
        x_axis.append(coord[0] * 365)
        z_axis.append(coord[2])


print(z_axis)
print('.................................................................')

xi = np.linspace(min(x_axis), max(x_axis), 100)
yi = np.linspace(min(y_axis), max(y_axis), 100)

xi, yi = np.meshgrid(xi, yi)

def paraboloid(X, a, b, c, d, e, f):
    x, y = X
    return (a * x**2) + (b * y**2) + (c * x * y) + (d * x) + (e * y) + f

xy_data = np.vstack((x_axis, y_axis))
initial_guess = [1, 1, 1, 1, 1, 1]
params, covariance = curve_fit(paraboloid, xy_data, z_axis, p0=initial_guess)
std_dev = np.sqrt(np.diag(covariance))

a,b,c,d,e,f = params


zi = paraboloid((xi, yi), a, b, c, d, e, f)

print(zi)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xi, yi, zi, cmap=cm.coolwarm)
ax.scatter(x_axis, y_axis, z_axis)

ax.set_ylabel('K/S')
ax.set_xlabel('Time to Maturity (Days)')
ax.set_zlabel('Implied Volatility')
plt.title(f'Volatility Surface, paraboloid with standard deviation: {std_dev}')
plt.show()

surface = go.Surface(z=zi, x=xi, y=yi)
layout = go.Layout(
    title='Implied Volatility best fit with covariance',
    scene=dict(
        xaxis_title='Time to Maturity (Days)',
        yaxis_title='Strike (USD)',
        zaxis_title='Implied Volatility'
    )
)
fig = go.Figure(data=[surface], layout=layout)
pio.renderers.default = 'browser'
pio.show(fig)
