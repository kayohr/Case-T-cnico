import requests
import json
import logging
from flask import jsonify
from google.cloud import bigquery

# Configuração básica dos logs
logging.basicConfig(level=logging.INFO)

def etl(request):
    # Configurações do projeto e da API
    ID_PROJETO = "lustrous-spirit-451917-p2"
    ID_DATASET = "teste_tecnico"
    ID_TABELA = "crypto_info"
    URL_API = "https://api.coincap.io/v2/assets"
    HEADERS = {"Accept": "application/json"}

    # Inicializa o cliente do BigQuery
    cliente = bigquery.Client()

    # Define o schema para as tabelas
    SCHEMA = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("symbol", "STRING"),
        bigquery.SchemaField("rank", "INTEGER"),
        bigquery.SchemaField("priceUsd", "FLOAT"),
        bigquery.SchemaField("marketCapUsd", "FLOAT"),
        bigquery.SchemaField("volumeUsd24Hr", "FLOAT"),
        bigquery.SchemaField("supply", "FLOAT"),
        bigquery.SchemaField("maxSupply", "FLOAT"),
        bigquery.SchemaField("changePercent24Hr", "FLOAT"),
        bigquery.SchemaField("vwap24Hr", "FLOAT"),
        bigquery.SchemaField("explorer", "STRING")
    ]

    def buscar_dados_criptos():
        """Busca dados de criptomoedas na API e retorna o JSON"""
        try:
            logging.info("Iniciando requisição para a API de criptomoedas.")
            resposta = requests.get(URL_API, headers=HEADERS)
            resposta.raise_for_status()
            dados = resposta.json().get("data", [])
            logging.info(f"Recebidos {len(dados)} registros da API.")
            return dados
        except requests.exceptions.RequestException as erro:
            logging.error(f"Erro na requisição: {str(erro)}")
            return {"error": f"Erro na requisição: {str(erro)}"}

    def criar_tabela_se_ausente(ref_tabela):
        """Cria a tabela no BigQuery caso ela não exista"""
        try:
            cliente.get_table(ref_tabela)
            logging.info(f"Tabela {ref_tabela} já existe.")
        except Exception:
            tabela = bigquery.Table(ref_tabela, schema=SCHEMA)
            cliente.create_table(tabela)
            logging.info(f"Tabela {ref_tabela} criada com sucesso!")

    def criar_tabela_temporaria(ref_tabela_temp):
        """Cria uma tabela temporária para armazenamento dos dados antes da inserção"""
        tabela_temp = bigquery.Table(ref_tabela_temp, schema=SCHEMA)
        cliente.create_table(tabela_temp, exists_ok=True)
        logging.info(f"Tabela temporária {ref_tabela_temp} pronta para uso.")

    def remover_registros_antigos(ref_tabela, criptos):
        """Remove registros antigos que possuam o mesmo ID dos novos dados"""
        ids_para_remover = [f"'{cripto['id']}'" for cripto in criptos]
        ids_str = ", ".join(ids_para_remover)
        consulta = f"""
        DELETE FROM `{ref_tabela}`
        WHERE id IN ({ids_str})
        """
        job = cliente.query(consulta)
        job.result()  # Aguarda a conclusão da query
        logging.info("Registros antigos removidos para evitar duplicações.")

    def inserir_dados_na_tabela_principal(ref_tabela, ref_tabela_temp):
        """Insere os novos dados da tabela temporária na tabela principal"""
        consulta = f"""
        INSERT INTO `{ref_tabela}` 
        SELECT * FROM `{ref_tabela_temp}`
        """
        job = cliente.query(consulta)
        job.result()  # Aguarda a conclusão da query
        logging.info("Novos registros inseridos na tabela principal.")

    def processar_dados():
        """Executa o fluxo completo de obtenção e armazenamento dos dados"""
        logging.info("Iniciando processamento dos dados.")
        dados_criptos = buscar_dados_criptos()
        if isinstance(dados_criptos, dict) and "error" in dados_criptos:
            logging.error("Erro ao buscar dados de criptomoedas.")
            return {"error": dados_criptos["error"]}
        
        logging.info(f"Processando {len(dados_criptos)} registros.")

        # Define as referências para a tabela principal e a temporária
        ref_tabela = f"{ID_PROJETO}.{ID_DATASET}.{ID_TABELA}"
        ref_tabela_temp = f"{ID_PROJETO}.{ID_DATASET}.{ID_TABELA}_temp"

        criar_tabela_se_ausente(ref_tabela)
        criar_tabela_temporaria(ref_tabela_temp)

        # Insere os dados na tabela temporária
        logging.info("Inserindo dados na tabela temporária.")
        erros = cliente.insert_rows_json(ref_tabela_temp, dados_criptos)
        if erros:
            logging.error(f"Erro ao inserir dados na tabela temporária: {erros}")
            return {"error": f"Erro ao inserir dados na tabela temporária: {erros}"}

        # Remove registros antigos e insere os novos dados na tabela principal
        remover_registros_antigos(ref_tabela, dados_criptos)
        inserir_dados_na_tabela_principal(ref_tabela, ref_tabela_temp)
        logging.info("Processamento dos dados concluído com sucesso.")

        return {"message": "Dados inseridos/atualizados com sucesso!"}

    resposta = processar_dados()
    return jsonify(resposta)