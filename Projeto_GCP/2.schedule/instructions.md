O agendamento configurado no Cloud Scheduler executa uma tarefa automatizada de coleta de informações de criptomoedas em intervalos regulares, e está configurado para fazer isso de acordo com os seguintes detalhes:

1. Definição do Agendamento
Nome do Job: agendamento

Descrição: "Coletar informações atualizadas" – o job está configurado para fazer a coleta de dados das criptomoedas.

Frequência (Cron Expression): 0 * * * *

Significado: O job será executado todo 1º minuto de cada hora.
Exemplo: A cada hora, o job faz uma requisição para coletar dados.
Timezone: Brasília Standard Time (BRT)

Isso significa que o agendamento será executado no horário de Brasília.
2. Configuração da Execução
Tipo de Alvo (Target type): HTTP
O job faz uma requisição HTTP POST para a URL fornecida, que corresponde ao endpoint da função ETL hospedada.
URL do Alvo: https://request-api-8623044835.us-central1.run.app/
A URL é o endpoint da função ETL que será chamada para coletar e processar os dados das criptomoedas.
Cabeçalhos HTTP (HTTP Headers):
User-Agent: Google-Cloud-Scheduler
Este cabeçalho é necessário para identificar a requisição como proveniente do Google Cloud Scheduler.
3. Estado e Execução
Status da Última Execução: Success – A última execução foi bem-sucedida.
Última Execução: Feb 25, 2025, 8:00:00 PM – O job foi executado pela última vez no horário mencionado.
Próxima Execução: Feb 25, 2025, 9:00:00 PM – O próximo agendamento será realizado uma hora depois.