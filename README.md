# Aurora Fit - Sistema de Gestão

Sistema web para gestão de studio de atividades físicas feminino.

## Tecnologias
- Python 3.11+
- Django 5.0
- PostgreSQL
- Mercado Pago

## Setup Local

1. Clone o repositório
2. Crie o ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate`
4. Instale dependências: `pip install -r requirements.txt`
5. Configure o .env
6. Rode as migrações: `python manage.py migrate`
7. Crie superusuário: `python manage.py createsuperuser`
8. Rode o servidor: `python manage.py runserver`

## Estrutura do Projeto
- `core/` - Páginas institucionais
- `accounts/` - Autenticação
- `students/` - Gestão de alunas
- `videos/` - Videoaulas e lives
- `payments/` - Pagamentos
- `dashboard_admin/` - Painel administrativo
- `branding/` - Customização de marca
