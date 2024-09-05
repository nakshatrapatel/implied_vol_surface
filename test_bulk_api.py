#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 17:30:27 2024

@author: nakshatrapatel
"""

import asyncio
import websockets
import json
import nest_asyncio
import pandas as pd

nest_asyncio.apply()

msg = \
{
  "method" : "public/get_instruments",
  "params" : {
    "currency" : "BTC",
    "kind" : "option"
  },
  "jsonrpc" : "2.0",
  "id" : 1
}

async def call_api(msg):
   async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
       await websocket.send(msg)
       while websocket.open:
           response = await websocket.recv()
           json_par = json.loads(response)
           return(json_par)
           

response = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
df = pd.DataFrame.from_dict(response)
result = df.result

lst_of_options = []

for ival, val in enumerate(result):
    lst_of_options.append(result[ival]['instrument_name'])
    

print(lst_of_options)

