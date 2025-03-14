import MetaTrader5 as mt5
import pandas as pd
import pickle
import os
#IMPORT INDICATOR MODULE HERE
from tqdm import tqdm

def read_pickle(path):
    if not os.path.exists(path):
        symbols = mt5.symbols_get()
        tickers = [symbol.name for symbol in symbols if 'FOREX' in symbol.path.upper()]
        with open(path, 'wb') as file:
            pickle.dump(tickers, file)
    else:
        with open(path, 'rb') as file:
            tickers = pickle.load(file)
    return tickers

def get_rates(symbol, n=1000, timeframe = mt5.TIMEFRAME_M1):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    df = pd.DataFrame(rates)
    return df

def add_signals(df):
    df['example indicator'] = #indicators.examples(df)
    return df

def save_raw_data():
    tickers = read_pickle('tickers.pickle')

    path = 'data_raw/'
    if not os.path.exists(path):
        os.makedirs(path)


    for ticker in tickers:
        df = get_rates(ticker)
        df.to_csv(f'{path}{ticker}.csv')

def save_mod_data():
    tickers = read_pickle('tickers.pickle')

    path = 'data_mod/'
    if not os.path.exists(path):
        os.makedirs(path)

    for ticker in tqdm(tickers):
        df = get_rates(ticker)
        df = add_signals(df)
        df.to_csv(f'{path}{ticker}.csv')

def offline_save_mod(new_path):
    tickers = read_pickle('tickers.pickle')

    if not os.path.exists(new_path):
        os.makedirs(new_path)


    path = 'data_raw/'
    for ticker in tqdm(tickers):
        df = pd.read_csv(f'{path}{ticker}.csv')
        df = add_signals(df)
        df.to_csv(f'{new_path}{ticker}.csv')
    

mt5.initialize(path="C:/Program Files/MetaTrader 5/terminal64.exe", timeout=180000)
save_raw_data()
offline_save_mod('inplace_data/')
