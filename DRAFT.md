django-placeholder
==================

Sim, mais um projeto para criação de placeholders (edição inline). A idéia do
django-placeholder é ser uma ferramenta simples e desaclopada usando o própio admin
sem precisar criar mais uma camada para seu software.

O uso padrão é feito apenas adicionando o "placehoder" ao INSTALLED_APPS e
usando suas template tags. Porém existem opções para aprimorar a edição em tempo rael.


Existe um projeto de exemplo no diretório example/ basta executar o comando runserver.
O usuário é admin e o password admin. Após executar o login na administração basta
visitar a home do projeto e apertar as teclas CTRL+SHIFT+X para editar os
placeholders.


Como funciona
----

Utilizando jquery e fancybox o placeholder busca elementos definidos como placeholder
na página caso o usuário esteja logado e tenha permissão de edição dos mmesmos
e então adiciona um botão que ativa o modo edição daquele elemento.  Ao clicar neste
botão a paǵina de edição do elemento no admin é aberta dentro da janela lightbox e após a edição
o elemento é recarregado.



Uso básico
----

1. Certifique-se de possuir jquery no seu projeto


2. Adiciona o css e js necessários usando a template com os includes:

{% include "placeholder/includes.html" %}

Esta template irá incluir primeiro o css e o logo depois o javascript. Caso prefira
incluir apenas o css use placeholder/includes/css.html e caso queira incluir apenas
o javascript use placeholder/includes/script.html


3. Adicione a templatetag no elemento relativo a instância do objeto (WAT?). Exemplo:

<div {% ph_instance_tagattrs post %}>
    <h4>{{ post.title }}</h4>
    {{ post.text|linebreaks }}
</div>

Esta templatetag irá retornar o atributo data-placeholder-instance com o JSON
necessário.


4. Estando autenticado como administrador (is_staff) e possuindo permissão de edição
para o objeto usado aperte ctrl+x para mostrar os elementos placeholders onde a
edição esta habilitada.


5. Clique no Botão, faça sua edição e feche a janela. Pronto.


Melhorando seu placeholder
----

Usando a classe PlaceholderAdmin para melhorar a visualização no popup e permitir
registrar formulários diferentes (Com fieldsets) para cada placeholder.

Criando um formulário customizado

EXAMPLE

Registrando este formulário customizado e seus fieldsets:

EXAMPLE

Usando na templatetag

EXAMPLE


Problemas que podem ocorrer
----


USO DE CACHE

Pode atrapalhar na inclusão e retorno da tag, solução é não realizar cache para
usuários logados ou caso seu sistema precise, não utilizar cache para usuários
logados que não tem acesso a admnistração

Usar o middleware que invalida o cache caso a chave __placeholder_bllblalbla
esteja na URL.
