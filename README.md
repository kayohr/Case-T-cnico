# Projeto ETL no GCP(Google Cloud Platform) utilizando Cloud Run ETL com BigQuery e Schedule 

## 📌 Configuração do Ambiente

### Configuração pelo Console do GCP
Este projeto foi configurado diretamente pelo **Google Cloud Console**. Abaixo estão os passos realizados:

1. **Cloud Run**: Implementação do serviço `request-api` através do console.
   - Base image: Python 3.11 (Ubuntu 22)

2. **Cloud Scheduler**: Agendamento de execução do serviço.
   - Frequência: `0 * * * *` (hora em hora)
   - Método HTTP: `POST`
   - Status: Configurado via **Google Cloud Console**

3. **BigQuery**: Modelagem de dados e criação da view.
   - Tabelas `cryptocurrency` e `market_data` criadas via console.
   - `crypto_market_view` consolidando os dados.

---
## 📌 Instalação de Dependências

Caso queira rodar localmente, instale as dependências do projeto:
```sh
pip install -r requirements.txt
```

---
## 📌 Estrutura do BigQuery

### Como Visualizar os Dados no BigQuery Console
Para depuração e análise dos dados, siga os passos abaixo no console do **Google Cloud BigQuery**:

1. Acesse o console do **BigQuery** no Google Cloud: [BigQuery Console](https://console.cloud.google.com/bigquery)
2. No painel esquerdo, selecione o projeto `lustrous-spirit-451917-p2`.
3. Expanda o dataset `teste_tecnico` e visualize as tabelas `cryptocurrency`, `market_data` e a view `crypto_market_view`.
4. Para executar queries:
   - Clique em **+ ADD** para criar uma nova consulta SQL.
   - Utilize `SELECT * FROM \`lustrous-spirit-451917-p2.teste_tecnico.crypto_market_view\`` para visualizar os dados consolidados.
   - Para análise mais específica, filtre por colunas e condições conforme necessário.




### 🔍 Dashboard no Looker Studio
Os dados processados podem ser visualizados no seguinte dashboard do Looker Studio:
[🔗 Link para o Dashboard](https://lookerstudio.google.com/reporting/cde78a73-ee72-4db3-b096-733dce43271f/page/k2rzE)

#### 📊 Métricas Disponíveis
No dashboard, você encontrará diversas métricas relacionadas ao mercado de criptomoedas, incluindo:
- **Preço Atual (USD)**: Cotação das criptomoedas em tempo real.
- **Capitalização de Mercado**: Classificação por tamanho de mercado (Mega Cap, Large Cap, etc.).
- **Volume de Negociação 24h**: Indicador do volume de negociação nas últimas 24 horas.
- **Oferta Circulante e Máxima**: Comparação entre o número atual de moedas disponíveis e o limite máximo.
- **Tendência por Período**: Análise da variação dos preços ao longo do tempo.
- **Criptomoedas em Alta e em Baixa**: Listagem das criptomoedas com maior valorização e maior desvalorização.
- **Ranking Top 10**: Principais criptomoedas por capitalização de mercado.
- **Mudança no Volume 24h**: Comparação da variação de volume das principais criptomoedas.
- **Distribuição de Volume por Moeda**: Gráfico de pizza mostrando a participação de cada criptomoeda no volume total negociado.
- **VolumeUSD24H por Moeda**: Mapa de calor mostrando a representatividade do volume negociado para cada criptomoeda.
No dashboard, você encontrará diversas métricas relacionadas ao mercado de criptomoedas, incluindo:
- **Preço Atual (USD)**: Cotação das criptomoedas em tempo real.
- **Capitalização de Mercado**: Classificação por tamanho de mercado (Mega Cap, Large Cap, etc.).
- **Volume de Negociação 24h**: Indicador do volume de negociação nas últimas 24 horas.
- **Oferta Circulante e Máxima**: Comparação entre o número atual de moedas disponíveis e o limite máximo.
- **Tendência por Período**: Análise da variação dos preços ao longo do tempo.

Essas métricas são atualizadas automaticamente conforme os dados são processados no BigQuery.
Os dados processados podem ser visualizados no seguinte dashboard do Looker Studio:
[🔗 Link para o Dashboard](https://lookerstudio.google.com/reporting/cde78a73-ee72-4db3-b096-733dce43271f/page/k2rzE)


---

# Representação do BigQuery no Projeto 

## 📌 Estrutura do Projeto

```
Projeto_GCP/
│── request_api/          # Código da Cloud Run Function
│   ├── main.py           # Código principal da Cloud Run Function
│   ├── requirements.txt  # Dependências do projeto
│   ├── config.yaml       # Configurações opcionais da Cloud Run
│
│── schedule/             # Configuração do Cloud Scheduler
│   ├── schedule_config.png  # Arquivo com a configuração do agendamento
│   ├── instructions.md      # Instruções sobre o agendamento
│
│── bigquery/             # Scripts SQL para o BigQuery
│   ├── datasets/           # Representação dos datasets no BigQuery
│   │   ├── dataset_config.sql  # Definição do dataset
│   │   ├── schema_crypto_info.json  # Esquema da tabela crypto_info
│   │   ├── schema_cryptocurrency.json  # Esquema da tabela cryptocurrency
│   │   ├── schema_market_data.json  # Esquema da tabela market_data
│   ├── create_tables.sql   # Script para criar as tabelas
│   ├── insert_data.sql     # Script para inserir os dados
│   ├── create_view.sql     # Script para criar a view consolidada
```

Cada pasta representa uma parte do GCP, e dentro delas serão armazenados os códigos e imagens do ambiente trabalhado, demonstrando como ficou cada etapa.

## 📌 Explicação do Processo

### **Cloud Run Functions (main.py)**
O objetivo do `main.py` foi criar uma requisição dos dados da API e armazená-los no **BigQuery**, permitindo consultas, modelagens e visualizações via dashboards.

Essa função **extrai** dados da API de criptomoedas, **transforma** removendo registros antigos e **carrega** os dados no BigQuery. Ela garante que os dados não sejam duplicados e otimiza a inserção, utilizando uma tabela temporária.

### **Resumo Completo do Processo ETL**
- **Extração (E):** A função `buscar_dados_criptos()` coleta os dados da API de criptomoedas.
- **Transformação (T):** Os dados são processados, duplicações removidas e o formato ajustado.
- **Carga (L):** Os dados são carregados no BigQuery, primeiro em uma tabela temporária e depois na principal, garantindo sempre informações atualizadas.

### **Cloud Scheduler**
O **Cloud Scheduler** no Google Cloud permite agendar e automatizar a execução de tarefas periodicamente. No meu caso:
- **Frequência:** A cada hora (`0 * * * *`).
- **Automação contínua:** O processo de coleta, transformação e carga de dados ocorre automaticamente, evitando erros manuais.
- **Atualização em tempo real:** Os dados de criptomoedas são monitorados regularmente, garantindo informações sempre atualizadas para análise.

### **BigQuery - Modelagem e Armazenamento**
Os dados extraídos foram armazenados e modelados no **BigQuery**, partindo da tabela `crypto_info`. A partir dela:
- Os dados foram organizados em **duas tabelas**:
  1. **cryptocurrency** - Armazena os identificadores e metadados das criptomoedas.
  2. **market_data** - Contém os valores financeiros das moedas.

- Embora o BigQuery não seja um banco de dados relacional tradicional (como MySQL ou PostgreSQL), ele é altamente otimizado para grandes volumes de dados.
- Ele suporta consultas SQL padrão e permite trabalhar tanto com dados estruturados quanto semi-estruturados (JSON, CSV, Parquet, etc.).


### Criação da view:

Essa view crypto_market_view tem como objetivo extrair e transformar dados de duas tabelas (cryptocurrency e market_data) e criar uma visão consolidada sobre as criptomoedas, com informações adicionais e transformações para facilitar a análise.

Principais pontos:

1. **Transformação de Dados Numéricos**

priceUsd: O preço da criptomoeda em dólares, arredondado para 8 casas decimais usando a função ROUND().
marketCapUsd: A capitalização de mercado da criptomoeda em dólares, arredondada para 2 casas decimais.
volumeUsd24Hr: O volume negociado nas últimas 24 horas da criptomoeda, arredondado para 2 casas decimais.
supply: O número total de unidades da criptomoeda em circulação.
maxSupply: O número máximo de unidades da criptomoeda que podem existir (se NULL, é substituído por 0 utilizando a função COALESCE()). 

2. **Extração de Data e Hora**

year: O ano da data fornecida (2025-02-25 13:46:40 UTC) extraído usando a função EXTRACT() para obter apenas o ano.
month: O mês da mesma data extraído com EXTRACT() para obter apenas o mês.
day: O dia da mesma data extraído com EXTRACT() para obter apenas o dia.
time_formatted: A hora extraída da data fornecida, formatada no estilo HH:MM:SS usando a função FORMAT_TIMESTAMP(). Isso facilita a visualização do horário específico da criptomoeda.

3. **lassificação da Criptomoeda**

market_cap_category: Uma nova coluna criada com base na capitalização de mercado (marketCapUsd), utilizando uma expressão CASE para categorizar as criptomoedas em:
Mega Cap: Para capitalizações acima de 100 bilhões de dólares.
Large Cap: Para capitalizações entre 10 bilhões e 100 bilhões de dólares.
Mid Cap: Para capitalizações entre 1 bilhão e 10 bilhões de dólares.
Small Cap: Para capitalizações entre 100 milhões e 1 bilhão de dólares.
Micro Cap: Para capitalizações abaixo de 100 milhões de dólares.

4. **Join entre Tabelas**

A view realiza um JOIN entre a tabela cryptocurrency (representada por c) e a tabela market_data (representada por m) usando o campo id como chave de junção. Isso significa que os dados de ambas as tabelas são combinados para formar um único conjunto de informações sobre cada criptomoeda.





### **Looker Studio - Dashboard Dinâmico**
O **Looker Studio** permite configurar dashboards dinâmicos e gráficos em tempo real conectados diretamente ao BigQuery. Os dados são apresentados de forma clara e interativa, facilitando a análise de tendências de mercado.

### **Dashboard Disponível**
O dashboard exibe informações em tempo real, incluindo:
- **Preço Atual das Criptomoedas**
- **Classificação por Capitalização de Mercado**
- **Variação no Volume de Negociação em 24h**
- **Ranking das 10 Maiores Criptomoedas**
- **Distribuição de Volume por Moeda**

📊 **Acesse o dashboard em:** [🔗 Looker Studio](https://lookerstudio.google.com/reporting/cde78a73-ee72-4db3-b096-733dce43271f/page/k2rzE)

### Acompanhamento e Organização

Para ajudar na organização do desenvolvimento do projeto, utilizei a aba Issues do GitHub para documentar e acompanhar as etapas do desafio.

🔗 Confira a issue no GitHub: https://github.com/kayohr/Case-Tecnico/issues/1

🚀 **Projeto completo, automatizado e pronto para análise de criptomoedas!**

**Tentei reproduzir ao máximo o que foi feito no GCP e estou aberto a sugestões de melhorias para aprimorar ainda mais o projeto. Espero que essa documentação e estrutura sejam úteis para quem deseja entender este processo e aplicá-lo no dia a dia. Qualquer feedback ou recomendação será muito bem-vindo! 🚀**





