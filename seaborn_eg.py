#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 08:40:19 2024

@author: nakshatrapatel
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Generate data for a 3D surface plot
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create a 3D surface plot with Seaborn
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.title('3D Surface Plot with Seaborn')
plt.show()






'''
for option in lst_of_options:
    result = my_instrument.get_order_book_1(option)
    df.loc[option] = [result.underlying_price,
                      result.best_bid_price, 
                      result.mark_price,
                      result.best_ask_price,
                      result.bid_iv,
                      result.mark_iv,
                      result.ask_iv,
                      result.greeks]
'''
    