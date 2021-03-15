# JuliaBot
Um bot de discord feito em python utilizando a API [discord.py](https://github.com/Rapptz/discord.py) e totalmente personalizável.

Clique [aqui](https://discord.com/oauth2/authorize?client_id=483054181176049685&scope=bot) para adicionar a `JuliaBot` ao seu servidor.
# O que tem no bot?

- Sistema de economia.
- Rank do servidor baseado em quem possui mais `coins`.
- Eventos aleatórios para distribuir `coins`.
- Possibilidade de criar comandos personalizádos para o servidor.
- Bot totalmente personalizável.

# Comandos 
## Guia de parâmetros
| Simbolo | Descrição | Exemplo na tabela | Exemplo no comando |
|---------|-----------|---------|-----------------|
| * | Parâmetro obrigatório. | `<preço>`* | j!roulette 50 |
| º | Possivel mais de um. | `<pessoa>`º | j!mute @pessoa1 @pessoa2 @pessoa3 |
## Configurações 
| Comando | Descrição | Parâmetros |
|---------|-----------|------------|
|j!setprefix|Mude o prefixo de comandos do bot.|`<prefixo>`* |
|j!addcmd|Adicione um comando personalizado, utilize virgula para separar os parametros. [Ainda em teste!]|`<comando>`* `<mensagem>`* `<descrição>`* |
|j!delcmd|Delete um comando personalizado!|`<comando>`* |
|j!cmdchannel|Modifique o canal de comandos!|`<canal>` |
|j!eventchannel|Modifique o canal de eventos!|`<canal>` |
|j!event|Desative ou ative os eventos automaticos.|`<booleano>`* |
## Core 
| Comando | Descrição | Parâmetros |
|---------|-----------|------------|
|j!help|Listar todos os comandos e suas descrições.|`<comando>` |
|j!prefix|Retorna o prefixo do bot no servidor.||
|j!ping|Pong!||
|j!rememberme|O bot irá te notificar no dia desejado, relembrando sua mensagem!|`<tempo>`* |
|j!upchat|"Limpe" o chat do discord!||
## Depuração 
| Comando | Descrição | Parâmetros |
|---------|-----------|------------|
|j!exec|Executar um comando através do bot.|`<comando>`* `<parametros_do_comando>` |
## Economia 
| Comando | Descrição | Parâmetros |
|---------|-----------|------------|
|j!coins|Verificar os pontos.|`<pessoa>`º |
|j!rank|Top coins do servidor.||
|j!roulette|Roletar pontos.|`<coins>`* |
|j!setcoins|Definir os seus pontos, ou os dos usuarios marcados.|`<coins>`* `<pessoa>`º |
|j!addcoins|Adicionar pontos.|`<coins>`* `<pessoa>`º |
|j!subcoins|Remover pontos.|`<coins>`* `<pessoa>`º |
|j!shop|Loja de itens||
|j!additem|Adicionar um item a loja!|`<preço>`* `<item>`* |
|j!buy|Comprar um item.|`<id_do_item>`* |
|j!delitem|Deletar itens da loja.|`<id_do_item>`* |
## Diversão 
| Comando | Descrição | Parâmetros |
|---------|-----------|------------|
|j!spam|Spam de mensagens.|`<quantidade>`* `<texto>`* |
|j!say|Fazer o bot dizer algo.|`<texto>`* |
|j!fmute|Silenciar alguem por alguns segundos.|`<pessoa>`*º |
|j!duel|Duele contra alguem valendo coins!|`<coins>`* `<pessoa>`* |
## Moderação 
| Comando | Descrição | Parâmetros |
|---------|-----------|------------|
|j!mastermute|Silenciar alguem, sem limite de tempo.|`<segundos>`* `<pessoa>`*º |
|j!c_event|Criar um evento.|`<evento>`* |
