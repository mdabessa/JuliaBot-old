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