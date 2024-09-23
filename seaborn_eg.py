#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 08:40:19 2024

@author: nakshatrapatel
"""

import matplotlib.pyplot as plt
import numpy as np


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
        
    elif opt == 'p':
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

# Generate data for a 3D surface plot
x = np.linspace(0, 100000, 100)
y = np.linspace(0, 365, 100)
X, Y = np.meshgrid(x, y)
Z = implied_vol_Newton(6500, 63000, y, x, 0, 'C', 500)

print(type(X))
print(Y.shape)
print(Z.shape)

print(Y)
print(X)

# Create a 3D surface plot with Seaborn
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.title('3D Surface Plot with Seaborn')
plt.show()



def data(self, **kwargs):
    n = kwargs.get('n')
    my_instrument = self
    
    try: 
        lst_of_options = my_instrument.list_of_options()[0:n]   
    except:
        lst_of_options = my_instrument.list_of_options()