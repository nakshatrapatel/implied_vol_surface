#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 00:22:07 2024

@author: nakshatrapatel
"""

# from main import instruments
# import pandas as pd
# import multiprocessing as mp

from implied_vol_project import instruments
import pandas as pd


my_instruments = instruments()

data, data_call, data_put = my_instruments.data()

print(data)

maturities_strikes_call, maturities_strikes_put = my_instruments.plotting_axis(data_call,
                                                                               data_put)





    