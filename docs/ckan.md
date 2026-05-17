# CKAN

'Veja como consultar uma api CKAN em  <https://docs.ckan.org/en/2.9/api/>`

## Dicas api CKAN

A api CKAN funciona por actions `/api/3/action/<nome_da_action>`. ASeguem alguns exemplos de actions possíveis:

### Packages

Gerenciam conjuntos de dados (o coração do CKAN)

- package_list <https://dadosabertos.tse.jus.br/api/3/action/package_list>
- package_show <https://dadosabertos.tse.jus.br/api/3/action/package_show?name_or_id=prestacao-de-contas-partidarias-2025>
- package_search

## Resoucres

Cada dataset pode ter vários arquivos (CSV, JSON, etc.)

- resource_show
- resource_update
- resource_delete
- resource_search

## Organizations

- organization_create
- organization_show
- organization_update
- organization_delete
- organization_list

## DataStore

```sh
curl https://dadosabertos.tse.jus.br/api/3/action/datastore_search \
  -d '{"resource_id": "7b097df8-6f06-44d3-8ed2-c4124d5b56c9", "limit": 5}'
```

## Exemplos de uso

- package_search → encontrar datasets <https://dadosabertos.tse.jus.br/api/3/action/package_search?q=2025>
- resource_show → identificar arquivos
- datastore_search → consultar dados estruturados

Para facilitar foi criado um CLI do projeto.
mais em `docs/cli.md`
