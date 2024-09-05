# -*- coding: utf-8 -*-

import asyncio
import websockets
import json
import nest_asyncio
import pandas as pd
# import multiprocessing as mp


class pull_data():
    
    def __init__(self):
        pass
        
    def get_order_book_1(self, inst_name):
        '''
        

        Parameters
        ----------
        inst_name : str
            TICKER NAME

        Returns
        -------
        result : pd.series
            ALL INFO REGARDING THE INSTRUMENT

        '''
        nest_asyncio.apply()
        msg = \
        {
          "jsonrpc" : "2.0",
          "id" : 8772,
          "method" : "public/get_order_book",
          "params" : {
            "instrument_name" : f"{inst_name}",
          }
        }
        async def call_api(msg):
            async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
                await websocket.send(msg)
                while websocket.open:
                    response = await websocket.recv()
                    json_par = json.loads(response)
                    #print(json_par)
                    return(json_par)
        response = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
        
        df = pd.DataFrame.from_dict(response)
        result = df.result
        return result
    
    def list_of_options(self):
        
    
        '''
        

        Returns
        -------
        lst_of_options : list
            LIST OF ALL BITCOIN OPTIONS TRADING ON THE MARKET

        '''
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
            
        return lst_of_options
    
    # remember data needs to be changed to pull all data
    
    def data(self, n: int):
        '''
        
        Parameters
        ----------
        n : int
            INPUT THE NUMBER OF OPTIONS TO CONSIDER IN THE DATASET (FIRST n FROM DERIBIT)

        Returns
        -------
        TYPE  dataframes
            DATA : DATAFRAME OF ALL OPTIONS DATA
            DATA_CALL : DATAFRAME OF JUST CALL OPTIONS
            DATA_PUT : DATAFRAME OF JUST PUT OPTIONS

        '''
        
        my_instrument = self
        '''
        def append_data(option):
            result = my_instrument.get_order_book_1(option)
            return [result.instrument_name,
                    result.underlying_price,
                    result.best_bid_price, 
                    result.mark_price,
                    result.best_ask_price,
                    result.bid_iv,
                    result.mark_iv,
                    result.ask_iv,
                    result.greeks]

        def main():
            lst_of_options = my_instrument.list_of_options()
            
            
            with mp.Pool(processes=6) as pool:
                results = pool.map(append_data, lst_of_options)
                
                df = pd.DataFrame(results)
                --
            return df

        if __name__ == "__main__":
            df = main()
            df = df.rename(columns = { '0': 'instr_name', 
                                       '1': 'underlying_price', 
                                       '2': 'best_bid_price',
                                       '3': 'mark_price',
                                       '4': 'best_ask_price',
                                       '5': 'bid_iv',
                                       '6': 'mark_iv',
                                       '7': 'ask_iv',
                                       '8': 'greeks'})

        '''

        lst_of_options = my_instrument.list_of_options()[0:n]   # need to change -- get rid off [0:5]

        df = pd.DataFrame({'instr_name': [], 
                           'underlying_price': [], 
                           'best_bid_price': [],
                           'mark_price': [],
                           'best_ask_price': [],
                           'bid_iv': [],
                           'mark_iv': [],
                           'ask_iv': [],
                           'greeks': []})

        df = df.set_index('instr_name')


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
            
        def split(df):
            '''
            Parameters
            ----------
            df : pandas dataframe
               PANDAS DATAFRAME WITH ALL THE DATA

            Returns
            -------
            df_call : pandas dataframe
                DATAFRAME OF CALL OPTIONS
            df_put : TYPE
                DATAFRAME OF PUT OPTIONS
            '''
            
            lst_of_indices = df.index
            lst_call = []
            lst_put = []
            df_call = pd.DataFrame(columns=df.columns, index=df.index)
            df_put = pd.DataFrame(columns=df.columns, index=df.index)
            for index in lst_of_indices:
                if index[-1] == 'C':
                    lst_call.append(index)
                    df_call.loc[index] = df.loc[index]
                elif index[-1] == 'P':
                    lst_put.append(index) 
                    df_put.loc[index] = df.loc[index]
                    
            df_call = df_call.dropna(axis='index')
            df_put = df_put.dropna(axis='index')
            return  df_call, df_put
        
        df_call, df_put = split(df)
            
        return df, df_call, df_put
        
    def plotting_axes(self, data_call, data_put):
        '''
        

        Parameters
        ----------
        data_call : Pandas Dataframe
            DATAFRAME OF ALL CALL OPTIONS 
        data_put : Pandas Dataframe
            DATAFRAME OF ALL PUT OPTIONS
            
        INPUTS NECESSARY TO ENSURE IT DOESN'T PULL DATA AT MULTIPLE TIMES
        WE INTEND TO LOAD DATA ONCE IN THE MAIN CODE ANYWAY

        Returns
        -------
        adjusted_maturies_strikes_call : Dict
            KEYS: MATURITIES
            VALUES: STRIKES -- FOR STRIKES >= SPOT
        adjusted_maturies_strikes_put : Dict
            KEYS: MATURITIES
            VALUES: STRIKES -- FOR STRIKES <= SPOT

        '''

        maturities_strikes_call = {}
        maturities_strikes_put = {}
        adjusted_maturies_strikes_call = {}
        adjusted_maturies_strikes_put = {}
        
        for index in data_call.index:
            temp_lst = index.split('-')
            maturities_strikes_call[f'{temp_lst[1]}'] = []
            adjusted_maturies_strikes_call[f'{temp_lst[1]}'] = []
            
        for index in data_put.index:
            temp_lst = index.split('-')
            maturities_strikes_put[f'{temp_lst[1]}'] = []
            adjusted_maturies_strikes_put[f'{temp_lst[1]}'] = []
            
        for index in data_call.index:
            temp_lst = index.split('-')
            maturities_strikes_call[f'{temp_lst[1]}'].append(int(temp_lst[2]))
            
        for index in data_put.index:
            temp_lst = index.split('-')
            maturities_strikes_put[f'{temp_lst[1]}'].append(int(temp_lst[2]))
            
        
        for maturity in maturities_strikes_call.keys():
            for strike in maturities_strikes_call[maturity]:
                if int(strike) >= int(data_call.loc[f'BTC-{maturity}-{strike}-C', 'underlying_price']):
                    adjusted_maturies_strikes_call[maturity].append(strike)
                    
        for maturity in maturities_strikes_put.keys():
            for strike in maturities_strikes_put[maturity]:
                if int(strike) <= int(data_call.loc[f'BTC-{maturity}-{strike}-C', 'underlying_price']):
                    adjusted_maturies_strikes_put[maturity].append(strike)
                    
        return adjusted_maturies_strikes_call, adjusted_maturies_strikes_put
    
    
    
class Option():
    
    def __init__(self, instr_name):
        self.instr_name = str(instr_name)
        temp_list = self.instr_name.split('-')
        self.maturity = str(temp_list[1])
        self.strike = int(temp_list[2])
    
    def black_scholes_solver():
        return print('working on it')
    
    def get_IV():
        pass
    
    
    
    
    
