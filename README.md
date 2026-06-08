# GeraSet

Base inicial para uma versao web moderna do gerador de arquivos `.set`.

## Stack escolhida

- `FastAPI`: backend e API para gerar/validar sets
- `Streamlit`: interface web rapida para prototipacao e operacao
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

1. Criar um modulo para carregar templates de parametros do EA.
2. Gerar arquivos `.set` a partir de formulario web ou planilha.
3. Expor download do arquivo final pela interface.
4. Adicionar historico, presets e validacao de ranges.
