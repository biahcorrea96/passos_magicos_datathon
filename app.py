import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
import pickle

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, roc_curve
)
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Passos Mágicos - Previsão de Defasagem",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS - PALETA FIAP (FUNDO CLARO, DETALHES ESCUROS)
# ============================================================
st.markdown("""
<style>
    /* Reset para tema claro */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Banner principal */
    .banner-fiap {
        background: linear-gradient(135deg, #ED145B 0%, #c4114d 100%);
        padding: 1.8rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .banner-fiap h2 {
        color: #ffffff;
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Cards de métricas - tema claro */
    .metric-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 1.4rem;
        text-align: center;
        border: 2px solid #ED145B;
        box-shadow: 0 2px 8px rgba(237, 20, 91, 0.1);
    }
    .metric-card h3 {
        color: #ED145B;
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }
    .metric-card p {
        color: #555555;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
        font-weight: 500;
    }

    /* Info box estilo referência */
    .info-box {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid #ED145B;
        margin-bottom: 1rem;
    }
    .info-box h4 {
        color: #1a1a2e;
        margin: 0 0 0.5rem 0;
        font-size: 1.05rem;
    }
    .info-box p, .info-box li {
        color: #333333;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    /* Benefícios em 2 colunas */
    .benefits-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .benefit-item {
        background: #ffffff;
        border-radius: 8px;
        padding: 1.2rem;
        border-left: 4px solid #ED145B;
    }
    .benefit-item h4 {
        color: #ED145B;
        margin-top: 0;
        font-size: 1.05rem;
    }
    .benefit-item ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    .benefit-item li {
        color: #333333;
        font-size: 0.92rem;
        margin-bottom: 0.4rem;
    }

    /* Tabelas */
    .dataframe {
        background: #ffffff !important;
    }
    .dataframe th {
        background: #ED145B !important;
        color: #ffffff !important;
        font-weight: 700;
    }
    .dataframe td {
        color: #333333;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f8f9fa;
    }
    [data-testid="stSidebar"] .stRadio > label {
        color: #1a1a2e;
        font-weight: 600;
    }

    /* Buttons */
    .stButton > button {
        background: #ED145B;
        color: #ffffff;
        border: none;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: #c4114d;
        color: #ffffff;
    }

    /* Links */
    a {
        color: #ED145B;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }

    /* Seção de Dashboard */
    .dashboard-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1.5rem;
    }
    .dashboard-section h3 {
        color: #ED145B;
        margin-top: 0;
    }

    /* Seção de Desenvolvedores */
    .developers-section {
        background: #ffffff;
        border-radius: 10px;
        padding: 1.5rem;
        border: 2px solid #ED145B;
        margin-top: 2rem;
    }
    .developers-section h3 {
        color: #ED145B;
        margin-top: 0;
    }
    .developer-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #ED145B;
    }
    .developer-card strong {
        color: #1a1a2e;
    }
    .developer-card p {
        color: #555555;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNÇÕES DE CARREGAMENTO E PROCESSAMENTO
# ============================================================

@st.cache_data
def carregar_dados_brutos():
    """Carrega os arquivos Excel brutos."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, 'data')

    df_2022 = pd.read_excel(os.path.join(data_path, 'base_2022.xlsx'))
    df_2023 = pd.read_excel(os.path.join(data_path, 'base_2023.xlsx'))
    df_2024 = pd.read_excel(os.path.join(data_path, 'base_2024.xlsx'))

    return df_2022, df_2023, df_2024


def build_temporal_pair(df_current, df_next, year_current, year_next):
    """
    Cruza alunos por RA entre dois anos consecutivos.
    Features vêm do ano atual, target (defasagem) vem do ano seguinte.
    """
    # Encontrar alunos em comum (RA)
    common_ras = set(df_current['RA'].dropna()) & set(df_next['RA'].dropna())

    curr = df_current[df_current['RA'].isin(common_ras)].copy()
    nxt = df_next[df_next['RA'].isin(common_ras)].copy()

    # 1. Extrair Features do Ano Atual
    features = {'RA': curr['RA'].values}

    # Indicadores PEDE (Ano Atual)
    for col in ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN']:
        if col in curr.columns:
            features[col] = pd.to_numeric(curr[col], errors='coerce').values

    # INDE (Ano Atual)
    possible_inde = [c for c in curr.columns if 'INDE' in c and str(year_current)[-2:] in c]
    if possible_inde:
        features['INDE'] = pd.to_numeric(curr[possible_inde[0]], errors='coerce').values
    else:
        features['INDE'] = np.nan

    # Idade
    idade_col = [c for c in curr.columns if 'Idade' in c or 'idade' in c]
    if idade_col:
        vals = curr[idade_col[0]]
        if vals.dtype == 'datetime64[ns]' or str(vals.dtype).startswith('datetime'):
            features['Idade'] = ((pd.Timestamp(f'{year_current}-06-01') - vals).dt.days / 365.25).values
        else:
            features['Idade'] = pd.to_numeric(vals, errors='coerce').values
    else:
        features['Idade'] = np.nan

    # Nº de Avaliações
    if 'Nº Av' in curr.columns:
        features['Num_Av'] = pd.to_numeric(curr['Nº Av'], errors='coerce').values
    else:
        features['Num_Av'] = np.nan

    # Anos na Passos Mágicos
    if 'Ano ingresso' in curr.columns:
        features['Anos_PM'] = year_current - pd.to_numeric(curr['Ano ingresso'], errors='coerce').values
    else:
        features['Anos_PM'] = np.nan

    df_features = pd.DataFrame(features)

    # 2. Extrair Target do Ano Seguinte
    defas_col = 'Defas' if 'Defas' in nxt.columns else 'Defasagem'
    target_df = nxt[['RA', defas_col]].copy()
    target_df.columns = ['RA', 'Defasagem_Next']
    target_df['Defasagem_Next'] = pd.to_numeric(target_df['Defasagem_Next'], errors='coerce')

    # 3. Mesclar e criar a variável alvo binária
    result = df_features.merge(target_df, on='RA', how='inner')

    # Risco = 1 se a defasagem no ano seguinte for menor que 0 (aluno atrasado)
    result['Risco'] = (result['Defasagem_Next'] < 0).astype(int)
    result['Periodo'] = f'{year_current}->{year_next}'

    return result


@st.cache_data
def carregar_e_processar_dados():
    """Carrega e processa as bases usando abordagem temporal."""
    df_2022, df_2023, df_2024 = carregar_dados_brutos()

    # Construir pares temporais
    try:
        pair_22_23 = build_temporal_pair(df_2022, df_2023, 2022, 2023)
        pair_23_24 = build_temporal_pair(df_2023, df_2024, 2023, 2024)

        # Combinar tudo em um único dataset
        df_all = pd.concat([pair_22_23, pair_23_24], ignore_index=True)
    except Exception as e:
        st.error(f"Erro na construção temporal: {e}")
        df_all = pd.DataFrame()

    return df_all, df_2022, df_2023, df_2024


@st.cache_resource
def treinar_modelo_xgboost(df_all):
    """Treina o modelo XGBoost com os dados processados (lógica temporal do notebook)."""
    
    # Features do modelo (conforme notebook)
    feature_cols = ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'INDE', 'Idade', 'Num_Av', 'Anos_PM']
    
    # Preparar dados
    X = df_all[feature_cols].copy()
    y = df_all['Risco'].copy()
    
    # Remover registros onde TODOS os indicadores principais estão vazios
    key_indicators = ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'INDE']
    valid_idx = X.dropna(subset=key_indicators, how='all').index
    
    X = X.loc[valid_idx]
    y = y.loc[valid_idx]
    
    # Imputar valores nulos com a mediana
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols, index=X.index)
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_imputed, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Normalizar
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_cols, index=X_train.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_cols, index=X_test.index)
    
    # Scaler para dados completos (usado no cross-validation)
    scaler_full = StandardScaler()
    X_all_scaled = pd.DataFrame(scaler_full.fit_transform(X_imputed), columns=feature_cols, index=X_imputed.index)
    
    # Calcular scale_pos_weight
    n_neg = (y_train == 0).sum()
    n_pos = (y_train == 1).sum()
    scale_pos_weight = n_neg / n_pos if n_pos > 0 else 1
    
    # Modelo XGBoost com hiperparâmetros otimizados (do notebook)
    model = XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.05,
        min_child_weight=5,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.5,
        reg_lambda=1.0,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric='logloss',
        verbosity=0
    )
    
    # Treinar
    model.fit(X_train_scaled, y_train)
    
    # Previsões
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Métricas
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    # Matriz de confusão
    cm = confusion_matrix(y_test, y_pred)
    
    # Curva ROC
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    
    # Cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_all_scaled, y, cv=cv, scoring='accuracy')
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    return {
        'model': model,
        'scaler': scaler_full,
        'feature_cols': feature_cols,
        'metrics': {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'auc': auc
        },
        'confusion_matrix': cm,
        'roc_curve': (fpr, tpr, auc),
        'cv_scores': cv_scores,
        'feature_importance': feature_importance,
        'X_test': X_test_scaled,
        'y_test': y_test
    }


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Passos Mágicos")
    st.markdown("**Modelo Preditivo de Risco de Defasagem Escolar**")
    st.markdown("---")
    
    page = st.radio(
        "Selecione uma opção:",
        ["Informações do Sistema", "Modelo Preditivo", "Validação do Modelo", "Realizar Previsão"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("**Versão**: 2.0.0")
    st.markdown("**Atualização**: Março 2026")
    st.markdown("---")
    st.markdown("**Tech Challenge 5 - FIAP**")
    st.markdown("Pós-Graduação em Data Analytics")

# Carregar dados
df_all, df_2022, df_2023, df_2024 = carregar_e_processar_dados()

# Treinar modelo
model_data = treinar_modelo_xgboost(df_all)

# ============================================================
# PÁGINA: INFORMAÇÕES DO SISTEMA
# ============================================================

if page == "Informações do Sistema":
    st.markdown('<div class="banner-fiap"><h2>Sistema de Previsão de Risco de Defasagem Escolar</h2></div>', unsafe_allow_html=True)
    
    # Sobre o Sistema
    st.markdown("### Sobre o Sistema")
    st.markdown("""
    Este sistema foi desenvolvido para auxiliar a **equipe pedagógica da Associação Passos Mágicos** na identificação de alunos em risco de defasagem escolar. 
    A ferramenta utiliza técnicas avançadas de aprendizado de máquina (XGBoost) para analisar múltiplos indicadores pedagógicos e fornecer uma classificação precisa, 
    apoiando a tomada de decisão preventiva.
    """)
    
    # Benefícios
    st.markdown("### Benefícios do Sistema")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="benefit-item">
        <h4>🚀 Identificação Precoce de Risco</h4>
        <ul>
        <li>Avaliação rápida e padronizada</li>
        <li>Resultados em segundos</li>
        <li>Interface intuitiva</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-item">
        <h4>📊 Precisão na Classificação</h4>
        <ul>
        <li>Modelo XGBoost com 82%+ de acurácia</li>
        <li>Análise de 10 variáveis principais</li>
        <li>Classificação binária (Em Risco / Sem Risco)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="benefit-item">
        <h4>💡 Apoio à Decisão Pedagógica</h4>
        <ul>
        <li>Probabilidades detalhadas por aluno</li>
        <li>Perfil visual dos indicadores</li>
        <li>Histórico de avaliações</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-item">
        <h4>✅ Padronização do Atendimento</h4>
        <ul>
        <li>Critérios objetivos de avaliação</li>
        <li>Protocolo consistente</li>
        <li>Documentação automática</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Classificação de Risco
    st.markdown("### Classificação de Risco")
    risk_data = {
        'Classificação': ['Sem Risco', 'Em Risco'],
        'Critério': ['Defasagem >= 0 (aluno no nível adequado ou acima)', 'Defasagem < 0 (aluno atrasado)'],
        'Ação Recomendada': ['Acompanhamento regular', 'Intervenção pedagógica imediata']
    }
    st.dataframe(risk_data, use_container_width=True, hide_index=True)
    
    # Indicadores PEDE
    st.markdown("### Indicadores PEDE Utilizados")
    indicators_data = {
        'Indicador': ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'INDE'],
        'Descrição': [
            'Índice de Autoavaliação',
            'Índice de Engajamento',
            'Índice Psicossocial',
            'Índice de Aprendizagem',
            'Índice de Ponto de Virada',
            'Índice de Aprendizagem Normalizado',
            'Índice de Desenvolvimento'
        ],
        'Escala': ['0 a 10', '0 a 10', '0 a 10', '0 a 10', '0 a 10', '0 a 10', '0 a 10'],
        'O que Mede': [
            'Percepção do aluno sobre seu próprio desempenho',
            'Nível de envolvimento e participação',
            'Aspectos emocionais e sociais',
            'Progresso no aprendizado acadêmico',
            'Potencial de transformação do aluno',
            'Desempenho normalizado em aprendizagem',
            'Desenvolvimento geral do aluno'
        ]
    }
    st.dataframe(indicators_data, use_container_width=True, hide_index=True)
    
    # Base de Dados
    st.markdown("### Base de Dados")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{len(df_all)}</h3>
        <p>Total de Registros</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{len(df_2022)}</h3>
        <p>Base 2022</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{len(df_2023)}</h3>
        <p>Base 2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{len(df_2024)}</h3>
        <p>Base 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Características do Modelo
    st.markdown("### Características do Modelo (XGBoost)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>🔄 Abordagem Temporal</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
        <li>Prevê defasagem do ano N+1</li>
        <li>Usa indicadores do ano N</li>
        <li>Elimina data leakage</li>
        <li>Permite intervenção preventiva</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>🎯 Features do Modelo</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
        <li>IAA, IEG, IPS, IDA, IPV</li>
        <li>IAN, INDE</li>
        <li>Idade, Anos na PM</li>
        <li>Número de Avaliações</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Desenvolvedores
    st.markdown("### 👥 Desenvolvedores")
    st.markdown("""
    <div class="developers-section">
    <h3>Equipe de Desenvolvimento</h3>
    
    <div class="developer-card">
    <strong>Datathon - FIAP</strong>
    <p>Pós-Graduação em Data Analytics</p>
    <p>Em parceria com a <strong>Associação Passos Mágicos</strong></p>
    </div>
    
    <div class="developer-card">
    <strong>Bianca Correa | Sócia</strong>
    <p>bianca.correa@fiap.com.br </p>
    </div>

    <div class="developer-card">
    <strong>Daniele Andrino | Sócia</strong>
    <p>daniele.andrino@fiap.com.br</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PÁGINA: MODELO PREDITIVO
# ============================================================

elif page == "Modelo Preditivo":
    st.markdown('<div class="banner-fiap"><h2>Arquitetura do Modelo Preditivo XGBoost</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### Pipeline de Treinamento")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>1. Dados de Entrada (10 features)</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
        <li>IAA, IEG, IPS, IDA, IPV</li>
        <li>IAN, INDE</li>
        <li>Idade</li>
        <li>Anos na PM</li>
        <li>Nº Avaliações</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>2. Pré-processamento</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
        <li>Imputação (mediana)</li>
        <li>Normalização</li>
        <li>StandardScaler</li>
        <li>Split 80/20</li>
        <li>Validação Cruzada 5-fold</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
        <h4>3. Modelo XGBoost</h4>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
        <li>n_estimators: 150</li>
        <li>max_depth: 4</li>
        <li>learning_rate: 0.05</li>
        <li>Regularização: L1 + L2</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Métricas de Desempenho")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{model_data['metrics']['accuracy']:.1%}</h3>
        <p>Acurácia (Test)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{model_data['metrics']['f1']:.1%}</h3>
        <p>F1-Score (Test)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{model_data['metrics']['auc']:.1%}</h3>
        <p>AUC-ROC (Test)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{model_data['metrics']['recall']:.1%}</h3>
        <p>Recall (Test)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Importância das Features")
    
    fig_importance = px.bar(
        model_data['feature_importance'],
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=['#f8f9fa', '#ED145B'],
        title='Top 10 Features mais Importantes'
    )
    fig_importance.update_layout(
        height=400,
        showlegend=False,
        template='plotly_white',
        font=dict(family='Arial, sans-serif', size=11, color='#1a1a2e')
    )
    st.plotly_chart(fig_importance, use_container_width=True)
    
    st.markdown("### Dados de Treinamento")
    st.markdown(f"""
    - **Total de Registros**: {len(df_all)}
    - **Registros Válidos**: {len(model_data['y_test']) + len(model_data['X_test']) // len(model_data['feature_cols'])}
    - **Conjunto de Teste**: {len(model_data['y_test'])} registros
    - **Distribuição**: {(model_data['y_test'] == 0).sum()} sem risco, {(model_data['y_test'] == 1).sum()} em risco
    """)

# ============================================================
# PÁGINA: VALIDAÇÃO DO MODELO
# ============================================================

elif page == "Validação do Modelo":
    st.markdown('<div class="banner-fiap"><h2>Validação e Análise do Modelo</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### Matriz de Confusão (Conjunto de Teste)")
    
    cm = model_data['confusion_matrix']
    fig_cm = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Sem Risco (Pred)', 'Em Risco (Pred)'],
        y=['Sem Risco (Real)', 'Em Risco (Real)'],
        colorscale='Blues',
        text=cm,
        texttemplate='%{text}',
        textfont={"size": 14},
        colorbar=dict(title="Frequência")
    ))
    fig_cm.update_layout(
        height=400,
        template='plotly_white',
        font=dict(family='Arial, sans-serif', size=11, color='#1a1a2e')
    )
    st.plotly_chart(fig_cm, use_container_width=True)
    
    st.markdown("### Curva ROC-AUC")
    
    fpr, tpr, auc = model_data['roc_curve']
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC = {auc:.3f})',
        line=dict(color='#ED145B', width=3)
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color='#cccccc', width=2, dash='dash')
    ))
    fig_roc.update_layout(
        title='Curva ROC - Desempenho do Modelo',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        height=400,
        template='plotly_white',
        font=dict(family='Arial, sans-serif', size=11, color='#1a1a2e'),
        hovermode='closest'
    )
    st.plotly_chart(fig_roc, use_container_width=True)
    
    st.markdown("### Validação Cruzada (5-fold)")
    
    cv_data = {
        'Fold': [f'Fold {i+1}' for i in range(len(model_data['cv_scores']))],
        'Acurácia': model_data['cv_scores']
    }
    cv_df = pd.DataFrame(cv_data)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_cv = px.bar(
            cv_df,
            x='Fold',
            y='Acurácia',
            color='Acurácia',
            color_continuous_scale=['#f8f9fa', '#ED145B'],
            title='Scores de Acurácia por Fold'
        )
        fig_cv.update_layout(
            height=300,
            showlegend=False,
            template='plotly_white',
            font=dict(family='Arial, sans-serif', size=11, color='#1a1a2e'),
            yaxis=dict(range=[0, 1])
        )
        st.plotly_chart(fig_cv, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-box">
        <h4>Resumo CV</h4>
        <p><strong>Média:</strong> {model_data['cv_scores'].mean():.1%}</p>
        <p><strong>Desvio Padrão:</strong> {model_data['cv_scores'].std():.1%}</p>
        <p><strong>Mín:</strong> {model_data['cv_scores'].min():.1%}</p>
        <p><strong>Máx:</strong> {model_data['cv_scores'].max():.1%}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Métricas Detalhadas")
    
    metrics_data = {
        'Métrica': ['Acurácia', 'Precisão', 'Recall', 'F1-Score', 'AUC-ROC'],
        'Valor': [
            f"{model_data['metrics']['accuracy']:.1%}",
            f"{model_data['metrics']['precision']:.1%}",
            f"{model_data['metrics']['recall']:.1%}",
            f"{model_data['metrics']['f1']:.1%}",
            f"{model_data['metrics']['auc']:.1%}"
        ]
    }
    st.dataframe(metrics_data, use_container_width=True, hide_index=True)

# ============================================================
# PÁGINA: REALIZAR PREVISÃO
# ============================================================

elif page == "Realizar Previsão":
    st.markdown('<div class="banner-fiap"><h2>Realizar Previsão Individual</h2></div>', unsafe_allow_html=True)
    
    st.markdown("Preencha os dados do aluno abaixo para obter uma previsão de risco de defasagem:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Indicadores PEDE")
        iaa = st.slider("IAA (Índice de Autoavaliação)", 0.0, 10.0, 5.0, 0.1)
        ieg = st.slider("IEG (Índice de Engajamento)", 0.0, 10.0, 5.0, 0.1)
        ips = st.slider("IPS (Índice Psicossocial)", 0.0, 10.0, 5.0, 0.1)
        ida = st.slider("IDA (Índice de Aprendizagem)", 0.0, 10.0, 5.0, 0.1)
        ipv = st.slider("IPV (Índice de Ponto de Virada)", 0.0, 10.0, 5.0, 0.1)
    
    with col2:
        st.markdown("#### Dados Adicionais")
        ian = st.slider("IAN (Índice de Aprendizagem Normalizado)", 0.0, 10.0, 5.0, 0.1)
        inde = st.slider("INDE (Índice de Desenvolvimento)", 0.0, 10.0, 5.0, 0.1)
        idade = st.slider("Idade (anos)", 10, 20, 15, 1)
        anos_pm = st.slider("Anos na Passos Mágicos", 1, 15, 5, 1)
        num_av = st.slider("Número de Avaliações", 5, 20, 10, 1)
    
    # Botão de previsão
    if st.button("🔮 Realizar Previsão", use_container_width=True):
        # Preparar dados para previsão
        input_data = np.array([[iaa, ieg, ips, ida, ipv, ian, inde, idade, num_av, anos_pm]])
        input_scaled = model_data['scaler'].transform(input_data)
        
        # Fazer previsão
        pred = model_data['model'].predict(input_scaled)[0]
        pred_proba = model_data['model'].predict_proba(input_scaled)[0]
        
        # Exibir resultado
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Perfil dos Indicadores")
            
            radar_data = {
                'Indicador': ['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'INDE'],
                'Valor': [iaa, ieg, ips, ida, ipv, ian, inde]
            }
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=[iaa, ieg, ips, ida, ipv, ian, inde],
                theta=['IAA', 'IEG', 'IPS', 'IDA', 'IPV', 'IAN', 'INDE'],
                fill='toself',
                name='Indicadores',
                line=dict(color='#ED145B'),
                fillcolor='rgba(237, 20, 91, 0.3)'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                height=400,
                template='plotly_white',
                font=dict(family='Arial, sans-serif', size=11, color='#1a1a2e')
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            st.markdown("#### Dados Adicionais")
            
            additional_data = {
                'Campo': ['Idade', 'Anos na PM', 'Nº Avaliações'],
                'Valor': [f'{idade} anos', f'{anos_pm} anos', f'{num_av}']
            }
            st.dataframe(additional_data, use_container_width=True, hide_index=True)
        
        # Resultado da previsão
        st.markdown("---")
        
        if pred == 1:
            st.markdown(f"""
            <div style="background: #d32f2f; border-radius: 10px; padding: 1.5rem; text-align: center; margin: 1rem 0;">
            <h3 style="color: #ffffff; margin: 0; font-size: 1.8rem;">⚠️ ALUNO EM RISCO</h3>
            <p style="color: #ffffff; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Probabilidade de Defasagem: <strong>{pred_proba[1]:.1%}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ Este aluno apresenta risco de defasagem. Recomenda-se intervenção pedagógica imediata.")
        else:
            st.markdown(f"""
            <div style="background: #2e7d32; border-radius: 10px; padding: 1.5rem; text-align: center; margin: 1rem 0;">
            <h3 style="color: #ffffff; margin: 0; font-size: 1.8rem;">✅ ALUNO SEM RISCO</h3>
            <p style="color: #ffffff; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Probabilidade de Defasagem: <strong>{pred_proba[1]:.1%}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Este aluno não apresenta risco aparente. Manter acompanhamento regular.")
