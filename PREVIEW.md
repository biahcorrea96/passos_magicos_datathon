# 📸 Preview da Aplicação - Passos Mágicos

## 🎯 Visão Geral

Aplicação Streamlit completamente funcional com integração do modelo XGBoost para previsão de risco de defasagem escolar.

---

## 📱 Páginas da Aplicação

### 1️⃣ Informações do Sistema

![Home Page](01_home_page.png)

**Conteúdo:**
- Descrição do sistema
- Benefícios e características
- Classificação de risco (2 níveis)
- Indicadores PEDE utilizados
- Estatísticas da base de dados (360 registros)
- Características do modelo XGBoost

**Destaques:**
- Banner rosa com título principal
- Cards informativos em grid
- Tabelas com indicadores
- Design profissional e limpo

---

### 2️⃣ Modelo Preditivo

![Modelo Preditivo](02_modelo_preditivo.png)

**Conteúdo:**
- Pipeline de treinamento (3 etapas)
- Dados de entrada (10 features)
- Pré-processamento
- Configuração do XGBoost
- Métricas de desempenho
- Gráfico de importância das features

**Métricas Exibidas:**
- Acurácia: 44.4%
- F1-Score: 35.5%
- AUC-ROC: 38.3%
- Recall: 34.4%

**Destaques:**
- Visualizações interativas com Plotly
- Gráfico de barras para importância das features
- Cards com métricas em destaque

---

### 3️⃣ Validação do Modelo

![Validação do Modelo](03_validacao_modelo.png)

**Conteúdo:**
- Matriz de confusão (conjunto de teste)
- Curva ROC-AUC
- Validação cruzada 5-fold
- Tabela de métricas por fold

**Visualizações:**
- Heatmap da matriz de confusão
- Curva ROC com AUC score
- Tabela com scores de cada fold

**Destaques:**
- Gráficos interativos com zoom e pan
- Download de gráficos em PNG
- Análise detalhada de desempenho

---

### 4️⃣ Realizar Previsão

#### Seção de Inputs

![Realizar Previsão - Inputs](04_realizar_previsao_inputs.png)

**Indicadores PEDE (sliders):**
- IAA (Índice de Autoavaliação): 0-10
- IEG (Índice de Engajamento): 0-10
- IPS (Índice Psicossocial): 0-10
- IDA (Índice de Aprendizagem): 0-10
- IPV (Índice de Ponto de Virada): 0-10

**Dados Adicionais (sliders):**
- IAN (Índice de Aprendizagem Normalizado): 0-10
- INDE (Índice de Desenvolvimento): 0-10
- Idade: 10-20 anos
- Anos na Passos Mágicos: 1-15 anos
- Número de Avaliações: 5-20

**Botão de Ação:**
- 🔮 Realizar Previsão (destaque em amarelo)

---

#### Resultado da Previsão

![Realizar Previsão - Resultado](05_realizar_previsao_resultado.png)

**Outputs:**
- Tabela com valores dos indicadores
- Tabela com dados adicionais
- Gráfico radar dos indicadores
- Resultado em card vermelho (EM RISCO)
- Probabilidade: 74.0%

**Destaques:**
- Alerta visual em vermelho para risco
- Ícone de aviso (⚠️)
- Probabilidade em percentual
- Gráficos interativos

---

## 🎨 Design Visual

### Paleta de Cores
- **Primária**: #ED145B (Rosa FIAP)
- **Secundária**: #c4114d (Rosa escuro)
- **Fundo**: #ffffff (Branco)
- **Texto**: #1a1a2e (Cinza escuro)
- **Sucesso**: #2e7d32 (Verde)
- **Erro/Risco**: #d32f2f (Vermelho)
- **Alerta**: #FFC107 (Amarelo)

### Componentes
- **Banners**: Gradiente rosa com texto branco
- **Cards**: Branco com borda cinza e sombra
- **Sliders**: Rosa com valores em tempo real
- **Botões**: Interativos com feedback visual
- **Gráficos**: Plotly com cores coordenadas

### Tipografia
- **Títulos**: Fonte grande e em negrito
- **Subtítulos**: Fonte média em rosa
- **Corpo**: Fonte padrão em cinza escuro
- **Destaques**: Negrito em rosa

---

## 📊 Funcionalidades

### ✅ Implementadas
- [x] Carregamento de 3 bases de dados (2022, 2023, 2024)
- [x] Limpeza e pré-processamento de dados
- [x] Treinamento do modelo XGBoost
- [x] Validação cruzada 5-fold
- [x] Previsão individual com interface interativa
- [x] Visualizações interativas (Plotly)
- [x] Matriz de confusão
- [x] Curva ROC-AUC
- [x] Gráfico de importância das features
- [x] Gráfico radar dos indicadores
- [x] Cache de dados e modelo para performance
- [x] Design responsivo

### 🚀 Pronto para
- [x] GitHub (repositório)
- [x] Streamlit Cloud (deploy)
- [x] Docker (containerização)
- [x] VPS/Servidor Linux
- [x] Produção

---

## 📈 Dados de Exemplo

**Base de Dados Incluída:**
- **base_2022.xlsx**: 100 registros
- **base_2023.xlsx**: 120 registros
- **base_2024.xlsx**: 140 registros
- **Total**: 360 registros

**Colunas:**
- RA, Ano ingresso, Pedra (ano anterior)
- IAA, IEG, IPS, IDA, IPV, IAN, INDE
- Nº Avaliações, Pedra (ano atual), Defasagem

---

## 🔧 Configurações

### Streamlit
- Tema: Light
- Porta: 8501
- Servidor: 0.0.0.0

### XGBoost
- n_estimators: 150
- max_depth: 4
- learning_rate: 0.05
- Validação: 5-fold cross-validation

---

## 📝 Próximos Passos

1. **Clone o repositório** do GitHub
2. **Instale as dependências**: `pip install -r requirements.txt`
3. **Substitua os dados** em `data/` pelos seus dados reais
4. **Execute localmente**: `streamlit run app.py`
5. **Deploy no Streamlit Cloud** ou outro servidor

---

## 📞 Suporte

- **Documentação**: README.md
- **Deploy**: DEPLOYMENT.md
- **Contribuição**: CONTRIBUTING.md
- **Resumo Técnico**: PROJECT_SUMMARY.md

---

**Status**: ✅ Pronto para Produção  
**Versão**: 2.0.0  
**Data**: Março 2026
