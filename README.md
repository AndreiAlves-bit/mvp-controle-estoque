# MVP — Controle de Estoque

Sistema web desenvolvido como projeto acadêmico do curso de Ciência da Computação da Universidade Cruzeiro do Sul, com o objetivo de facilitar o gerenciamento de produtos, o controle de estoque e o registro de movimentações comerciais.

## Objetivo

Desenvolver uma solução simples e acessível para auxiliar pequenos comércios no controle de seus produtos, permitindo acompanhar quantidades disponíveis, registrar entradas e vendas e identificar itens que precisam de reposição.

O projeto busca reduzir erros associados ao controle manual de estoque e facilitar a organização das informações.

## Sistema publicado

O MVP está disponível online:

**https://mvp-controle-estoque.onrender.com**

A aplicação está hospedada no Render e utiliza PostgreSQL para persistência dos dados em produção.

O acesso às funcionalidades de gerenciamento exige autenticação.

## Tecnologias utilizadas

**Backend**
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Werkzeug
- Gunicorn

**Frontend**
- HTML5
- CSS3
- JavaScript

**Banco de dados**
- SQLite — desenvolvimento local
- PostgreSQL (Supabase) — ambiente de produção

**Hospedagem e versionamento**
- Render — hospedagem da aplicação
- GitHub — versionamento do código
- UptimeRobot — monitoramento de disponibilidade

## Funcionalidades implementadas

### HU01 — Cadastro de produtos

- Cadastro de novos produtos.
- Registro de nome, descrição, preço, quantidade inicial e estoque mínimo.
- Validação dos dados informados.
- Armazenamento das informações no banco de dados.

### HU02 — Movimentação de estoque

- Registro de entradas de produtos.
- Atualização automática das quantidades disponíveis.
- Registro das movimentações no banco de dados.
- Exibição do saldo atualizado após cada operação.

### HU03 — Registro de vendas

- Registro de vendas de produtos.
- Baixa automática das quantidades vendidas.
- Verificação de estoque insuficiente.
- Armazenamento das informações da venda.

### Consulta e reposição

- Consulta das quantidades disponíveis.
- Identificação dos produtos com quantidade igual ou inferior ao estoque mínimo.
- Exibição de alertas de reposição.
- Atualização dos dados após as movimentações.

### Interface

- Layout responsivo.
- Menu principal com quatro funcionalidades.
- Modo claro e modo escuro.
- Mensagens de sucesso e erro.
- Campos identificados por rótulos.
- Indicadores visuais de estoque baixo.

## Autenticação e segurança

O sistema implementa mecanismos de proteção para restringir o acesso às funcionalidades de gerenciamento.

Entre os recursos utilizados estão:

- Autenticação com Flask-Login.
- Senhas armazenadas com hash utilizando scrypt.
- Proteção de rotas com `login_required`.
- Gerenciamento de sessões autenticadas.
- Cookies configurados com `HttpOnly` e `SameSite=Lax`.
- Cookies `Secure` no ambiente Render.
- Proteção contra CSRF utilizando Flask-WTF.
- Chave de segurança configurada por variável de ambiente.
- Validação de dados recebidos pela API.

Foram realizados testes funcionais e verificações de acesso não autorizado, incluindo a rejeição de requisições sem token CSRF válido.

Esses mecanismos representam medidas básicas de segurança para o MVP, não substituindo uma auditoria completa.

## Estrutura do projeto

```text
mvp-controle-estoque/
├── app.py
├── extensions.py
├── criar_admin.py
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── produto.py
│   ├── venda.py
│   ├── movimentacao.py
│   └── usuario.py
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── produto_routes.py
│   └── movimentacao_routes.py
├── templates/
│   └── index.html
├── static/
└── tests/
```

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/AndreiAlves-bit/mvp-controle-estoque.git
```

### 2. Entrar na pasta do projeto

```bash
cd mvp-controle-estoque
```

### 3. Criar o ambiente virtual

No Windows:

```powershell
py -m venv .venv
```

### 4. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```powershell
py -m pip install -r requirements.txt
```

### 6. Configurar as variáveis de ambiente

O sistema utiliza variáveis de ambiente para configurações sensíveis.

Principais variáveis:

- `SECRET_KEY`: chave secreta utilizada pelo Flask.
- `DATABASE_URL`: endereço de conexão com o banco de dados.
- `ADMIN_EMAIL`: e-mail do administrador, quando utilizado pela rotina de criação.
- `ADMIN_PASSWORD`: senha inicial do administrador, quando utilizada pela rotina de criação.

A variável `DATABASE_URL` é opcional no desenvolvimento local, pois a aplicação possui SQLite como configuração alternativa.

As credenciais reais não devem ser publicadas no repositório.

### 7. Iniciar a aplicação

```powershell
py app.py
```

### 8. Acessar pelo navegador

```text
http://127.0.0.1:5000
```

Para utilizar as funcionalidades protegidas, é necessário possuir um usuário cadastrado no banco de dados.

## Banco de dados

O sistema utiliza SQLAlchemy para o gerenciamento das entidades e a persistência das informações.

Principais entidades:

- **Produto:** informações dos itens cadastrados.
- **Venda:** registro das operações de venda.
- **ItemVenda:** associação entre vendas e produtos.
- **MovimentacaoEstoque:** histórico de entradas e saídas.
- **Usuario:** informações dos usuários autenticados.

Durante o desenvolvimento local, a aplicação pode utilizar SQLite.

No ambiente de produção, utiliza PostgreSQL hospedado no Supabase.

## Testes realizados

Foram realizados testes das principais funcionalidades:

- Login e logout.
- Cadastro de produtos.
- Registro de entradas.
- Registro de vendas.
- Atualização do saldo disponível.
- Identificação de produtos que precisam de reposição.
- Bloqueio de acesso a rotas protegidas sem autenticação.
- Envio de tokens CSRF nas requisições.
- Rejeição de requisições sem token CSRF válido.

Os testes funcionais executados na aplicação publicada apresentaram resultados satisfatórios.

## Limitações do MVP

Por se tratar de um Produto Mínimo Viável, o sistema possui escopo reduzido.

Entre as funcionalidades não contempladas nesta versão estão:

- Relatórios financeiros avançados.
- Controle de múltiplas filiais.
- Integração com sistemas fiscais.
- Leitura de códigos de barras.
- Gerenciamento avançado de permissões de usuários.
- Painéis analíticos detalhados.

Esses recursos poderão ser considerados em versões futuras.

## Repositório

https://github.com/AndreiAlves-bit/mvp-controle-estoque

## Autor

Andrei da Silva Alves

Curso: Ciência da Computação

Instituição: Universidade Cruzeiro do Sul

Projeto acadêmico — 2026.
