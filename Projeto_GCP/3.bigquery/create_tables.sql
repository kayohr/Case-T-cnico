CREATE TABLE `lustrous-spirit-451917-p2.teste_tecnico.cryptocurrency` (
    id STRING,
    name STRING,
    symbol STRING,
    rank INT
);

CREATE TABLE `lustrous-spirit-451917-p2.teste_tecnico.market_data` (
    id STRING,
    priceUsd FLOAT64,
    marketCapUsd FLOAT64,
    volumeUsd24Hr FLOAT64,
    supply FLOAT64,
    maxSupply FLOAT64,
    timestamp TIMESTAMP
);