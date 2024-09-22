#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 00:22:07 2024

@author: nakshatrapatel
"""
from implied_vol_project import deribit_options, Option



my_instruments = deribit_options()

data, data_call, data_put = my_instruments.data(num_options=50)

maturities_strikes_call, maturities_strikes_put = my_instruments.plotting_axes(data_call,
                                                                                data_put)

for maturity in maturities_strikes_call.keys():
    for strike in maturities_strikes_call[f'{maturity}']:
        instr_name = f'BTC-{maturity}-{strike}-C'
        print(type(maturity))
        print(data.loc[instr_name, 'mark_price'])
        

# TICKER = 'BTC-6SEP24-61000-C'

# option = Option(TICKER)

# print(option.instr_name)
# print(option.maturity)
# print(option.strike)

# pulling_data = pull_data()

# info = pulling_data.get_order_book_1(TICKER)

# print(info)




    