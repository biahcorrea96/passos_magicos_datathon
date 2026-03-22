# Guia de Deploy

Este documento fornece instruções para fazer deploy da aplicação em diferentes ambientes.

## 📋 Pré-requisitos

- Conta no Streamlit Cloud, Heroku, AWS ou plataforma de escolha
- Git instalado
- Repositório GitHub com o código

## 🚀 Deploy no Streamlit Cloud (Recomendado)

### Passo 1: Prepare o Repositório GitHub

```bash
# Certifique-se de que os arquivos estão no repositório
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Passo 2: Acesse Streamlit Cloud

1. Visite [share.streamlit.io](https://share.streamlit.io)
2. Clique em "New app"
3. Selecione seu repositório GitHub
4. Configure:
   - **Repository**: seu-usuario/passos-magicos-app
   - **Branch**: main
   - **Main file path**: app.py

### Passo 3: Deploy

Clique em "Deploy" e aguarde a aplicação ser iniciada. A URL será algo como:
```
https://seu-usuario-passos-magicos-app-xxxxx.streamlit.app
```

## 🐳 Deploy com Docker

### Passo 1: Crie um Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie requirements
COPY requirements.txt .

# Instale Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copie aplicação
COPY . .

# Exponha porta
EXPOSE 8501

# Comando para iniciar
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Passo 2: Build da imagem

```bash
docker build -t passos-magicos-app:latest .
```

### Passo 3: Execute localmente

```bash
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  passos-magicos-app:latest
```

### Passo 4: Deploy em produção

**AWS ECR:**
```bash
# Faça login no ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin xxxxx.dkr.ecr.us-east-1.amazonaws.com

# Tag da imagem
docker tag passos-magicos-app:latest xxxxx.dkr.ecr.us-east-1.amazonaws.com/passos-magicos-app:latest

# Push
docker push xxxxx.dkr.ecr.us-east-1.amazonaws.com/passos-magicos-app:latest
```

## ☁️ Deploy no Heroku

### Passo 1: Instale Heroku CLI

```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Passo 2: Crie um Procfile

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Passo 3: Crie um arquivo setup.sh

```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
" > ~/.streamlit/config.toml
```

### Passo 4: Deploy

```bash
# Login no Heroku
heroku login

# Crie um app
heroku create seu-app-name

# Configure variáveis de ambiente (se necessário)
heroku config:set VARIAVEL=valor

# Deploy
git push heroku main

# Abra a aplicação
heroku open
```

## 🔧 Deploy em Servidor Linux (VPS)

### Passo 1: SSH no servidor

```bash
ssh usuario@seu-servidor.com
```

### Passo 2: Clone o repositório

```bash
cd /home/usuario
git clone https://github.com/seu-usuario/passos-magicos-app.git
cd passos-magicos-app
```

### Passo 3: Configure o ambiente

```bash
# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### Passo 4: Configure Nginx como reverse proxy

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Passo 5: Configure systemd service

Crie `/etc/systemd/system/passos-magicos.service`:

```ini
[Unit]
Description=Passos Magicos Streamlit App
After=network.target

[Service]
Type=simple
User=usuario
WorkingDirectory=/home/usuario/passos-magicos-app
ExecStart=/home/usuario/passos-magicos-app/venv/bin/streamlit run app.py --server.port=8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Passo 6: Inicie o serviço

```bash
sudo systemctl daemon-reload
sudo systemctl enable passos-magicos
sudo systemctl start passos-magicos
```

## 📊 Monitoramento

### Logs do Streamlit Cloud
Acesse a aba "Logs" no painel do Streamlit Cloud

### Logs do Heroku
```bash
heroku logs --tail
```

### Logs do systemd
```bash
sudo journalctl -u passos-magicos -f
```

## 🔐 Segurança

### Variáveis de Ambiente
Nunca commit credenciais. Use variáveis de ambiente:

```python
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'default-value')
```

### HTTPS
- **Streamlit Cloud**: Automático
- **Heroku**: Automático
- **VPS**: Use Let's Encrypt com Certbot

```bash
sudo certbot certonly --nginx -d seu-dominio.com
```

### Firewall
```bash
# Apenas portas necessárias
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 🧪 Teste Antes de Deploy

```bash
# Teste local
streamlit run app.py

# Verifique se não há erros
python -m py_compile app.py

# Teste com dados de exemplo
# Acesse http://localhost:8501
```

## 📈 Performance

### Cache
O app já usa `@st.cache_data` e `@st.cache_resource` para otimizar performance.

### Otimizações Adicionais
```python
# Aumente timeout para dados grandes
@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_dados():
    pass
```

## 🆘 Troubleshooting

### Erro: "No such file or directory: 'data/base_2022.xlsx'"
- Certifique-se de que os arquivos estão na pasta `data/`
- Ou use caminhos absolutos

### Erro: "Out of memory"
- Reduza o tamanho do dataset
- Aumente a memória do servidor
- Use processamento em chunks

### App lento
- Ative cache
- Reduza frequência de retrainamento
- Use `@st.cache_resource` para o modelo

## 📞 Suporte

Para problemas de deploy, abra uma issue no repositório GitHub.

---

**Última atualização**: Março 2026
