# Telegram Bot para sortear Amigo Oculto.

# A ideia:

Criar um bot capaz de sortear um amigo oculto de forma mais simples, apenas um participante necessita interagir com o bot.

# Como funciona:

Um dos amigos inicia a conversa com o bot
 
Envia o nome e o email de cada amigo com o  comando `/add` amigo amigo@example.com

A qualquer momento é possível verificar todos os participantes e os respectivos emails com o comando `/lista`

Em seguida executa o comando `/sorteio`

O bot informa quais são os nomes que foram incluidos na lista para sorteio
 
O usuário confirma se estão todos os amigos que deseja e em seguida executa o comando `/enviar`

Em caso de um particpante ter sido incluído incorretamente pode removê-lo com o comando `/apagar`+ nome

Todos os amigos são informados por email com o resultado de qual participante deverá presentear.
O bot por fim apaga toda a lista de nomes e e-mails inseridos.
