# Passos Mágicos - Modelo Preditivo de Risco de Defasagem Escolar

Aplicação desenvolvida para o **Tech Challenge Fase 5** da Pós-Graduação em Data Analytics da FIAP, em parceria com a **Associação Passos Mágicos**.

## Objetivo

Desenvolver um **modelo preditivo de machine learning** utilizando **XGBoost** para identificar alunos em risco de defasagem escolar, permitindo intervenção pedagógica preventiva com base em indicadores de desempenho.

## Características Principais

### Modelo Preditivo
- **Algoritmo**: XGBoost (Gradient Boosting)
- **Abordagem**: Temporal (prediz defasagem do ano N+1 usando dados do ano N)
- **Acurácia**: ~82% no conjunto de teste
- **Features**: 10 indicadores principais (IAA, IEG, IPS, IDA, IPV, IAN, INDE, Idade, Anos na PM, Nº Avaliações)

### Interface Streamlit
- **Dashboard Interativo**: Visualizações em tempo real com Plotly
- **4 Seções Principais**:
  1. **Informações do Sistema**: Contexto, benefícios e documentação
  2. **Modelo Preditivo**: Arquitetura, pipeline e métricas de desempenho
  3. **Validação do Modelo**: Matriz de confusão, curva ROC e validação cruzada
  4. **Realizar Previsão**: Interface para previsão individual com gráficos interativos

### Design Visual
- **Paleta FIAP**: Cores corporativas (Rosa #ED145B, branco, cinza)
- **Tema Claro**: Interface profissional e acessível
- **Responsivo**: Funciona em desktop e mobile

## Requisitos

- Python 3.8+
- Streamlit 1.30.0+
- XGBoost 2.0.0+
- Pandas 2.0.0+
- Scikit-learn 1.3.0+
- Plotly 5.18.0+
- NumPy 1.24.0+
- OpenPyXL 3.1.0+ (para leitura de arquivos Excel)

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/passos-magicos-app.git
cd passos-magicos-app
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Prepare os dados
Coloque os arquivos Excel na pasta `data/`:
- `base_2022.xlsx`
- `base_2023.xlsx`
- `base_2024.xlsx`

**Estrutura esperada das colunas:**
```
RA, Ano ingresso, Pedra [ano anterior], IAA, IEG, IPS, IDA, IPV, 
IAN, INDE [ano], Nº Av, Pedra [ano atual], Defasagem/Defas
```

## Como Executar

```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

## Estrutura do Projeto

```
passos-magicos-app/
├── app.py                      # Aplicação principal Streamlit
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
├── .streamlit/
│   └── config.toml            # Configuração de tema e servidor
└── data/
    ├── base_2022.xlsx         # Dados PEDE 2022
    ├── base_2023.xlsx         # Dados PEDE 2023
    └── base_2024.xlsx         # Dados PEDE 2024
```

## Indicadores PEDE Utilizados

| Indicador | Descrição | Escala |
|-----------|-----------|--------|
| **IAA** | Índice de Autoavaliação | 0 a 10 |
| **IEG** | Índice de Engajamento | 0 a 10 |
| **IPS** | Índice Psicossocial | 0 a 10 |
| **IDA** | Índice de Aprendizagem | 0 a 10 |
| **IPV** | Índice de Ponto de Virada | 0 a 10 |
| **IAN** | Índice de Aprendizagem Normalizado | 0 a 10 |
| **INDE** | Índice de Desenvolvimento | 0 a 10 |

## Arquitetura do Modelo

### Pipeline de Treinamento

1. **Carregamento de Dados**: Leitura de 3 bases (2022, 2023, 2024)
2. **Limpeza**: Remoção de registros com todos os indicadores vazios
3. **Imputação**: Preenchimento de valores faltantes com mediana
4. **Normalização**: StandardScaler para padronização
5. **Split**: 80% treino, 20% teste (estratificado)
6. **Treinamento**: XGBoost com hiperparâmetros otimizados
7. **Validação**: 5-fold cross-validation

### Hiperparâmetros XGBoost

```python
XGBClassifier(
    n_estimators=150,
    max_depth=4,
    learning_rate=0.05,
    min_child_weight=5,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.5,
    reg_lambda=1.0,
    scale_pos_weight=1,
    random_state=42,
    eval_metric='logloss'
)
```

## Métricas de Desempenho

| Métrica | Valor |
|---------|-------|
| Acurácia | ~82% |
| Precisão | ~82% |
| Recall | ~82% |
| F1-Score | ~82% |
| AUC-ROC | ~89% |

## 🔍 Abordagem Temporal

**Diferencial desta solução:**

- **Problema Tradicional**: Prever defasagem usando indicadores do mesmo ano → Data Leakage
- **Nossa Solução**: Prever defasagem do ano N+1 usando dados do ano N → Sem data leakage + Intervenção preventiva

Isso permite:
- ✅ Uso seguro de IAN e INDE como features
- ✅ Intervenção **antes** que o problema aconteça
- ✅ Eliminação completa de vazamento de dados

## Interface do Usuário

### Página de Informações
- Contexto do projeto
- Benefícios do sistema
- Classificação de risco
- Indicadores PEDE
- Base de dados utilizada

### Página do Modelo
- Pipeline de treinamento
- Métricas de desempenho
- Importância das features
- Dados de treinamento

### Página de Validação
- Matriz de confusão
- Curva ROC-AUC
- Validação cruzada 5-fold

### Página de Previsão
- Sliders para entrada de dados
- Previsão em tempo real
- Visualização em gráfico radar
- Indicador de dados incompletos

## Customização

### Alterar Cores da Paleta
Edite as cores CSS no arquivo `app.py`:
```python
# Busque por "primaryColor" e "backgroundColor" no CSS
.banner-fiap {
    background: linear-gradient(135deg, #ED145B 0%, #c4114d 100%);
}
```

### Adicionar Novos Indicadores
1. Adicione as colunas aos arquivos Excel
2. Atualize a função `carregar_e_processar_dados()` em `app.py`
3. Inclua o novo indicador na lista `feature_cols`

### Treinar com Novos Dados
Simplesmente substitua os arquivos em `data/` e reinicie a aplicação. O modelo será retreinado automaticamente.

## Notas Importantes

- O modelo é retreinado **toda vez que a aplicação é iniciada** (cache com `@st.cache_resource`)
- Os dados são carregados em cache para melhor performance
- A validação cruzada é executada automaticamente durante o treinamento
- Dados incompletos (3+ indicadores faltando) recebem classificação automática de risco alto

## 🚀 Deploy

### Streamlit Cloud
```bash
# 1. Push para GitHub
git push origin main

# 2. Acesse https://share.streamlit.io
# 3. Conecte seu repositório GitHub
# 4. Configure o arquivo principal como app.py
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## Referências

- [Documentação XGBoost](https://xgboost.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Plotly](https://plotly.com/)

## Equipe de Desenvolvimento

Projeto desenvolvido como parte do **Tech Challenge 5** da Pós-Graduação em Data Analytics da **FIAP**, em parceria com a **Associação Passos Mágicos**.

## Licença

Este projeto é fornecido como está para fins educacionais.

## Suporte

Para dúvidas ou sugestões, abra uma issue no repositório GitHub.

---

**Versão**: 2.0.0  
**Última atualização**: Março 2026  
**Status**: ✅ Produção
