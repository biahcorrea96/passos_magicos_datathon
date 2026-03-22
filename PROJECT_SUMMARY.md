# 📋 Resumo do Projeto - Passos Mágicos

## 🎯 Visão Geral

**Nome**: Passos Mágicos - Modelo Preditivo de Risco de Defasagem Escolar  
**Versão**: 2.0.0  
**Data**: Março 2026  
**Status**: ✅ Pronto para Produção

## 📊 Integração XGBoost

Este projeto foi **atualizado para consumir a lógica do modelo XGBoost** do notebook `Tech_Challenge_5_Previsão_Defasagem___XGBoost(2).ipynb`, mantendo toda a **configuração visual original** do app Streamlit.

### Principais Mudanças

| Aspecto | Antes | Depois |
|--------|-------|--------|
| **Modelo** | XGBoost com 800 estimadores | XGBoost com 150 estimadores (otimizado) |
| **Features** | 20 features derivadas | 10 features principais (mais eficiente) |
| **Hiperparâmetros** | Customizados para o app | Do notebook (validado) |
| **Abordagem** | Não temporal | **Temporal** (prediz ano N+1 com dados do ano N) |
| **Data Leakage** | Possível | Eliminado |

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│   Dados (2022, 2023, 2024)              │
│   base_2022.xlsx, base_2023.xlsx, etc   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Carregamento e Processamento          │
│   - Limpeza de dados                    │
│   - Imputação (mediana)                 │
│   - Normalização (StandardScaler)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Modelo XGBoost                        │
│   - n_estimators: 150                   │
│   - max_depth: 4                        │
│   - learning_rate: 0.05                 │
│   - Validação cruzada 5-fold            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Interface Streamlit                   │
│   - 4 páginas interativas               │
│   - Visualizações Plotly                │
│   - Design FIAP (Rosa + Branco)         │
└─────────────────────────────────────────┘
```

## 📁 Estrutura de Arquivos

```
passos-magicos-app/
├── app.py                          # Aplicação principal (36KB)
├── requirements.txt                # Dependências
├── README.md                       # Documentação principal
├── CONTRIBUTING.md                 # Guia de contribuição
├── DEPLOYMENT.md                   # Guia de deploy
├── PROJECT_SUMMARY.md              # Este arquivo
├── .gitignore                      # Arquivos a ignorar no Git
├── .streamlit/
│   └── config.toml                # Configuração de tema
└── data/
    ├── base_2022.xlsx             # Dados 2022 (100 registros)
    ├── base_2023.xlsx             # Dados 2023 (120 registros)
    └── base_2024.xlsx             # Dados 2024 (140 registros)
```

## 🔑 Funcionalidades Principais

### 1️⃣ Informações do Sistema
- Contexto do projeto
- Benefícios e características
- Classificação de risco
- Indicadores PEDE
- Estatísticas da base de dados

### 2️⃣ Modelo Preditivo
- Pipeline de treinamento
- Métricas de desempenho
- Importância das features (gráfico interativo)
- Dados de treinamento

### 3️⃣ Validação do Modelo
- Matriz de confusão
- Curva ROC-AUC
- Validação cruzada 5-fold
- Comparação de métricas

### 4️⃣ Realizar Previsão
- Sliders para entrada de dados
- Previsão em tempo real
- Gráfico radar dos indicadores
- Detalhes da previsão

## 📊 Métricas de Desempenho

| Métrica | Valor | Descrição |
|---------|-------|-----------|
| **Acurácia** | ~82% | Proporção de previsões corretas |
| **Precisão** | ~82% | De alunos previstos em risco, quantos realmente estão |
| **Recall** | ~82% | De alunos em risco, quantos foram identificados |
| **F1-Score** | ~82% | Média harmônica entre precisão e recall |
| **AUC-ROC** | ~89% | Capacidade de discriminação do modelo |

## 🧠 Modelo XGBoost

### Hiperparâmetros
```python
n_estimators=150          # Número de árvores
max_depth=4               # Profundidade máxima
learning_rate=0.05        # Taxa de aprendizado
min_child_weight=5        # Peso mínimo de folha
subsample=0.8             # Fração de amostras por árvore
colsample_bytree=0.8      # Fração de features por árvore
reg_alpha=0.5             # Regularização L1
reg_lambda=1.0            # Regularização L2
scale_pos_weight=1        # Peso para classe positiva
```

### Features (10)
1. **IAA** - Índice de Autoavaliação
2. **IEG** - Índice de Engajamento
3. **IPS** - Índice Psicossocial
4. **IDA** - Índice de Aprendizagem
5. **IPV** - Índice de Ponto de Virada
6. **IAN** - Índice de Aprendizagem Normalizado
7. **INDE** - Índice de Desenvolvimento
8. **Idade** - Idade do aluno
9. **Num_Av** - Número de avaliações
10. **Anos_PM** - Anos na Passos Mágicos

### Target
- **0**: Sem Risco (Defasagem >= 0)
- **1**: Em Risco (Defasagem < 0)

## 🎨 Design Visual

### Paleta de Cores
- **Primária**: #ED145B (Rosa FIAP)
- **Secundária**: #c4114d (Rosa escuro)
- **Fundo**: #ffffff (Branco)
- **Texto**: #1a1a2e (Cinza escuro)
- **Sucesso**: #2e7d32 (Verde)
- **Erro**: #d32f2f (Vermelho)

### Componentes
- **Banner**: Gradiente rosa com texto branco
- **Cards**: Branco com borda cinza e sombra leve
- **Botões**: Interativos com feedback visual
- **Gráficos**: Plotly com cores coordenadas

## 🚀 Como Usar

### Instalação
```bash
git clone https://github.com/seu-usuario/passos-magicos-app.git
cd passos-magicos-app
pip install -r requirements.txt
```

### Execução
```bash
streamlit run app.py
```

### Acesso
```
http://localhost:8501
```

## 📈 Fluxo de Dados

1. **Carregamento**: Excel → Pandas DataFrame
2. **Limpeza**: Remoção de nulos e outliers
3. **Imputação**: Preenchimento com mediana
4. **Normalização**: StandardScaler
5. **Split**: 80% treino, 20% teste
6. **Treinamento**: XGBoost
7. **Validação**: 5-fold cross-validation
8. **Previsão**: Probabilidade + Classificação

## 🔄 Abordagem Temporal

### Problema Tradicional ❌
```
Ano N: Indicadores + Defasagem → Prever Defasagem (Ano N)
Resultado: Data Leakage! Não permite intervenção.
```

### Nossa Solução ✅
```
Ano N: Indicadores → Prever Defasagem (Ano N+1)
Resultado: Sem data leakage! Permite intervenção preventiva.
```

## 🔧 Customização

### Adicionar Novo Indicador
1. Adicione coluna ao Excel
2. Atualize `carregar_e_processar_dados()`
3. Inclua em `feature_cols`
4. Retreine o modelo

### Alterar Cores
Edite CSS em `app.py`:
```python
.banner-fiap {
    background: linear-gradient(135deg, #NOVA_COR 0%, #NOVA_COR_ESCURA 100%);
}
```

### Ajustar Hiperparâmetros
Modifique em `treinar_modelo_xgboost()`:
```python
model = XGBClassifier(
    n_estimators=200,  # Aumentar árvores
    max_depth=5,       # Aumentar profundidade
    learning_rate=0.1, # Aumentar taxa
    # ... outros parâmetros
)
```

## 📦 Dependências

| Pacote | Versão | Uso |
|--------|--------|-----|
| streamlit | ≥1.30.0 | Framework web |
| xgboost | ≥2.0.0 | Modelo ML |
| pandas | ≥2.0.0 | Manipulação de dados |
| scikit-learn | ≥1.3.0 | Preprocessing e métricas |
| plotly | ≥5.18.0 | Visualizações |
| numpy | ≥1.24.0 | Computação numérica |
| openpyxl | ≥3.1.0 | Leitura de Excel |

## 🧪 Testes

```bash
# Verificar sintaxe
python -m py_compile app.py

# Executar localmente
streamlit run app.py

# Acessar http://localhost:8501
```

## 🚀 Deploy

### Streamlit Cloud (Recomendado)
1. Push para GitHub
2. Acesse share.streamlit.io
3. Conecte repositório
4. Deploy automático

### Docker
```bash
docker build -t passos-magicos-app .
docker run -p 8501:8501 passos-magicos-app
```

### VPS/Servidor Linux
Ver `DEPLOYMENT.md` para instruções detalhadas

## 📞 Suporte

- **Issues**: Abra no GitHub
- **Documentação**: Veja README.md
- **Deploy**: Veja DEPLOYMENT.md
- **Contribuição**: Veja CONTRIBUTING.md

## 📝 Changelog

### v2.0.0 (Março 2026)
- ✨ Integração com modelo XGBoost do notebook
- 🎨 Mantém design visual original
- 📊 Abordagem temporal implementada
- 🔧 Otimização de hiperparâmetros
- 📚 Documentação completa

### v1.0.0 (Versão anterior)
- Versão inicial com modelo customizado

## 👥 Equipe

**Tech Challenge 5 - FIAP**  
Pós-Graduação em Data Analytics  
Em parceria com Associação Passos Mágicos

## 📄 Licença

Projeto educacional - Uso livre para fins de aprendizado

---

**Última atualização**: 22 de Março de 2026  
**Versão**: 2.0.0  
**Status**: ✅ Pronto para GitHub
