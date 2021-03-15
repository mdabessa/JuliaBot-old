from random import randint
import discord
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