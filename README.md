# Livraria — Monolito Modular (Exercício 8.3)

MVP da livraria refatorado de MVC ([livraria-mvc](https://github.com/gabrielmarinhorosa/livraria-mvc))
para **monolito modular**. Os módulos seguem os microsserviços do diagrama do Exercício 8.2:
**Catálogo, Usuários, Estoque e Pagamento**, cada um com as camadas **Aplicação → Negócio → Dados**.

É uma aplicação só (um processo Flask, um deploy), mas organizada como se fossem serviços separados.

## Estrutura

```
livraria-monolito-modular/
├── app.py                 # ponto de entrada: registra os módulos (papel do API Gateway/BFF)
├── web.py                 # front-end: seções Catálogo, Carrinho e Compra
├── templates/index.html
└── modulos/
    ├── comum.py           # ErroNegocio (compartilhado)
    ├── catalogo/          # livros            (Items-DB)
    ├── usuarios/          # clientes          (User-DB)
    ├── estoque/           # quantidades       (Estoque-DB)
    └── pagamento/         # compras PIX/cartão (Pagamento-DB)
        ├── __init__.py    # INTERFACE PÚBLICA do módulo
        ├── aplicacao.py   # rotas REST (/api/pagamento/...)
        ├── negocio.py     # regras
        └── dados.py       # armazenamento (em memória)
```

## Regras do monolito modular

1. **Um "banco" por módulo**: cada `dados.py` guarda só os seus dados. O estoque, por exemplo,
   conhece apenas `livro_id` e quantidade; título e preço são do catálogo.
2. **Comunicação só pela interface pública**: um módulo usa outro apenas pelo `__init__.py`
   (`from modulos import catalogo` → `catalogo.obter_livro(id)`), nunca importando `negocio` ou `dados` direto.
3. **Pagamento orquestra**: na compra, ele confere o cliente (`usuarios`), busca o preço oficial
   (`catalogo`) e baixa o estoque (`estoque`).

Por causa dessas regras, cada módulo poderia virar um microsserviço depois: bastaria trocar
as chamadas de função por chamadas HTTP.

## API REST

| Módulo | Rotas |
|---|---|
| Catálogo | `GET/POST /api/catalogo/livros` |
| Usuários | `GET/POST /api/usuarios` |
| Estoque | `GET /api/estoque`, `GET/PUT /api/estoque/<livro_id>` |
| Pagamento | `GET/POST /api/pagamento/compras` |

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000

Testes: `pip install pytest && pytest`

## Deploy (Exercício 8.4)

Funciona em qualquer serviço Python (Render, Railway etc.):

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`

Os dados ficam em memória, então voltam ao estado inicial quando o servidor reinicia.
