# JuliaBot
Um bot de discord feito em python utilizando a API [discord.py](https://github.com/Rapptz/discord.py) e totalmente personalizável.

Clique [aqui](https://discord.com/oauth2/authorize?client_id=483054181176049685&scope=bot) para adicionar a `JuliaBot` ao seu servidor.
# O que tem no bot?

- Sistema de economia.
- Rank do servidor baseado em quem possui mais `coins`.
- Eventos aleatórios para distribuir `coins`.
- Possibilidade de criar comandos personalizádos para o servidor.
- Notificar episódios novos de animes.
- Bot totalmente personalizável.

# Comandos 
## Guia de parâmetros
| Simbolo | Descrição | Exemplo na tabela | Exemplo no comando |
|---------|-----------|---------|-----------------|
| * | Parâmetro obrigatório. | `<preço>`* | j!roulette 50 |
| º | Possivel mais de um. | `<pessoa>`º | j!coins @pessoa1 @pessoa2 @pessoa3 |
## Animes 
| Comando | Descrição | Parâmetros | Permissão |
|---------|-----------|------------|-----------|
|j!animechannel|Define o canal de notificações de novos episódios de animes.|`<canal>`* |Admin.|
|j!add_anime|Marque um anime para você ser notificado quando lancar episódio novo.|`<anime>`* |Livre.|
|j!del_anime|Remova um anime da sua lista de notificações.|`<anime>`* |Livre.|
|j!anime_info|Informações sobre um anime.|`<anime>`* |Livre.|
|j!character|Informações sobre um personagem.|`<char>`* |Livre.|
|j!anime_list|Liste todos os animes da sua lista, ou da pessoa mensionada.||Livre.|
## Configurações 
| Comando | Descrição | Parâmetros | Permissão |
|---------|-----------|------------|-----------|
|j!setprefix|Mude o prefixo de comandos do bot.|`<prefixo>`* |Admin.|
|j!addcommand|Adicione um comando personalizado, utilize virgula para separar os parametros. [Ainda em teste!]|`<comando>`* `<mensagem>`* `<descrição>`* |Admin.|
|j!delcommand|Delete um comando personalizado!|`<comando>`* |Admin.|
|j!cmdchannel|Modifique o canal de comandos!|`<canal>` |Admin.|
|j!eventchannel|Modifique o canal de eventos!|`<canal>` |Admin.|
|j!event|Desative ou ative os eventos automaticos.|`<booleano>`* |Admin.|
## Core 
| Comando | Descrição | Parâmetros | Permissão |
|---------|-----------|------------|-----------|
|j!help|Listar todos os comandos e suas descrições.|`<comando>` |Livre.|
|j!prefix|Retorna o prefixo do bot no servidor.||Livre.|
|j!ping|Retorna a latência do bot.||Livre.|
|j!remindme|O bot irá te notificar no dia desejado, relembrando sua mensagem!|`<tempo>`* |Livre.|
|j!upchat|"Limpe" o chat do discord!||Admin.|
## Depuração 
| Comando | Descrição | Parâmetros | Permissão |
|---------|-----------|------------|-----------|
|j!exec|Executar um comando através do bot.|`<comando>`* `<parametros_do_comando>` |Depuração.|
|j!get_all_scripts|Listar todos os scripts rodando.||Depuração.|
|j!get_allowed_bots|Listar todos os bots permitidos.||Depuração.|
|j!add_allowed_bot|Permitir com que um bot especifico seja respondido.|`<bot_id>`* |Depuração.|
|j!del_allowed_bot|Remover um bot especifico da lista de bots permitidos.|`<bot_id>`* |Depuração.|
## Economia 
| Comando | Descrição | Parâmetros | Permissão |
|---------|-----------|------------|-----------|
|j!coins|Verificar os pontos.|`<pessoa>`º |Livre.|
|j!rank|Top coins do servidor.||Livre.|
|j!roulette|Roletar pontos.|`<coins>`* |Livre.|
|j!shop|Loja de itens.||Livre.|
|j!iteminfo|Veja as informações de um item da loja.|`<id_do_item>`* |Livre.|
|j!buy|Comprar um item.|`<id_do_item>`* |Livre.|
|j!distance|Calcula a diferença de coins entre você e outra pessoa.|`<pessoa>`* |Livre.|
## Diversão 
| Comando | Descrição | Parâmetros | Permissão |
|---------|-----------|------------|-----------|
|j!say|Fazer o bot dizer algo.|`<texto>`* |Livre.|
|j!duel|Duele contra alguem valendo coins!|`<coins>`* `<pessoa>`* |Livre.|
## Moderação 
| Comando | Descrição | Parâmetros | Permissão |
|---------|-----------|------------|-----------|
|j!c_event|Criar um evento.|`<evento>`* |Admin.|
|j!clean_events|Limpar todos os eventos.||Admin.|
|j!setcoins|Definir os seus pontos, ou os dos usuarios marcados.|`<coins>`* `<pessoa>`º |Admin.|
|j!addcoins|Adicionar pontos.|`<coins>`* `<pessoa>`º |Admin.|
|j!subcoins|Remover pontos.|`<coins>`* `<pessoa>`º |Admin.|
|j!additem|Adicionar um item a loja.|`<preço>`* `<item>`* |Admin.|
|j!delitem|Deletar itens da loja.|`<id_do_item>`* |Admin.|
