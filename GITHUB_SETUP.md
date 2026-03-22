# 🚀 Guia de Upload para GitHub

## Passo 1: Criar um Repositório no GitHub

1. Acesse [github.com](https://github.com)
2. Clique em **"New"** ou vá para [github.com/new](https://github.com/new)
3. Preencha os dados:
   - **Repository name**: `passos-magicos-app`
   - **Description**: `Modelo Preditivo de Risco de Defasagem Escolar - FIAP`
   - **Visibility**: Public (ou Private, conforme preferência)
   - **Initialize this repository with**: Deixe desmarcado (vamos fazer isso localmente)
4. Clique em **"Create repository"**

## Passo 2: Configurar Git Localmente

```bash
# Navegue até o diretório do projeto
cd passos-magicos-app

# Inicialize o repositório Git
git init

# Configure seu nome e email (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"

# Adicione todos os arquivos
git add .

# Faça o primeiro commit
git commit -m "Initial commit: XGBoost temporal model with real data and FIAP design"

# Renomeie a branch para 'main' (se necessário)
git branch -M main

# Adicione o repositório remoto (substitua seu-usuario)
git remote add origin https://github.com/seu-usuario/passos-magicos-app.git

# Faça o primeiro push
git push -u origin main
```

## Passo 3: Verificar no GitHub

1. Acesse seu repositório: `https://github.com/seu-usuario/passos-magicos-app`
2. Verifique se todos os arquivos foram enviados:
   - ✅ `app.py`
   - ✅ `requirements.txt`
   - ✅ `README.md`
   - ✅ `DEPLOYMENT.md`
   - ✅ `CONTRIBUTING.md`
   - ✅ `.gitignore`
   - ✅ `.streamlit/config.toml`
   - ✅ `data/` (com os 3 arquivos Excel)

## Passo 4: Deploy no Streamlit Cloud (Opcional)

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"New app"**
3. Selecione seu repositório GitHub
4. Configure:
   - **Repository**: seu-usuario/passos-magicos-app
   - **Branch**: main
   - **Main file path**: app.py
5. Clique em **"Deploy"**

A aplicação estará disponível em: `https://seu-usuario-passos-magicos-app.streamlit.app`

## Passo 5: Atualizações Futuras

Para fazer atualizações no código:

```bash
# Faça as alterações no código

# Adicione os arquivos modificados
git add .

# Faça um commit
git commit -m "Descrição das alterações"

# Faça push para o GitHub
git push origin main
```

O Streamlit Cloud atualizará automaticamente a aplicação!

## 📋 Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Git configurado localmente
- [ ] Todos os arquivos foram adicionados
- [ ] Primeiro commit foi feito
- [ ] Push para o GitHub foi bem-sucedido
- [ ] Arquivos aparecem no GitHub
- [ ] README.md está visível
- [ ] Deploy no Streamlit Cloud (opcional)

## 🔗 Links Úteis

- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://github.github.com/training-kit/downloads/github-git-cheat-sheet.pdf)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)

## ⚠️ Dicas Importantes

1. **Não commite dados sensíveis**: Senhas, chaves de API, etc.
2. **Use .gitignore**: Já está configurado no projeto
3. **Commits descritivos**: Use mensagens claras e objetivas
4. **Branches**: Para mudanças grandes, crie uma branch separada
5. **Pull Requests**: Para colaboração, use PRs

## 📞 Suporte

Se tiver dúvidas:
- Consulte a [documentação do GitHub](https://docs.github.com)
- Abra uma issue no repositório
- Procure por tutoriais no YouTube

---

**Boa sorte com seu repositório! 🎉**
