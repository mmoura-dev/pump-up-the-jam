# pump-up-the-jam
Online detection of pump-and-dump schemes in cryptocurrency exchanges.

## Used Datasets
The directory `datasets` contains labeled pump-and-dump data from other works which are listed below:
- `lamorgia`: Contains the raw data from Binance pump-and-dump events obtained using the Download script of the repository: https://github.com/SystemsLab-Sapienza/pump-and-dump-dataset

- `lamorgia2020`: Contains a CSV file which points to a subset of the file in the `lamorgia` directory. This subset represents the intersection of the events the download script was able to download the data and the events which were used in their published work [Pump and Dumps in the Bitcoin Era: Real Time Detection of Cryptocurrency Market Manipulations](https://ieeexplore.ieee.org/document/9209660). It was created because their repository only has the transformed data versioned and the Binance may delist some coins.

- `bello2023`: Dataset of Binance pump-and-dump events from the work [LLD: A Low Latency Detection Solution to Thwart Cryptocurrency Pump & Dumps](https://ieeexplore.ieee.org/document/10174922) but the spot data was retrived using the script `binance_collector/historic_collector`, since the work only made available the ohlc data. 

> The [Binance API has changed in 2025-03-03 08:00](https://www.binance.com/en/support/announcement/detail/f04e986e02464015b3e85d5ef76cbb2a) (UTC) to not include historical market data before 2025-03-01 00:00 (UTC) but some data may still be retried in: https://data.binance.vision/?prefix=data/futures/um/daily/trades/

### Glossary
- `isBuyerMaker`: Field in the Response JSON that indicates if the Buy side (the Buyer) was also the market maker (the Maker).
- `isBestMatch`: Field in the Response JSON that determines if the price of the trade was the best available on the exchange.
Source: https://developers.binance.com/docs/binance-spot-api-docs/faqs/spot_glossary
