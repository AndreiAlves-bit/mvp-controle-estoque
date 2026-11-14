
# MVP — Controle de Estoque

Sistema web desenvolvido como projeto acadêmico para gerenciamento de estoque e registro de vendas.

## Objetivo

Facilitar o controle de produtos, o acompanhamento das quantidades disponíveis e o registro de entradas e vendas, reduzindo erros no controle manual do estoque.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- HTML5
- CSS3
- JavaScript

## Funcionalidades

- Interface web responsiva.
- Acesso demonstrativo ao sistema.
- Cadastro de produtos pela API.
- Consulta de produtos cadastrados.
- Registro de entradas no estoque.
- Registro de vendas com baixa automática.
- Atualização das quantidades no banco de dados.
- Validação de estoque insuficiente.
- Identificação de produtos com estoque baixo.
- Registro de movimentações de estoque.

## Estrutura do projeto

- `app.py`: inicialização da aplicação Flask.
- `extensions.py`: configuração do SQLAlchemy.
- `models/`: modelos do banco de dados.
- `routes/`: rotas da API.
- `templates/`: interface HTML.
- `static/`: arquivos CSS e JavaScript.
- `requirements.txt`: dependências Python.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/AndreiAlves-bit/mvp-controle-estoque.git
```

### 2. Entrar na pasta

```bash
cd mvp-controle-estoque
```

### 3. Criar o ambiente virtual

No Windows:

```powershell
py -m venv .venv
```

### 4. Ativar o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```powershell
py -m pip install -r requirements.txt
```

### 6. Iniciar o sistema

```powershell
py app.py
```

### 7. Acessar pelo navegador

http://127.0.0.1:5000

## Acesso demonstrativo

E-mail: `usuario@exemplo.com`

Senha: `demonstracao`

**Observação:** o login é demonstrativo e não constitui autenticação de produção.

## Banco de dados

O sistema utiliza SQLite para armazenar produtos, vendas e movimentações de estoque.

O banco de dados local é criado automaticamente ao iniciar a aplicação.

## Limitações da versão atual

- Login demonstrativo.
- Cadastro de produtos disponível pela API.
- Aplicação executada localmente.
- Banco SQLite utilizado nesta versão do MVP.

## Repositório

https://github.com/AndreiAlves-bit/mvp-controle-estoque
