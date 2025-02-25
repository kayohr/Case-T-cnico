INSERT INTO `lustrous-spirit-451917-p2.teste_tecnico.cryptocurrency` (id, name, symbol, rank)
SELECT DISTINCT id, name, symbol, rank
FROM `lustrous-spirit-451917-p2.teste_tecnico.crypto_info`;


INSERT INTO `lustrous-spirit-451917-p2.teste_tecnico.market_data` (id, priceUsd, marketCapUsd, volumeUsd24Hr, supply, maxSupply, timestamp)
SELECT DISTINCT id, priceUsd, marketCapUsd, volumeUsd24Hr, supply, maxSupply, CURRENT_TIMESTAMP()
FROM `lustrous-spirit-451917-p2.teste_tecnico.crypto_info`;