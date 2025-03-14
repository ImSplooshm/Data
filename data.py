import MetaTrader5 as mt5
import pandas as pd
import pickle
import os
from indicators import *
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
    df['ema_3'] = EMA.ema(df['close'], 3)
    df['ema_9'] = EMA.ema(df['close'], 9)
    df['ema_12'] = EMA.ema(df['close'], 12)
    df['ema_26'] = EMA.ema(df['close'], 26)
    df['ema_50'] = EMA.ema(df['close'], 50)
    df['size'] = EMA.cand_size(df['close'], df['open'])
    df['roll_size'] = EMA.roll_size(df['size'])
    
    
    df['rsi'] = VOL.rsi(df['close'])
    df['atr'] = VOL.atr(df['high'],df['close'],df['low'])

    df['stoch_k'] = VOL.stoch_k(df['low'],df['high'],df['close'])
    df['stoch_d'] = VOL.stoch_d(df['stoch_k'])

    df['adx'] = VOL.adx(df['high'], df['low'], df['close'], n = 14)

    df['bb_std'] = BBANDS.std(df['close'])
    df['middle'] = BBANDS.middle(df['close'])
    df['upper'] = BBANDS.upper(df['bb_std'], df['middle'])
    df['lower'] = BBANDS.lower(df['bb_std'], df['middle'])
    df['width'] = BBANDS.width(df['upper'], df['lower'])


    df['macd'] = MACD.macd(df['close'])
    df['macd_signal'] = MACD.macd_signal(df['macd'])
    df['macd_h'] = MACD.macd_histo(df['macd'], df['macd_signal'])
    df['macd_std'] = MACD.std(df['macd'])

    df['movement'] = ST.supertrend(df)
    
    df['donch_max'] = DONCH.high(df['high'])
    df['donch_min'] = DONCH.low(df['low'])
    df['donch_mid'] = DONCH.middle(df['high'], df['low'])

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
    

# mt5.initialize(path="C:/Program Files/MetaTrader 5/terminal64.exe", timeout=180000)
# save_raw_data()
# offline_save_mod('inplace_data/')