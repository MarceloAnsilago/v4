# GeraSet

Aplicacao web para montar e baixar arquivos `.set` a partir dos grupos de parametros do EA.

## Stack escolhida

- `Flask`: backend e rotas da interface
- `Jinja2`: renderizacao dos formularios e preview do `.set`
- `pandas` e `openpyxl`: leitura de planilhas e tabelas de parametros
- `pydantic`: validacao de configuracoes
- `pytest`: testes automatizados

## Ambiente virtual

Criado em `.venv` com Python 3.11.

## Ativacao

```powershell
.venv\Scripts\Activate.ps1
```

## Instalar ou atualizar dependencias

```powershell
python -m pip install -r requirements.txt
```

## Proximos passos sugeridos

1. Consolidar presets por estrategia e validar compatibilidade com cada EA.
2. Adicionar testes automatizados para o fluxo unificado e o download final.
3. Expor importacao/exportacao por planilha sem perder o preview da interface.
4. Adicionar historico, presets nomeados e validacao de ranges.
