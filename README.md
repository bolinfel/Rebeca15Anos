# 🔐 Roteiro: Implementação de Acessos Distintos

## 1. Segurança e Autenticação
* **Superuser:** Crie um usuário admin para a aniversariante via `python manage.py createsuperuser`.
* **Login:** Utilize a URL padrão de login do Django (`/accounts/login/`) para que ela se autentique.

## 2. A Página da Aniversariante (Dashboard)
* **Visualização de Dados:** Diferente da página do convidado, aqui você deve exibir:
    * Uma tabela com Nome, Telefone e E-mail de cada confirmado.
    * Uma lista de presentes indicando quem reservou cada item.
* **Filtros:** Adicione botões simples para filtrar quem "Confirmou" vs "Não vai".


## 3. A Página do Convidado (Front-end)
* **Filtro de Presentes:** Na página pública, a QuerySet deve ser: 
  `Presente.objects.filter(esta_reservado=False)`. 
  *Isso impede que um convidado veja o que já foi escolhido ou por quem.*
* **Privacidade:** Nunca exiba a lista de outros convidados na página pública.

## 4. Diferenciais de Robustez
* **Exportação para PDF/Excel:** Adicione um botão na Dashboard para a aniversariante baixar a lista de convidados para entregar ao buffet ou recepção.
* **Proteção de URL:** Certifique-se de que a URL `/dashboard/` redirecione para o login caso um convidado tente acessá-la manualmente.

# 🎨 Guia de Interface e Template Estático

Para uma visualização robusta, utilizaremos a técnica de **DRY (Don't Repeat Yourself)** com herança de templates.

## 1. Estrutura de Diretórios
```text
static/
├── css/
│   └── style.css
├── img/
│   └── background-aniversario.jpg
templates/
├── base.html              <-- Estrutura comum (Navbar, Footer, CSS)
└── convites/
    ├── home.html          <-- Formulário RSVP
    ├── lista_presentes.html
    └── dashboard.html     <-- Painel da Aniversariante