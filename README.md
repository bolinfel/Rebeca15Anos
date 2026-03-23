# Rebeca15Anos
# 📅 Plano de Projeto: RSVP & Lista de Presentes (Django)

Este roteiro foca na criação de uma aplicação intuitiva para o usuário final e robusta no backend para evitar conflitos de dados.

## 1. Modelagem de Dados (O Coração do Sistema)
Definir modelos claros para evitar redundância.
* **Model `Convidado`:** * Nome Completo, E-mail, Telefone.
    * Status (Confirmado/Não vai/Pendente).
    * Quantidade de acompanhantes (se aplicável).
* **Model `Presente`:**
    * Nome do item, Descrição, Link de referência (opcional).
    * Status (Disponível/Reservado).
    * Relacionamento (FK) com o `Convidado` que o reservou.

## 2. Interface do Usuário (UX/UI)
Dividir o site em três seções principais em uma "Single Page" ou fluxo linear:
* **Hero Section:** Informações vitais (Data, Horário, Local com link para Google Maps).
* **Formulário de RSVP:** Campo de busca ou seleção de nome + inputs de contato.
* **Vitrine de Presentes:** Cards visuais com botão "Escolher este".

## 3. Fluxo de Desenvolvimento (Passo a Passo)

### Fase A: Setup e Estrutura
1.  Iniciar o projeto e app (`convites`, `presentes`).
2.  Configurar `Static Files` e `Templates`.
3.  Criar os Models e rodar as Migrations.

### Fase B: Lógica de Negócio
1.  **Formulários:** Utilizar `Django Forms` para validação automática de e-mail e telefone.
2.  **Lógica de Reserva:** Criar uma View que, ao confirmar o presente, use um `transaction.atomic()` para garantir que duas pessoas não reservem o mesmo item simultaneamente.
3.  **Busca:** Implementar um filtro simples para o convidado achar seu nome na lista (caso você pré-cadastre os nomes).

### Fase C: Backend Administrativo
1.  Customizar o `admin.py` para exibir totais (Ex: "Total de Confirmados: 50").
2.  Adicionar filtros por status de confirmação e itens reservados.

### Fase D: Refinamento e Deploy
1.  **Responsividade:** Garantir que o formulário funcione bem no celular (onde 90% dos convidados acessarão).
2.  **Segurança:** Configurar `CSRF tokens` em todos os formulários.
3.  **Notificação (Opcional):** Configurar `django-environ` para disparar um e-mail automático de "Obrigado por confirmar".

## 4. Diferenciais de Robustez
* **Slug de Acesso:** Gerar uma URL única para cada convidado (ex: `/fulano-detal`) para evitar que estranhos acessem a lista.
* **Exportação:** Criar uma função no Admin para exportar a lista de confirmados em `.csv` ou `.xlsx`.