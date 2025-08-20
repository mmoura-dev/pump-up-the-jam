# pump-up-the-jam
Online detection of pump-and-dump schemes in cryptocurrency exchanges.

## Used Datasets
The directory `datasets` contains labeled pump-and-dump data from other works which are listed below:
- `lamorgia`: Contains the raw data from Binance pump-and-dump events obtained using the Download script of the repository: https://github.com/SystemsLab-Sapienza/pump-and-dump-dataset

- `lamorgia2020`: Contains a CSV file which points to a subset of the file in the `lamorgia` directory. This subset represents the intersection of the events the download script was able to download the data and the events which were used in their published work [Pump and Dumps in the Bitcoin Era: Real Time Detection of Cryptocurrency Market Manipulations](https://ieeexplore.ieee.org/document/9209660). It was created because their repository only has the transformed data versioned and the Binance may delist some coins.

> The [Binance API has changed in 2025-03-03 08:00](https://www.binance.com/en/support/announcement/detail/f04e986e02464015b3e85d5ef76cbb2a) (UTC) to not include historical market data before 2025-03-01 00:00 (UTC) but some data may still be retried in: https://data.binance.vision/?prefix=data/futures/um/daily/trades/

> Meaning of columns: `is_buyer_maker` is True, that means the order was filled by seller market selling into a maker and if it's False, the order was filled by a buyer market buying into a maker; `is_best_match` means that the price of the buyer was matched with a seller [source](https://github.com/sammchardy/python-binance/issues/374).
