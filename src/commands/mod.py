from random import randint
import discord
import modules.database as db
import modules.entity as entity


category = 'Moderação'
entity.Command.newcategory(category, ':shield:Moderação.')


async def c_event(message, commandpar, connection, bot):
    if commandpar != None:
        marc = 0
        for eve in entity.Event.events:
            if eve.command_create == False:
                continue
            if eve.name == commandpar:
                eve.clear(str(message.guild.id))
                await message.channel.send(f'{message.author.mention} evento `{eve.name}` criado com sucesso!')
                await eve.create([message.channel], str(message.guild.id))
                marc = 1

        if marc == 0:
            raise entity.CommandError('Nenhum evento com esse nome')
    else:
        raise entity.CommandError('Falta algo!')
entity.Command(name='c_event', func=c_event , category=category, desc=f'Criar um evento.', args=[['evento', '*']], perm=1)
