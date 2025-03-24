#%% 

# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import warnings
import logging
import requests
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.express as px
from sklearn.preprocessing import StandardScaler

# ===========================================
# CONFIGURAÇÕES GERAIS
# ===========================================
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)

# Configuração de temas e estilo
sns.set_theme(style="darkgrid", context="notebook", 
             rc={"axes.titlesize": 18, 
                 "axes.labelsize": 14,
                 "figure.dpi": 150,
                 "figure.figsize": (12, 6)})

CORES = ['#2E86AB', '#F24236', '#FF9F1C', '#4CB944', '#6D597A']
sns.set_palette(CORES)

# Constantes globais
CAMINHO_DADOS = "D:/leitura-escrita/leitura-escrita/data/Anuário Brasileiro de Segurança Pública.xlsx"
GEOJSON_URL = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
COLUNAS_ESSENCIAIS = ['ano', 'sigla_uf', 'quantidade_homicidio_doloso', 
                     'quantidade_latrocinio', 'quantidade_lesao_corporal_morte']

# ===========================================
# FUNÇÕES PRINCIPAIS 
# ===========================================

def configurar_ambiente():
    """Cria estrutura de diretórios necessária"""
    print("🛠️ Configurando ambiente...")
    diretorios = [
        'visualizacoes/analise_temporal',
        'visualizacoes/distribuicao_geografica',
        'visualizacoes/mapas_interativos',
        'dados_processados',
        'logs'
    ]
    
    for diretorio in diretorios:
        try:
            os.makedirs(diretorio, exist_ok=True)
            print(f"📂 Diretório criado: {diretorio}")
        except Exception as e:
            print(f"❌ Erro ao criar diretório {diretorio}: {str(e)}")

def carregar_dados():
    """Carrega e valida os dados brutos"""
    print("\n📥 Carregando dados...")
    try:
        df = pd.read_excel(CAMINHO_DADOS, engine='openpyxl')
        print("✅ Dados carregados com sucesso!")
        print("\n🔍 Primeiras linhas do dataset:")
        print(df[COLUNAS_ESSENCIAIS].head())
        return df
    except Exception as e:
        print(f"❌ Erro na carga de dados: {str(e)}")
        return None

def processar_dados(df):
    """Pipeline completo de tratamento de dados"""
    print("\n🧹 Processando dados...")
    try:
        df_clean = (
            df[COLUNAS_ESSENCIAIS]
            .dropna(subset=['ano', 'sigla_uf'])
            .drop_duplicates()
            .reset_index(drop=True)
        )
        
        df_clean = df_clean.assign(
            ano = lambda x: pd.to_numeric(x['ano'], errors='coerce'),
            quantidade_homicidio_doloso = lambda x: x['quantidade_homicidio_doloso'].clip(0, 1e6),
            quantidade_latrocinio = lambda x: x['quantidade_latrocinio'].clip(0, 1e5)
        )
        
        ano_atual = datetime.now().year
        df_clean = df_clean[
            (df_clean['ano'] >= 2000) & 
            (df_clean['ano'] <= ano_atual)
        ]
        
        print("\n✅ Dados processados com sucesso!")
        print("📊 Estatísticas descritivas:")
        print(df_clean.describe().round(2))
        
        return df_clean
    except Exception as e:
        print(f"❌ Erro no processamento: {str(e)}")
        return None

def criar_visualizacoes(df):
    """Gera e salva todas as visualizações analíticas"""
    print("\n📊 Criando visualizações...")
    
    try:
        # 1. Heatmap de Correlação
        print("\n🔥 Gerando heatmap de correlação...")
        plt.figure(figsize=(10, 6))
        corr = df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlação entre Variáveis de Segurança Pública')
        plt.savefig('visualizacoes/analise_temporal/heatmap_correlacao.png', bbox_inches='tight')
        plt.close()
        print("✅ Heatmap salvo em visualizacoes/analise_temporal/heatmap_correlacao.png")

        # 2. Série Temporal
        print("\n📈 Gerando série temporal...")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            data=df.groupby('ano')['quantidade_homicidio_doloso'].sum().reset_index(),
            x='ano', y='quantidade_homicidio_doloso',
            marker='o', linewidth=2)
        plt.title('Evolução de Homicídios Dolosos')
        plt.ylabel('Número de Ocorrências')
        plt.grid(True, alpha=0.3)
        plt.savefig('visualizacoes/analise_temporal/serie_temporal_homicidios.png', bbox_inches='tight')
        plt.close()
        print("✅ Série temporal salva em visualizacoes/analise_temporal/serie_temporal_homicidios.png")

        # 3. Visualizações Geográficas
        print("\n🌎 Gerando visualizações geográficas...")
        df_geo = df.groupby('sigla_uf', as_index=False).agg({
            'quantidade_homicidio_doloso': 'sum',
            'quantidade_latrocinio': 'sum'
        })

        # Mapa Interativo
        print("\n🗺️ Salvando mapa interativo...")
        fig = px.choropleth(
            df_geo,
            geojson=requests.get(GEOJSON_URL).json(),
            locations='sigla_uf',
            color='quantidade_homicidio_doloso',
            featureidkey='properties.sigla',
            color_continuous_scale='OrRd',
            labels={'quantidade_homicidio_doloso': 'Homicídios'},
            title='Distribuição Geográfica de Homicídios Dolosos'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.write_html('visualizacoes/mapas_interativos/mapa_coropletico.html')
        print("✅ Mapa interativo salvo em visualizacoes/mapas_interativos/mapa_coropletico.html")

        # Gráfico de Barras por Estado
        print("\n📊 Gerando gráfico de distribuição por estado...")
        plt.figure(figsize=(14, 8))
        df_geo_sorted = df_geo.sort_values('quantidade_homicidio_doloso', ascending=False)
        sns.barplot(
            data=df_geo_sorted,
            x='sigla_uf',
            y='quantidade_homicidio_doloso',
            palette='rocket'
        )
        plt.title('Distribuição de Homicídios Dolosos por Estado')
        plt.xlabel('Estado')
        plt.ylabel('Número de Homicídios')
        plt.xticks(rotation=45)
        plt.savefig('visualizacoes/distribuicao_geografica/distribuicao_estados.png', bbox_inches='tight')
        plt.close()
        print("✅ Gráfico de estados salvo em visualizacoes/distribuicao_geografica/distribuicao_estados.png")

        # Mapa de Calor Temporal-Estados
        print("\n🔥 Gerando mapa de calor temporal...")
        df_heatmap = df.pivot_table(
            index='ano',
            columns='sigla_uf',
            values='quantidade_homicidio_doloso',
            aggfunc='sum'
        )
        plt.figure(figsize=(16, 10))
        sns.heatmap(df_heatmap, cmap='viridis', linewidths=0.5)
        plt.title('Evolução Temporal de Homicídios por Estado')
        plt.xlabel('Estado')
        plt.ylabel('Ano')
        plt.savefig('visualizacoes/distribuicao_geografica/mapa_calor_temporal.png', bbox_inches='tight')
        plt.close()
        print("✅ Mapa de calor salvo em visualizacoes/distribuicao_geografica/mapa_calor_temporal.png")
        
    except Exception as e:
        print(f"❌ Erro nas visualizações: {str(e)}")

def gerar_previsoes(df):
    """Executa e salva modelagem preditiva"""
    print("\n🔮 Gerando previsões...")
    try:
        df_serie = df.groupby('ano', as_index=False)['quantidade_homicidio_doloso'].sum()
        
        modelos = {
            'Regressão Linear': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        X = df_serie[['ano']]
        y = df_serie['quantidade_homicidio_doloso']
        
        previsoes = pd.DataFrame()
        previsoes['ano'] = [df_serie['ano'].max() + i for i in range(1, 4)]
        
        for nome, modelo in modelos.items():
            if nome == 'Random Forest':
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                modelo.fit(X_scaled, y)
                futuros = scaler.transform([[x] for x in previsoes['ano']])
            else:
                modelo.fit(X, y)
                futuros = previsoes[['ano']]
            
            previsoes[nome] = modelo.predict(futuros)
        
        # Salvar gráfico de previsões
        plt.figure(figsize=(10, 5))
        plt.plot(df_serie['ano'], df_serie['quantidade_homicidio_doloso'], label='Histórico')
        plt.plot(previsoes['ano'], previsoes['Regressão Linear'], '--', label='Regressão Linear')
        plt.plot(previsoes['ano'], previsoes['Random Forest'], '--', label='Random Forest')
        plt.title('Projeção de Homicídios Dolosos')
        plt.legend()
        plt.savefig('visualizacoes/analise_temporal/previsao_homicidios.png', bbox_inches='tight')
        plt.close()
        print("✅ Gráfico de previsões salvo em visualizacoes/analise_temporal/previsao_homicidios.png")
        
        return previsoes
    except Exception as e:
        print(f"❌ Erro nas previsões: {str(e)}")
        return None

# ===========================================
# FLUXO PRINCIPAL
# ===========================================
if __name__ == "__main__":
    print("="*50)
    print("🔍 ANÁLISE DE SEGURANÇA PÚBLICA - BRASIL")
    print("="*50)
    
    configurar_ambiente()
    
    df_raw = carregar_dados()
    
    if df_raw is not None:
        df_processado = processar_dados(df_raw)
        
        if df_processado is not None:
            criar_visualizacoes(df_processado)
            
            previsoes = gerar_previsoes(df_processado)
            
            print("\n💾 Salvando resultados...")
            try:
                df_processado.to_excel('dados_processados/dados_processados.xlsx', index=False)
                if previsoes is not None:
                    previsoes.to_excel('dados_processados/previsoes.xlsx', index=False)
                print("✅ Dados salvos com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao salvar dados: {str(e)}")
    
    print("\n✅ Análise concluída!")