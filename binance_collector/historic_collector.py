import glob
import os
import pprint
import tempfile
from typing import List
import zipfile
import numpy as np
import pandas as pd
from binance_public_data import *


EXPECTED_DATASET_COLUMNS = ['symbol', 'date', 'hour', 'exchange']
BINANCE_VISION_DAILY_SPOT_COLUMNS = [
    'tradeId', 'price', 'qty', 'quoteQty', 'time', 'isBuyerMaker', 'isBestMatch']


def get_historic_binance_dataset(dataset_name: str, days_before: int = 12, days_later: int = 7) -> None:
    dataset = pd.read_csv(f'datasets/{dataset_name}/{dataset_name}.csv')
    validate_dataset(dataset)
    assert days_before > 0 and days_before <= 365
    assert days_later > 0 and days_later <= 365

    # Columns filters
    dataset.columns = [col.lower() for col in dataset.columns]
    dataset = dataset[EXPECTED_DATASET_COLUMNS]

    # Rows filters
    dataset['exchange'] = dataset['exchange'].str.lower()
    dataset = dataset[dataset['exchange'] == 'binance']
    dataset.drop(columns=['exchange'], inplace=True)

    error_tuples = []
    for _, symbol, pump_date_str, pump_hour_str in dataset.itertuples():
        pump_date = datetime.strptime(pump_date_str, '%Y-%m-%d')
        start_date = (pump_date - timedelta(days=days_before)
                      ).strftime("%Y-%m-%d")
        end_date = (pump_date + timedelta(days=days_later)
                    ).strftime("%Y-%m-%d")

        with tempfile.TemporaryDirectory() as tmp_path:
            try:
                zip_files_path = download_daily_trades('spot', [symbol + 'BTC'], 1, get_arg_dates(),
                                                    start_date, end_date, tmp_path, 0)
                csv_files = extract_zip_files(tmp_path, zip_files_path)
                merged_df = merge_csv_files(csv_files)
                merged_df = transform_df(symbol, merged_df)
                write_output_csv(dataset_name, symbol,
                                pump_date_str, pump_hour_str, merged_df)
            except Exception:
                error_tuples.append((symbol, pump_date_str, pump_hour_str))
                continue
        
    pprint.pprint(error_tuples)


def write_output_csv(dataset_name, symbol, pump_date_str, pump_hour_str, combined_df):
    output_path = os.path.join('datasets', dataset_name, 'trading_records')
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(
        output_path, f'{symbol}_{pump_date_str}_{pump_hour_str.replace(":", "h")}.csv')
    combined_df.to_csv(output_file, index=False)


def transform_df(symbol: str, merged_df: pd.DataFrame) -> pd.DataFrame:
    column_names_map = {'tradeId': 'trade_id',
                        'price': 'price',
                        'qty': 'amount',
                        'quoteQty': 'btc_volume',
                        'time': 'timestamp',
                        'isBuyerMaker': 'is_buyer_maker',
                        'isBestMatch': 'is_best_match'}
    result_df = merged_df.rename(columns=column_names_map)
    result_df['symbol'] = symbol + '/BTC'
    result_df['datetime'] = pd.to_datetime(result_df['timestamp'], unit='ms').map(
        lambda x: datetime.strftime(x, '%Y-%m-%dT%H:%M:%S.%fZ'))
    result_df['side'] = np.where(result_df['is_buyer_maker'], 'sell', 'buy')
    result_df['is_buyer_maker'] = result_df['is_buyer_maker'].astype(str).str.lower()
    result_df['is_best_match'] = result_df['is_best_match'].astype(str).str.lower()

    return result_df[['symbol', 'timestamp', 'datetime', 'side', 'price', 'amount', 'btc_volume', 'trade_id', 'is_buyer_maker', 'is_best_match']]


def merge_csv_files(csv_files: List[str]) -> pd.DataFrame:
    df_list = [pd.read_csv(file, header=None, names=BINANCE_VISION_DAILY_SPOT_COLUMNS)
               for file in sorted(csv_files)]
    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df = combined_df.sort_values(by='time')
    return combined_df


def extract_zip_files(tmp_path: str, zip_files_path: str) -> str:
    extract_dir = os.path.join(tmp_path, 'extract_dir')
    os.makedirs(extract_dir)

    for zip_file_name in os.listdir(zip_files_path):
        with zipfile.ZipFile(zip_files_path + zip_file_name, 'r') as zip_file:
            zip_file.extractall(extract_dir)
    return glob.glob(os.path.join(extract_dir, '*.csv'))


def get_arg_dates():
    period = convert_to_date_object(datetime.today().strftime('%Y-%m-%d')) - convert_to_date_object(
        PERIOD_START_DATE)
    dates = pd.date_range(end=datetime.today(),
                          periods=period.days + 1).to_pydatetime().tolist()
    dates = [date.strftime("%Y-%m-%d") for date in dates]
    return dates


def validate_dataset(dataset: pd.DataFrame) -> None:
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError('Input dataset was not correctly parsed')

    columns_set = {col.lower() for col in dataset.columns}
    missing_columns = set(EXPECTED_DATASET_COLUMNS) - set(columns_set)
    if len(missing_columns) > 0:
        raise ValueError(f'Missing required columns: {missing_columns}')


get_historic_binance_dataset('bello2023')
