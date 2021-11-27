from random import randint
import discord
import modules.database as db
import modules.entity as entity


category = 'Configurações'
entity.Command.newcategory(category, ':gear:Configurações.')


async def setprefix(message, commandpar, bot):
    if commandpar != None:
        cont = commandpar.split()
        prefix = cont[0]
        db.editserver(message.guild.id, bot.db_connection, 'prefix', prefix)
        await message.channel.send(f'Prefixo de comandos mudado para `{prefix}`')

    else:
        raise entity.CommandError('Falta os parametros do comando!')
entity.Command(name='setprefix', func=setprefix , category=category, desc=f'Mude o prefixo de comandos do bot.', aliases=['definirprefixo', 'defprefixo'], args=[['prefixo', '*']], perm=1)


async def addcmd(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    if len(commandpar.split(',')) != 3:
        raise entity.CommandError('Parametros invalidos!')

    commandpar = commandpar.split(',')

    if ' ' in commandpar[0] or ':' in commandpar[0]:
        raise entity.CommandError('O nome do comando não pode conter nenhum espaço ou dois pontos ":".')

    if entity.Command.getcommand(message.guild.id, commandpar[0], bot.db_connection) != None:
        raise entity.CommandError('Um comando com esse nome ja existe!')

    db.addcommand(message.guild.id, bot.db_connection, commandpar[0], commandpar[1], commandpar[2])

    emb = discord.Embed(title='Novo Comando:', description=commandpar[0], color=bot.color)

    emb.add_field(name='Mensagem:', value=commandpar[1], inline=False)
    emb.add_field(name='Descrição:', value=commandpar[2], inline=False)


    await message.channel.send(embed=emb)
entity.Command(name='addcommand', func=addcmd, category=category, desc=f'Adicione um comando personalizado, utilize virgula para separar os parametros. [Ainda em teste!]', aliases=['addcmd', 'addcomando', 'adicionarcomando'], args=[['comando', '*'], ['mensagem', '*'], ['descrição', '*']], perm=1)


async def delcmd(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    cmd = entity.Command.getcommand(message.guild.id, commandpar, bot.db_connection)
    if cmd == None:
        raise entity.CommandError(f'O comando com o nome `{commandpar}` não existe!')

    if cmd['overwritten'] == 0:
        await message.channel.send(f'O comando `{commandpar}` é um comando próprio da {bot.user.mention}, ele não pode ser deletado!')
    else:
        db.delcommand(message.guild.id, bot.db_connection, commandpar)
        await message.channel.send(f'O comando `{commandpar}` foi deletado com sucesso!')
entity.Command(name='delcommand', func=delcmd, category=category, desc=f'Delete um comando personalizado!', aliases=['delcmd', 'deletecommand', 'deletarcomando', 'delcomando'], args=[['comando', '*']], perm=1)


async def commandchannel(message, commandpar, bot):
    if commandpar == None:
        server = db.getserver(message.guild.id, bot.db_connection)
        channel = server['commandchannel']
        prefix = server['prefix']

        if channel == None:
            await message.channel.send(f'O servidor `{message.guild}` permite comandos em qualquer canal!\n' +
            f'Para mudar o canal de comandos, utilize `{prefix}cmdchannel #canal` ou `{prefix}cmdchannel .` para poder utilizar comandos em todos os canais.')
        else:
            channel = bot.get_channel(int(channel))
            await message.channel.send(f'Canal de comandos: <#{channel.id}>\n' +
            f'Para mudar o canal de comandos, utilize `{prefix}cmdchannel #canal` ou `{prefix}cmdchannel .` para poder utilizar comandos em todos os canais.'
            )
    else:
        if commandpar == '.':
            db.editserver(message.guild.id, bot.db_connection, 'commandchannel', None)
            await message.channel.send(f'Comandos agora podem ser utilizados em `qualquer` canal.')

        else:
            channel = commandpar
            rep = ['<','#','>']
            for r in rep:
                channel = channel.replace(r, '')

            try:
                channel = bot.get_channel(int(channel))
            except:
               raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com `#` para selecionar o canal desejado.')

            if channel == None:
                raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com `#` para selecionar o canal desejado.')
            
            db.editserver(message.guild.id, bot.db_connection, 'commandchannel', str(channel.id))
            await message.channel.send(f'O canal de comandos foi definido para `<#{channel.id}>`')
entity.Command(name='cmdchannel', func=commandchannel, category=category, desc=f'Modifique o canal de comandos!', aliases=['commandchannel', 'cmdcanal', 'canaldecomandos'], args=[['canal', '']], perm=1)


async def eventchannel(message, commandpar, bot):
    if commandpar == None:
        server = db.getserver(message.guild.id, bot.db_connection)
        channel = server['eventchannel']
        prefix = server['prefix']

        if channel == None:
            await message.channel.send(f'O servidor `{message.guild}` permite que apareca eventos em qualquer canal!\n' +
            f'Para mudar o canal de eventos, utilize `{prefix}eventchannel #canal` ou `{prefix}eventchannel .` para aparecer eventos em `qualquer` canal.')
        else:
            channel = bot.get_channel(int(channel))
            await message.channel.send(f'Canal de eventos: <#{channel.id}>\n' +
            f'Para mudar o canal de eventos, utilize [{prefix}eventchannel #canal] ou [{prefix}eventchannel .] para aparecer eventos em `qualquer` canal.')
    else:
        if commandpar == '.':
            db.editserver(message.guild.id, bot.db_connection, 'eventchannel', None)
            await message.channel.send(f'Eventos agora podem aparecer em `qualquer` canal.')

        else:
            channel = commandpar
            rep = ['<','#','>']
            for r in rep:
                channel = channel.replace(r, '')

            try:
                channel = bot.get_channel(int(channel))
            except:
               raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com `#` para selecionar o canal desejado.')

            if channel == None:
                raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com `#` para selecionar o canal desejado.')
            
            db.editserver(message.guild.id, bot.db_connection, 'eventchannel', str(channel.id))
            await message.channel.send(f'O canal de eventos foi definido para `<#{channel.id}>`')
entity.Command(name='eventchannel', func=eventchannel, category=category, desc=f'Modifique o canal de eventos!', aliases=['canaldeevento', 'eventocanal'], args=[['canal', '']], perm=1)


async def auto_event(message, commandpar, bot):
    if commandpar != None:
        on = ['on', '1', 'true', 'yes', 'sim']
        off = ['off', '0', 'false', 'no', 'nao', 'não']

        if commandpar.lower() in off:
            db.editserver(message.guild.id, bot.db_connection, 'auto_events', False)
            await message.channel.send('Os eventos automaticosforam `desativados`.')
        
        elif commandpar.lower() in on:
            db.editserver(message.guild.id, bot.db_connection, 'auto_events', True)
            await message.channel.send('Os eventos automaticosforam `ativados`.')

        else:
            raise entity.CommandError(f'Parametros invalidos!, utilize `on` ou `off`.')
        
    else:
        auto_events = db.getserver(message.guild.id, bot.db_connection)['auto_events']
        
        if auto_events:
            await message.channel.send(f'Os eventos automaticos estão `ativos`.')
        else:
            await message.channel.send(f'Os eventos automaticos estão `desativos`.')
entity.Command(name='event', func=auto_event, category=category, desc=f'Desative ou ative os eventos automaticos.', aliases=['evento', 'events', 'eventos'], args=[['booleano', '*']], perm=1)
