# Guia de Contribuição

Obrigado por considerar contribuir para o projeto Passos Mágicos! Este documento fornece diretrizes e instruções para contribuir.

## Como Contribuir

### Reportar Bugs

Antes de criar um relatório de bug, verifique a lista de issues, pois você pode descobrir que o erro já foi reportado. Ao criar um relatório de bug, inclua:

- **Título claro e descritivo**
- **Descrição exata do comportamento observado**
- **Comportamento esperado**
- **Passos para reproduzir o problema**
- **Exemplos específicos para demonstrar os passos**
- **Ambiente** (SO, versão Python, versão Streamlit)

### Sugerir Melhorias

Melhorias podem incluir novos recursos, melhorias de performance ou melhorias de documentação. Ao sugerir uma melhoria:

- Use um **título claro e descritivo**
- Forneça uma **descrição detalhada** da melhoria sugerida
- Liste **exemplos de como a melhoria funcionaria**
- Explique **por que essa melhoria seria útil**

### Pull Requests

- Preencha o template de PR fornecido
- Siga os padrões de código Python (PEP 8)
- Inclua testes apropriados
- Atualize a documentação conforme necessário
- Termine todos os arquivos com uma nova linha

## Padrões de Código

### Python
- Use **PEP 8** como guia de estilo
- Comprimento máximo de linha: **100 caracteres**
- Use **type hints** quando possível
- Adicione **docstrings** em funções públicas

Exemplo:
```python
def prever_risco(model: XGBClassifier, 
                 dados: pd.DataFrame) -> Tuple[float, str]:
    """
    Prediz o risco de defasagem para um aluno.
    
    Args:
        model: Modelo XGBoost treinado
        dados: DataFrame com features do aluno
        
    Returns:
        Tupla (probabilidade, classificação)
    """
    pass
```

### Commits
- Use mensagens de commit **claras e descritivas**
- Comece com um verbo no imperativo: "Add", "Fix", "Update", "Remove"
- Exemplos:
  - ✅ "Add validation for missing data"
  - ✅ "Fix bug in model training pipeline"
  - ❌ "Fixed stuff"
  - ❌ "Changes"

### Branches
- Use nomes descritivos: `feature/nome-da-feature`, `fix/nome-do-bug`
- Exemplos:
  - `feature/add-new-indicator`
  - `fix/data-loading-error`
  - `docs/update-readme`

## Processo de Desenvolvimento

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/passos-magicos-app.git`
3. **Crie uma branch** para sua feature: `git checkout -b feature/minha-feature`
4. **Faça as mudanças** e commit: `git commit -m "Add minha feature"`
5. **Push** para a branch: `git push origin feature/minha-feature`
6. **Abra um Pull Request** no repositório original

## Checklist para Pull Requests

- [ ] Meu código segue os padrões de estilo do projeto
- [ ] Executei testes localmente
- [ ] Adicionei testes para novas funcionalidades
- [ ] Atualizei a documentação conforme necessário
- [ ] Meus commits têm mensagens claras e descritivas
- [ ] Não há conflitos com a branch main

## Dúvidas?

Sinta-se livre para abrir uma issue com a tag `question` ou entrar em contato com os mantenedores.

---

Obrigado por contribuir! 🎉
