import modules.database as db
import modules.entity as entity


category = 'Depuração'
entity.Command.newcategory(category, 'Depuração',is_visible=False)


async def exe(message, commandpar, connection, bot):
    if commandpar != None:
        cont = commandpar.split()
        text = f'Executando: {cont[0]}'
        
        if len(cont) > 1:
            text += ' [' + ' '.join(cont[1:]) + ']'

        m = await message.channel.send(text)
        await entity.Command.trycommand(m, commandpar, connection, '', bot)

    else:
        raise entity.CommandError('Falta algo nesse comando!')
entity.Command(name='exec', func=exe , category=category, desc=f'Executar um comando através do bot.', args=[['comando', '*'], ['parametros do comando', '']], perm=2)


async def get_all_scripts(message, commandpar, connection, bot):
    scripts = entity.Script.get_scripts()
    text = 'Scripts infos:\n'
    for script in scripts:
        text += f'''    Nome: {script.name}\n   Cache: {script.cache}\n'''
        text += '==========\n'
    await message.channel.send(text)
entity.Command(name='get_all_scripts', func=get_all_scripts, category=category, desc='Listar todos os scripts rodando.', aliases=['gas'], perm=2)


async def get_allowed_bots(message, commandpar, connection, bot):
    bots = db.get_allowed_bots(connection)
    await message.channel.send('Bots(ids) permitidos:\n'+' ,'.join(bots))
entity.Command(name='get_allowed_bots', func=get_allowed_bots, category=category, desc='Listar todos os bots permitidos.', aliases=['gab'], perm=2)


async def add_allowed_bot(message, commandpar, connection, bot):
    if commandpar != None:
        bots = db.get_allowed_bots(connection)
        if str(commandpar) in bots:
            raise entity.CommandError('Esse id de bot, ja esta registrado como um `allowed_bot`')
        
        db.add_bot(commandpar, connection)
        await message.add_reaction('✅')

    else:
        raise entity.CommandError('Falta parametros nesse comando!')
entity.Command(name='add_allowed_bot', func=add_allowed_bot, category=category, desc='Permitir com que um bot especifico seja respondido.', aliases=['aab'], args=[['bot_id', '*']], perm=2)


async def del_allowed_bot(message, commandpar, connection, bot):
    if commandpar != None:
        db.del_bot(commandpar, connection)
        await message.add_reaction('✅')

    else:
        raise entity.CommandError('Falta parametros nesse comando!')
entity.Command(name='del_allowed_bot', func=del_allowed_bot, category=category, desc='Remover um bot especifico da lista de bots permitidos.', aliases=['dab'], args=[['bot_id', '*']], perm=2)
