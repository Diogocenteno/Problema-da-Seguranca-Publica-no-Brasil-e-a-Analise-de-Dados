Análise de Segurança Pública no Brasil
Este projeto realiza uma análise de dados de segurança pública no Brasil utilizando informações extraídas do "Anuário Brasileiro de Segurança Pública". O objetivo é explorar dados de homicídios dolosos, latrocínios e lesões corporais com morte, além de realizar previsões sobre o futuro desses crimes. O código inclui etapas de processamento de dados, criação de visualizações e modelagem preditiva.

Tecnologias Utilizadas
Python: Linguagem de programação utilizada para análise de dados.

Pandas: Manipulação e análise de dados.

Matplotlib e Seaborn: Geração de gráficos estáticos.

Plotly: Criação de mapas interativos.

Scikit-learn: Modelagem preditiva com regressão linear e random forest.

Statsmodels: Decomposição sazonal.

Requests: Acesso ao arquivo GeoJSON para visualizações geográficas.

Funcionalidades
O script principal realiza as seguintes funções:

Configuração do Ambiente:

Criação de diretórios para armazenar os resultados, gráficos e logs.

Carregamento de Dados:

Carrega o arquivo de dados do "Anuário Brasileiro de Segurança Pública".

Filtra e valida as colunas essenciais.

Processamento de Dados:

Limpeza dos dados, incluindo remoção de valores ausentes e duplicados.

Conversão de variáveis para tipos corretos.

Filtragem de dados dentro do intervalo de anos (2000 até o ano atual).

Criação de Visualizações:

Heatmap de Correlação: Exibe a correlação entre as variáveis.

Série Temporal: Visualização da evolução dos homicídios dolosos ao longo dos anos.

Distribuição Geográfica: Gráfico de barras e mapa interativo para visualização dos homicídios por estado.

Mapa de Calor Temporal-Estados: Mapa de calor mostrando a evolução temporal de homicídios por estado.

Modelagem Preditiva:

Utiliza modelos de regressão linear e random forest para prever os homicídios dolosos nos próximos 3 anos.

Gera gráficos com as previsões comparadas ao histórico.

Armazenamento de Resultados:

Salva os dados processados e as previsões em arquivos Excel.

Estrutura de Diretórios
Copiar
.
├── visualizacoes/
│   ├── analise_temporal/
│   ├── distribuicao_geografica/
│   └── mapas_interativos/
├── dados_processados/
└── logs/
visualizacoes: Contém os gráficos e mapas gerados.

dados_processados: Armazena os dados processados e as previsões.

logs: Armazena os logs de execução do código.

Instalação
Instale as dependências necessárias:

bash
Copiar
pip install pandas matplotlib seaborn plotly scikit-learn statsmodels openpyxl requests
Certifique-se de ter o arquivo Anuário Brasileiro de Segurança Pública.xlsx disponível no caminho correto.

Executando o Código
Para rodar a análise, basta executar o script Python:

bash
Copiar
python analise_seguranca.py
O código criará as visualizações e armazenará os resultados no diretório visualizacoes/ e dados_processados/.

Contribuições
Este projeto está aberto a contribuições. Caso queira colaborar, fique à vontade para enviar pull requests!

Licença
Este projeto é de código aberto. Sinta-se à vontade para usar, modificar e distribuir conforme necessário.
