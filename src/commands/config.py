from random import randint
import discord
import modules.database as db
import modules.entity as entity


category = 'Configurações'
entity.command.newcategory(category, ':gear:Configurações.')


async def setprefix(message, commandpar, connection, bot):
    if commandpar != None:
        cont = commandpar.split()
        prefix = cont[0]
        db.editserver(message.guild.id, connection, 'prefix', prefix)
        await message.channel.send(f'Prefixo de comandos mudado para `{prefix}`')

    else:
        raise entity.CommandError('Falta os parametros do comando!')
entity.command(name='setprefix', func=setprefix , category=category, desc=f'Mude o prefixo de comandos do bot.', args=[['prefixo', '*']], perm=1)


async def addcmd(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    if len(commandpar.split(',')) != 3:
        raise entity.CommandError('Parametros invalidos!')

    commandpar = commandpar.split(',')

    if ' ' in commandpar[0] or ':' in commandpar[0]:
        raise entity.CommandError('O nome do comando não pode conter nenhum espaço ou dois pontos ":".')

    if entity.command.getcommand(message.guild.id, commandpar[0], connection) != None:
        raise entity.CommandError('Um comando com esse nome ja existe!')

    db.addcommand(message.guild.id, connection, commandpar[0], commandpar[1], commandpar[2])

    emb = discord.Embed(title='Novo Comando:', description=commandpar[0], color=0xe6dc56)

    emb.add_field(name='Mensagem:', value=commandpar[1], inline=False)
    emb.add_field(name='Descrição:', value=commandpar[2], inline=False)


    await message.channel.send(embed=emb)
entity.command(name='addcmd', func=addcmd, category=category, desc=f'Adicione um comando personalizado, utilize virgula para separar os parametros. [Ainda em teste!]', args=[['comando', '*'], ['mensagem', '*'], ['descrição', '*']], perm=1)


async def delcmd(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    cmd = entity.command.getcommand(message.guild.id, commandpar, connection)
    if cmd == None:
        raise entity.CommandError(f'O comando com o nome `{commandpar}` não existe!')

    if cmd['overwritten'] == 0:
        await message.channel.send(f'O comando `{commandpar}` é um comando próprio da {bot.user.mention}, ele não pode ser deletado!')
    else:
        db.delcommand(message.guild.id, connection, commandpar)
        await message.channel.send(f'O comando `{commandpar}` foi deletado com sucesso!')
entity.command(name='delcmd', func=delcmd, category=category, desc=f'Delete um comando personalizado!', args=[['comando', '*']], perm=1)


async def commandchannel(message, commandpar, connection, bot):
    if commandpar == None:
        server = db.getserver(message.guild.id, connection)
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
            db.editserver(message.guild.id, connection, 'commandchannel', None)
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
            
            db.editserver(message.guild.id, connection, 'commandchannel', str(channel.id))
            await message.channel.send(f'O canal de comandos foi definido para `<#{channel.id}>`')
entity.command(name='cmdchannel', func=commandchannel, category=category, desc=f'Modifique o canal de comandos!', args=[['canal', '']], perm=1)


async def eventchannel(message, commandpar, connection, bot):
    if commandpar == None:
        server = db.getserver(message.guild.id, connection)
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
            db.editserver(message.guild.id, connection, 'eventchannel', None)
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
            
            db.editserver(message.guild.id, connection, 'eventchannel', str(channel.id))
            await message.channel.send(f'O canal de eventos foi definido para `<#{channel.id}>`')
entity.command(name='eventchannel', func=eventchannel, category=category, desc=f'Modifique o canal de eventos!', args=[['canal', '']], perm=1)


async def auto_event(message, commandpar, connection, bot):
    if commandpar != None:
        if commandpar.lower() == 'off':
            db.editserver(message.guild.id, connection, 'auto_events', False)
            await message.channel.send('Os eventos automaticosforam `desativados`.')
        
        elif commandpar.lower() == 'on':
            db.editserver(message.guild.id, connection, 'auto_events', True)
            await message.channel.send('Os eventos automaticosforam `ativados`.')

        else:
            raise entity.CommandError(f'Parametros invalidos!, utilize `on` ou `off`.')
        
    else:
        auto_events = db.getserver(message.guild.id, connection)['auto_events']
        
        if auto_events:
            await message.channel.send(f'Os eventos automaticos estão `ativos`.')
        else:
            await message.channel.send(f'Os eventos automaticos estão `desativos`.')

entity.command(name='event', func=auto_event, category=category, desc=f'Desative ou ative os eventos automaticos.', args=[['booleano', '*']], perm=1)
