# pump-up-the-jam
Online detection of pump-and-dump schemes in cryptocurrency exchanges.

## Used Datasets
The directory `datasets` contains labeled pump-and-dump data from other works which are listed below:
- `lamorgia`: Contains the raw data from Binance pump-and-dump events obtained using the Download script of the repository: https://github.com/SystemsLab-Sapienza/pump-and-dump-dataset

- `lamorgia2020`: Contains a CSV file which points to a subset of the file in the `lamorgia` directory. This subset represents the intersection of the events the download script was able to download the data and the events which were used in their published work [Pump and Dumps in the Bitcoin Era: Real Time Detection of Cryptocurrency Market Manipulations](https://ieeexplore.ieee.org/document/9209660). It was created because their repository only has the transformed data versioned and the Binance may delist some coins.
