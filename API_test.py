#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 00:22:07 2024

@author: nakshatrapatel
"""
from implied_vol_project import pull_data, Option



# my_instruments = instruments()

# data, data_call, data_put = my_instruments.data(n=50)

# print(data)

# maturities_strikes_call, maturities_strikes_put = my_instruments.plotting_axis(data_call,
#                                                                                data_put)

TICKER = 'BTC-6SEP24-61000-C'

option = Option(TICKER)

print(option.instr_name)
print(option.maturity)
print(option.strike)

pulling_data = pull_data()

info = pulling_data.get_order_book_1(TICKER)

print(info)




    